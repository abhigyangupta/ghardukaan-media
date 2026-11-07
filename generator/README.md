# GharDukaan daily video generator

Makes one vertical (1080×1920) video per day from `topics.json`: Hindi AI voice-over, Hinglish captions,
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
