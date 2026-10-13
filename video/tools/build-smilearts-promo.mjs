// 12 s "promo" motion cuts of the Smile Arts price ads (offer layout: scaling, implant5000, aligner), livelier than
// the 7.5 s versions: the question slams in word by word at the centre, then carries up into the headline while the
// picture rises in; the price box draws itself and the price counts up; the checklist ticks in; the Book button grows
// out of the price and gets tapped; then the frame holds still on exactly the static design (the PNG is the poster).
// Writes sa-<branch>-<concept>-promo-<916|45>-<lang>.html. Music: DUR=12 python tools/compose-music-motion.py promo.
// Usage (from video/): PLAYWRIGHT=<path to playwright/index.mjs> [CHROME=<chrome.exe>] [BRANCH=kd|kp] [LANGS=en,zh]
//                      node tools/build-smilearts-promo.mjs [concept...] [--formats=916,45]
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright');
const args = process.argv.slice(2);
const fmtArg = args.find(a => a.startsWith('--formats='));
const named = args.filter(a => !a.startsWith('--'));
const CONCEPTS = named.length ? named : ['scaling', 'implant5000', 'aligner'];
const FORMATS = Object.fromEntries(Object.entries({ '916': 1920, '45': 1350 }).filter(([f]) => !fmtArg || fmtArg.slice(10).split(',').includes(f)));
const BR = process.env.BRANCH || 'kd';
const LANGS = process.env.LANGS ? process.env.LANGS.split(',') : ['en', 'zh'];
const DUR = 12;

const src = readFileSync('smilearts/kd-ads.html', 'utf8');
const css = src.match(/<style>([\s\S]*?)<\/style>/)[1].replace(/\.\.\/assets\//g, 'assets/');
const fix = html => html.replace(/src="source\//g, 'src="smilearts/source/');
const JS = readFileSync('tools/smilearts-promo-timeline.js', 'utf8').replace('__DUR__', String(DUR));

const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const tab = await browser.newPage();
const page = pathToFileURL(resolve('smilearts', 'kd-ads.html')).href;
for (const l of LANGS) {
  for (const [f, h] of Object.entries(FORMATS)) {
    await tab.setViewportSize({ width: 1080, height: h });
    for (const c of CONCEPTS) {
      await tab.goto(`${page}?c=${c}&f=${f}&l=${l}&b=${BR}`);
      await tab.evaluate(async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 200)); });
      const [ad, cls] = await tab.evaluate(() => {
        const a = document.querySelector('.ad');
        a.querySelectorAll('[hidden]').forEach(e => e.remove());
        // split the question (headline text before <em>) into words so they can slam in one by one
        const h1 = a.querySelector('h1');
        [...h1.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).forEach(n => {
          const frag = document.createDocumentFragment();
          const zh = /[㐀-鿿]/.test(n.textContent);
          const parts = zh ? n.textContent.split(/(?<=[，？！、])/) : n.textContent.split(/(\s+)/);
          parts.forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.append(p); return; }
            const s = document.createElement('span'); s.className = 'w'; s.textContent = p; frag.append(s);
          });
          n.replaceWith(frag);
        });
        // wrap the number in the price so it can count up
        const price = a.querySelector('.price');
        if (price) [...price.childNodes].filter(n => n.nodeType === 3 && /\d/.test(n.textContent)).forEach(n => {
          const s = document.createElement('span'); s.className = 'num'; s.textContent = n.textContent.trim(); n.replaceWith(s);
        });
        return [a.innerHTML, document.documentElement.className];
      });
      const html = `<!doctype html>
<html lang="${l}" class="${cls}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=${h}" />
    <title>Smile Arts ${BR === 'kp' ? 'Kepong' : 'Kota Damansara'} - ${c} promo</title>
    <script src="assets/gsap.min.js"></script>
    <style>${css}
  html, body { width: 1080px; height: ${h}px; overflow: hidden; }
  #root { position: relative; width: 1080px; height: ${h}px; overflow: hidden; }
  .clip { position: absolute; inset: 0; }
  h1 .w { display: inline-block; }
  .tap { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; background: radial-gradient(circle, rgba(255,250,240,.9) 0%, rgba(255,250,240,0) 70%); opacity: 0; pointer-events: none; z-index: 20; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${DUR}" data-width="1080" data-height="${h}">
      <div class="ad clip" data-start="0" data-duration="${DUR}" data-track-index="0">${fix(ad)}<div class="tap"></div></div>
      <audio id="music" src="assets/music-motion-promo.mp3" data-start="0" data-duration="${DUR}" data-volume="1" data-track-index="8"></audio>
    </div>
    <script>
${JS}
    </script>
  </body>
</html>
`;
      const out = `sa-${BR}-${c}-promo-${f}-${l}.html`;
      writeFileSync(out, html);
      console.log('wrote', out);
    }
  }
}
await browser.close();
