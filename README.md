# Fourskales: dental clinic campaign

Fixed-price clinic websites with WhatsApp booking, for Johor Bahru and Kuala Lumpur.

- `docs/copy-deck.md`: ad scripts (EN/Manglish, Mandarin), agency site outline, deployment notes.
- `demo-clinic/index.html`: demo clinic site (Lumen Dental, a fictional clinic) showing the package: three-tap WhatsApp reservation, fee ranges, live opening hours, parking, panels. Static, no build step.
- `brand/`: 4Skales logo, traced to SVG (`4skales-logo.svg` uses currentColor) plus ink/ivory SVG and transparent PNG versions.
- `video/`: three 7.5s Meta ads, each in 9:16 (Reels/Stories) and 4:5 (Feed), built with HyperFrames. Finished files are in `video/renders/`; ad copy is in `video/share-copy.txt`.
  - ad1 Missed calls, ad2 Three-tap booking, ad3 The offer.

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
