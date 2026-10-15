"""Generate an original, royalty-free upbeat backing track (WAV) for stories.

Usage: python3 tools/make_music.py <out.wav> [seconds=10] [variant=0]
120 BPM, I-V-vi-IV progression, pad + pluck arpeggio + bass + light drums.
variant picks the key and arpeggio pattern so stories don't all sound identical.
"""
import sys, wave
import numpy as np

out = sys.argv[1]
secs = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
variant = int(sys.argv[3]) if len(sys.argv) > 3 else 0
SR = 44100
BPM = 120
beat = 60 / BPM
n = int(SR * secs)
t_all = np.arange(n) / SR
mix = np.zeros((n, 2))

keys = [0, 2, -3, 5, -2]                      # C, D, A, F, Bb
root = 60 + keys[variant % len(keys)]          # MIDI
prog = [(0, 4, 7), (7, 11, 14), (9, 12, 16), (5, 9, 12)]   # I V vi IV
patterns = [[0, 1, 2, 1, 0, 2, 1, 2], [0, 2, 1, 2, 0, 1, 2, 1], [0, 1, 2, 3, 2, 1, 0, 1]]
pat = patterns[variant % len(patterns)]

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def env(length, a, r):
    e = np.ones(length)
    ai, ri = int(a * SR), int(r * SR)
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e

def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= n: return
    sig = sig[: n - i] * gain
    mix[i:i + len(sig), 0] += sig * (1 - pan) / 2 * 2 ** .5
    mix[i:i + len(sig), 1] += sig * (1 + pan) / 2 * 2 ** .5

def lowpass(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y

bar = 4 * beat
nbars = int(np.ceil(secs / bar))
for b in range(nbars):
    chord = prog[b % 4]
    t0 = b * bar
    L = int(bar * SR)
    tt = np.arange(L) / SR
    # pad: detuned saws, softened
    pad = np.zeros(L)
    for c in chord:
        f = hz(root + c - 12)
        for d in (-0.08, 0.08):
            ph = (tt * f * (1 + d / 100 * 12)) % 1
            pad += (2 * ph - 1)
    pad = lowpass(pad / 6, 0.035) * env(L, 0.35, 0.4)
    add(pad, t0, 0, 0.30)
    # bass: root, eighth-note pulse
    for k in range(8):
        Lb = int(beat / 2 * SR); tb = np.arange(Lb) / SR
        f = hz(root + chord[0] - 24)
        s = np.sin(2 * np.pi * f * tb) + 0.3 * np.sin(4 * np.pi * f * tb)
        add(s * np.exp(-tb * 6) * env(Lb, 0.005, 0.02), t0 + k * beat / 2, 0, 0.32)
    # pluck arpeggio, 8ths, slight echo
    for k, idx in enumerate(pat):
        notes = list(chord) + [chord[0] + 12]
        f = hz(root + notes[idx % len(notes)] + 12)
        Lp = int(0.45 * SR); tp = np.arange(Lp) / SR
        s = (np.sin(2 * np.pi * f * tp) + 0.25 * np.sin(6 * np.pi * f * tp)) * np.exp(-tp * 9)
        st = t0 + k * beat / 2
        add(s, st, -0.35, 0.16)
        add(s, st + beat * 0.75, 0.45, 0.07)   # dotted-eighth echo
    # drums
    for k in range(4):
        st = t0 + k * beat
        Lk = int(0.25 * SR); tk = np.arange(Lk) / SR
        kick = np.sin(2 * np.pi * (45 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 11)
        if b > 0 or k >= 2:                    # drums enter after half a bar
            add(kick, st, 0, 0.55)
        if k in (1, 3) and b > 0:
            Lc = int(0.18 * SR)
            clap = np.random.default_rng(b * 10 + k).normal(0, 1, Lc) * np.exp(-np.arange(Lc) / SR * 22)
            add(lowpass(clap, 0.5), st, 0.1, 0.16)
        for h in (0, 0.5):
            if b == 0: continue
            Lh = int(0.05 * SR)
            hat = np.random.default_rng(int(st * 1000 + h * 10)).normal(0, 1, Lh)
            hat = (hat - lowpass(hat, 0.6)) * np.exp(-np.arange(Lh) / SR * 70)
            add(hat, st + h * beat, 0.3, 0.07 if h else 0.04)

mix = np.tanh(mix * 1.3) * 0.85
mix /= np.max(np.abs(mix)) / 0.89
data = (mix * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(data.tobytes())
print("ok", out)
