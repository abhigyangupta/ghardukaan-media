"""Make one daily GharDukaan video.

  python make.py next [--date YYYY-MM-DD]     render the next unposted topic
  python make.py <topic_id> [--date ...]       render a specific topic
  python make.py preview <topic_id>            write still frames only (fast check)
  python make.py mark-posted <topic_id> <date> <json-of-post-ids>

Output goes to ../<date>/daily_<topic_id>.mp4 plus ../<date>/daily_<topic_id>.json (captions for each platform).
"""
import datetime, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
TOPICS = os.path.join(HERE, 'topics.json'); POSTED = os.path.join(HERE, 'posted.json')
CTA = 'Dukaan Pro ₹99/month • Pehle 30 din FREE'

def load(p, d): return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else d

def next_topic():
    done = {p['id'] for p in load(POSTED, [])}
    for t in load(TOPICS, []):
        if t['id'] not in done: return t
    raise SystemExit('NO_TOPICS_LEFT: add new topics to topics.json (see TOPICS_GUIDE.md)')

def captions(t):
    body, tags = t['caption'].strip(), t['hashtags'].strip()
    title = t['yt_title'].strip()
    if '#Shorts' not in title: title = (title + ' | GharDukaan #Shorts')
    # Tagged links let the site credit sign-ups to the channel and the daily topic.
    link = lambda src, med: f"https://www.ghardukaan.shop/?utm_source={src}&utm_medium={med}&utm_campaign=daily_{t['id']}"
    return {'instagram': f'{body}\n\n{CTA}\n👉 Link in bio: www.ghardukaan.shop\n\n{tags}',
            'facebook': f'{body}\n\n{CTA}\n👉 {link("facebook", "reel")}\n\n{tags}',
            'youtube': f'{body}\n\n{CTA}\n👉 {link("youtube", "shorts")}\n\n{tags} #Shorts',
            'youtube_title': title[:100]}

def build(t, date, preview=False):
    from voice import make_voiceover
    from render import Video, OUTRO
    from music import make_music
    outdir = os.path.join(REPO, date); os.makedirs(outdir, exist_ok=True)
    work = os.path.join(HERE, '.cache', 'work'); os.makedirs(work, exist_ok=True)
    lines = [s['vo'] for s in t['scenes']] + [OUTRO['vo']]
    vo = os.path.join(work, 'vo.wav'); marks, total = make_voiceover(lines, vo)
    v = Video(t, marks, total)
    if preview:
        for i, m in enumerate(marks):
            ts = round((m['start'] + m['end']) / 2 + 0.6, 2)
            v.frame(ts).resize((540, 960)).save(os.path.join(work, f'preview_{i}.png'))
        print(json.dumps({'preview': work, 'marks': marks, 'total': total})); return
    silent = os.path.join(work, 'video.mp4'); v.render(silent)
    mus = os.path.join(work, 'music.wav')
    make_music(mus, v.dur, cues=[m['start'] for m in marks[1:]], seed=sum(map(ord, t['id'])) % 1000, key_semi=[0, 2, -3, 5][len(t['id']) % 4])
    out = os.path.join(outdir, f"daily_{t['id']}.mp4")
    fc = ('[2:a]apad,volume=1.0,aformat=channel_layouts=stereo,asplit=2[vo][sc];'
          '[1:a]apad,volume=0.5[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];'
          '[duck][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', silent, '-i', mus, '-i', vo, '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(v.dur), '-movflags', '+faststart', out], check=True)
    meta = {'id': t['id'], 'date': date, 'video': os.path.relpath(out, REPO), 'duration': v.dur,
            'thumbnail_ms': int((marks[0]['start'] + marks[0]['end']) / 2 * 1000), **captions(t)}
    json.dump(meta, open(out.replace('.mp4', '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False))

if __name__ == '__main__':
    a = sys.argv[1:]; date = datetime.date.today().isoformat()
    if '--date' in a: i = a.index('--date'); date = a[i + 1]; a = a[:i] + a[i + 2:]
    if a[0] == 'mark-posted':
        log = load(POSTED, []); log.append({'id': a[1], 'date': a[2], 'posts': json.loads(a[3]) if len(a) > 3 else {}})
        json.dump(log, open(POSTED, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('logged', a[1])
    elif a[0] == 'preview':
        build(next(t for t in load(TOPICS, []) if t['id'] == a[1]), date, preview=True)
    else:
        t = next_topic() if a[0] == 'next' else next(t for t in load(TOPICS, []) if t['id'] == a[0])
        build(t, date)
