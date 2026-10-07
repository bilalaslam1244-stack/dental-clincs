"""Builds the 14 s main ad: before -> after -> targeting -> free 30 days -> CTA.

Writes main-916.html (Reels/Stories) and main-45.html (Feed). Shares the look
and end card with tools/build-ads.py. Timing is on an 80 BPM grid (B = 0.75 s);
tools/compose-music-main.py places its hits on the same beats.

  0  - 3B   Before   old site, "CALL ONLY", slow push-in
  3B - 7B   After    redesigned site, zoom into the 3-tap booking
  7B - 11B  Reach    JB map, radius around the clinic, bookings arrive
  11B - 15B Offer    30 days of patient leads, free; keep going or walk away
  15B - end CTA      4Skales, claim your free 30 days
"""
import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ba", HERE / "build-ads.py")
ba = importlib.util.module_from_spec(spec); spec.loader.exec_module(ba)

ROOT = HERE.parent
BPM = 80
B = 60 / BPM
DUR = 14.0

FMT = {
    "916": dict(mapT=600, mapH=640, offerLabel=400, offerHead=450, freeT=770, oline1=930, oline2=1040),
    "45": dict(mapT=320, mapH=720, offerLabel=250, offerHead=300, freeT=620, oline1=780, oline2=890),
}

EXTRA_CSS = r"""
      /* before / after labels on the phone window */
      .ba { position: absolute; left: 76px; top: 18px; height: 52px; padding: 0 22px; display: flex; align-items: center; clip-path: var(--chamfer); font: 500 22px var(--sans); letter-spacing: .3em; }
      .ba.before { background: #a8443a; color: #fff; }
      .ba.after { background: var(--gold); color: var(--ink); }
      #old { position: absolute; inset: 0; background: #fff; overflow: hidden; }
      .old-page { position: absolute; left: 0; top: 0; width: 1000px; height: 1960px; font-family: 'Times New Roman', 'Liberation Serif', serif; color: #000; background: #fff; transform-origin: 0 0; }
      .old-head { background: linear-gradient(#3b6bd6, #1c3f96); color: #ff0; text-align: center; padding: 22px; font-size: 46px; font-weight: bold; text-shadow: 2px 2px #000; }
      .old-nav { display: flex; background: #ddd; border-bottom: 2px solid #999; }
      .old-nav span { flex: 1; text-align: center; padding: 8px; font: bold 18px Arial, sans-serif; color: #00c; text-decoration: underline; }
      .old-body { display: flex; gap: 20px; padding: 20px; }
      .old-side { width: 220px; background: #ffc; border: 2px dashed #f90; padding: 12px; font-size: 16px; }
      .old-main { flex: 1; font-size: 17px; line-height: 1.3; }
      .old-main h2 { color: #c00; font-size: 26px; margin: 6px 0 10px; }
      .broken { border: 2px inset #aaa; display: flex; align-items: center; justify-content: center; color: #555; font: 14px Arial, sans-serif; margin: 12px 0; }
      .stamp { position: absolute; left: 90px; top: 560px; padding: 18px 30px; border: 6px solid #c8574a; color: #c8574a; font: 500 54px/1 var(--sans); letter-spacing: .12em; text-transform: uppercase; background: rgba(255,255,255,.92); }

      /* reach: map */
      .map { position: absolute; left: 70px; right: 70px; top: [[mapT]]px; height: [[mapH]]px; clip-path: var(--chamfer); background: #161c19; overflow: hidden; }
      .map svg { position: absolute; inset: 0; width: 100%; height: 100%; }
      .map-tag { position: absolute; left: 30px; top: 26px; color: var(--gold); }
      .toasts { position: absolute; left: 30px; right: 30px; bottom: 26px; }
      .ltoast { position: relative; height: 86px; margin-top: 10px; border-radius: 24px; background: rgba(244,243,239,.96); color: var(--ink); display: flex; align-items: center; gap: 20px; padding: 0 24px; }
      .ltoast i { width: 54px; height: 54px; border-radius: 14px; background: #2f8a57; flex: none; display: flex; align-items: center; justify-content: center; }
      .ltoast b { display: block; font: 500 26px var(--sans); }
      .ltoast span { display: block; font: 300 23px var(--sans); color: #4b4a45; }

      /* offer (light) */
      .o-label { position: absolute; left: 80px; top: [[offerLabel]]px; color: var(--gold-deep); }
      .o-head { position: absolute; left: 76px; right: 76px; top: [[offerHead]]px; font: 300 128px/0.98 var(--serif); letter-spacing: -.03em; }
      .free { position: absolute; left: 80px; top: [[freeT]]px; height: 120px; padding: 0 46px; display: flex; align-items: center; background: var(--ink); color: var(--gold); clip-path: var(--chamfer); font: 300 italic 92px/1 var(--serif); }
      .o-line { position: absolute; left: 80px; right: 80px; font: 300 64px/1.1 var(--serif); }
      .o-line em { color: var(--gold-deep); }
"""


