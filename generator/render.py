"""Scene templates for daily GharDukaan videos. Each scene is timed to its voice-over line."""
import math, subprocess
from PIL import Image, ImageDraw
from brand import (F, text, twidth, rrect, circle, paste, SYM, WORD, check, clamp, ease, back, prog, glow, wrap,
                   W, H, FPS, PAPER, INK, JAG, CLAY, WHEAT, TERRA, TERRA2, OK, BLUSH, CANVAS)

THEMES = {
    'light': dict(bg_top=CANVAS, bg_bot=(246, 232, 214), dots=(240, 222, 200), head1=JAG, head2=TERRA, body=INK, sub=CLAY,
                  card=PAPER, card_line=WHEAT, accent=TERRA, accent_text=PAPER, num_bg=BLUSH, num_fg=TERRA, cap_bg=(30, 27, 19), cap_fg=PAPER),
    'night': dict(bg_top=(34, 18, 12), bg_bot=(84, 38, 14), dots=(70, 36, 18), head1=PAPER, head2=(255, 196, 84), body=INK, sub=CLAY,
                  card=PAPER, card_line=WHEAT, accent=TERRA2, accent_text=PAPER, num_bg=(255, 226, 150), num_fg=TERRA, cap_bg=(15, 8, 5), cap_fg=(255, 226, 150)),
    # Extra looks so consecutive videos don't feel the same. Optional keys: pattern (blobs|stripes|grid|waves|rings|confetti),
    # cards (card|brutal|pill|ticket|numeral), hook (center|left), stat_fg/stat_body/stat_note, outro_box.
    'marigold': dict(bg_top=(255, 207, 82), bg_bot=(255, 172, 52), dots=(246, 186, 50), head1=INK, head2=(125, 25, 20), body=INK, sub=(105, 72, 50),
                     card=PAPER, card_line=INK, accent=(125, 25, 20), accent_text=PAPER, num_bg=(255, 207, 82), num_fg=INK,
                     cap_bg=INK, cap_fg=(255, 214, 100), pattern='stripes', cards='brutal', hook='left', outro_box=PAPER),
    'teal': dict(bg_top=(8, 64, 68), bg_bot=(3, 33, 40), dots=(22, 92, 94), head1=PAPER, head2=(128, 234, 204), body=INK, sub=(84, 106, 106),
                 card=PAPER, card_line=(190, 230, 220), accent=(0, 128, 112), accent_text=PAPER, num_bg=(0, 128, 112), num_fg=PAPER,
                 cap_bg=(2, 20, 24), cap_fg=(150, 240, 212), pattern='grid', cards='pill', hook='center', stat_fg=(0, 110, 96)),
    'rose': dict(bg_top=(255, 238, 240), bg_bot=(252, 210, 220), dots=(244, 186, 204), head1=(64, 20, 42), head2=(178, 20, 86), body=(40, 18, 30),
                 sub=(118, 78, 94), card=PAPER, card_line=(240, 192, 208), accent=(178, 20, 86), accent_text=PAPER, num_bg=(178, 20, 86), num_fg=PAPER,
                 cap_bg=(64, 20, 42), cap_fg=PAPER, pattern='waves', cards='ticket', hook='left', stat_fg=(178, 20, 86), outro_box=PAPER),
    'indigo': dict(bg_top=(24, 22, 72), bg_bot=(62, 34, 116), dots=(48, 42, 112), head1=PAPER, head2=(255, 200, 87), body=PAPER, sub=(196, 190, 236),
                   card=PAPER, card_line=(255, 200, 87), accent=(214, 120, 20), accent_text=PAPER, num_bg=(255, 200, 87), num_fg=(255, 200, 87),
                   cap_bg=(12, 10, 42), cap_fg=(255, 214, 120), pattern='rings', cards='numeral', hook='center', stat_fg=(62, 34, 116)),
    'leaf': dict(bg_top=(238, 247, 232), bg_bot=(212, 236, 204), dots=(22, 101, 52), head1=(20, 50, 30), head2=(18, 96, 48), body=INK, sub=(76, 98, 82),
                 card=PAPER, card_line=(196, 224, 190), accent=(18, 96, 48), accent_text=PAPER, num_bg=(18, 96, 48), num_fg=PAPER,
                 cap_bg=(20, 50, 30), cap_fg=PAPER, pattern='confetti', cards='card', hook='left', stat_fg=(18, 96, 48), outro_box=PAPER),
}

