"""Instagram highlight covers + story slides for the GharDukaan profile. Writes PNGs to ../profile/."""
import os
from PIL import Image, ImageDraw
from brand import F, text, twidth, rrect, circle, paste, shape, SYM, WORD, wrap, W, H, PAPER, INK, JAG, CLAY, WHEAT, TERRA, TERRA2, OK, BLUSH, CANVAS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'profile'); os.makedirs(OUT, exist_ok=True)
GOLD = (255, 196, 84)

def canvas(dark=False):
    img = Image.new('RGBA', (W, H), ((34, 18, 12) if dark else CANVAS) + (255,)); d = ImageDraw.Draw(img)
    for cx, cy, r in [(110, 300, 230), (990, 1650, 280), (1000, 520, 110)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=((70, 36, 18) if dark else (244, 228, 208)) + (255,))
    return img

# ---------- covers: icon centred on terracotta, readable inside Instagram's circle crop
def cover(name, draw_icon):
    img = Image.new('RGBA', (W, H), TERRA + (255,)); circle(img, W / 2, H / 2, 380, TERRA2)
    circle(img, W / 2, H / 2, 300, CANVAS); draw_icon(img, W / 2, H / 2)
    img.convert('RGB').save(os.path.join(OUT, f'cover_{name}.png'))

def icon_how(img, x, y):
    for i in range(3):
        cy = y - 120 + i * 120; circle(img, x - 120, cy, 42, TERRA); text(img, (x - 120, cy + 2), str(i + 1), F('Black', 48), PAPER)
        rrect(img, (x - 50, cy - 18, x + 150, cy + 18), 18, TERRA)
def icon_price(img, x, y): text(img, (x, y + 10), '₹', F('Black', 330), TERRA)
def icon_faq(img, x, y): text(img, (x, y + 15), '?', F('Black', 340), TERRA)
def icon_trial(img, x, y):
    text(img, (x, y - 40), '30', F('Black', 230), TERRA); text(img, (x, y + 120), 'din FREE', F('Black', 64), OK)
def icon_shop(img, x, y): paste(img, SYM, x, y, 420, 1)

# ---------- story slides (keep text inside y 260..1580 so Instagram UI never covers it)
def header(img, small, big, dark=False, y=330):
    text(img, (W / 2, y), small, F('SemiBold', 58), PAPER if dark else JAG)
    f = F('Black', 86)
    while twidth(big, f) > W - 120: f = F('Black', f[0].size - 4)
    text(img, (W / 2, y + 95), big, f, GOLD if dark else TERRA)

def brand_tag(img, dark=False):
    paste(img, SYM, W / 2 - 150, 1660, 90, 1); text(img, (W / 2 - 90, 1660), 'ghardukaan.shop', F('Black', 40), GOLD if dark else TERRA, anchor='lm')

def cards(img, items, y0=560, h=200, gap=24):
    for i, it in enumerate(items):
        y = y0 + i * (h + gap); rrect(img, (90, y, W - 90, y + h), 34, PAPER, shadow=True, outline=WHEAT, width=2)
        circle(img, 180, y + h / 2, 54, BLUSH); text(img, (180, y + h / 2 + 2), it[0], F('Black', 50), TERRA)
        if len(it) > 2:
            text(img, (265, y + h / 2 - 28), it[1], F('Black', 42), INK, anchor='lm')
            text(img, (265, y + h / 2 + 32), it[2], F('Medium', 30), CLAY, anchor='lm')
        else:
            text(img, (265, y + h / 2), it[1], F('Black', 42), INK, anchor='lm')

def save(img, name): img.convert('RGB').save(os.path.join(OUT, name + '.png'))

