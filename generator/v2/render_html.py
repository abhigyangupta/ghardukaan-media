"""Render an HTML/GSAP animation frame-by-frame with headless Chromium and mux with voice + music.

  python3 v2/render_html.py stills 2.5 7.9 12 ...     -> v2/out/still_<t>.png
  python3 v2/render_html.py video                     -> v2/out/commission-maths_v2.mp4
"""
import json, os, subprocess, sys
from playwright.sync_api import sync_playwright

V2 = os.path.dirname(os.path.abspath(__file__)); GEN = os.path.dirname(V2); OUT = os.path.join(V2, 'out')
sys.path.insert(0, GEN)
FPS = 30
m = json.load(open(os.path.join(OUT, 'marks.json'))); MARKS, DUR = m['marks'], round(m['total'] + 0.6, 2)

def page_ctx(p):
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    pg.add_init_script(f'window.__MARKS={json.dumps(MARKS)};window.__DUR={DUR};')
    pg.on('console', lambda msg: print('console:', msg.text) if msg.type == 'error' else None)
    pg.on('pageerror', lambda e: print('pageerror:', e))
    pg.goto('file://' + os.path.join(V2, 'commission.html')); pg.evaluate('window.ready')
    return b, pg

def stills(ts):
    with sync_playwright() as p:
        b, pg = page_ctx(p)
        for t in ts:
            pg.evaluate(f'seek({t})'); pg.screenshot(path=os.path.join(OUT, f'still_{t}.png'))
        b.close()

def video():
    silent = os.path.join(OUT, 'silent.mp4'); n = int(DUR * FPS)
    ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS), silent], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = page_ctx(p)
        for i in range(n):
            pg.evaluate(f'seek({i / FPS})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=96))
            if i % 150 == 0: print('frame', i, '/', n, flush=True)
        b.close()
    ff.stdin.close(); ff.wait()
    from music import make_music
    mus = os.path.join(OUT, 'music.wav'); vo = os.path.join(OUT, 'vo.wav'); tid = 'commission-maths'
    make_music(mus, DUR, cues=[x['start'] for x in MARKS[1:]], seed=sum(map(ord, tid)) % 1000, key_semi=[0, 2, -3, 5][len(tid) % 4])
    out = os.path.join(OUT, 'commission-maths_v2.mp4')
    fc = ('[2:a]apad,volume=1.0,aformat=channel_layouts=stereo,asplit=2[vo][sc];'
          '[1:a]apad,volume=0.5[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];'
          '[duck][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', silent, '-i', mus, '-i', vo, '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), '-movflags', '+faststart', out], check=True)
    print(out)

if __name__ == '__main__':
    if sys.argv[1] == 'stills': stills([float(x) for x in sys.argv[2:]])
    else: video()
