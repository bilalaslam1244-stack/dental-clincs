# Fourskales: dental clinic campaign

Fixed-price clinic websites with WhatsApp booking, for Johor Bahru and Kuala Lumpur.

- `docs/copy-deck.md`: ad scripts (EN/Manglish, Mandarin), agency site outline, deployment notes.
- `demo-clinic/index.html`: demo clinic site (Lumen Dental, a fictional clinic) showing the package: three-tap WhatsApp reservation, fee ranges, live opening hours, parking, panels. Static, no build step.
- `brand/`: 4Skales logo, traced to SVG (`4skales-logo.svg` uses currentColor) plus ink/ivory SVG and transparent PNG versions.
- `video/`: Meta ads built with HyperFrames, each in 9:16 (Reels/Stories) and 4:5 (Feed). Finished files are in `video/renders/`; ad copy is in `video/share-copy.txt`.
  - Main ad (19.9s, 80 BPM, light theme): problem (empty appointment book, outdated site) / "here's how we fix it" / step 1 Instagram-style sponsored post for the clinic / step 2 book on the new site in three taps / step 3 booking lands in WhatsApp / 2 weeks of leads free / CTA. Built by `tools/build-main.py`, music by `tools/compose-music-main.py`, site demo `assets/screen-80.mp4` (`BPM=80 OUT=assets/screen-80.mp4 node tools/record-site.mjs ...`).
  - Bahasa Malaysia and Chinese versions of the main ad: `tools/build-main-i18n.py` (run after `build-main.py`) writes `main-916-ms.html`, `main-45-ms.html`, `main-916-zh.html`, `main-45-zh.html`; Chinese uses Noto Serif SC / Noto Sans SC subsets downloaded for exactly the characters used. The recorded demo site in step 2 stays in English.
  - Short cuts (7.5s, 92 BPM) for retargeting: ad1 Missed calls, ad2 Three-tap booking, ad3 The offer. Built by `tools/build-ads.py`.
  - Static ads (light theme, "For dental clinic owners" qualifier on each): hook (near-empty week), week (before/after calendar), lock (WhatsApp enquiries on a lock screen), offer (2 weeks free). Source `statics/statics.html`; `node tools/render-statics.mjs` writes PNGs to `renders/statics/` in 9:16 and 4:5. Each carries an offer band and a "Claim 2 free weeks on WhatsApp" button.
  - Motion ads (7.5s, 92 BPM): lock, week and offer, animated from the statics so the last frame matches the static exactly. `python3 tools/compose-music-motion.py` (music), `python3 tools/build-motion.py` (writes `motion-<name>-<916|45>.html`), render each with `npx hyperframes render`, then the static PNG is overlaid on frame 0 as the poster. Finished files in `renders/motion/`.
  - Bahasa Malaysia and Chinese statics and motion ads: `python3 tools/build-statics-i18n.py` writes `statics/statics-ms.html` and `statics/statics-zh.html` (Chinese downloads Noto Serif SC / Noto Sans SC subsets as `*-statics-subset.woff2`); `render-statics.mjs` and `build-motion.py` then pick them up and output `-ms` / `-zh` files.

## Rebuilding the ads

```bash
python3 -m http.server 8765            # from the repo root, serves the demo site
cd video
node tools/record-site.mjs "http://localhost:8765/demo-clinic/index.html?now=2026-10-10T10:15" /tmp/screen-frames
python3 tools/compose-music.py         # three original 92 BPM lo-fi tracks, sound effects on each ad's cuts
python3 tools/build-ads.py             # writes ad1-916.html ... ad3-45.html
npx hyperframes render -c ad1-916.html --quality high -o renders/4skales-ad1-missed-calls-9x16.mp4
```

9:16 versions keep all text between y=290 and y=1250, clear of the Reels header and the caption/CTA overlay.
`tools/record-site.mjs` records the real demo site being used (scroll, taps, typing) into `assets/screen.mp4`, which the composition plays inside the phone.

Music: composed in code by `tools/compose-music.py` (original, no third-party samples or licences).
