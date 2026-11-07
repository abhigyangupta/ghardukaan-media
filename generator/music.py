"""Original royalty-free music bed, synthesized from scratch (tabla-style beat, sitar-like pluck, drone)."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100

def make_music(out_wav, total, cues=(), seed=7, bpm=112, key_semi=0):
    rng = np.random.default_rng(seed); N = int(SR * total); out = np.zeros((N, 2)); BEAT = 60 / bpm

    def add(sig, t0, gain=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= N or i < 0: return
        sig = sig[:N - i] * gain
        out[i:i + len(sig), 0] += sig * (1 - max(pan, 0)); out[i:i + len(sig), 1] += sig * (1 + min(pan, 0))

    def env(n, a=0.003, d=0.3):
        t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)

    def bayan(f0=70):
        n = int(0.6 * SR); t = np.arange(n) / SR; f = f0 * (1 + 0.6 * np.exp(-t / 0.04))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.18)

    def dayan(f0=520):
        n = int(0.5 * SR); t = np.arange(n) / SR
        s = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 2.01 * t) + 0.3 * np.sin(2 * np.pi * f0 * 2.98 * t)
        return (s * env(n, 0.001, 0.12) + 0.4 * rng.normal(0, 1, n) * np.exp(-t / 0.006)) * 0.5

    def shaker():
        n = int(0.08 * SR); b, a = butter(2, 6000 / (SR / 2), 'high')
        return lfilter(b, a, rng.normal(0, 1, n)) * env(n, 0.004, 0.025)

    def pluck(freq, dur=0.6):
        n = int(dur * SR); p = max(2, int(SR / freq)); buf = rng.uniform(-1, 1, p); y = np.zeros(n)
        for i in range(n):
            y[i] = buf[i % p]; buf[i % p] = 0.996 * (0.55 * buf[i % p] + 0.45 * buf[(i + 1) % p])
        return y * env(n, 0.002, dur)

    def pad(freq, dur):
        n = int(dur * SR); t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * freq * m * t + m) / m for m in (1, 2, 3, 4))
        e = np.minimum(t / 0.4, 1) * np.minimum((dur - t) / 0.4, 1); b, a = butter(2, 1800 / (SR / 2))
        return lfilter(b, a, s * e) * 0.18

    def whoosh(dur=0.5):
        n = int(dur * SR); t = np.arange(n) / SR; noise = rng.normal(0, 1, n); o = np.zeros(n)
        for k in range(0, n, 512):
            fc = 400 + 5000 * (k / n); b, a = butter(2, [fc / (SR / 2) * 0.7, min(fc / (SR / 2) * 1.3, 0.99)], 'band')
            o[k:k + 512] = lfilter(b, a, noise[k:k + 512])
        return o * np.sin(np.pi * t / dur) * 0.6

    def ding(freq=1568):
        n = int(1.2 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2.76 * t)) * env(n, 0.001, 0.35) * 0.35

    D = 146.83 * 2 ** (key_semi / 12)
    note = lambda s, o=0: D * 2 ** (s / 12 + o)
    pattern = ['B', 'b', 'T', 't', 'T', 'k', 'B', 'T']
    for i in range(int(total / BEAT)):
        t0 = i * BEAT
        if t0 > total - 0.6: break
        p = pattern[i % 8]
        if p == 'B': add(bayan(), t0, 0.9); add(dayan(520), t0, 0.4, 0.2)
        if p == 'b': add(bayan(90), t0, 0.5)
        if p == 'T': add(dayan(520), t0, 0.55, 0.2)
        if p == 't': add(dayan(780), t0, 0.35, 0.3)
        if p == 'k': add(dayan(640), t0, 0.3, -0.2)
        add(shaker(), t0, 0.15, -0.4); add(shaker(), t0 + BEAT / 2, 0.25, -0.4)
    chords = [(0, 7), (5, 9), (7, 11), (0, 7)]; bar = 4 * BEAT
    for b in range(int(total / bar) + 1):
        r, f = chords[b % 4]; add(pad(note(r, -1), bar + 0.05), b * bar, 1.0); add(pad(note(f, -1), bar + 0.05), b * bar, 0.7)
    mel = [4, 7, 9, 7, 4, 2, 0, None, 2, 4, 7, 4, 2, None, 0, None, 7, 9, 12, 9, 7, 4, 7, None, 9, 7, 4, 2, 4, None, None, None]
    t0, k = BEAT * 2, 0
    while t0 < total - 1.0:
        s = mel[k % len(mel)]
        if s is not None: add(pluck(note(s, 1), 0.7), t0, 0.28, 0.25)
        t0 += BEAT / 2; k += 1
    for c in cues: add(whoosh(), c - 0.45, 0.3)
    add(ding(), total - 2.4, 0.8); add(ding(1975), total - 2.25, 0.6)
    fade = np.ones(N); fl = int(0.9 * SR); fade[-fl:] = np.linspace(1, 0, fl); out *= fade[:, None]
    out = np.tanh(out / np.abs(out).max() * 1.6) * 0.89
    wavfile.write(out_wav, SR, (out * 32767).astype(np.int16))
