"""Calm, beat-synced soundtrack for the 14 s main ad (before/after + free 30 days).

80 BPM. Keys and a warm pad carry it; a soft kick and rim enter on the
"after" cut and step back for the end card. Every hit sits on a cut
(beats listed in CUES, matching tools/build-main.py).
Writes assets/music-main.mp3.
"""
import importlib.util
import subprocess
import wave
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location("cm", Path(__file__).with_name("compose-music.py"))
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
SR, tax, env, filt, hz, place = cm.SR, cm.tax, cm.env, cm.filt, cm.hz, cm.place

BPM = 80
B = 60 / BPM               # 0.75 s
BAR = B * 4
DUR = 14.0
CUES = dict(after=3, taps=[4, 5, 6], targeting=7, pings=[8, 9, 10], offer=11, lines=[13, 14], end=15)
PROG = [(41, [53, 57, 60, 64]), (40, [52, 55, 59, 62]), (38, [50, 53, 57, 60]),
        (36, [48, 52, 55, 59]), (41, [53, 57, 60, 64, 67])]


def pad(notes, length, rng):
    n = int(length * SR); t = tax(n); s = np.zeros(n)
    for m in notes:
        for d in (-0.003, 0.003):
            s += np.sin(2 * np.pi * hz(m) * (1 + d) * t) + 0.3 * np.sin(2 * np.pi * hz(m) * 2 * (1 + d) * t)
    a = np.minimum(1, t / 0.8) * np.clip((length - t) / 0.8, 0, 1)
    return filt(s / (len(notes) * 2), "low", 1800) * a * 0.09


def rim(rng):
    n = int(0.12 * SR)
    return (np.sin(2 * np.pi * 820 * tax(n)) * env(n, 0.012) + filt(rng.standard_normal(n), "band", [1500, 4000]) * env(n, 0.006) * 0.3) * 0.22


def main():
    rng = np.random.default_rng(80)
    N = int(DUR * SR)
    keys, pads, drums, bass, fx = (np.zeros(N) for _ in range(5))
    duck = np.ones(N)

    for bar, (root, notes) in enumerate(PROG):
        t0 = bar * BAR
        length = BAR if bar < 4 else DUR - t0
        place(keys, cm.chord(notes, min(length, BAR) * 0.98, rng, strum=0.03), t0, 0.85)
        place(keys, cm.chord([notes[2] + 12], B * 1.2, rng), t0 + B * 2.5, 0.35)
        place(pads, pad(notes, length + 0.4, rng), t0)
        place(bass, cm.sub(hz(root), min(length, BAR) * 0.9), t0, 0.8)

    # drums only between the "after" cut and the end card
    for beat in range(CUES["after"], CUES["end"]):
        tb = beat * B
        if beat % 2 == 1:      # soft kick on the cut beats (3, 5, 7, ...)
            place(drums, cm.kick(rng), tb, 0.75)
            k = int(tb * SR); m = min(N, k + int(0.35 * SR))
            duck[k:m] = np.minimum(duck[k:m], 0.7 + 0.3 * np.linspace(0, 1, m - k))
        else:
            place(drums, rim(rng), tb + 0.01)
        place(drums, cm.shaker(rng), tb + B / 2, 0.5)

    def swell_into(beat, g=1.0):
        sw = cm.swell(rng, 1.4)
        place(fx, sw, beat * B - len(sw) / SR, g)

    swell_into(CUES["after"])
    for b in CUES["taps"]:
        place(fx, cm.soft_tap(rng), b * B, 0.9)
    place(fx, cm.whoosh(rng, 0.7), CUES["targeting"] * B - 0.35, 0.8)
    for b in CUES["pings"]:
        place(fx, cm.soft_ping(), b * B, 0.85)
    swell_into(CUES["offer"], 1.2)
    place(fx, cm.kick(rng), CUES["offer"] * B, 0.6)
    for b in CUES["lines"]:
        place(fx, cm.tick(rng), b * B, 0.8)
    swell_into(CUES["end"], 1.2)

    keys = cm.reverb(filt(keys, "low", 3400), 2.2, 0.45, rng) * duck
    pads = cm.reverb(pads, 2.5, 0.3, rng)
    drums = cm.reverb(filt(drums, "low", 7000), 1.0, 0.18, rng)
    fx = cm.reverb(fx, 1.6, 0.35, rng)
    mix = keys + pads + drums * 0.7 + bass * duck * 0.8 + fx + cm.crackle(N, rng) * 0.7
    t = tax(N)
    mix *= np.minimum(1, t / 0.05) * np.clip((DUR - t) / 1.4, 0, 1)
    mix = np.tanh(mix * 1.4)
    mix /= np.max(np.abs(mix)) / 0.89
    right = np.roll(filt(mix, "low", 10000), 18)
    pcm = (np.stack([mix, right], axis=1) * 32767).astype(np.int16)
    with wave.open("/tmp/music-main.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/music-main.wav", "-af", "loudnorm=I=-16:TP=-1.0:LRA=9",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "256k", "assets/music-main.mp3"], check=True)
    print("wrote assets/music-main.mp3")


if __name__ == "__main__":
    main()
