// Screenshots every static ad concept in statics/statics.html as PNG, in 9:16 and 4:5.
// Usage (from video/): node tools/render-statics.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const CONCEPTS = ['hook', 'week', 'lock', 'offer'];
const FORMATS = { '916': [1080, 1920, '9x16'], '45': [1080, 1350, '4x5'] };
const page = resolve('statics/statics.html');
mkdirSync('renders/statics', { recursive: true });

const browser = await chromium.launch();
const tab = await browser.newPage();
for (const [f, [w, h, label]] of Object.entries(FORMATS)) {
  await tab.setViewportSize({ width: w, height: h });
  for (const c of CONCEPTS) {
    await tab.goto(`file://${page}?c=${c}&f=${f}`);
    await tab.evaluate(() => document.fonts.ready);
    await tab.waitForTimeout(150);
    const out = `renders/statics/4skales-static-${c}-${label}.png`;
    await tab.screenshot({ path: out });
    console.log(out);
  }
}
await browser.close();
