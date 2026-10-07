"""Original soundtrack for the 4Skales clinic ad.

128 BPM, A minor, 19.7 s. Every hit is placed on the video's cut points
(see CUES below), so the music and the edit move together.
Writes assets/soundtrack.wav and assets/soundtrack.mp3.

Usage: python3 tools/compose-music.py
"""
import subprocess
import numpy as np
from scipy import signal

SR = 44100
BPM = 128
BEAT = 60 / BPM            # 0.46875 s
BAR = BEAT * 4             # 1.875 s
DUR = 19.7
N = int(DUR * SR)
rng = np.random.default_rng(4)

# Cut points in the video (seconds); keep in sync with index.html.
CUES = {
    "old_site": BAR * 1,          # 1.875
    "logo": BAR * 2,              # 3.75
    "taps": [BEAT * 12, BEAT * 13, BEAT * 14, BEAT * 15],
    "send": BEAT * 18,            # 8.4375
    "ping": BEAT * 19.4,          # 9.09
    "chips": [BEAT * 23 + i * BEAT for i in range(5)],
    "price": BEAT * 28,           # 13.125
    "proof": BEAT * 32,           # 15.0
    "end": BEAT * 36,             # 16.875
}


def t_axis(n):
    return np.arange(n) / SR


def place(bus, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(bus):
        return
    j = min(len(bus), i + len(sig))
    bus[i:j] += sig[: j - i] * gain


def env_exp(n, decay):
    return np.exp(-t_axis(n) / decay)


def lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc, SR / 2 - 100) / (SR / 2), "low")
    return signal.lfilter(b, a, x)


def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), "high")
    return signal.lfilter(b, a, x)


def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), hi / (SR / 2)], "band")
    return signal.lfilter(b, a, x)


def note(n):
    """MIDI note number to Hz."""
    return 440 * 2 ** ((n - 69) / 12)


# ---------- instruments ----------
def kick():
    n = int(0.42 * SR); t = t_axis(n)
    f = 46 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, 0.16)
    click = hp(rng.standard_normal(n), 3000) * env_exp(n, 0.004) * 0.35
    return np.tanh((body + click) * 1.6) * 0.9


def clap():
    n = int(0.3 * SR); out = np.zeros(n)
    for k, d in enumerate([0, 0.011, 0.022]):
        burst = bp(rng.standard_normal(n), 900, 2600) * env_exp(n, 0.006 if k < 2 else 0.09)
        out[int(d * SR):] += burst[: n - int(d * SR)]
    return out * 0.5


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    return hp(rng.standard_normal(n), 7500, 3) * env_exp(n, 0.05 if open_ else 0.01) * 0.09


def sub(freq, length):
    n = int(length * SR); t = t_axis(n)
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    a = np.minimum(1, t / 0.006) * np.exp(-t / (length * 0.9))
    return np.tanh(s * a * 1.4) * 0.55


def saw(freq, n, detune=0.0):
    t = t_axis(n)
    return 2 * ((t * freq * (1 + detune)) % 1) - 1


def pluck(freq, length=0.28, bright=3200):
    n = int(length * SR)
    s = (saw(freq, n) + saw(freq, n, 0.006) + saw(freq, n, -0.006)) / 3
    s = lp(s, bright) * env_exp(n, 0.09)
    return s * np.minimum(1, t_axis(n) / 0.003) * 0.32


def pad(freqs, length):
    n = int(length * SR); t = t_axis(n); s = np.zeros(n)
    for f in freqs:
        for d in (-0.004, 0, 0.004):
            s += saw(f, n, d)
    s = lp(s / (len(freqs) * 3), 1400, 2)
    a = np.minimum(1, t / 0.25) * np.minimum(1, (length - t) / 0.6).clip(0, 1)
    return s * a * 0.22


