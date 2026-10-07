# Fourskales: dental clinic campaign

Fixed-price clinic websites with WhatsApp booking, for Johor Bahru and Kuala Lumpur.

- `docs/copy-deck.md`: ad scripts (EN/Manglish, Mandarin), agency site outline, deployment notes.
- `demo-clinic/index.html`: demo clinic site (Lumen Dental, a fictional clinic) showing the package: three-tap WhatsApp reservation, fee ranges, live opening hours, parking, panels. Static, no build step.
- `video/`: 23.5s vertical (1080x1920) ad built with HyperFrames. `renders/fourskales-demo.mp4` is the finished video, `renders/poster.jpg` the thumbnail, `share-copy.txt` the post caption.

## Rebuilding the video

```bash
python3 -m http.server 8765            # from the repo root, serves the demo site
cd video
node tools/record-site.mjs "http://localhost:8765/demo-clinic/index.html?now=2026-10-10T10:15" /tmp/screen-frames
npx hyperframes check
npx hyperframes render --quality high --output renders/fourskales-demo.mp4
```

`tools/record-site.mjs` records the real demo site being used (scroll, taps, typing) into `assets/screen.mp4`, which the composition plays inside the phone.

Music: "Happy Beats / Business Moves" by ende.app (bundled with the /brag skill); confirm the licence before running paid ads. Sound effects: Kenney (CC0).
