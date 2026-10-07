"""Builds the 18.4 s main ad, light and luxurious:
problem -> how we fix it -> 3 steps -> free 30 days -> CTA.

Writes main-916.html (Reels/Stories) and main-45.html (Feed). Shares the base
layout and end card with tools/build-ads.py, restyled light here. Timing is on
an 80 BPM grid (B = 0.75 s); tools/compose-music-main.py places its hits on the
same beats.

  0   - 3B   Problem  "Struggling to get bookings?" near-empty appointment book
  3B  - 5B   Problem  "Your website isn't bringing in leads." old site, CALL ONLY
  5B  - 7B   Turn     old site wipes away: "Here's how we fix it. Three steps."
  7B  - 11B  Step 1   we run ads to patients nearby: sponsored post, tap Book now
  11B - 15B  Step 2   they book on the new website in three taps
  15B - 18B  Step 3   the booking lands in the clinic's WhatsApp
  18B - 21B  Offer    30 days of leads, free; keep going or walk away
  21B - end  CTA      4Skales, claim your free 30 days
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ba", HERE / "build-ads.py")
ba = importlib.util.module_from_spec(spec); spec.loader.exec_module(ba)

ROOT = HERE.parent
BPM = 80
B = 60 / BPM
DUR = 18.4

FMT = {
    "916": dict(hookCap=380, calT=640, calH=560, stepCap=372,
                offerLabel=400, offerHead=450, freeT=770, oline1=930, oline2=1040),
    "45": dict(hookCap=150, calT=450, calH=640, stepCap=118,
               offerLabel=250, offerHead=300, freeT=620, oline1=780, oline2=890),
}

# Light, luxurious restyle of the shared base: porcelain ground, ink type,
# bronze/champagne accents, hairlines, paper grain, soft shadows.
LIGHT_CSS = r"""
      html, body, #bg, #end { background: #f3f0e9; }
      #root { color: #1a1714; }
      .grid { background-image: linear-gradient(rgba(26,23,20,.04) 2px, transparent 2px), linear-gradient(90deg, rgba(26,23,20,.04) 2px, transparent 2px); }
      .grain { position: absolute; inset: 0; opacity: .5; mix-blend-mode: multiply; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .09 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
      .frame { position: absolute; inset: 34px; border: 1px solid rgba(138,106,56,.35); }
      .frame::after { content: ""; position: absolute; inset: 8px; border: 1px solid rgba(138,106,56,.18); }
      .it { color: #8a6a38; }
      .hud span { color: #6d665c; }
      .ghost { opacity: .045; }
      .wipe { background: #d9c7a3; }
      #phone { box-shadow: 0 0 0 1px rgba(138,106,56,.45), 0 50px 110px rgba(70,52,24,.28); }
      .end-rule { background: rgba(138,106,56,.45); }
      .end-cities { color: #6d665c; }
      .cta { background: #1a1714; color: #f3f0e9; }
      .cta span { color: #d9c7a3; }
      .round-arrow { background: #c9a96e; }
      .light { background: #e9e1d3; color: #1a1714; }
"""

EXTRA_CSS = r"""
      /* hook: a near-empty appointment book */
      .hook-cap { position: absolute; left: 76px; right: 76px; top: [[hookCap]]px; font: 300 112px/1.0 var(--serif); letter-spacing: -.025em; }
      .book { position: absolute; left: 76px; right: 76px; top: [[calT]]px; height: [[calH]]px; background: #fbfaf6; box-shadow: 0 40px 90px rgba(70,52,24,.18); padding: 34px 36px; }
      .book::before { content: ""; position: absolute; inset: 10px; border: 1px solid rgba(138,106,56,.28); pointer-events: none; }
      .book-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 18px; }
      .book-head b { font: 300 46px var(--serif); }
      .book-head span { color: #8a6a38; }
      .book-grid { display: grid; grid-template-columns: 70px repeat(6, 1fr); gap: 8px; }
      .book-grid div { height: calc(([[calH]]px - 170px) / 6 - 8px); border-top: 1px solid rgba(26,23,20,.12); font: 400 18px var(--sans); color: #635c52; padding-top: 6px; letter-spacing: .08em; }
      .book-grid .slot-booked { background: #1a1714; color: #e9e1d3; border-top: 0; padding: 8px 10px; font: 400 17px var(--sans); }
      .book-grid .empty { background: rgba(138,106,56,.05); }
      .book-tally { position: absolute; right: 36px; bottom: 26px; font: 300 italic 34px var(--serif); color: #8a6a38; }

      /* before / after labels on the phone window */
      .ba { position: absolute; left: 76px; top: 18px; height: 52px; padding: 0 22px; display: flex; align-items: center; clip-path: var(--chamfer); font: 500 22px var(--sans); letter-spacing: .3em; }
      .ba.before { background: #a8443a; color: #fff; }
      .ba.after { background: #1a1714; color: #e9d9b8; }
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

      /* steps */
      .step-cap { position: absolute; left: 76px; right: 76px; top: [[stepCap]]px; }
      .step-cap .label { display: block; color: #74572a; margin-bottom: 14px; }
      .step-cap .label b { font-weight: 500; color: #1a1714; }
      .step-cap span.t { display: block; font: 300 72px/1.04 var(--serif); letter-spacing: -.02em; }
      .chip2 { position: absolute; top: 18px; height: 52px; padding: 0 22px; display: flex; align-items: center; clip-path: var(--chamfer); font: 500 22px var(--sans); letter-spacing: .26em; }

      /* step 1: a social feed with the clinic's sponsored post */
      #feed { position: absolute; inset: 0; background: #faf9f6; overflow: hidden; }
      #feedScroll { position: absolute; left: 0; right: 0; top: 0; }
      .f-top { height: 150px; padding: 80px 34px 0; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ebe7df; background: #faf9f6; position: relative; z-index: 2; }
      .f-top b { font: 500 34px var(--sans); letter-spacing: .02em; }
      .f-top span { width: 120px; height: 18px; border-radius: 9px; background: #e7e2d8; }
      .f-ghost { height: 280px; margin: 22px 26px; border-radius: 22px; background: linear-gradient(135deg, #e9e4da, #ddd6c9); }
      .f-head { height: 104px; display: flex; align-items: center; gap: 18px; padding: 0 30px; }
      .f-head i { width: 64px; height: 64px; border-radius: 50%; border: 1px solid #c9a96e; display: flex; align-items: center; justify-content: center; font: 300 italic 30px var(--serif); color: #8a6a38; background: #fff; }
      .f-head b { display: block; font: 500 28px var(--sans); }
      .f-head span { display: block; font: 300 22px var(--sans); color: #6d665c; }
      .f-img { height: 420px; margin: 0 0; background: #f1ece2; position: relative; padding: 52px 56px; border-top: 1px solid #ebe7df; border-bottom: 1px solid #ebe7df; }
      .f-img::before { content: ""; position: absolute; inset: 22px; border: 1px solid rgba(138,106,56,.35); }
      .f-brand { font: 300 64px var(--serif); }
      .f-brand em { color: #8a6a38; }
      .f-line { font: 300 80px/1.0 var(--serif); margin-top: 34px; letter-spacing: -.02em; }
      .f-sub { font: 400 24px var(--sans); color: #5f584e; letter-spacing: .14em; text-transform: uppercase; margin-top: 22px; }
      .f-badge { display: inline-block; margin-top: 22px; padding: 14px 24px; background: #1a1714; color: #e9d9b8; font: 300 italic 32px var(--serif); }
      .f-cta { height: 96px; margin: 0; padding: 0 30px; display: flex; align-items: center; justify-content: space-between; background: #1a1714; color: #f3f0e9; font: 500 28px var(--sans); letter-spacing: .12em; text-transform: uppercase; }
      .f-copy { padding: 22px 30px; font: 300 26px/1.4 var(--sans); color: #3c3832; }
      .f-copy b { font-weight: 500; }
      .finger { position: absolute; width: 70px; height: 70px; margin: -35px 0 0 -35px; border-radius: 50%; background: rgba(255,255,255,.6); border: 3px solid rgba(26,23,20,.55); box-shadow: 0 8px 20px rgba(0,0,0,.2); }

      /* step 3: WhatsApp */
      .chat-top { background: #1f2a25; }

      /* offer (sand) */
      .o-label { position: absolute; left: 80px; top: [[offerLabel]]px; color: #8a6a38; }
      .o-head { position: absolute; left: 76px; right: 76px; top: [[offerHead]]px; font: 300 128px/0.98 var(--serif); letter-spacing: -.03em; }
      .free { position: absolute; left: 80px; top: [[freeT]]px; height: 120px; padding: 0 46px; display: flex; align-items: center; background: #1a1714; color: #d9c7a3; clip-path: var(--chamfer); font: 300 italic 92px/1 var(--serif); }
      .o-line { position: absolute; left: 80px; right: 80px; font: 300 64px/1.1 var(--serif); }
      .o-line em { color: #8a6a38; }
"""


def appointment_book():
    days = ["", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    times = ["9AM", "10AM", "11AM", "2PM", "3PM"]
    booked = {(1, 2): "Scaling", (4, 4): "Filling"}
    cells = [f"<div>{d}</div>" for d in days]
    for r, t in enumerate(times):
        cells.append(f"<div>{t}</div>")
        for c in range(1, 7):
            if (r, c) in booked:
                cells.append(f'<div class="slot-booked">{booked[(r, c)]}</div>')
            else:
                cells.append('<div class="empty"></div>')
    return "".join(cells)


BODY = r"""
      <section id="hook" class="clip" data-start="0" data-duration="2.3" data-track-index="1">
        <div id="hookCam" class="clip">
          <div class="hook-cap"><span id="hookT">Struggling to get <span class="it">bookings?</span></span></div>
          <div class="book" id="book">
            <div class="book-head"><b>This week</b><span class="label">Appointments</span></div>
            <div class="book-grid" id="bookGrid">[[BOOK]]</div>
            <div class="book-tally" id="tally">2 of 30 slots filled</div>
          </div>
        </div>
      </section>
      <section id="cOld" class="clip" data-start="2.25" data-duration="1.55" data-track-index="2"><div class="cap"><span id="cOt">Your website isn't <span class="it">bringing in leads.</span></span></div></section>
      <section id="cFix" class="clip" data-start="3.75" data-duration="1.55" data-track-index="2"><div class="cap"><span id="cFt">Here's how we fix it. <span class="it">Three steps.</span></span></div></section>
      <section id="s1" class="clip" data-start="5.25" data-duration="3.05" data-track-index="2"><div class="step-cap" id="s1t"><span class="label"><b>Step 1</b> of 3 · Meta &amp; Google ads · within 5 km</span><span class="t">We run ads to patients <span class="it">near your clinic.</span></span></div></section>
      <section id="s2" class="clip" data-start="8.25" data-duration="3.05" data-track-index="2"><div class="step-cap" id="s2t"><span class="label"><b>Step 2</b> of 3 · Website</span><span class="t">They book on your new site <span class="it">in three taps.</span></span></div></section>
      <section id="s3" class="clip" data-start="11.25" data-duration="2.3" data-track-index="2"><div class="step-cap" id="s3t"><span class="label"><b>Step 3</b> of 3 · WhatsApp</span><span class="t">The booking lands in <span class="it">your WhatsApp.</span></span></div></section>

      <div class="phone-window" id="phoneWindow"><div class="phone-wrap"><div id="phone">
        <div class="screen">
          <video id="screen-video" src="assets/screen-80.mp4" data-start="8.25" data-duration="3.05" data-media-start="[[vMedia]]" data-track-index="3" muted playsinline></video>
          <div id="feed" data-layout-allow-overlap data-layout-allow-occlusion>
            <div class="f-top"><span></span><b>Feed</b></div>
            <div id="feedScroll">
              <div style="height:150px"></div>
              <div class="f-ghost"></div>
              <div class="f-head"><i>L</i><div><b>Lumen Dental</b><span>Sponsored · Mount Austin</span></div></div>
              <div class="f-img"><div class="f-brand">Lumen <em>Dental</em></div><div class="f-line">Check-up &amp; scaling</div><div class="f-sub">Mount Austin · Open weekends</div></div>
              <div class="f-cta" id="bookNow"><span>Book now</span><span>›</span></div>
              <div class="f-copy"><b>Lumen Dental</b> Unhurried dental care, five minutes from you.</div>
              <div class="f-ghost"></div>
            </div>
            <div class="finger" id="adFinger"></div>
          </div>
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
          [[CHAT]]
        </div>
      </div></div>
        <div class="ba before" id="baBefore">BEFORE</div>
      </div>

      <section id="offer" class="clip light" data-start="13.5" data-duration="2.3" data-track-index="5">
        <div id="offerCam" class="clip">
          <div class="o-label label" id="oLabel">Try it</div>
          <div class="o-head" id="oHead">30 days of leads.</div>
          <div class="free" id="free">Free.</div>
          <div class="o-line" id="ol1" style="top:[[oline1]]px">Like the results? <em>Keep going.</em></div>
          <div class="o-line" id="ol2" style="top:[[oline2]]px">Not for you? <em>Walk away.</em></div>
        </div>
      </section>
"""

JS = r"""
      // ---- PROBLEM (0 - 3B): the question, a near-empty appointment book
      tl.fromTo('#hookT', { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'expo.out' }, 0);
      tl.fromTo('#book', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: 'expo.out' }, 0.25);
      tl.fromTo('#hookCam', { scale: 1 }, { scale: 1.05, duration: B * 3, ease: 'none', transformOrigin: '50% 60%' }, 0);
      tl.fromTo('#bookGrid .empty', { opacity: 0 }, { opacity: 1, duration: 0.25, stagger: { each: 0.02, from: 'random' } }, 0.6);
      tl.fromTo('#tally', { x: 20, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'expo.out' }, B * 2);
      tl.to(['#hookT', '#book'], { opacity: 0, y: -24, duration: 0.25, ease: 'power2.in', stagger: 0.04 }, B * 3 - 0.3);

      // ---- PROBLEM (3B - 5B): the outdated site, CALL ONLY on the beat
      tl.fromTo('#phone', { y: 1500 }, { y: 0, duration: 0.7, ease: 'expo.out' }, B * 3 - 0.1);
      tl.fromTo('#cOt', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 3);
      tl.fromTo('#baBefore', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, B * 3 + 0.2);
      tl.fromTo('#oldPage', { scale: 0.702, x: 0, y: 0 }, { scale: 1.2, x: -150, y: -230, duration: 1.6, ease: 'power1.inOut' }, B * 3);
      tl.fromTo('#stamp', { scale: 2.2, opacity: 0, rotation: -14 }, { scale: 1, opacity: 1, rotation: -8, duration: 0.3, ease: 'back.out(2.2)' }, B * 4);
      tl.to(['#cOt', '#baBefore'], { opacity: 0, duration: 0.2 }, B * 5 - 0.2);

      // ---- THE TURN (5B - 7B): the old site wipes away
      tl.fromTo('#old', { x: 0, opacity: 1 }, { x: -720, duration: 0.55, ease: 'expo.inOut' }, B * 5 - 0.2);
      tl.to('#old', { opacity: 0, duration: 0.01 }, B * 5 + 0.4);
      tl.fromTo('#cFt', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 5);
      tl.to('#cFt', { opacity: 0, duration: 0.2 }, B * 7 - 0.2);

      // ---- STEP 1 (7B - 11B): the clinic's ad appears in the feed, tap Book now on the beat
      tl.fromTo('#s1t', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 7);
      tl.fromTo('#feedScroll', { y: 0 }, { y: -320, duration: 1.0, ease: 'power3.inOut' }, B * 7.4);
      tl.to('#phone', { y: -150, duration: 1.0, ease: 'power3.inOut' }, B * 7.6);
      tl.fromTo('#phone', { scale: 1, transformOrigin: '50% 60%' }, { scale: 1.08, duration: 1.2, ease: 'power2.inOut', immediateRender: false }, B * 8.3);
      tl.fromTo('#adFinger', { x: 520, y: 1000, opacity: 0 }, { x: 351, y: 576, opacity: 1, duration: 0.6, ease: 'power2.out' }, B * 9.1);
      tl.fromTo('#adFinger', { scale: 1 }, { scale: 0.75, duration: 0.1, yoyo: true, repeat: 1, ease: 'power1.inOut', immediateRender: false }, B * 10);
      tl.fromTo('#bookNow', { backgroundColor: '#1a1714' }, { backgroundColor: '#8a6a38', duration: 0.12, ease: 'none' }, B * 10);
      tl.to('#s1t', { opacity: 0, duration: 0.2 }, B * 11 - 0.2);

      // ---- STEP 2 (11B - 15B): the tap opens the clinic's new site; zoom into the booking card for the taps
      tl.fromTo('#feed', { x: 0, opacity: 1 }, { x: -720, duration: 0.45, ease: 'expo.inOut' }, B * 11 - 0.15);
      tl.to('#feed', { opacity: 0, duration: 0.01 }, B * 11 + 0.35);
      tl.to('#phone', { y: 0, scale: 1.36, transformOrigin: '45% 40%', duration: 0.6, ease: 'power2.inOut' }, B * 11.1);
      tl.fromTo('#s2t', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 11);
      tl.to('#phone', { scale: 1, duration: 0.5, ease: 'power2.inOut' }, B * 14.3);
      tl.to('#s2t', { opacity: 0, duration: 0.2 }, B * 15 - 0.2);

      // ---- STEP 3 (15B - 18B): WhatsApp slides up, push in on the new-booking notification
      tl.fromTo('#chat', { y: 1400, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'expo.out' }, B * 15 - 0.1);
      tl.fromTo('#s3t', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' }, B * 15);
      tl.fromTo('#toast', { y: -160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.8)' }, B * 16);
      tl.fromTo('#phone', { scale: 1, transformOrigin: '50% 18%' }, { scale: 1.28, duration: 0.7, ease: 'power2.inOut', immediateRender: false }, B * 16);
      tl.fromTo('#bubIn', { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, B * 17);
      tl.to('#s3t', { opacity: 0, duration: 0.2 }, B * 18 - 0.25);
      wipe(B * 18 - 0.4, 0.65);
      tl.to('#phoneWindow', { opacity: 0, duration: 0.01 }, B * 18);

      // ---- OFFER (18B - 21B): "30 days of leads. Free." on the beat
      tl.fromTo('#oHead', { scale: 1.6, opacity: 0, transformOrigin: '0% 30%' }, { scale: 1, opacity: 1, duration: 0.9, ease: 'expo.out' }, B * 18);
      tl.fromTo('#oLabel', { opacity: 0 }, { opacity: 1, duration: 0.4 }, B * 18 + 0.2);
      tl.fromTo('#free', { scale: 0.6, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2)' }, B * 19);
      tl.fromTo('#ol1', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'expo.out' }, B * 19.67);
      tl.fromTo('#ol2', { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'expo.out' }, B * 20.33);
      tl.fromTo('#offerCam', { scale: 1 }, { scale: 1.04, duration: B * 3, ease: 'none', transformOrigin: '30% 40%' }, B * 18);
      tl.to('#hud', { opacity: 0, duration: 0.01 }, B * 18);
      wipe(B * 21 - 0.4, 0.65);

      const E = B * 21;
"""


def build():
    head = ba.HEAD.replace('data-duration="7.5"', f'data-duration="{DUR}"')
    head = head.replace("    </style>", EXTRA_CSS + LIGHT_CSS + "    </style>")
    head = head.replace('src="assets/4skales-logo-ivory.svg" alt="4Skales"', 'src="assets/4skales-logo-ink.svg" alt="4Skales"')
    head = head.replace('<img class="ghost" id="ghost" src="assets/4skales-logo-ivory.svg"', '<img class="ghost" id="ghost" src="assets/4skales-logo-ink.svg"')
    head = head.replace('        <div class="grid" id="grid"></div>\n', '        <div class="grid" id="grid"></div>\n        <div class="grain"></div>\n        <div class="frame"></div>\n')
    end = ba.END.replace("FREE SITE REVIEW", "CLAIM 30 FREE DAYS").replace("assets/4skales-logo-ivory.svg", "assets/4skales-logo-ink.svg")
    end = end.replace('stroke="#f4f3ef"', 'stroke="#1a1714"')
    js_head = ba.JS_HEAD.replace("const B = 60 / 92, DUR = 7.5;", f"const B = 60 / {BPM}, DUR = {DUR};")
    for fmt, f in ba.FORMATS.items():
        m = FMT[fmt]
        html = (head + BODY + end + '      <div class="wipe" id="wipe"></div>\n'
                f'      <audio id="music" src="assets/music-main.mp3" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="8"></audio>'
                + js_head + JS + ba.END_JS + ba.JS_TAIL)
        vals = dict(f, **m, TITLE="Redesign + free 30 days", TAG='Redesigned to <span class="it">get you booked.</span>',
                    vMedia=round(B * 2.5, 4), endStart=round(B * 21, 4), endDur=round(DUR - B * 21, 4),
                    phoneTw=f["phoneT"] - f["winT"], BOOK=appointment_book(), CHAT=ba.CHAT)
        for k, v in vals.items():
            html = html.replace(f"[[{k}]]", str(v))
        assert "[[" not in html, (fmt, html[html.index("[["):html.index("[[") + 40])
        (ROOT / f"main-{fmt}.html").write_text(html)
        print("wrote", f"main-{fmt}.html")


if __name__ == "__main__":
    build()