def riser(length, peak=9000):
    n = int(length * SR); out = np.zeros(n); noise = rng.standard_normal(n)
    chunks = 40
    for c in range(chunks):
        a, b = c * n // chunks, (c + 1) * n // chunks
        fc = 300 * (peak / 300) ** (c / chunks)
        out[a:b] = bp(noise, fc * 0.7, min(fc * 1.4, SR / 2 - 200))[a:b]
    t = t_axis(n)
    return out * (t / length) ** 2 * 0.35


def whoosh(length=0.32):
    n = int(length * SR); t = t_axis(n); out = np.zeros(n); noise = rng.standard_normal(n)
    for c in range(16):
        a, b = c * n // 16, (c + 1) * n // 16
        fc = 600 + 5000 * np.sin(np.pi * c / 16)
        out[a:b] = bp(noise, fc * 0.6, fc * 1.5)[a:b]
    return out * np.sin(np.pi * t / length) ** 2 * 0.3


def impact():
    n = int(1.4 * SR); t = t_axis(n)
    boom = np.sin(2 * np.pi * (38 + 60 * np.exp(-t / 0.05)) * t) * env_exp(n, 0.45)
    crack = lp(rng.standard_normal(n), 5000) * env_exp(n, 0.05) * 0.5
    return np.tanh((boom + crack) * 1.3) * 0.8


def tap_click():
    n = int(0.03 * SR)
    return bp(rng.standard_normal(n), 2500, 6000) * env_exp(n, 0.004) * 0.5


def ping():
    n = int(0.6 * SR); t = t_axis(n); out = np.zeros(n)
    for f, d in ((1318.5, 0), (1975.5, 0.085)):
        i = int(d * SR); m = n - i
        out[i:] += np.sin(2 * np.pi * f * t[:m]) * env_exp(m, 0.16) * 0.28
    return out


def buzz(length=0.36):
    n = int(length * SR); t = t_axis(n)
    s = np.sign(np.sin(2 * np.pi * 170 * t)) * 0.5 + np.sin(2 * np.pi * 85 * t)
    am = (np.sin(2 * np.pi * 24 * t) > -0.2).astype(float)
    return lp(s * am, 900) * np.minimum(1, t / 0.01) * np.minimum(1, (length - t) / 0.02) * 0.32


def tick():
    n = int(0.02 * SR)
    return hp(rng.standard_normal(n), 4000) * env_exp(n, 0.003) * 0.35


def reverb(x, length=1.1, mix=0.22):
    n = int(length * SR)
    ir = rng.standard_normal(n) * np.exp(-t_axis(n) / (length / 5))
    ir = lp(ir, 6000); ir /= np.sqrt(np.sum(ir ** 2))
    wet = signal.fftconvolve(x, ir)[: len(x)]
    return x + wet * mix


# ---------- arrangement ----------
drums = np.zeros(N); bass = np.zeros(N); music = np.zeros(N); fx = np.zeros(N)
duck = np.ones(N)

# chord roots per bar: Am  F  C  G
PROG = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]

# Bar 1 (intro): phone buzzes + ticking clock + filtered arp
place(fx, buzz(), 0.02); place(fx, buzz(), 0.55); place(fx, buzz(), 1.08)
for i in range(16):
    place(fx, tick(), i * BEAT / 4, 0.6 if i % 4 else 1.0)
for i in range(8):
    root, chord = PROG[0]
    place(music, pluck(note(chord[i % 3] + 12), 0.2, 1400), i * BEAT / 2, 0.6)
place(fx, riser(BAR * 0.9), BAR * 0.1, 0.8)

