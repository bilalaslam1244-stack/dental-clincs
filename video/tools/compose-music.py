"""Original chill soundtracks for the three 4Skales Meta ads.

92 BPM lo-fi: soft Rhodes-style chords (Fmaj7 Em7 Dm7 Cmaj7), round kick,
brushed snare, shaker, warm sub and light vinyl crackle. Each ad gets its
own sound effects on its cut points (CUES below; keep in sync with
tools/build-ads.py).

Usage: python3 tools/compose-music.py      -> assets/music-ad1.mp3 ... ad3
"""
import subprocess
import wave
import numpy as np
from scipy import signal

SR = 44100
BPM = 92
B = 60 / BPM                # 0.652 s
BAR = B * 4
DUR = 7.5

CUES = {
    "ad1": {"buzz": [0.0, 0.42, 0.84], "whoosh": [2.0], "taps": [B * 4, B * 5, B * 6, B * 7],
            "swell": B * 8, "ping": [], "ticks": []},
    "ad2": {"buzz": [], "whoosh": [B * 7.3], "taps": [B * 1, B * 2, B * 3, B * 4, B * 7],
            "swell": B * 9, "ping": [B * 8], "ticks": []},
    "ad3": {"buzz": [], "whoosh": [B * 7 - 0.15], "taps": [], "swell": B * 9, "ping": [],
            "ticks": [B * 4, B * 5, B * 6], "open_hit": 0.0},
}


def tax(n):
    return np.arange(n) / SR


def env(n, d):
    return np.exp(-tax(n) / d)


def filt(x, kind, fc, order=2):
    w = np.array(fc) / (SR / 2)
    b, a = signal.butter(order, w, kind)
    return signal.lfilter(b, a, x)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def place(bus, sig, at, g=1.0):
    i = int(at * SR)
    if 0 <= i < len(bus):
        j = min(len(bus), i + len(sig))
        bus[i:j] += sig[: j - i] * g


def rhodes(freq, length, vel=1.0, rng=None):
    """Electric-piano tone: sine body + soft FM bell, tremolo, slow decay."""
    n = int(length * SR); t = tax(n)
    mod = np.sin(2 * np.pi * freq * 14 * t) * 1.2 * env(n, 0.05)
    body = np.sin(2 * np.pi * freq * t + mod) * env(n, 1.4)
    body += 0.35 * np.sin(2 * np.pi * freq * 2 * t) * env(n, 0.5)
    trem = 1 - 0.12 * (0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * t))
    att = np.minimum(1, t / 0.004)
    rel = np.clip((length - t) / 0.25, 0, 1)
    return body * trem * att * rel * 0.16 * vel


def chord(notes, length, rng, strum=0.018):
    n = int(length * SR); out = np.zeros(n + int(0.2 * SR))
    for k, m in enumerate(notes):
        place(out, rhodes(hz(m), length, 0.85 + 0.15 * rng.random()), k * strum)
    return out


def kick(rng):
    n = int(0.5 * SR); t = tax(n)
    f = 44 + 70 * np.exp(-t / 0.04)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.22)
    return filt(np.tanh(s * 1.2), "low", 1800) * 0.7


def snare(rng):
    n = int(0.35 * SR)
    noise = filt(rng.standard_normal(n), "band", [700, 4200]) * env(n, 0.09)
    tone = np.sin(2 * np.pi * 190 * tax(n)) * env(n, 0.04)
    return (noise * 0.5 + tone * 0.3) * 0.5


def shaker(rng):
    n = int(0.07 * SR)
    return filt(rng.standard_normal(n), "high", 6000) * env(n, 0.02) * np.minimum(1, tax(n) / 0.01) * 0.05


def sub(freq, length):
    n = int(length * SR); t = tax(n)
    a = np.minimum(1, t / 0.02) * np.clip((length - t) / 0.1, 0, 1)
    return np.sin(2 * np.pi * freq * t) * a * 0.38


def crackle(n, rng):
    out = filt(rng.standard_normal(n), "band", [800, 6000]) * 0.006
    pops = (rng.random(n) > 0.99985).astype(float) * rng.standard_normal(n)
    return out + filt(pops, "high", 1500) * 0.12


def soft_tap(rng):
    n = int(0.06 * SR)
    wood = np.sin(2 * np.pi * 1700 * tax(n)) * env(n, 0.012)
    return (wood + filt(rng.standard_normal(n), "band", [2000, 5000]) * env(n, 0.004) * 0.4) * 0.38


def soft_ping():
    n = int(1.0 * SR); out = np.zeros(n)
    for f, d in ((1046.5, 0), (1568.0, 0.11)):
        i = int(d * SR); m = n - i; t = tax(m)
        out[i:] += np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * 2 * t) * env(m, 0.05)) * env(m, 0.35) * 0.16
    return out


