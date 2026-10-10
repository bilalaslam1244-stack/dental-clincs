// Screenshots every static ad concept as PNG, in 9:16 and 4:5, for English (statics/statics.html)
// and the -ms / -zh versions from tools/build-statics-i18n.py when present.
// Usage (from video/): node tools/render-statics.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { existsSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const CONCEPTS = ['hook', 'week', 'lock', 'offer'];
const FORMATS = { '916': [1080, 1920, '9x16'], '45': [1080, 1350, '4x5'] };
const LANGS = { en: 'statics.html', ms: 'statics-ms.html', zh: 'statics-zh.html' };
mkdirSync('renders/statics', { recursive: true });

const browser = await chromium.launch();
const tab = await browser.newPage();
for (const [lang, file] of Object.entries(LANGS)) {
  const page = resolve('statics', file);
  if (!existsSync(page)) continue;
  const suffix = lang === 'en' ? '' : `-${lang}`;
  for (const [f, [w, h, label]] of Object.entries(FORMATS)) {
    await tab.setViewportSize({ width: w, height: h });
    for (const c of CONCEPTS) {
      await tab.goto(`file://${page}?c=${c}&f=${f}`);
      await tab.evaluate(() => document.fonts.ready);
      await tab.waitForTimeout(150);
      const out = `renders/statics/4skales-static-${c}${suffix}-${label}.png`;
      await tab.screenshot({ path: out });
      console.log(out);
    }
  }
}
await browser.close();
