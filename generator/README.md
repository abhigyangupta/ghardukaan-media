# GharDukaan daily video generator

Makes vertical (1080×1920) videos from `topics.json` (posted twice a day, slots `am` and `pm`): Hindi AI voice-over, Hinglish captions,
brand colours/fonts/logo, and an original synthesized music bed ducked under the voice.

```bash
bash setup.sh                         # installs deps, downloads the Kokoro voice model and fonts into .cache/
python3 make.py preview <topic_id>    # still frames only, in .cache/work/
python3 make.py next --date 2026-11-10  # renders ../2026-11-10/daily_<id>.mp4 + .json (captions per platform)
python3 make.py mark-posted <id> <date> '{"instagram":"<post id>", ...}'
```

- `topics.json` – the queue (posted in order). `posted.json` – what has gone out.
- `TOPICS_GUIDE.md` – rules for writing new topics (allowed facts, format).
- Voice: Kokoro `hf_alpha` at speed 1.0 + ffmpeg polish (see `voice.py`). Pronunciation fixes live in `voice.FIXES`.
- Everything here is generated locally; the music is synthesized, so there are no third-party rights in the audio.
- Animation (v2): `v2/scene.html` is an HTML/GSAP template (hook, list, stat, vs, outro) with an illustrated presenter whose mouth
  follows the voice track; `v2/engine.py` captures it frame by frame with headless Chromium (Playwright). A hand-built scene for one
  topic can live in `v2/custom/<topic_id>.html`. If v2 cannot run, `make.py` falls back to the old Pillow renderer (`render.py`);
  the output json says which `engine` was used. Force the old look with `GD_ENGINE=v1`.
- Formats: each topic has a `format` (tips, skit, quiz, myth, demo; see `TOPICS_GUIDE.md`). `make.py next` rotates them so the
  same format never runs twice in a row. `demo` scenes play real app footage cropped from `../tutorials`.
- Twice a day: `python3 make.py status --date <d> --slot am|pm` prints `DONE <id>` or `TODO`; pass `--slot` to `mark-posted` too.