def buzz(rng):
    n = int(0.26 * SR); t = tax(n)
    s = np.sin(2 * np.pi * 150 * t) * (np.sin(2 * np.pi * 28 * t) > -0.3)
    return filt(s, "low", 700) * np.minimum(1, t / 0.01) * np.clip((0.26 - t) / 0.03, 0, 1) * 0.2


def whoosh(rng, length=0.55):
    n = int(length * SR); t = tax(n); noise = rng.standard_normal(n); out = np.zeros(n)
    for c in range(12):
        a, b2 = c * n // 12, (c + 1) * n // 12
        fc = 400 + 2600 * np.sin(np.pi * c / 12)
        out[a:b2] = filt(noise, "band", [fc * 0.6, fc * 1.4])[a:b2]
    return out * np.sin(np.pi * t / length) ** 2 * 0.12


def swell(rng, length=1.3):
    """Reverse-piano style swell that lands on `at` (placed at at - length)."""
    n = int(length * SR); t = tax(n)
    s = sum(np.sin(2 * np.pi * hz(m) * t) for m in (65, 69, 72, 76)) / 4
    return s * (t / length) ** 3 * 0.18


def tick(rng):
    n = int(0.05 * SR)
    return np.sin(2 * np.pi * 2400 * tax(n)) * env(n, 0.01) * 0.2


def reverb(x, length, mix, rng):
    n = int(length * SR)
    ir = filt(rng.standard_normal(n), "low", 5000) * np.exp(-tax(n) / (length / 4))
    ir /= np.sqrt(np.sum(ir ** 2))
    return x + signal.fftconvolve(x, ir)[: len(x)] * mix


PROG = [(41, [53, 57, 60, 64]),   # Fmaj7
        (40, [52, 55, 59, 62]),   # Em7
        (38, [50, 53, 57, 60]),   # Dm7
        (36, [48, 52, 55, 59])]   # Cmaj7


def build(ad):
    rng = np.random.default_rng({"ad1": 1, "ad2": 2, "ad3": 3}[ad])
    cue = CUES[ad]
    N = int(DUR * SR)
    keys, drums, bass, fx = (np.zeros(N) for _ in range(4))
    duck = np.ones(N)

    bars = int(np.ceil(DUR / BAR))
    for bar in range(bars):
        t0 = bar * BAR
        root, notes = PROG[bar % 4]
        place(keys, chord(notes, BAR * 0.98, rng), t0)
        place(keys, chord([notes[1] + 12, notes[3] + 12], BEAT_HALF, rng), t0 + B * 2.5, 0.5)
        place(bass, sub(hz(root), B * 1.6), t0)
        place(bass, sub(hz(root), B * 0.8), t0 + B * 2.5)
        for b in range(4):
            tb = t0 + b * B
            if b in (0,) or (b == 2):
                place(drums, kick(rng), tb + (0.0 if b == 0 else B * 0.5))
                k = int((tb + (0.0 if b == 0 else B * 0.5)) * SR); m = min(N, k + int(0.3 * SR))
                if k < N:
                    duck[k:m] = np.minimum(duck[k:m], 0.6 + 0.4 * np.linspace(0, 1, m - k))
            if b in (1, 3):
                place(drums, snare(rng), tb + 0.012)
            for e in range(2):
                place(drums, shaker(rng), tb + e * B / 2 + 0.01 * rng.random(), 1.0 if e else 0.6)

    for at in cue["buzz"]:
        place(fx, buzz(rng), at)
    for at in cue["whoosh"]:
        place(fx, whoosh(rng), at)
    for at in cue["taps"]:
        place(fx, soft_tap(rng), at)
    for at in cue["ping"]:
        place(fx, soft_ping(), at)
    for at in cue["ticks"]:
        place(fx, tick(rng), at)
    sw = swell(rng)
    place(fx, sw, cue["swell"] - len(sw) / SR)
    if "open_hit" in cue:
        place(fx, kick(rng), cue["open_hit"], 0.9)

    keys = reverb(filt(keys, "low", 4200), 1.6, 0.35, rng) * duck
    drums = reverb(filt(drums, "low", 9000), 0.8, 0.12, rng)
    fx = reverb(fx, 1.2, 0.25, rng)
    mix = keys * 1.0 + drums * 0.8 + bass * duck * 0.9 + fx * 1.0 + crackle(N, rng)
    t = tax(N)
    mix *= np.minimum(1, t / 0.03) * np.clip((DUR - t) / 0.7, 0, 1)
    mix = np.tanh(mix * 1.6)
    mix /= np.max(np.abs(mix)) / 0.89
    right = np.roll(filt(mix, "low", 11000), 14)
    pcm = (np.stack([mix, right], axis=1) * 32767).astype(np.int16)
    wav = f"/tmp/music-{ad}.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "loudnorm=I=-15:TP=-1.0:LRA=9",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "256k", f"assets/music-{ad}.mp3"], check=True)
    print("wrote", f"assets/music-{ad}.mp3")


BEAT_HALF = B * 1.4

if __name__ == "__main__":
    for ad in CUES:
        build(ad)
