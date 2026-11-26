"""v2 renderer: animated HTML (GSAP) scenes with a lip-synced presenter, captured frame-by-frame with headless Chromium.

Uses v2/custom/<topic_id>.html when it exists (hand-built animation for one topic), otherwise the generic v2/scene.html.
make.py falls back to the old Pillow renderer (render.py) if anything here fails.
"""
import json, os, subprocess

V2 = os.path.dirname(os.path.abspath(__file__))
FPS = 30

def envelope(vo_wav):
    """Per-frame mouth openness (0..1) from the voice track, for lip-sync."""
    import numpy as np, soundfile as sf
    a, sr = sf.read(vo_wav); a = a if a.ndim == 1 else a.mean(1); hop = sr // FPS
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    e = np.clip(rms / (np.percentile(rms, 92) + 1e-9), 0, 1); e[e < 0.12] = 0; out = []; p = 0.0
    for v in e: p = v if v > p else p * 0.55 + v * 0.45; out.append(round(float(p), 3))
    return out

class Animation:
    def __init__(self, topic, marks, total, vo_wav):
        from render import THEMES, OUTRO
        self.dur = round(total + 0.6, 2)
        custom = os.path.join(V2, 'custom', topic['id'] + '.html')
        self.html = custom if os.path.exists(custom) else os.path.join(V2, 'scene.html')
        th = {k: v for k, v in THEMES[topic.get('theme', 'light')].items() if isinstance(v, tuple)}
        clips = self._clips(topic, marks)
        data = {'__TOPIC': {'id': topic['id'], 'format': topic.get('format', 'tips'), 'scenes': topic['scenes']}, '__CLIPS': clips, '__MARKS': marks, '__DUR': self.dur,
                '__ENV': envelope(vo_wav), '__THEME': th, '__OUTRO': OUTRO}
        self.init = ''.join(f'window.{k}={json.dumps(v, ensure_ascii=False)};' for k, v in data.items())

    @staticmethod
    def _clips(topic, marks):
        """'demo' scenes show a real app screen recording inside a phone frame. The phone screen is cropped from the
        finished tutorial videos in ../tutorials (1080x1920, phone screen at x 160-920, y 215-1920) and written as
        JPEG frames, which the page swaps in frame by frame. Returns {scene index: [frame dir, frame count]}."""
        out = {}
        for i, sc in enumerate(topic['scenes']):
            if sc.get('kind') != 'demo': continue
            src = os.path.join(os.path.dirname(V2), '..', 'tutorials', sc['clip'] + '.mp4')
            d = os.path.join(os.path.dirname(V2), '.cache', 'clips', f"{topic['id']}_{i}")
            subprocess.run(['rm', '-rf', d]); os.makedirs(d)
            dur = marks[i + 1]['start'] - marks[i]['start'] + 1.0
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(sc.get('from', 0)), '-t', str(dur), '-i', src,
                            '-vf', f'crop=760:1705:160:215,scale=464:1040,fps={FPS}', '-q:v', '3', os.path.join(d, '%04d.jpg')], check=True)
            n = len([f for f in os.listdir(d) if f.endswith('.jpg')])
            if not n: raise RuntimeError(f'no frames from clip {sc["clip"]}')
            out[i] = [os.path.abspath(d), n]
        return out

    def _page(self, p):
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.add_init_script(self.init); pg.goto('file://' + self.html); pg.evaluate('window.ready')
        if errs: b.close(); raise RuntimeError('page error: ' + '; '.join(errs))
        return b, pg, errs

    def stills(self, times, outdir):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b, pg, errs = self._page(p)
            for i, t in enumerate(times):
                pg.evaluate(f'seek({t})'); pg.screenshot(path=os.path.join(outdir, f'preview_{i}.png'))
            b.close()
            if errs: raise RuntimeError('page error: ' + '; '.join(errs))

    def render(self, out_mp4):
        from playwright.sync_api import sync_playwright
        ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS), out_mp4], stdin=subprocess.PIPE)
        try:
            with sync_playwright() as p:
                b, pg, errs = self._page(p)
                for i in range(int(self.dur * FPS)):
                    pg.evaluate(f'seek({i / FPS})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=96))
                b.close()
                if errs: raise RuntimeError('page error: ' + '; '.join(errs))
        finally:
            ff.stdin.close(); ff.wait()
        if ff.returncode: raise RuntimeError('ffmpeg failed')
