// 7.5 s motion versions (92 BPM) of the Smile Arts Kota Damansara ads in smilearts/kd-ads.html.
// Loads each concept/format/language in Chromium, takes the finished layout, and writes a
// HyperFrames composition sa-kd-<concept>-<916|45>-<lang>.html that animates into exactly that
// layout, so the static PNG doubles as the poster frame. Music: tools/compose-music-motion.py smilearts.
// Usage (from video/): PLAYWRIGHT=<path to playwright/index.mjs> [CHROME=<chrome.exe>] node tools/build-smilearts-motion.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright');
const CONCEPTS = ['braces', 'implants', 'veneers', 'clinic', 'implant5000', 'aligner', 'scaling'];
const FORMATS = { '916': 1920, '45': 1350 };
const LANGS = ['en', 'zh'];
const TITLES = { braces: 'Braces or Invisalign', implants: 'Dental implants', veneers: 'Porcelain veneers',
                 clinic: 'Your dentist at The Strand', implant5000: 'Dental implant RM 5,000', aligner: 'Clear aligners from RM 6,000', scaling: 'Scaling and whitening RM 399' };

const src = readFileSync('smilearts/kd-ads.html', 'utf8');
const css = src.match(/<style>([\s\S]*?)<\/style>/)[1].replace(/\.\.\/assets\//g, 'assets/');
const fix = html => html.replace(/src="source\//g, 'src="smilearts/source/');

// beats at 92 BPM; cues match the "smilearts" entry in tools/compose-music-motion.py
const JS = `
      tl.fromTo('.portrait', { opacity: 0, x: 80, scale: 1.04 }, { opacity: 1, x: 0, scale: 1, duration: 1.1, ease: 'expo.out' }, 0);
      tl.fromTo('.arc', { opacity: 0, scale: 0.85, rotation: -20 }, { opacity: 0.7, scale: 1, rotation: 0, duration: 1.4, ease: 'expo.out' }, 0.1);
      tl.fromTo('.band', { y: 120 }, { y: 0, duration: 0.7, ease: 'expo.out' }, 0);
      tl.fromTo('.hero img', { scale: 1.12 }, { scale: 1, duration: DUR, ease: 'power1.out' }, 0);
      tl.fromTo('.bgphoto img', { scale: 1.12 }, { scale: 1.03, duration: DUR, ease: 'power1.out' }, 0);
      tl.fromTo('.visual', { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 1.0, ease: 'expo.out' }, 0.2);
      tl.fromTo('.visual img', { scale: 1.1 }, { scale: 1, duration: DUR, ease: 'power1.out' }, 0);
      tl.fromTo('.strip figure', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out', stagger: 0.2 }, 4 * B);
      tl.fromTo('.top', { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 0.5 * B);
      tl.fromTo('.eyebrow', { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' }, 0.75 * B);
      tl.fromTo('h1', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.8, ease: 'expo.out' }, 1 * B);
      tl.fromTo('h1 em', { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'power1.out' }, 1.5 * B);
      tl.fromTo('.sub, .price-label', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 2.25 * B);
      tl.fromTo('.price', { opacity: 0, scale: 1.25, transformOrigin: '0% 70%' }, { opacity: 1, scale: 1, duration: 0.8, ease: 'expo.out' }, 2.25 * B);
      tl.fromTo('.price-to', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 2.75 * B);
      tl.fromTo('.list p', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.45, ease: 'expo.out', stagger: B / 3 }, 3 * B);
      tl.fromTo('.fine', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 4.5 * B);
      tl.fromTo('.tag', { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.6, ease: 'expo.out' }, 4.25 * B);
      tl.fromTo('.band .row', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 3.5 * B);
      tl.fromTo('.wa i', { scale: 1 }, { scale: 1.12, duration: B / 2, repeat: 7, yoyo: true, ease: 'sine.inOut' }, 5 * B);
`;

const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const tab = await browser.newPage();
const page = pathToFileURL(resolve('smilearts', 'kd-ads.html')).href;
for (const l of LANGS) {
  for (const [f, h] of Object.entries(FORMATS)) {
    await tab.setViewportSize({ width: 1080, height: h });
    for (const c of CONCEPTS) {
      await tab.goto(`${page}?c=${c}&f=${f}&l=${l}`);
      await tab.evaluate(() => document.fonts.ready);
      const [ad, cls] = await tab.evaluate(() => {
        const a = document.querySelector('.ad');
        a.querySelectorAll('[hidden]').forEach(e => e.remove());
        return [a.innerHTML, document.documentElement.className];
      });
      const html = `<!doctype html>
<html lang="${l}" class="${cls}">
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
