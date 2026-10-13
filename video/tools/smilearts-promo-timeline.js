// Timeline for the 12 s Smile Arts promo cuts (inlined by tools/build-smilearts-promo.mjs). Beats at 92 BPM; the
// cues match the "promo" entry in tools/compose-music-motion.py. Every tween ends on the static layout.
const B = 60 / 92, DUR = __DUR__, W = 1080, H = document.querySelector('#root').offsetHeight;
const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)];
const tl = gsap.timeline({ paused: true });
const ad = q('.ad'), h1 = q('h1'), em = q('h1 em'), words = qa('h1 .w');

// the question starts big and centred: measure its words and compute the transform that puts them there
const box = words.reduce((r, w) => {
  const b = w.getBoundingClientRect();
  return { l: Math.min(r.l, b.left), t: Math.min(r.t, b.top), r: Math.max(r.r, b.right), b: Math.max(r.b, b.bottom) };
}, { l: 1e9, t: 1e9, r: -1e9, b: -1e9 });
const h1r = h1.getBoundingClientRect(), S = Math.min(2.1, (W - 110) / (box.r - box.l));
const dx = (W - (box.r - box.l) * S) / 2 - h1r.left - (box.l - h1r.left) * S;
const dy = (H * 0.42 - (box.b - box.t) * S / 2) - h1r.top - (box.t - h1r.top) * S;

// 0 - 2.6 B: the question slams in word by word, centred; a small camera kick on each slam
tl.set(h1, { transformOrigin: '0 0', x: dx, y: dy, scale: S }, 0);
tl.fromTo(em, { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1.1, ease: 'power2.inOut' }, 4.5 * B);
const slams = [0.25, 1, 1.75];
words.forEach((w, i) => {
  const at = slams[Math.min(i, slams.length - 1)] * B + Math.max(0, i - slams.length + 1) * 0.12;
  tl.fromTo(w, { opacity: 0, scale: 1.9, filter: 'blur(14px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.42, ease: 'expo.out' }, at);
});
slams.forEach(b => tl.fromTo(ad, { scale: 1.012 }, { scale: 1, duration: 0.35, ease: 'power3.out', immediateRender: false }, b * B));

// 3 B: the question carries up into the headline; brand, eyebrow and the picture arrive with it
tl.to(h1, { x: 0, y: 0, scale: 1, duration: 1.0, ease: 'expo.inOut' }, 3 * B - 0.25);
tl.fromTo('.top', { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }, 3 * B + 0.2);
tl.fromTo('.eyebrow', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.6, ease: 'power2.out' }, 3 * B + 0.35);
if (q('.ad > .bgphoto')) {
  tl.fromTo('.ad > .bgphoto', { opacity: 0, yPercent: 14 }, { opacity: 1, yPercent: 0, duration: 1.3, ease: 'expo.out' }, 3 * B);
  tl.fromTo('.ad > .bgphoto img', { scale: 1.16 }, { scale: 1, duration: DUR - 3 * B, ease: 'power1.out' }, 3 * B);
}
if (q('.ad > .visual')) {
  tl.fromTo('.ad > .visual', { opacity: 0, x: 140, rotation: 8 }, { opacity: 1, x: 0, rotation: 0, duration: 1.2, ease: 'expo.out' }, 3 * B + 0.2);
  tl.fromTo('.ad > .visual', { y: 0 }, { y: -14, duration: 1.6, ease: 'sine.inOut', yoyo: true, repeat: 3, immediateRender: false }, 5 * B);
}

// 6 B: the price box draws itself, then the price counts up and lands with a flash
const label = q('.price-label'), num = q('.price .num'), target = Number(num.textContent.replace(/,/g, ''));
tl.fromTo(label, { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 0.5, ease: 'power2.out' }, 6 * B - 0.1);
tl.fromTo('.price', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: 'power2.out' }, 6.4 * B);
const ctr = { v: 0 };
tl.fromTo(ctr, { v: 0 }, { v: target, duration: 1.45 * B, ease: 'power2.out',
  onUpdate: () => { num.textContent = Math.round(ctr.v).toLocaleString('en-US'); } }, 6.5 * B);
tl.fromTo('.price', { scale: 1.12, transformOrigin: '0% 80%' }, { scale: 1, duration: 0.5, ease: 'back.out(2.4)', immediateRender: false }, 8 * B);
tl.fromTo('.price', { filter: 'brightness(1.7)' }, { filter: 'brightness(1)', duration: 0.6, ease: 'power2.out', immediateRender: false }, 8 * B);
if (q('.price-to')) tl.fromTo('.price-to', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 8 * B + 0.1);
tl.fromTo(ad, { scale: 1.01 }, { scale: 1, duration: 0.4, ease: 'power3.out', immediateRender: false }, 8 * B);

// 9 B: checklist ticks in, then the perks
qa('.list p').forEach((p, i) => tl.fromTo(p, { opacity: 0, x: -36 }, { opacity: 1, x: 0, duration: 0.4, ease: 'expo.out' }, (9 + i * 0.5) * B));
tl.fromTo('.perks span', { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)', stagger: 0.12 }, 11 * B);

// 12 B: the Book button grows out of the price and gets tapped twice; band and fine print settle
tl.fromTo('.cta', { opacity: 0, scale: 0.4, y: -120, transformOrigin: '20% 50%' }, { opacity: 1, scale: 1, y: 0, duration: 0.7, ease: 'back.out(1.7)' }, 12 * B - 0.15);
tl.fromTo('.fine', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 12.6 * B);
tl.fromTo('.band', { yPercent: 100 }, { yPercent: 0, duration: 0.7, ease: 'expo.out' }, 12.2 * B);
tl.fromTo('.band .row', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 12.6 * B);
const cta = q('.cta').getBoundingClientRect(), tap = q('.tap');
tap.style.left = (cta.left + cta.width * 0.62) + 'px';
tap.style.top = (cta.top + cta.height / 2) + 'px';
[13.5, 14.5].forEach(b => {
  tl.fromTo(tap, { opacity: 0.55, scale: 0.2 }, { opacity: 0, scale: 2.4, duration: 0.6, ease: 'power2.out', immediateRender: false }, b * B);
  tl.fromTo('.cta', { scale: 0.94 }, { scale: 1, duration: 0.35, ease: 'back.out(3)', immediateRender: false }, b * B);
});
tl.fromTo('.cta b', { x: 0 }, { x: 10, duration: B / 2, repeat: 3, yoyo: true, ease: 'sine.inOut', immediateRender: false }, 15 * B);
tl.set({}, {}, DUR);
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
