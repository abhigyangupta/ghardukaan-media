# Writing new daily topics

Each entry in `topics.json` becomes one ~25–35 s vertical video (Hindi voice-over, Hinglish captions)
plus an automatic outro ("ghardukaan.shop pe aaj hi apni dukaan banao. Pehle 30 din FREE.").

## Formats (rotate them!)
Every topic has a `"format"`. Reels were all looking the same, so `make.py next` never posts the same format twice
in a row (and avoids the last two when it can). When writing new topics, spread them across all five:

| format | what it is | scenes | theme |
|---|---|---|---|
| `tips` | classic hook + list/stat/vs | `hook`, `list`, `stat`, `vs` | `light` / `night` |
| `skit` | WhatsApp chat between a customer and the seller (problem chat, then tip, then happy chat) | `chat` + `list` | `teal` / `night` |
| `quiz` | question with A/B(/C) options and a 3-2-1 countdown, then the answer | `quiz`, `quiz` with `"reveal": true`, then `list` or `stat` | `indigo` / `night` |
| `myth` | a common wrong belief gets stamped GALAT, then the SACH card | `myth` + `list` / `stat` | `rose` / `leaf` |
| `demo` | real app screen recording in a phone frame, with steps beside it | `demo` (1–2 scenes) | `marigold` / `teal` |

New scene kinds:
```json
{"kind": "chat", "vo": "...", "cap": "...", "head": ["small line", "big line"], "who": "Customer",
 "msgs": [["c", "customer message"], ["s", "seller reply"], ["c", "..."]]}
{"kind": "quiz", "vo": "... (ask the question; 3 s of silence is added for the countdown)", "cap": "...",
 "q": "Question?", "opts": ["Option A", "Option B", "Option C"], "ans": 1}
{"kind": "quiz", "reveal": true, "vo": "Sahi jawab ...", "cap": "...", "q": "same question", "opts": [same], "ans": 1,
 "why": "one-line reason"}
{"kind": "myth", "vo": "...", "cap": "...", "myth": "the wrong belief", "fact": "the truth, short"}
{"kind": "demo", "vo": "...", "cap": "...", "clip": "t1b_add_first_product", "from": 1, "head": ["small", "big"],
 "steps": ["step 1", "step 2", "step 3"]}
```
- `chat`: 2–4 messages, each under ~45 characters. `c` = customer (left, white), `s` = seller (right, green).
- `quiz`: 2–3 options, under ~26 characters each; `ans` is the 0-based index of the right one. Always follow with the reveal scene.
- `myth`: myth and fact under ~60 characters each. The myth must be a real belief sellers have, and the fact must be true.
- `demo`: `clip` is a file name (without .mp4) in `../tutorials`; `from` is the second to start at. Check the clip shows
  what the voice says (extract a few frames first). Available: t1b_add_first_product (0–37 s: photos, name, price,
  variants), t1c_upi_and_approval (UPI ID, trial), t2a_storefront_branding_policies, t2b_upi_qr_delivery,
  t2c_help_ticket, t3c_categories_new_product (0–8 s categories, 9–20 s new product form; ends on a logo card).
  Avoid the last 2–3 s of each clip (end card). 2–3 short steps.

## Shape
```json
{"id": "kebab-case-unique", "format": "tips|skit|quiz|myth|demo",
 "theme": "light|night|teal|indigo|rose|leaf|marigold (see the formats table; differ from the previous topic)",
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
