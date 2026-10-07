// Records the real demo clinic site being used, frame by frame, into assets/screen.mp4.
// Usage: node tools/record-site.mjs <url> <outDir>
import { createRequire } from 'module';
import { execFileSync } from 'child_process';
import fs from 'fs';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');

const [url, out] = process.argv.slice(2);
const B = 60 / 92;            // taps land on the soundtrack's beats (92 BPM)
const FPS = 30, DUR = B * 10.2;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, a, b) => clamp((t - a) / (b - a));
const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const lerp = (a, b, x) => a + (b - a) * x;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 390, height: 760 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle' });
await page.addStyleTag({ content: `html{scroll-behavior:auto!important}*{transition:none!important;animation:none!important}
  #finger{position:fixed;z-index:999;width:38px;height:38px;margin:-19px 0 0 -19px;border-radius:50%;background:rgba(255,255,255,.55);border:2px solid rgba(26,23,20,.55);box-shadow:0 6px 16px rgba(0,0,0,.25);pointer-events:none}` });
await page.evaluate(async () => { await document.fonts.ready; const f = document.createElement('div'); f.id = 'finger'; f.style.opacity = 0; document.body.appendChild(f); });

const pos = await page.evaluate(() => {
  const abs = sel => { const r = document.querySelector(sel).getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 + scrollY, top: r.top + scrollY, bottom: r.bottom + scrollY }; };
  return {
    card: abs('#book'), tr: abs('fieldset.row'), send: abs('#sendBtn'), name: abs('#nameInput'),
    t1: abs('[data-group="treatment"] .chip[data-value="Check-up & scaling"]'),
    t2: abs('[data-group="day"] .chip[data-value="Saturday"]'),
    t3: abs('[data-group="time"] .chip[data-value="morning"]'),
  };
});
const S1 = Math.round(pos.tr.top - 70 - 22);          // card top under the sticky header
const S2 = Math.round(pos.send.bottom - (760 - 92));    // send button clear of the dock
// [time, target, scroll at that moment]
const TAPS = [[B * 3.5, pos.t1, S1], [B * 4.5, pos.t2, S1], [B * 5.5, pos.t3, S1], [B * 6.5, pos.name, S1], [B * 9.5, pos.send, S2]];

fs.mkdirSync(out, { recursive: true });
const n = Math.round(DUR * FPS);
for (let i = 0; i < n; i++) {
  const t = i / FPS;
  let scroll = lerp(0, S1, ease(prog(t, 0.9, 1.6)));
  scroll = lerp(scroll, S2, ease(prog(t, B * 7.7, B * 8.6)));
  const st = {
    treatment: t >= TAPS[0][0] ? 'Check-up & scaling' : 'Filling',
    day: t >= TAPS[1][0] ? 'Saturday' : 'today',
    time: t >= TAPS[2][0] ? 'morning' : 'evening',
    name: 'Mei Ling'.slice(0, Math.floor(clamp((t - (B * 6.5 + 0.1)) / 0.065, 0, 8))),
  };
  // finger: glide between targets, press on each tap
  let fx = 300, fy = 640, press = 0, fo = Math.min(prog(t, 1.2, 1.4), 1 - prog(t, DUR - 0.3, DUR - 0.12));
  let prev = { x: 320, y: 600 };
  for (const [tt, tg, sc] of TAPS) {
    const target = { x: tg.x + (tg === pos.name ? -100 : 0), y: tg.y - sc };
    const mv = ease(prog(t, tt - 0.4, tt - 0.06));
    if (t >= tt - 0.4) { fx = lerp(prev.x, target.x, mv); fy = lerp(prev.y, target.y, mv); }
    prev = target;
    const d = t - tt; if (d > -0.08 && d < 0.2) press = Math.sin(clamp((d + 0.08) / 0.28) * Math.PI);
  }
  await page.evaluate(([st, scroll, fx, fy, fo, press]) => {
    window.lumen.setBooking(st); window.scrollTo(0, scroll);
    const f = document.getElementById('finger');
    f.style.left = fx + 'px'; f.style.top = fy + 'px'; f.style.opacity = fo;
    f.style.transform = `scale(${1 - press * 0.28})`; f.style.background = `rgba(255,255,255,${0.6 + press * 0.35})`;
  }, [st, Math.round(scroll), fx, fy, fo, press]);
  await page.screenshot({ path: `${out}/${String(i).padStart(4, '0')}.png` });
}
await browser.close();
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', `${out}/%04d.png`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '15', '-preset', 'slow', 'assets/screen.mp4']);
console.log('wrote assets/screen.mp4', n, 'frames; S1', S1, 'S2', S2);