def map_svg(h, seed=7):
    """A stylised night map of JB around Mount Austin: roads, the Straits, a radius and audience dots."""
    rnd = random.Random(seed)
    w = 940
    cx, cy = 470, int(h * 0.30)
    parts = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    # the Straits of Johor along the bottom
    parts.append(f'<path d="M0 {h*0.80:.0f} C 220 {h*0.74:.0f}, 520 {h*0.86:.0f}, {w} {h*0.76:.0f} L {w} {h} L 0 {h} Z" fill="#1b2a2c"/>')
    # minor grid of streets, slightly rotated
    for i in range(-6, 22):
        x = i * 52 + rnd.uniform(-8, 8)
        parts.append(f'<line x1="{x:.0f}" y1="0" x2="{x + 120:.0f}" y2="{h}" stroke="#222a26" stroke-width="2"/>')
    for j in range(0, 16):
        y = j * 48 + rnd.uniform(-6, 6)
        parts.append(f'<line x1="0" y1="{y:.0f}" x2="{w}" y2="{y - 90:.0f}" stroke="#222a26" stroke-width="2"/>')
    # main roads
    parts.append(f'<path d="M-20 {h*0.30:.0f} C 260 {h*0.36:.0f}, 520 {h*0.22:.0f}, 980 {h*0.30:.0f}" stroke="#3a4640" stroke-width="7" fill="none"/>')
    parts.append(f'<path d="M{w*0.30:.0f} -20 C {w*0.42:.0f} {h*0.30:.0f}, {w*0.55:.0f} {h*0.55:.0f}, {w*0.62:.0f} {h+20}" stroke="#3a4640" stroke-width="7" fill="none"/>')
    parts.append(f'<path d="M-20 {h*0.62:.0f} C 300 {h*0.58:.0f}, 640 {h*0.70:.0f}, 980 {h*0.60:.0f}" stroke="#333e38" stroke-width="5" fill="none"/>')
    # place labels
    for txt, x, y in (("SKUDAI", 90, h * 0.20), ("MOUNT AUSTIN", cx + 40, cy - 80), ("JOHOR BAHRU", 560, h * 0.70), ("STRAITS OF JOHOR", 40, h * 0.93)):
        parts.append(f'<text x="{x:.0f}" y="{y:.0f}" fill="#a3ada6" font-family="Jost" font-weight="500" font-size="18" letter-spacing="5">{txt}</text>')
    # radius rings (animated by the timeline)
    for k, r in enumerate((120, 190)):
        parts.append(f'<circle id="ring{k}" cx="{cx}" cy="{cy}" r="{r}" fill="rgba(201,169,110,.06)" stroke="#c9a96e" stroke-width="2" stroke-dasharray="{"8 10" if k else "none"}"/>')
    # audience dots inside the radius
    for d in range(34):
        a = rnd.uniform(0, 2 * math.pi); rr = 190 * math.sqrt(rnd.random())
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.9
        parts.append(f'<circle class="dot" cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#c9a96e"/>')
    # the clinic pin
    parts.append(f'<g id="pin"><circle cx="{cx}" cy="{cy}" r="16" fill="#f4f3ef"/><circle cx="{cx}" cy="{cy}" r="7" fill="#121413"/>'
                 f'<text x="{cx + 28}" y="{cy + 8}" fill="#f4f3ef" font-family="Newsreader" font-style="italic" font-size="30">Your clinic</text></g>')
    parts.append("</svg>")
    return "".join(parts)


