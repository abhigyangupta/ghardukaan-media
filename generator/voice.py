"""Hindi voice-over: Kokoro (ONNX, offline) + studio polish via ffmpeg.

Voice choice (tested 2026-11-07 with Whisper round-trip intelligibility):
hf_alpha at speed 1.0 scored best; 1.14x was clearly worse, so keep speed at 1.0.
"""
import json, os, subprocess, tempfile
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '.cache')
VOICE, SPEED, SR = 'hf_alpha', 1.0, 24000
LEAD, GAP = 0.35, 0.3

# Pronunciation fixes applied to every line before synthesis.
FIXES = {'GharDukaan': 'घरदुकान', 'घरदुकान': 'घर-दुकान', 'UPI': 'यू-पी-आई', 'यूपीआई': 'यू-पी-आई',
         'WhatsApp': 'व्हाट्सऐप', 'QR': 'क्यू-आर', '₹99': 'निन्यानवे रुपये', '₹199': 'एक सौ निन्यानवे रुपये'}

# Studio polish: clean lows, gentle presence lift, de-ess, compression, light room, loudness to -16 LUFS.
POLISH = ('highpass=f=75,lowpass=f=11500,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=3,'
          'deesser=i=0.35,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,'
          'aecho=0.8:0.5:22:0.12,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=44100')

def _clean(s):
    for a, b in FIXES.items(): s = s.replace(a, b)
    return s

def make_voiceover(lines, out_wav):
    """Synthesize lines in order; returns marks [{start,end}] in seconds and total length."""
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(CACHE, 'kokoro-v1.0.onnx'), os.path.join(CACHE, 'voices-v1.0.bin'))
    parts = [np.zeros(int(LEAD * SR), np.float32)]; t = LEAD; marks = []
    for line in lines:
        s, _ = k.create(_clean(line), voice=VOICE, speed=SPEED, lang='hi')
        s = s.astype(np.float32); idx = np.where(np.abs(s) > 0.01)[0]
        s = s[max(0, idx[0] - 600): idx[-1] + 1500]
        # 8 ms fades avoid clicks at the cut points
        f = int(0.008 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
        marks.append({'start': round(t, 3), 'end': round(t + len(s) / SR, 3)})
        parts += [s, np.zeros(int(GAP * SR), np.float32)]; t += len(s) / SR + GAP
    raw = tempfile.mktemp(suffix='.wav'); sf.write(raw, np.concatenate(parts), SR)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-af', POLISH, '-ac', '1', out_wav], check=True)
    os.remove(raw)
    total = sf.info(out_wav).duration
    return marks, round(total, 3)
