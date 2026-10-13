// Prints a Smile Arts KD document to PDF, A4 landscape: smilearts/preview-deck.html (default), or with
// DECK=lookbook smilearts/lookbook.html (ad preview for Dr. Daren), or DECK=plan smilearts/plan.html (launch plan).
// IMGS points at a folder of JPEG copies of renders/smilearts (keeps the PDF small); without it the PNGs are used.
// Usage (from video/): PLAYWRIGHT=<path to playwright/index.mjs> [CHROME=<chrome.exe>] [DECK=lookbook] [IMGS=<dir>] node tools/render-smilearts-deck.mjs <out.pdf>
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright');
const deck = ['lookbook', 'plan', 'kp-plan'].includes(process.env.DECK) ? process.env.DECK : 'preview-deck';
const out = process.argv[2] || `renders/smilearts/smilearts-kd-${deck}.pdf`;
const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const tab = await browser.newPage();
let url = pathToFileURL(resolve('smilearts', `${deck}.html`)).href;
if (process.env.IMGS) url += `?${deck === 'preview-deck' ? 'thumbs' : 'imgs'}=` + encodeURIComponent(pathToFileURL(resolve(process.env.IMGS)).href);
await tab.goto(url);
await tab.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
await tab.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
if (process.env.SHOTS) {
  await tab.setViewportSize({ width: 1123, height: 794 });
  const pages = await tab.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${process.env.SHOTS}/page-${i + 1}.png` });
}
console.log('wrote', out);
await browser.close();
