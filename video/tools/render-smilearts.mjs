// Screenshots the Smile Arts Kota Damansara ads (smilearts/kd-ads.html) as PNG:
// 3 treatment + 3 price ads x EN/ZH/MS x 9:16 + 4:5, into renders/smilearts/.
// BRANCH=kd (default) or kp (Kepong) picks the branch label, WhatsApp number and file prefix.
// Usage (from video/): PLAYWRIGHT=<path to playwright/index.mjs> [CHROME=<chrome.exe>] node tools/render-smilearts.mjs [concept...]
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright');
const CONCEPTS = process.argv.slice(2).length ? process.argv.slice(2) : ['braces', 'implants', 'veneers', 'implant5000', 'aligner', 'scaling'];
const FORMATS = { '916': [1080, 1920, '9x16'], '45': [1080, 1350, '4x5'] };
const BR = process.env.BRANCH || 'kd';
const U = process.env.URGENT || '';  // e.g. 31oct: adds the dated urgency ribbon, files get a -urgent suffix
const LANGS = process.env.LANGS ? process.env.LANGS.split(',') : ['en', 'zh', 'ms'];
mkdirSync('renders/smilearts', { recursive: true });

const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const tab = await browser.newPage();
const page = pathToFileURL(resolve('smilearts', 'kd-ads.html')).href;
for (const l of LANGS) {
  for (const [f, [w, h, label]] of Object.entries(FORMATS)) {
    await tab.setViewportSize({ width: w, height: h });
    for (const c of CONCEPTS) {
      await tab.goto(`${page}?c=${c}&f=${f}&l=${l}&b=${BR}${U ? '&u=' + U : ''}`);
      await tab.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
      await tab.waitForTimeout(150);
      const out = `renders/smilearts/smilearts-${BR}-${c}${U ? '-urgent' : ''}-${l}-${label}.png`;
      await tab.screenshot({ path: out });
      console.log(out);
    }
  }
}
await browser.close();
