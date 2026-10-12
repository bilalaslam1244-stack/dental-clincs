// Prints smilearts/preview-deck.html (the ad preview for Dr. Daren) to PDF, A4 landscape.
// THUMBS points at a folder of JPEG copies of renders/smilearts (keeps the PDF small); without it the PNGs are used.
// Usage (from video/): PLAYWRIGHT=<path to playwright/index.mjs> [CHROME=<chrome.exe>] [THUMBS=<dir>] node tools/render-smilearts-deck.mjs <out.pdf>
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright');
const out = process.argv[2] || 'renders/smilearts/smilearts-kd-ad-preview.pdf';
const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const tab = await browser.newPage();
let url = pathToFileURL(resolve('smilearts', 'preview-deck.html')).href;
if (process.env.THUMBS) url += '?thumbs=' + encodeURIComponent(pathToFileURL(resolve(process.env.THUMBS)).href);
await tab.goto(url);
await tab.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
await tab.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
console.log('wrote', out);
await browser.close();