BODY = r"""
      <section id="cBefore" class="clip" data-start="0" data-duration="2.3" data-track-index="2"><div class="cap"><span id="cBt">Your clinic's website, <span class="it">today.</span></span></div></section>
      <section id="cAfter" class="clip" data-start="2.25" data-duration="3.05" data-track-index="2"><div class="cap"><span id="cAt">After: patients book <span class="it">in three taps.</span></span></div></section>
      <section id="cReach" class="clip" data-start="5.25" data-duration="3.05" data-track-index="2"><div class="cap"><span id="cRt">Then we put it in front of <span class="it">patients nearby.</span></span></div></section>

      <div class="phone-window" id="phoneWindow"><div class="phone-wrap"><div id="phone">
        <div class="screen">
          <video id="screen-video" src="assets/screen-80.mp4" data-start="2.25" data-duration="3.1" data-media-start="[[vMedia]]" data-track-index="3" muted playsinline></video>
          <div id="old" data-layout-allow-overlap data-layout-allow-occlusion>
            <div class="old-page" id="oldPage">
              <div class="old-head">★ Welcome To Our Dental Clinic Homepage ★</div>
              <div class="old-nav"><span>Home</span><span>About Us</span><span>Services</span><span>Gallery</span><span>Contact</span></div>
              <div class="old-body">
                <div class="old-side"><b>NEWS!!!</b> We have moved to our new premises. Please call for details.</div>
                <div class="old-main">
                  <h2>Our Services</h2>
                  We provide many dental services for the whole family. Please call us to make appointment during office hours.
                  <div class="broken" style="height:160px;width:300px">[ image not found ]</div>
                  <b>Operating Hours:</b> Mon - Sat 9am - 6pm (before renovation)
                  <p style="margin-top:12px"><i>Appointment by phone call only.</i></p>
                  <h2 style="margin-top:24px">Location</h2>
                  Please refer map below.
                  <div class="broken" style="height:420px">[ Google Map could not be loaded ]</div>
                </div>
              </div>
            </div>
            <div class="stamp" id="stamp" data-layout-allow-overlap>Call only</div>
          </div>
        </div>
      </div></div>
        <div class="ba before" id="baBefore">BEFORE</div>
        <div class="ba after" id="baAfter">AFTER</div>
      </div>

      <section id="reach" class="clip" data-start="5.25" data-duration="3.05" data-track-index="4">
        <div class="map" id="map">
          <div id="mapCam" class="clip">[[MAP]]</div>
          <div class="map-tag label">Targeting · 5 km</div>
          <div class="toasts" data-layout-allow-overlap>
            <div class="ltoast" id="t1"><i></i><div><b>New booking · Mei Ling</b><span>Check-up &amp; scaling · Saturday</span></div></div>
            <div class="ltoast" id="t2"><i></i><div><b>New booking · Arif</b><span>Tooth pain · today</span></div></div>
            <div class="ltoast" id="t3"><i></i><div><b>New booking · Wei Jie</b><span>Braces consultation · Sunday</span></div></div>
          </div>
        </div>
      </section>

      <section id="offer" class="clip light" data-start="8.25" data-duration="3.05" data-track-index="5">
        <div id="offerCam" class="clip">
          <div class="o-label label" id="oLabel">The offer</div>
          <div class="o-head" id="oHead">30 days of patient leads.</div>
          <div class="free" id="free">Free.</div>
          <div class="o-line" id="ol1" style="top:[[oline1]]px">Like the results? <em>Keep going.</em></div>
          <div class="o-line" id="ol2" style="top:[[oline2]]px">Not for you? <em>Walk away.</em></div>
        </div>
      </section>
"""

