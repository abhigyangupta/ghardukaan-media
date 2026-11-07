"""GharDukaan brand drawing helpers: fonts, colours, text with rupee fallback, shapes, logo."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FDIR = os.path.join(HERE, '.cache/node_modules/@fontsource/plus-jakarta-sans/files/')
WEIGHT = {'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Bold': 700, 'Black': 800}
_cache = {}
def F(w, s):
    k = (w, s)
    if k not in _cache:
        n = WEIGHT[w]
        _cache[k] = (ImageFont.truetype(f'{FDIR}plus-jakarta-sans-latin-{n}-normal.woff2', s),
                     ImageFont.truetype(f'{FDIR}plus-jakarta-sans-latin-ext-{n}-normal.woff2', s))
    return _cache[k]

# Brand palette (DESIGN.md)
CANVAS = (250, 244, 234); PAPER = (255, 255, 255); INK = (30, 27, 19); JAG = (66, 43, 34)
CLAY = (138, 114, 104); WHEAT = (235, 220, 200); TERRA = (158, 61, 0); TERRA2 = (204, 87, 5)
OK = (21, 128, 61); WA = (37, 211, 102); WABUB = (220, 248, 198); BLUSH = (255, 219, 205)

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(t): t = clamp(t); return 1 - (1 - t) ** 3
def back(t):
    t = clamp(t); c = 1.5
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def prog(t, a, b): return clamp((t - a) / (b - a))
def win(t, a, b, fi=0.35, fo=0.35): return ease(prog(t, a, a + fi)) * (1 - ease(prog(t, b - fo, b)))

def segs(s, fonts):
    out, cur, curf = [], '', None
    for ch in s:
        f = fonts[1] if ch == '₹' else fonts[0]
        if f is not curf and cur: out.append((cur, curf)); cur = ''
        cur += ch; curf = f
    if cur: out.append((cur, curf))
    return out

def twidth(s, fonts): return sum(f.getlength(x) for x, f in segs(s, fonts))

def text(img, xy, s, fonts, fill, alpha=1.0, anchor='mm'):
    if alpha <= 0.01 or not s: return
    x, y = xy; w = twidth(s, fonts)
    asc = fonts[0].getmetrics()[0]; size = fonts[0].size
    if anchor[0] == 'm': x -= w / 2
    elif anchor[0] == 'r': x -= w
    base = y + size * 0.36 if anchor[1] == 'm' else y + asc if anchor[1] == 't' else y
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for part, f in segs(s, fonts):
        d.text((x, base), part, font=f, fill=fill + (int(255 * alpha),), anchor='ls'); x += f.getlength(part)
    img.alpha_composite(layer)

def shape(img, fn, alpha, blur_shadow=None):
    if alpha <= 0.01: return
    if blur_shadow:
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(sh), (90, 40, 10, int(55 * alpha)), blur_shadow)
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L), None, 0)
    if alpha < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * alpha)))
    img.alpha_composite(L)

def rrect(img, box, r, fill, alpha=1.0, shadow=False, outline=None, width=0):
    def fn(d, sc, off):
        x0, y0, x1, y1 = box
        if sc: d.rounded_rectangle((x0, y0 + off, x1, y1 + off), r, fill=sc)
        else: d.rounded_rectangle(box, r, fill=fill + (255,), outline=(outline + (255,)) if outline else None, width=width)
    shape(img, fn, alpha, 16 if shadow else None)

def circle(img, cx, cy, r, fill, alpha=1.0):
    shape(img, lambda d, sc, off: d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill + (255,)), alpha)

def check(img, cx, cy, s, col, alpha):
    shape(img, lambda d, sc, off: d.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.7)], fill=col + (255,), width=max(3, int(s / 3)), joint='curve'), alpha)

SYM = Image.open(os.path.join(HERE, 'assets/symbol.png')).convert('RGBA')
WORD = Image.open(os.path.join(HERE, 'assets/wordmark.png')).convert('RGBA')
def paste(img, src, cx, cy, width, alpha):
    if alpha <= 0.01 or width < 2: return
    im = src.resize((int(width), max(1, int(src.height * width / src.width))), Image.LANCZOS)
    if alpha < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def glow(img, cx, cy, r, col, a):
    if a <= 0.01: return
    L = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(L).ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(150 * a),))
    img.alpha_composite(L.filter(ImageFilter.GaussianBlur(r * 0.5)))

def wrap(s, fonts, maxw):
    words, lines, cur = s.split(' '), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if twidth(trial, fonts) > maxw and cur: lines.append(cur); cur = w
        else: cur = trial
    return lines + [cur]
