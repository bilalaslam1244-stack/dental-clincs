"""Calm 92 BPM beds for the 7.5 s motion ads (lock, week, offer, calls, site, steps, claim).

Same instruments as tools/compose-music.py, softer drums, and sound effects on
the cues set in tools/build-motion.py (notification pings, calendar ticks, the
offer band). Writes assets/music-motion-<name>.mp3.
"""
import importlib.util
import subprocess
import wave
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location("cm", Path(__file__).with_name("compose-music.py"))
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
SR, B, tax, filt, hz, place = cm.SR, cm.B, cm.tax, cm.filt, cm.hz, cm.place
BAR, DUR = B * 4, 7.5
PROG = [(45, [57, 60, 64, 67]), (41, [53, 57, 60, 64]), (48, [55, 60, 64, 67]), (43, [55, 59, 62, 67])]

# cue times in beats (B = 0.652 s), matching tools/build-motion.py
CUES = {
    "lock":  dict(seed=11, whoosh=[1.5, 6], pings=[3, 4, 5], ticks=[], swell=6),
    "week":  dict(seed=12, whoosh=[2, 3, 6.5], pings=[6], ticks=[3.5, 4, 4.5, 5, 5.5], swell=6.5),
    "offer": dict(seed=13, whoosh=[6], pings=[2], ticks=[3, 4, 5], swell=6, hit=0),
    "calls": dict(seed=14, whoosh=[1.5, 6], pings=[], ticks=[2, 3, 4, 5], swell=6),
    "site":  dict(seed=15, whoosh=[1.5, 6], pings=[], ticks=[], hits=[3, 4, 5], swell=6),
    "steps": dict(seed=16, whoosh=[2, 3.25, 4.5, 6], pings=[], ticks=[], swell=6),
    "claim": dict(seed=17, whoosh=[5.5], pings=[1.5], ticks=[2.5, 3, 3.5, 4], swell=5.5, hit=0),
}


def build(name):
    c = CUES[name]
    rng = np.random.default_rng(c["seed"])
    N = int(DUR * SR)
    keys, drums, bass, fx = (np.zeros(N) for _ in range(4))
    duck = np.ones(N)
    for bar in range(int(np.ceil(DUR / BAR))):
        t0 = bar * BAR
        root, notes = PROG[bar % 4]
        place(keys, cm.chord(notes, BAR * 0.98, rng, strum=0.03), t0, 0.9)
        place(keys, cm.chord([notes[2] + 12], B * 1.2, rng), t0 + B * 2.5, 0.35)
        place(bass, cm.sub(hz(root), BAR * 0.9), t0, 0.8)
        for b in range(4):
            tb = t0 + b * B
            if b in (0, 2):
                place(drums, cm.kick(rng), tb, 0.7)
                k = int(tb * SR); m = min(N, k + int(0.3 * SR))
                if k < N:
                    duck[k:m] = np.minimum(duck[k:m], 0.72 + 0.28 * np.linspace(0, 1, m - k))
            place(drums, cm.shaker(rng), tb + B / 2, 0.5)
    for b in c["whoosh"]:
        place(fx, cm.whoosh(rng, 0.6), b * B - 0.3, 0.6)
    for b in c["pings"]:
        place(fx, cm.soft_ping(), b * B, 0.9)
    for b in c["ticks"]:
        place(fx, cm.tick(rng), b * B, 0.8)
    sw = cm.swell(rng)
    place(fx, sw, c["swell"] * B - len(sw) / SR, 0.9)
    for b in c.get("hits", []):
        place(fx, cm.kick(rng), b * B, 0.55)
    if "hit" in c:
        place(fx, cm.kick(rng), c["hit"] * B, 0.8)

    keys = cm.reverb(filt(keys, "low", 3600), 2.0, 0.4, rng) * duck
    drums = cm.reverb(filt(drums, "low", 7000), 0.9, 0.15, rng)
    fx = cm.reverb(fx, 1.4, 0.3, rng)
    mix = keys + drums * 0.6 + bass * duck * 0.8 + fx + cm.crackle(N, rng) * 0.7
    t = tax(N)
    mix *= np.minimum(1, t / 0.03) * np.clip((DUR - t) / 0.8, 0, 1)
    mix = np.tanh(mix * 1.4)
    mix /= np.max(np.abs(mix)) / 0.89
    right = np.roll(filt(mix, "low", 10000), 16)
    pcm = (np.stack([mix, right], axis=1) * 32767).astype(np.int16)
    wav = f"/tmp/music-motion-{name}.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "loudnorm=I=-15:TP=-1.0:LRA=9",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "256k", f"assets/music-motion-{name}.mp3"], check=True)
    print("wrote", f"assets/music-motion-{name}.mp3")


if __name__ == "__main__":
    for name in CUES:
        build(name)