# Bars 2 onward: full groove, with breaks around the hits
bars_total = int(np.ceil(DUR / BAR))
for bar in range(1, bars_total):
    t0 = bar * BAR
    root, chord = PROG[bar % 4]
    for b in range(4):
        tb = t0 + b * BEAT
        if tb >= CUES["end"] + BEAT * 4:
            break
        place(drums, kick(), tb)
        k = int(tb * SR); m = min(N, k + int(0.22 * SR))
        duck[k:m] = np.minimum(duck[k:m], 0.25 + 0.75 * (np.arange(m - k) / (m - k)) ** 0.7)
        if b in (1, 3):
            place(drums, clap(), tb, 0.85)
        for s16 in range(4):
            place(drums, hat(open_=(s16 == 2)), tb + s16 * BEAT / 4, 1.0 if s16 == 2 else 0.6)
        # offbeat sub bass
        place(bass, sub(note(root - 12), BEAT * 0.45), tb + BEAT / 2)
    # 16th arp
    for s in range(16):
        ts = t0 + s * BEAT / 4
        if ts >= CUES["end"] + BEAT * 4:
            break
        nt = chord[[0, 1, 2, 1][s % 4]] + (12 if s % 8 >= 4 else 0)
        place(music, pluck(note(nt), 0.18, 2200 + 1600 * (bar % 2)), ts, 0.55)

# stutter fill into the logo hit + reverse riser
for i in range(6):
    place(drums, clap(), CUES["logo"] - BEAT + i * BEAT / 6, 0.35 + i * 0.08)
place(fx, riser(BEAT * 1.4, 12000), CUES["logo"] - BEAT * 1.4, 1.0)
place(fx, impact(), CUES["logo"], 1.0)
place(fx, whoosh(), CUES["old_site"] - 0.16, 0.9)

# taps, send, ping
for tt in CUES["taps"]:
    place(fx, tap_click(), tt, 1.0)
place(fx, tap_click(), CUES["send"], 1.0)
place(fx, whoosh(0.28), CUES["send"] + 0.05, 0.7)
place(fx, ping(), CUES["ping"], 1.0)

# feature chips: rising stabs
for i, tc in enumerate(CUES["chips"]):
    place(music, pluck(note(72 + [0, 3, 7, 10, 12][i]), 0.25, 5000), tc, 0.9)
    place(fx, whoosh(0.18), tc - 0.06, 0.4)

# price drop: clap roll, riser, impact, pad
for i in range(8):
    place(drums, clap(), CUES["price"] - BEAT + i * BEAT / 8, 0.25 + i * 0.07)
place(fx, riser(BEAT * 2, 11000), CUES["price"] - BEAT * 2, 0.9)
place(fx, impact(), CUES["price"], 0.9)
place(music, pad([note(57), note(60), note(64)], BAR), CUES["price"], 1.0)

place(fx, whoosh(), CUES["proof"] - 0.15, 0.8)

# end: final impact, sustained chord, tail
place(fx, riser(BEAT * 2, 12000), CUES["end"] - BEAT * 2, 0.9)
place(fx, impact(), CUES["end"], 1.1)
place(music, pad([note(57), note(64), note(69), note(72)], DUR - CUES["end"]), CUES["end"], 1.6)
place(bass, sub(note(45), 2.4), CUES["end"], 1.2)

# ---------- mix ----------
music = reverb(lp(music, 9000), 1.2, 0.3) * duck
bass = bass * duck
drums = reverb(drums, 0.6, 0.08)
fx = reverb(fx, 1.0, 0.18)
mix = drums * 0.9 + bass * 0.95 + music * 0.75 + fx * 0.85

fade_in = np.minimum(1, t_axis(N) / 0.01)
fade_out = np.clip((DUR - t_axis(N)) / 0.9, 0, 1)
mix *= fade_in * fade_out
mix = np.tanh(mix * 1.25)
mix /= np.max(np.abs(mix)) / 0.89
stereo = np.stack([mix, np.roll(lp(mix, 12000), 12)], axis=1)

pcm = (stereo * 32767).astype(np.int16)
import wave
with wave.open("assets/soundtrack.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "assets/soundtrack.wav",
                "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "44100",
                "-c:a", "libmp3lame", "-b:a", "256k", "assets/soundtrack.mp3"], check=True)
print("wrote assets/soundtrack.mp3", DUR, "s")