def slides():
    # How it works
    s = canvas(); paste(s, SYM, W / 2, 560, 360, 1); header(s, 'GharDukaan kya hai?', 'Aapki apni online dukaan', y=850)
    for i, ln in enumerate(wrap('Ghar se bechne walon ke liye ek link, jisme saare products, daam aur WhatsApp order button ho.', F('SemiBold', 44), W - 200)):
        text(s, (W / 2, 1110 + i * 64), ln, F('SemiBold', 44), JAG)
    brand_tag(s); save(s, 'how_1')
    s = canvas(); header(s, 'Shuru karna', 'bas 3 steps mein')
    cards(s, [['1', 'Photo khicho', 'Phone camera se products'], ['2', 'Details bharo', 'Naam, daam, description'], ['3', 'Review ke baad live', 'Phir link share karo']], h=230)
    brand_tag(s); save(s, 'how_2')
    s = canvas(); header(s, 'Order aur payment', 'seedha aapko')
    cards(s, [['1', 'Order WhatsApp pe', 'Items, quantity, total ke saath'], ['₹', 'Payment seedha UPI mein', 'Customer aapko pay karta hai'], ['%', '0% sales commission', 'Har rupaya aapka']], h=230)
    brand_tag(s); save(s, 'how_3')
    # Pricing
    s = canvas(); header(s, 'Dukaan Pro', '₹99/month')
    cards(s, [['1', 'Unlimited products'], ['2', 'Apna yourname.ghardukaan.shop'], ['3', '10 categories tak'], ['4', 'Printable QR standee kit'], ['%', '0% commission, direct UPI']], h=165, gap=20)
    rrect(s, (190, 1470, W - 190, 1580), 55, OK); text(s, (W / 2, 1525), 'Pehle 30 din FREE', F('Black', 50), PAPER)
    brand_tag(s); save(s, 'pricing_1')
    s = canvas(True); header(s, 'Dukaan Premium', '₹199/month', dark=True)
    cards(s, [['1', 'Pro ke saare features'], ['2', 'Unlimited categories'], ['3', 'Photo se AI product listing'], ['4', 'Bol ke product jodo', 'Hindi, Hinglish, English']], h=180)
    text(s, (W / 2, 1450), 'Saalana: Pro ₹999  •  Premium ₹1,999', F('Bold', 40), PAPER)
    brand_tag(s, True); save(s, 'pricing_2')
    # FAQ
    qa = [('Kya commission lagta hai?', 'Nahi. 0% sales commission. Bas ek flat monthly fee.'),
          ('Payment kaise milta hai?', 'Customer seedha aapko UPI se pay karta hai. Paisa hum hold nahi karte.'),
          ('Trial ke liye card chahiye?', 'Nahi. Pro plan ke 30 din free, koi card nahi.'),
          ('Shop turant live hogi?', 'Details bharne ke baad shop review hoti hai, approve hote hi live.'),
          ('Kitne products daal sakte hain?', 'Unlimited. Pro mein 10 categories, Premium mein unlimited.'),
          ('AI features kahan hain?', 'Dukaan Premium (₹199/month) mein: photo aur voice se listing.')]
    for k in range(3):
        s = canvas(); header(s, 'Aapke sawaal,', 'humare jawab')
        for j, (q, a) in enumerate(qa[k * 2: k * 2 + 2]):
            y = 600 + j * 450; rrect(s, (90, y, W - 90, y + 400), 40, PAPER, shadow=True, outline=WHEAT, width=2)
            text(s, (140, y + 75), q, F('Black', 44), TERRA, anchor='lm')
            for i, ln in enumerate(wrap(a, F('SemiBold', 40), W - 280)): text(s, (140, y + 170 + i * 60), ln, F('SemiBold', 40), INK, anchor='lm')
        brand_tag(s); save(s, f'faq_{k + 1}')
    # Start free
    s = canvas(True); paste(s, SYM, W / 2, 560, 380, 1)
    header(s, 'Aaj hi shuru karo', 'Pehle 30 din FREE', dark=True, y=880)
    text(s, (W / 2, 1120), 'No card required  •  Dukaan Pro', F('SemiBold', 42), PAPER)
    rrect(s, (150, 1250, W - 150, 1390), 70, TERRA2); text(s, (W / 2, 1320), 'www.ghardukaan.shop', F('Black', 58), PAPER)
    text(s, (W / 2, 1480), '(Yahan link sticker lagao)', F('Medium', 34), (200, 170, 150))
    save(s, 'start_1')

if __name__ == '__main__':
    cover('how', icon_how); cover('pricing', icon_price); cover('faq', icon_faq); cover('start', icon_trial); cover('sellers', icon_shop)
    slides(); print(sorted(os.listdir(OUT)))