OUTRO = {'vo': 'घरदुकान डॉट शॉप पर आज ही अपनी दुकान बनाइए। पहले तीस दिन बिल्कुल मुफ़्त।',
         'cap': 'ghardukaan.shop pe aaj hi apni dukaan banao. Pehle 30 din FREE.', 'kind': 'outro'}

class Video:
    def __init__(self, topic, marks, total):
        self.t = THEMES[topic.get('theme', 'light')]; self.scenes = topic['scenes'] + [OUTRO]
        self.marks = marks; self.dur = round(total + 0.6, 2); self._bg = None

    def bg(self, t):
        if self._bg is None:
            g = Image.new('RGB', (1, H)); a, b = self.t['bg_top'], self.t['bg_bot']
            for y in range(H):
                k = (y / H) ** 1.5; g.putpixel((0, y), tuple(int(a[c] + (b[c] - a[c]) * k) for c in range(3)))
            self._bg = g.resize((W, H)).convert('RGBA')
        img = self._bg.copy(); d = ImageDraw.Draw(img); c = self.t['dots'] + (255,); pat = self.t.get('pattern', 'blobs')
        if pat == 'stripes':
            off = (t * 40) % 160
            for k in range(-14, 16):
                x = k * 160 + off
                d.polygon([(x, 0), (x + 60, 0), (x + 60 - H * 0.6, H), (x - H * 0.6, H)], fill=c)
        elif pat == 'grid':
            oy = (t * 18) % 90
            for gx in range(45, W, 90):
                for gy in range(-90, H + 90, 90):
                    y = gy + oy; r = 6 + 3 * math.sin(t * 2 + gx * 0.01 + gy * 0.01)
                    d.ellipse((gx - r, y - r, gx + r, y + r), fill=c)
        elif pat == 'waves':
            for k in range(14):
                y0 = 80 + k * 140; pts = [(x, y0 + 26 * math.sin(x / 120 + t * 1.6 + k)) for x in range(-20, W + 40, 20)]
                d.line(pts, fill=c, width=10, joint='curve')
        elif pat == 'rings':
            for cx, cy in ((W + 60, -60), (-80, H + 60)):
                for k in range(1, 12):
                    r = k * 130 + 40 * math.sin(t * 0.8 + k * 0.5)
                    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=14)
        elif pat == 'confetti':
            cols = [(18, 96, 48), (240, 170, 40), (204, 87, 5), (120, 180, 90)]
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            for k in range(46):
                x = (k * 211) % W; y = ((k * 397) % (H + 200) + t * (30 + k % 5 * 12)) % (H + 200) - 100
                a = (k * 37 + t * 50 * (1 if k % 2 else -1)) % 360; s = 14 + k % 4 * 5
                pts = [(x + s * math.cos(math.radians(a + q)), y + s * 0.55 * math.sin(math.radians(a + q))) for q in (0, 90, 180, 270)]
                d.polygon(pts, fill=cols[k % 4] + (90,))
            img.alpha_composite(L)
        else:
            for i, (cx, cy, r) in enumerate([(110, 260, 230), (990, 1650, 280), (1000, 420, 110)]):
                dx, dy = 24 * math.sin(t * 0.6 + i), 24 * math.cos(t * 0.5 + i)
                d.ellipse((cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r), fill=c)
        return img

    def span(self, i):
        s0 = self.marks[i]['start'] - 0.25 if i else 0
        s1 = self.marks[i + 1]['start'] - 0.05 if i + 1 < len(self.marks) else self.dur + 1
        return s0, s1

    def alpha(self, t, i):
        s0, s1 = self.span(i); return ease(prog(t, s0, s0 + 0.3)) * (1 - ease(prog(t, s1 - 0.3, s1))), s0

    def head(self, img, t, t0, a, lines, y=330):
        p = ease(prog(t, t0, t0 + 0.45)); l1, l2 = (lines + [''])[:2]
        f2 = F('Black', 84)
        while twidth(l2, f2) > W - 120 and f2[0].size > 56: f2 = F('Black', f2[0].size - 4)
        text(img, (W / 2, y), l1, F('SemiBold', 62), self.t['head1'], a * p)
        text(img, (W / 2, y + 96), l2, f2, self.t['head2'], a * p)

    def corner(self, img, t):
        a = ease(prog(t, self.marks[1]['start'] - 0.3, self.marks[1]['start'])) * (1 - ease(prog(t, self.marks[-1]['start'] - 0.4, self.marks[-1]['start'])))
        paste(img, SYM, 112, 130, 92, a); text(img, (170, 130), 'GharDukaan', F('Black', 36), self.t['head2'], a, 'lm')

    def caption(self, img, t):
        for i, m in enumerate(self.marks):
            a = ease(prog(t, m['start'] - 0.1, m['start'] + 0.15)) * (1 - ease(prog(t, m['end'] + 0.15, m['end'] + 0.3)))
            if a <= 0.01: continue
            fonts = F('Bold', 40); lines = wrap(self.scenes[i]['cap'], fonts, W - 200)
            h = 60 * len(lines) + 40; y0 = 1660 - h
            rrect(img, (70, y0, W - 70, y0 + h), 30, self.t['cap_bg'], a * 0.85)
            for j, ln in enumerate(lines): text(img, (W / 2, y0 + 50 + j * 60), ln, fonts, self.t['cap_fg'], a)

    # ---- scene kinds
    def s_hook(self, img, t, sc, i):
        a, t0 = self.alpha(t, i)
        if self.t.get('hook') == 'left':
            pb = back(prog(t, t0, t0 + 0.5))
            rrect(img, (90, 360, 90 + 230 * pb, 590), 40, self.t.get('outro_box', CANVAS), a, shadow=True)
            paste(img, SYM, 90 + 115 * pb, 475, 180 * pb, a)
            big = sc['big']
            for j, ln in enumerate(big):
                p = ease(prog(t, t0 + 0.25 + 0.3 * j, t0 + 0.7 + 0.3 * j))
                f = F('Black', 124 if j == 1 else 82)
                while twidth(ln, f) > W - 180 and f[0].size > 56: f = F('Black', f[0].size - 4)
                col = self.t['head2'] if j == 1 else self.t['head1']
                text(img, (90 - 80 * (1 - p), 760 + j * 140), ln, f, col, a * clamp(p * 1.4), 'lm')
            pu = ease(prog(t, t0 + 1.1, t0 + 1.5))
            rrect(img, (90, 760 + len(big) * 140 - 40, 90 + 240 * pu, 760 + len(big) * 140 - 16), 12, self.t['accent'], a * pu)
            return
        paste(img, SYM, W / 2, 470, 260 * back(prog(t, t0, t0 + 0.5)), a)
        big = sc['big']; y = 800 - (len(big) - 2) * 60
        for j, ln in enumerate(big):
            p = back(prog(t, t0 + 0.25 + 0.35 * j, t0 + 0.7 + 0.35 * j))
            f = F('Black', 112 if j == 1 else 80)
            while twidth(ln, f) > W - 100 and f[0].size > 56: f = F('Black', f[0].size - 4)
            col = self.t['head2'] if j == 1 else self.t['head1']
            text(img, (W / 2, y + j * 130 + 40 * (1 - p)), ln, f, col, a * clamp(p * 1.4))

    def s_list(self, img, t, sc, i):
        a, t0 = self.alpha(t, i); self.head(img, t, t0, a, sc['head'])
        items = sc['items']; n = len(items); m = self.marks[i]; dur = m['end'] - m['start']
        ch = 270 if n <= 3 else 215; y0 = 600
        for j, it in enumerate(items):
            ta = m['start'] + dur * j / n - 0.1
            p = back(prog(t, ta, ta + 0.45)); al = a * clamp(p * 1.4); y = y0 + j * (ch + 22) + int(40 * (1 - p))
            style = self.t.get('cards', 'card'); tx = 260; mid = y + ch / 2
            if style == 'brutal':
                rrect(img, (102, y + 14, W - 76, y + ch + 14), 18, INK, al)
                rrect(img, (90, y, W - 90, y + ch), 18, self.t['card'], al, outline=INK, width=5)
                rrect(img, (128, mid - 56, 240, mid + 56), 14, self.t['num_bg'], al, outline=INK, width=4)
                text(img, (184, mid + 2), it[0], F('Black', 56), self.t['num_fg'], al)
            elif style == 'pill':
                ch2 = ch - 40; y += 20; mid = y + ch2 / 2
                rrect(img, (90, y, W - 90, y + ch2), ch2 / 2, self.t['card'], al, shadow=True)
                circle(img, 90 + ch2 / 2, mid, ch2 / 2 - 18, self.t['num_bg'], al)
                text(img, (90 + ch2 / 2, mid + 2), it[0], F('Black', 60), self.t['num_fg'], al); tx = 90 + ch2 + 10
            elif style == 'ticket':
                rrect(img, (90, y, W - 90, y + ch), 26, self.t['card'], al, shadow=True, outline=self.t['card_line'], width=2)
                rrect(img, (90, y, 250, y + ch), 26, self.t['num_bg'], al)
                for k in range(int(ch / 34)): circle(img, 250, y + 22 + k * 34, 7, self.t['card'], al)
                text(img, (170, mid + 2), it[0], F('Black', 72), self.t['num_fg'], al); tx = 290
            elif style == 'numeral':
                text(img, (175, mid + 6), it[0], F('Black', 150), self.t['num_fg'], al)
                if j < n - 1: rrect(img, (270, y + ch + 8, W - 90, y + ch + 12), 2, self.t['sub'], al * 0.5)
                tx = 290
            else:
                rrect(img, (90, y, W - 90, y + ch), 34, self.t['card'], al, shadow=True, outline=self.t['card_line'], width=2)
                circle(img, 180, mid, 58, self.t['num_bg'], al)
                text(img, (180, mid + 2), it[0], F('Black', 56), self.t['num_fg'], al)
            ft = F('Black', 46 if style != 'numeral' else 52)
            while twidth(it[1], ft) > W - tx - 110 and ft[0].size > 30: ft = F('Black', ft[0].size - 2)
            if len(it) > 2 and it[2]:
                text(img, (tx, mid - 30), it[1], ft, self.t['body'], al, 'lm')
                fs = F('Medium', 32)
                while twidth(it[2], fs) > W - tx - 120 and fs[0].size > 22: fs = F('Medium', fs[0].size - 1)
                text(img, (tx, mid + 32), it[2], fs, self.t['sub'], al, 'lm')
            else:
                text(img, (tx, mid), it[1], ft, self.t['body'], al, 'lm')

    def s_stat(self, img, t, sc, i):
        a, t0 = self.alpha(t, i); self.head(img, t, t0, a, sc['head'])
        p = back(prog(t, t0 + 0.4, t0 + 0.9)); al = a * clamp(p * 1.4); oy = int(50 * (1 - p))
        glow(img, W / 2, 900, 360, (255, 180, 80), a * 0.3)
        rrect(img, (120, 600 + oy, W - 120, 1330 + oy), 56, self.t['card'], al, shadow=True, outline=self.t['accent'], width=5)
        f = F('Black', 230)
        while twidth(sc['stat'], f) > W - 340 and f[0].size > 90: f = F('Black', f[0].size - 8)
        text(img, (W / 2, 870 + oy), sc['stat'], f, self.t.get('stat_fg', TERRA), al)
        text(img, (W / 2, 1070 + oy), sc.get('sub', ''), F('Bold', 48), self.t.get('stat_body', INK), al)
        for j, ln in enumerate(wrap(sc.get('note', ''), F('Medium', 34), W - 360)):
            text(img, (W / 2, 1160 + j * 50 + oy), ln, F('Medium', 34), self.t.get('stat_note', CLAY), al * ease(prog(t, t0 + 1.0, t0 + 1.4)))

    def s_vs(self, img, t, sc, i):
        a, t0 = self.alpha(t, i); self.head(img, t, t0, a, sc['head'])
        m = self.marks[i]; dur = m['end'] - m['start']
        for j, (bad, good) in enumerate(sc['rows']):
            ta = m['start'] + dur * j / len(sc['rows']) - 0.1
            p = back(prog(t, ta, ta + 0.45)); al = a * clamp(p * 1.4); y = 600 + j * 330 + int(40 * (1 - p))
            rrect(img, (80, y, W / 2 - 10, y + 290), 30, (253, 232, 228), al, outline=(240, 200, 190), width=2)
            rrect(img, (W / 2 + 10, y, W - 80, y + 290), 30, (226, 244, 232), al, outline=(190, 225, 200), width=2)
            text(img, (110, y + 40), 'Pehle', F('Bold', 26), (190, 60, 40), al, 'lm'); text(img, (W / 2 + 40, y + 40), 'Ab', F('Bold', 26), OK, al, 'lm')
            for k, ln in enumerate(wrap(bad, F('SemiBold', 38), W / 2 - 140)[:3]): text(img, (110, y + 110 + k * 50), ln, F('SemiBold', 38), INK, al, 'lm')
            for k, ln in enumerate(wrap(good, F('Bold', 38), W / 2 - 140)[:3]): text(img, (W / 2 + 40, y + 110 + k * 50), ln, F('Bold', 38), INK, al, 'lm')

    def s_outro(self, img, t, sc, i):
        a, t0 = self.alpha(t, i)
        pb = back(prog(t, t0, t0 + 0.5))
        rrect(img, (W / 2 - 210 * pb, 470 - 165 * pb, W / 2 + 210 * pb, 470 + 165 * pb), 60, self.t.get('outro_box', CANVAS), a, shadow=True)
        paste(img, SYM, W / 2, 470, 330 * pb, a)
        p = ease(prog(t, t0 + 0.3, t0 + 0.8))
        paste(img, WORD, W / 2, 760, 700, a * p) if self.t is THEMES['light'] else text(img, (W / 2, 760), 'GharDukaan', F('Black', 110), self.t['head2'], a * p)
        text(img, (W / 2, 870), 'Apni Dukaan. Apne Phone Se.', F('Black', 54), self.t['head2'], a * p)
        pu = back(prog(t, t0 + 0.6, t0 + 1.1)); pulse = 1 + 0.025 * math.sin(t * 7) * (t > t0 + 1.2)
        bw, bh = 410 * pulse, 66 * pulse
        rrect(img, (W / 2 - bw, 1010 - bh, W / 2 + bw, 1010 + bh), 66, self.t['accent'], a * clamp(pu * 1.4), shadow=True)
        text(img, (W / 2, 1010), 'www.ghardukaan.shop', F('Black', 56), self.t['accent_text'], a * clamp(pu * 1.4))
        p2 = back(prog(t, t0 + 1.4, t0 + 1.9))
        rrect(img, (220, 1130, W - 220, 1230), 50, OK, a * clamp(p2 * 1.4))
        text(img, (W / 2, 1180), 'Pehle 30 din FREE', F('Black', 46), PAPER, a * clamp(p2 * 1.4))
        text(img, (W / 2, 1290), 'Dukaan Pro ₹99/month  •  0% commission', F('SemiBold', 32), self.t['head1'], a * ease(prog(t, t0 + 1.8, t0 + 2.2)))

    def frame(self, t):
        img = self.bg(t); self.corner(img, t)
        for i, sc in enumerate(self.scenes):
            s0, s1 = self.span(i)
            if s0 <= t < s1: getattr(self, 's_' + sc['kind'])(img, t, sc, i)
        self.caption(img, t)
        return img.convert('RGB')

    def render(self, out_mp4):
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out_mp4], stdin=subprocess.PIPE)
        for k in range(int(self.dur * FPS)): p.stdin.write(self.frame(k / FPS).tobytes())
        p.stdin.close(); p.wait()