JS = r"""
      // ---- BEFORE (0 - 3B): old site, slow push toward "phone call only", stamp on the beat
      tl.fromTo('#cBt', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, 0);
      tl.fromTo('#baBefore', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, 0.2);
      tl.fromTo('#oldPage', { scale: 0.702, x: 0, y: 0 }, { scale: 1.25, x: -170, y: -250, duration: 2.2, ease: 'power1.inOut' }, 0);
      tl.fromTo('#stamp', { scale: 2.2, opacity: 0, rotation: -14 }, { scale: 1, opacity: 1, rotation: -8, duration: 0.3, ease: 'back.out(2.2)' }, B * 2);
      tl.to(['#cBt', '#baBefore'], { opacity: 0, duration: 0.2 }, B * 3 - 0.2);

      // ---- AFTER (3B - 7B): wipe the old site away, zoom into the booking card for the taps
      tl.fromTo('#old', { y: 0, opacity: 1 }, { y: -1400, duration: 0.5, ease: 'expo.inOut' }, B * 3 - 0.25);
      tl.to('#old', { opacity: 0, duration: 0.01 }, B * 3 + 0.3);
      tl.fromTo('#baAfter', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, B * 3);
      tl.fromTo('#cAt', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 3 + 0.05);
      tl.fromTo('#phone', { scale: 1, transformOrigin: '45% 40%' }, { scale: 1.36, duration: 0.7, ease: 'power2.inOut' }, B * 3.3);
      tl.to('#phone', { scale: 1, duration: 0.6, ease: 'power2.inOut' }, B * 6.3);
      tl.to(['#cAt', '#baAfter'], { opacity: 0, duration: 0.2 }, B * 7 - 0.25);
      wipe(B * 7 - 0.4, 0.65);
      tl.to('#phoneWindow', { opacity: 0, duration: 0.01 }, B * 7);

      // ---- REACH (7B - 11B): pull back over the map, radius pulses, dots fill in, bookings ping in on the beat
      tl.fromTo('#cRt', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 7 + 0.05);
      tl.fromTo('#mapCam', { scale: 1.5, transformOrigin: '50% 40%' }, { scale: 1, duration: 1.4, ease: 'expo.out' }, B * 7);
      tl.fromTo('#ring0', { scale: 0, transformOrigin: '50% 50%', transformBox: 'fill-box' }, { scale: 1, duration: 0.8, ease: 'expo.out' }, B * 7.3);
      tl.fromTo('#ring1', { scale: 0, opacity: 0, transformOrigin: '50% 50%', transformBox: 'fill-box' }, { scale: 1, opacity: 1, duration: 1.0, ease: 'expo.out' }, B * 7.6);
      tl.fromTo('#ring1', { scale: 1 }, { scale: 1.06, duration: B, repeat: 3, yoyo: true, ease: 'sine.inOut', immediateRender: false }, B * 9);
      tl.fromTo('.dot', { opacity: 0, scale: 0, transformOrigin: '50% 50%', transformBox: 'fill-box' }, { opacity: 0.85, scale: 1, duration: 0.3, ease: 'back.out(2)', stagger: 0.035 }, B * 7.8);
      ['#t1', '#t2', '#t3'].forEach((t, i) => tl.fromTo(t, { y: 60, opacity: 0, scale: 0.94 }, { y: 0, opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(1.6)' }, B * (8 + i)));
      tl.fromTo('#mapCam', { scale: 1 }, { scale: 1.06, duration: B * 3, ease: 'none', immediateRender: false }, B * 8.6);
      tl.to('#cRt', { opacity: 0, duration: 0.2 }, B * 11 - 0.25);

      // ---- OFFER (11B - 15B): headline pulls back from a close-up, "Free." lands on the beat
      tl.fromTo('#oHead', { scale: 1.7, opacity: 0, transformOrigin: '0% 30%' }, { scale: 1, opacity: 1, duration: 1.0, ease: 'expo.out' }, B * 11);
      tl.fromTo('#oLabel', { opacity: 0 }, { opacity: 1, duration: 0.4 }, B * 11 + 0.2);
      tl.fromTo('#free', { scale: 0.6, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2)' }, B * 12);
      tl.fromTo('#ol1', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'expo.out' }, B * 13);
      tl.fromTo('#ol2', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'expo.out' }, B * 14);
      tl.fromTo('#offerCam', { scale: 1 }, { scale: 1.04, duration: B * 4, ease: 'none', transformOrigin: '30% 40%' }, B * 11);
      tl.to('#hud', { opacity: 0, duration: 0.01 }, B * 11);
      wipe(B * 15 - 0.4, 0.65);

      const E = B * 15;
"""


def build():
    base_head = ba.HEAD.replace('data-duration="7.5"', f'data-duration="{DUR}"')
    head = base_head.replace("    </style>", EXTRA_CSS + "    </style>")
    end = ba.END.replace("FREE SITE REVIEW", "CLAIM 30 FREE DAYS")
    js_head = ba.JS_HEAD.replace("const B = 60 / 92, DUR = 7.5;", f"const B = 60 / {BPM}, DUR = {DUR};")
    for fmt, f in ba.FORMATS.items():
        m = FMT[fmt]
        html = (head + BODY + end + '      <div class="wipe" id="wipe"></div>\n'
                f'      <audio id="music" src="assets/music-main.mp3" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="8"></audio>'
                + js_head + JS + ba.END_JS + ba.JS_TAIL)
        vals = dict(f, **m, TITLE="Redesign + free 30 days", TAG='Redesigned to <span class="it">get you booked.</span>',
                    vMedia=round(B * 3.5 - B, 4), endStart=round(B * 15, 4), endDur=round(DUR - B * 15, 4),
                    phoneTw=f["phoneT"] - f["winT"], MAP=map_svg(m["mapH"]))
        for k, v in vals.items():
            html = html.replace(f"[[{k}]]", str(v))
        assert "[[" not in html, (fmt, html[html.index("[["):html.index("[[") + 40])
        (ROOT / f"main-{fmt}.html").write_text(html)
        print("wrote", f"main-{fmt}.html")


if __name__ == "__main__":
    build()
