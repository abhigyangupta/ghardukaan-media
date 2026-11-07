# Writing new daily topics

Each entry in `topics.json` becomes one ~25–35 s vertical video (Hindi voice-over, Hinglish captions)
plus an automatic outro ("ghardukaan.shop pe aaj hi apni dukaan banao. Pehle 30 din FREE.").

## Shape
```json
{"id": "kebab-case-unique", "theme": "light|night (alternate with the previous topic)",
 "yt_title": "Short hook title, under 70 chars",
 "caption": "Hinglish post body: hook line, 3-5 short points, a save/share/comment prompt. No link, no hashtags.",
 "hashtags": "#GharDukaan + 5 relevant tags",
 "scenes": [
   {"kind": "hook", "vo": "...", "cap": "...", "big": ["line 1", "BIG line 2", "line 3"]},
   {"kind": "list", "vo": "...", "cap": "...", "head": ["small line", "big line"], "items": [["1", "Title", "optional sub"], ...]},
   {"kind": "stat", "vo": "...", "cap": "...", "head": [..], "stat": "0%", "sub": "...", "note": "..."},
   {"kind": "vs",   "vo": "...", "cap": "...", "head": [..], "rows": [["Pehle (bad)", "Ab (good)"], ...]}
 ]}
```
- 3 scenes (hook + 2 body) is the sweet spot; each `vo` line about 10–16 Hindi words.
- `vo` is in Devanagari (for the voice). `cap` is the same meaning in Roman Hinglish.
- Item markers must be digits, `₹` or `%` only — the font has no emoji. No emoji anywhere in scenes.
- List items appear one by one while the line is spoken, so order them the way the voice says them.

## Facts you may state (from the app's `src/config/plans.ts`)
- Dukaan Pro ₹99/month or ₹999/year: unlimited products, up to 10 categories, own *.ghardukaan.shop link,
  branding, printable QR standee kit, 0% sales commission, direct UPI payouts. **No AI.**
- Dukaan Premium ₹199/month or ₹1,999/year: everything in Pro + unlimited categories + AI photo-to-product,
  voice-to-product (Hindi/Hinglish/English), AI descriptions/SEO/marketing. **Paid from day one, no trial.**
- 30-day free trial is for **Pro only**; no card required.
- Customers order on WhatsApp (prefilled message with items, quantity, total) and pay the seller directly by UPI.
- Shops are reviewed/approved before going live — never promise "2 minute mein live".
- Only *.ghardukaan.shop subdomains; no custom domains.

## Never
- Invent numbers about GharDukaan (sellers, orders, earnings) or name competitors.
- Promise income or results. Hypothetical maths must be labelled ("udaharan ke liye").
- Repeat a topic already in `topics.json` or `posted.json`.

## Good topic areas
Seller skills (photos, pricing, descriptions, packaging, delivery, replies, reviews), marketing (WhatsApp status,
Instagram, QR at stalls, festivals and seasons), business ideas by category, and one GharDukaan feature
explainer roughly every 4–5 days.
