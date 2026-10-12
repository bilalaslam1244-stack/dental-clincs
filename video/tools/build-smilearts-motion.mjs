// 7.5 s motion versions (92 BPM) of the Smile Arts Kota Damansara ads in smilearts/kd-ads.html.
// Loads each concept/format/language in Chromium, takes the finished layout, and writes a
// HyperFrames composition sa-kd-<concept>-<916|45>-<lang>.html that animates into exactly that
// layout, so the static PNG doubles as the poster frame. Music: tools/compose-music-motion.py smilearts.
// Usage (from video/): PLAYWRIGHT=<path to playwright/index.mjs> [CHROME=<chrome.exe>] node tools/build-smilearts-motion.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright');
const CONCEPTS = ['braces', 'implants', 'veneers'];
const FORMATS = { '916': 1920, '45': 1350 };
const LANGS = ['en', 'zh'];
const TITLES = { braces: 'Braces or Invisalign', implants: 'Dental implants', veneers: 'Porcelain veneers' };

const src = readFileSync('smilearts/kd-ads.html', 'utf8');
const css = src.match(/<style>([\s\S]*?)<\/style>/)[1].replace(/\.\.\/assets\//g, 'assets/');
const fix = html => html.replace(/src="source\//g, 'src="smilearts/source/');

// beats at 92 BPM; cues match the "smilearts" entry in tools/compose-music-motion.py
const JS = `
      tl.fromTo('.photo img', { scale: 1.14 }, { scale: 1, duration: DUR, ease: 'power1.out' }, 0);
      tl.fromTo('.photo', { opacity: 0 }, { opacity: 1, duration: 0.6, ease: 'power1.out' }, 0);
      tl.fromTo('.creds span', { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.5, ease: 'expo.out', stagger: 0.18 }, 0.5 * B);
      tl.fromTo('.avatar', { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.8)' }, 0.75 * B);
      tl.fromTo('.head', { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 0.5 * B);
      tl.fromTo('.eyebrow', { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' }, 0.75 * B);
      tl.fromTo('h1', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.8, ease: 'expo.out' }, 1 * B);
      tl.fromTo('h1 em', { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'power1.out' }, 1.5 * B);
      tl.fromTo('.sub', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 2.25 * B);
      tl.fromTo('.cta', { opacity: 0, y: 60, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: 'back.out(1.6)' }, 3.5 * B - 0.1);
      tl.fromTo('.note', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 4.25 * B);
      tl.fromTo('.foot', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 4.5 * B);
      tl.fromTo('.cta', { scale: 1 }, { scale: 1.045, duration: B / 2, repeat: 7, yoyo: true, ease: 'sine.inOut' }, 5 * B);
`;

const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const tab = await browser.newPage();
const page = pathToFileURL(resolve('smilearts', 'kd-ads.html')).href;
for (const l of LANGS) {
  for (const [f, h] of Object.entries(FORMATS)) {
    await tab.setViewportSize({ width: 1080, height: h });
    for (const c of CONCEPTS) {
      await tab.goto(`${page}?c=${c}&f=${f}&l=${l}`);
      const ad = await tab.evaluate(() => {
        const a = document.querySelector('.ad');
        a.querySelectorAll('[hidden]').forEach(e => e.remove());
        return a.innerHTML;
      });
      const html = `<!doctype html>
<html lang="${l}" class="f${f}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=${h}" />
    <title>Smile Arts Kota Damansara · ${TITLES[c]}</title>
    <script src="assets/gsap.min.js"></script>
    <style>${css}
  html, body { width: 1080px; height: ${h}px; overflow: hidden; }
  #root { position: relative; width: 1080px; height: ${h}px; overflow: hidden; }
  .clip { position: absolute; inset: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="7.5" data-width="1080" data-height="${h}">
      <div class="ad clip" data-start="0" data-duration="7.5" data-track-index="0">${fix(ad)}</div>
      <audio id="music" src="assets/music-motion-smilearts.mp3" data-start="0" data-duration="7.5" data-volume="1" data-track-index="8"></audio>
    </div>
    <script>
      const B = 60 / 92, DUR = 7.5;
      const tl = gsap.timeline({ paused: true });
${JS}
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
      const out = `sa-kd-${c}-${f}-${l}.html`;
      writeFileSync(out, html);
      console.log('wrote', out);
    }
  }
}
await browser.close();
