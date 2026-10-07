"""Builds the three 7.5 s Meta ads in 9:16 (Reels/Stories) and 4:5 (Feed).

  ad1  Missed calls  : 17 missed calls -> zoom into a 3-tap booking -> end card
  ad2  3-tap booking : zoomed booking -> WhatsApp arrives -> end card
  ad3  The offer     : RM 6,800 pull-back -> no retainer / yours / 3 weeks -> proof -> end card

Writes ad1-916.html ... ad3-45.html next to index.html. Render with
  npx hyperframes render -c ad1-916.html -o renders/4skales-ad1-missed-calls-9x16.mp4

Timing is on a 92 BPM grid (B); the soundtracks in tools/compose-music.py use
the same cue points. 9:16 keeps all text between y=290 and y=1250, clear of the
Reels header and the caption/CTA overlay in the bottom 35%.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUR = 7.5

FORMATS = {
    "916": dict(H=1920, hud=300, cap=380, capSize=82, winT=590, phoneL=180, phoneT=640, phoneS=1.0,
                notifT=400, countT=640, countSize=430, labelT=1010, lineT=1060,
                endLogo=470, endRule=690, endTag=730, endCities=960, endCta=1030,
                priceLabel=420, priceT=480, priceRule=800, line1=850, lineGap=120,
                proofT=430, proofSub=720, caseT=900, ghostT=1380),
    "45": dict(H=1350, hud=64, cap=140, capSize=74, winT=330, phoneL=295, phoneT=370, phoneS=0.68,
               notifT=210, countT=420, countSize=400, labelT=770, lineT=820,
               endLogo=330, endRule=540, endTag=580, endCities=810, endCta=890,
               priceLabel=270, priceT=330, priceRule=640, line1=690, lineGap=120,
               proofT=290, proofSub=580, caseT=770, ghostT=2400),
}

HEAD = r"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=[[H]]" />
    <title>4Skales · [[TITLE]]</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face { font-family: 'Jost'; font-weight: 300; font-style: normal; src: url('assets/fonts/Jost-300-normal.woff2') format('woff2'); }
      @font-face { font-family: 'Jost'; font-weight: 400; font-style: normal; src: url('assets/fonts/Jost-400-normal.woff2') format('woff2'); }
      @font-face { font-family: 'Jost'; font-weight: 500; font-style: normal; src: url('assets/fonts/Jost-500-normal.woff2') format('woff2'); }
      @font-face { font-family: 'Newsreader'; font-weight: 300; font-style: normal; src: url('assets/fonts/Newsreader-300-normal.woff2') format('woff2'); }
      @font-face { font-family: 'Newsreader'; font-weight: 300; font-style: italic; src: url('assets/fonts/Newsreader-300-italic.woff2') format('woff2'); }
      :root {
        --ink: #121413; --ink-2: #1c1f1d; --white: #f4f3ef; --dim: #a19e96;
        --hair: rgba(201,169,110,.34); --gold: #c9a96e; --gold-deep: #7d5f30; --red: #d66a5c;
        --serif: 'Newsreader', Georgia, serif; --sans: 'Jost', sans-serif;
        --chamfer: polygon(26px 0, 100% 0, 100% calc(100% - 26px), calc(100% - 26px) 100%, 0 100%, 0 26px);
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: [[H]]px; overflow: hidden; background: var(--ink); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; color: var(--white); font-family: var(--sans); }
      .clip { position: absolute; inset: 0; }
      .it { font-style: italic; color: var(--gold); }
      .label { font: 500 22px/1 var(--sans); letter-spacing: .32em; text-transform: uppercase; }
      #bg, #end { background: var(--ink); }
      .grid { position: absolute; inset: -120px; background-image: linear-gradient(rgba(244,243,239,.045) 2px, transparent 2px), linear-gradient(90deg, rgba(244,243,239,.045) 2px, transparent 2px); background-size: 120px 120px; }
      .ghost { position: absolute; left: -40px; top: [[ghostT]]px; width: 1500px; height: auto; opacity: .06; }
      .hud { position: absolute; top: [[hud]]px; left: 76px; right: 76px; display: flex; align-items: center; justify-content: space-between; }
      .hud img { height: 32px; width: auto; display: block; }
      .hud span { color: var(--dim); }
      .cap { position: absolute; left: 76px; right: 76px; top: [[cap]]px; font: 300 [[capSize]]px/1.04 var(--serif); letter-spacing: -.02em; }
      .cap span { display: block; }
      .wipe { position: absolute; top: -300px; height: 2520px; width: 1700px; left: -310px; background: var(--white); }

      /* phone: the wrapper sets the per-format size; the timeline moves #phone */
      .phone-window { position: absolute; left: 0; right: 0; top: [[winT]]px; bottom: 0; overflow: hidden; }
      .phone-wrap { position: absolute; left: [[phoneL]]px; top: [[phoneTw]]px; width: 720px; height: 1360px; transform: scale([[phoneS]]); transform-origin: 0 0; }
      #phone { position: absolute; inset: 0; border-radius: 84px; background: #070908; padding: 9px; box-shadow: 0 0 0 1px rgba(201,169,110,.5), 0 60px 140px rgba(0,0,0,.6); }
      .screen { position: relative; width: 702px; height: 1342px; border-radius: 76px; overflow: hidden; background: var(--white); }
      .screen video { position: absolute; left: 0; top: 0; width: 702px; height: 1368px; object-fit: cover; }
      #chat { position: absolute; inset: 0; background: #e9e7e1; }
      .chat-top { height: 200px; background: #1b2420; padding: 96px 34px 0; display: flex; align-items: center; gap: 22px; color: var(--white); }
      .chat-av { width: 74px; height: 74px; border-radius: 50%; border: 1px solid var(--gold); display: flex; align-items: center; justify-content: center; font: 300 italic 36px var(--serif); color: var(--gold); }
      .chat-top b { display: block; font: 400 32px var(--sans); }
      .chat-top span { display: block; font: 300 22px var(--sans); color: #b5b2aa; }
      .chat-body { padding: 180px 28px 44px; }
      .bub { max-width: 560px; padding: 22px 26px 14px; border-radius: 28px; font: 400 30px/1.42 var(--sans); color: #1a1714; margin-bottom: 26px; }
      .bub small { display: block; text-align: right; font: 400 19px var(--sans); color: #4f5a54; margin-top: 6px; }
      .bub.out { margin-left: auto; background: #dcf3d4; border-top-right-radius: 8px; }
      .bub.in { background: #fff; border-top-left-radius: 8px; }
      .toast { position: absolute; left: 24px; right: 24px; top: 224px; height: 120px; border-radius: 30px; background: rgba(28,31,29,.95); display: flex; align-items: center; gap: 22px; padding: 0 28px; color: var(--white); }
      .toast i { width: 64px; height: 64px; border-radius: 16px; background: #2f8a57; flex: none; }
      .toast b { display: block; font: 500 27px var(--sans); }
      .toast span { display: block; font: 300 24px var(--sans); color: #c9c6be; }

      /* hook */
      .notifs { position: absolute; left: 520px; right: 76px; top: [[notifT]]px; height: 330px; }
      .notif { position: absolute; left: 0; right: 0; top: 0; height: 92px; background: var(--ink-2); border: 1px solid rgba(244,243,239,.12); clip-path: var(--chamfer); display: flex; align-items: center; gap: 22px; padding: 0 30px; }
      .notif i { width: 12px; height: 12px; border-radius: 50%; background: var(--red); flex: none; }
      .notif b { font: 400 29px var(--sans); flex: 1; }
      .notif span { font: 300 italic 27px var(--serif); color: var(--dim); }
      .count { position: absolute; left: 60px; top: [[countT]]px; font: 300 [[countSize]]px/0.8 var(--serif); letter-spacing: -.05em; }
      .count-label { position: absolute; left: 80px; top: [[labelT]]px; color: var(--red); }
      .hook-line { position: absolute; left: 76px; right: 76px; top: [[lineT]]px; font: 300 76px/1.04 var(--serif); }

      /* price (light) */
      .light { background: var(--white); color: var(--ink); }
      .p-label { position: absolute; left: 80px; top: [[priceLabel]]px; color: var(--gold-deep); }
      .price { position: absolute; left: 60px; top: [[priceT]]px; font: 300 290px/0.9 var(--serif); letter-spacing: -.05em; white-space: nowrap; }
      .price small { font-size: 116px; letter-spacing: -.02em; margin-right: 18px; }
      .p-rule { position: absolute; left: 80px; right: 80px; top: [[priceRule]]px; height: 3px; background: var(--ink); transform-origin: left center; }
      .p-line { position: absolute; left: 80px; right: 80px; font: 300 96px/1 var(--serif); letter-spacing: -.02em; }
      .p-line em { color: var(--gold-deep); }

      /* proof */
      .proof-head { position: absolute; left: 76px; right: 76px; top: [[proofT]]px; font: 300 120px/0.98 var(--serif); letter-spacing: -.03em; }
      .proof-sub { position: absolute; left: 80px; right: 120px; top: [[proofSub]]px; font: 300 46px/1.3 var(--sans); color: #d6d3cb; }
      .case { position: absolute; left: 76px; right: 76px; top: [[caseT]]px; height: 250px; background: var(--white); color: var(--ink); clip-path: var(--chamfer); padding: 46px 52px; }
      .case .label { color: var(--gold-deep); }
      .case b { display: block; font: 300 64px/1.05 var(--serif); margin-top: 22px; }
      .case b em { color: var(--gold-deep); }
      .round-arrow { position: absolute; right: 52px; bottom: 46px; width: 88px; height: 88px; border-radius: 50%; background: var(--ink); display: flex; align-items: center; justify-content: center; }

      /* end card */
      .end-logo { position: absolute; left: 110px; top: [[endLogo]]px; width: 860px; }
      .end-logo img { width: 860px; height: auto; display: block; }
      .end-rule { position: absolute; left: 110px; width: 860px; top: [[endRule]]px; height: 2px; background: var(--hair); transform-origin: left center; }
      .end-tag { position: absolute; left: 110px; right: 80px; top: [[endTag]]px; font: 300 86px/1.02 var(--serif); letter-spacing: -.02em; }
      .end-cities { position: absolute; left: 112px; top: [[endCities]]px; color: var(--dim); }
      .cta { position: absolute; left: 110px; right: 110px; top: [[endCta]]px; height: 150px; background: var(--white); color: var(--ink); clip-path: var(--chamfer); display: flex; align-items: center; justify-content: space-between; padding: 0 52px; }
      .cta b { font: 500 36px var(--sans); letter-spacing: .08em; }
      .cta span { display: block; font: 300 italic 32px var(--serif); color: var(--gold-deep); margin-top: 4px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="7.5" data-width="1080" data-height="[[H]]">
      <section id="bg" class="clip" data-start="0" data-duration="7.5" data-track-index="0">
        <div class="grid" id="grid"></div>
        <img class="ghost" id="ghost" src="assets/4skales-logo-ivory.svg" alt="" aria-hidden="true" data-layout-allow-occlusion data-layout-allow-overflow>
        <div class="hud" id="hud"><img src="assets/4skales-logo-ivory.svg" alt="4Skales"><span class="label">JB · KL</span></div>
      </section>
"""

PHONE = r"""
      <div class="phone-window"><div class="phone-wrap"><div id="phone">
        <div class="screen">
          <video id="screen-video" src="assets/screen.mp4" data-start="[[vStart]]" data-duration="[[vDur]]" data-media-start="[[vMedia]]" data-track-index="3" muted playsinline></video>
          [[CHAT]]
        </div>
      </div></div></div>
"""

CHAT = r"""<div id="chat" data-layout-allow-overlap data-layout-allow-occlusion>
            <div class="chat-top" data-layout-allow-overlap><div class="chat-av">L</div><div><b>Lumen Dental</b><span>online</span></div></div>
            <div class="chat-body">
              <div class="bub out">Hi Lumen Dental, I'm Mei Ling. I'd like to reserve: Check-up &amp; scaling. Preferred: Saturday, morning.<small>10:42 ✓✓</small></div>
              <div class="bub in" id="bubIn">Hello Mei Ling, Saturday at 10:00am is available. Shall we confirm?<small>10:44</small></div>
            </div>
            <div class="toast" id="toast" data-layout-allow-overlap><i></i><div><b>New booking · Mei Ling</b><span>Check-up &amp; scaling · Sat morning</span></div></div>
          </div>"""

END = r"""
      <section id="end" class="clip" data-start="[[endStart]]" data-duration="[[endDur]]" data-track-index="7">
        <div id="endCam" class="clip">
          <div class="end-logo" id="endLogo"><img src="assets/4skales-logo-ivory.svg" alt="4Skales"></div>
          <div class="end-rule" id="endRule"></div>
          <div class="end-tag" id="endTag">[[TAG]]</div>
          <div class="end-cities label" id="endCities">Johor Bahru · Kuala Lumpur</div>
          <div class="cta" id="cta"><div><b>FREE SITE REVIEW</b><span>Tap Send Message</span></div>
            <div class="round-arrow" style="position:static" id="ctaArrow"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#f4f3ef" stroke-width="1.8"><path d="M12 5v14M6 13l6 6 6-6"/></svg></div></div>
        </div>
      </section>
"""

END_JS = r"""
      // ---- end card: logo pull-back, slow push-in, pointer to Meta's Send Message button
      tl.fromTo('#endLogo', { scale: 1.45, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.7, ease: 'expo.out' }, E);
      tl.fromTo('#endCam', { scale: 1 }, { scale: 1.04, duration: DUR - E, ease: 'none', transformOrigin: '50% 40%' }, E);
      tl.fromTo('#endRule', { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: 'expo.out' }, E + 0.15);
      tl.fromTo('#endTag', { y: 34, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'expo.out' }, E + 0.3);
      tl.fromTo('#endCities', { opacity: 0 }, { opacity: 1, duration: 0.4 }, E + 0.55);
      tl.fromTo('#cta', { x: 1100, skewX: -10 }, { x: 0, skewX: 0, duration: 0.6, ease: 'expo.out' }, E + 0.5);
      tl.fromTo('#ctaArrow', { y: -6 }, { y: 8, duration: B / 2, repeat: 5, yoyo: true, ease: 'sine.inOut' }, E + 1.0);
      tl.to('#hud', { opacity: 0, duration: 0.2 }, E);
"""

JS_HEAD = r"""
    </div>
    <script>
      const B = 60 / 92, DUR = 7.5;
      const tl = gsap.timeline({ paused: true });
      tl.fromTo('#grid', { y: 0 }, { y: -120, duration: DUR, ease: 'none' }, 0);
      tl.fromTo('#ghost', { x: 0 }, { x: -220, duration: DUR, ease: 'none' }, 0);
      tl.set('#wipe', { x: 1500, skewX: -10 }, 0);
      function wipe(at, dur = 0.55) {
        tl.fromTo('#wipe', { x: 1500, skewX: -10 }, { x: -1900, skewX: -10, duration: dur, ease: 'power3.inOut', immediateRender: false }, at);
      }
"""
JS_TAIL = r"""
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

B = 60 / 92

# --------------------------------------------------------------------------- ad 1
AD1_BODY = r"""
      <section id="hook" class="clip" data-start="0" data-duration="2.15" data-track-index="1">
        <div id="hookCam" class="clip">
          <div class="notifs" id="notifs" data-layout-allow-overlap>
            <div class="notif"><i></i><b>Missed call</b><span>9:02</span></div>
            <div class="notif"><i></i><b>Missed call</b><span>11:57</span></div>
            <div class="notif"><i></i><b>Missed call</b><span>2:31</span></div>
          </div>
          <div class="count" id="count">0</div>
          <div class="count-label label" id="countLabel">Missed calls today</div>
          <div class="hook-line" id="hookLine">17 patients, <span class="it">gone to the next clinic.</span></div>
        </div>
      </section>
      <section id="c1" class="clip" data-start="2.05" data-duration="3.2" data-track-index="2"><div class="cap"><span id="c1t">The fix: patients book <span class="it">in three taps.</span></span></div></section>
""" + PHONE.replace("[[CHAT]]", "") + END
AD1_JS = r"""
      // ---- hook: notifications buzz in, count to 17, slow push-in
      tl.fromTo('#hookCam', { scale: 1 }, { scale: 1.07, duration: 2.15, ease: 'none', transformOrigin: '30% 60%' }, 0);
      document.querySelectorAll('#notifs .notif').forEach((n, i) => {
        tl.fromTo(n, { y: -70, opacity: 0 }, { y: (2 - i) * 106, opacity: 1 - (2 - i) * 0.2, duration: 0.4, ease: 'back.out(1.8)' }, i * 0.42);
        tl.fromTo(n, { x: -7 }, { x: 7, duration: 0.04, repeat: 5, yoyo: true, ease: 'none', immediateRender: false }, i * 0.42);
      });
      const counter = { v: 0 };
      tl.fromTo(counter, { v: 0 }, { v: 17, duration: 1.3, ease: 'power2.out', onUpdate: () => { document.getElementById('count').textContent = Math.round(counter.v); } }, 0);
      tl.fromTo('#count', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 0);
      tl.fromTo('#countLabel', { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power3.out' }, 0.3);
      tl.fromTo('#hookLine', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' }, 0.85);

      // ---- the fix: phone in, zoom into the booking card for the taps, zoom back out
      wipe(1.85);
      tl.fromTo('#phone', { y: 1500 }, { y: 0, duration: 0.55, ease: 'expo.out' }, 2.05);
      tl.fromTo('#c1t', { y: 34, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' }, 2.15);
      tl.fromTo('#phone', { scale: 1, transformOrigin: '45% 40%' }, { scale: 1.4, duration: 0.6, ease: 'power3.inOut', immediateRender: false }, B * 3.4);
      tl.to('#phone', { scale: 1.05, duration: 0.6, ease: 'power3.inOut' }, B * 6.4);
      tl.to('#c1t', { opacity: 0, y: -16, duration: 0.25 }, 5.0);
      wipe(B * 8 - 0.3);

      const E = B * 8;
      tl.to('#phone', { opacity: 0, duration: 0.01 }, E);
""" + END_JS

# --------------------------------------------------------------------------- ad 2
AD2_BODY = r"""
      <section id="c1" class="clip" data-start="0" data-duration="4.65" data-track-index="2"><div class="cap"><span id="c1t">Book a dentist <span class="it">in three taps.</span></span></div></section>
      <section id="c2" class="clip" data-start="4.6" data-duration="1.3" data-track-index="2"><div class="cap"><span id="c2t">Straight into <span class="it">your WhatsApp.</span></span></div></section>
""" + PHONE.replace("[[CHAT]]", CHAT) + END
AD2_JS = r"""
      // ---- opens already zoomed into the booking card; taps on the beat
      tl.fromTo('#phone', { scale: 1.42, transformOrigin: '45% 40%' }, { scale: 1.38, duration: B * 3.6, ease: 'none' }, 0);
      tl.fromTo('#c1t', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, 0);
      tl.to('#phone', { scale: 1, duration: 0.7, ease: 'power3.inOut' }, B * 3.7);
      tl.to('#c1t', { opacity: 0, y: -16, duration: 0.25 }, 4.35);

      // ---- WhatsApp: chat slides up, push in on the new-booking notification
      tl.fromTo('#chat', { y: 1400, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, 4.62);
      tl.fromTo('#c2t', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, 4.65);
      tl.fromTo('#toast', { y: -160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.8)' }, B * 8);
      tl.fromTo('#phone', { scale: 1, transformOrigin: '50% 18%' }, { scale: 1.3, duration: 0.6, ease: 'power3.inOut', immediateRender: false }, B * 8);
      tl.to('#c2t', { opacity: 0, y: -16, duration: 0.2 }, B * 9 - 0.2);
      wipe(B * 9 - 0.3);

      const E = B * 9;
      tl.to('#phone', { opacity: 0, duration: 0.01 }, E);
"""+ END_JS

# --------------------------------------------------------------------------- ad 3
AD3_BODY = r"""
      <section id="offer" class="clip light" data-start="0" data-duration="4.6" data-track-index="1">
        <div id="offerCam" class="clip">
          <div class="p-label label" id="pLabel">Your clinic website · one price</div>
          <div class="price" id="price"><small>RM</small>6,800</div>
          <div class="p-rule" id="pRule"></div>
          <div class="p-line" id="pl1" style="top:[[line1]]px">No retainer.</div>
          <div class="p-line" id="pl2" style="top:[[line2]]px"><em>Yours</em> to keep.</div>
          <div class="p-line" id="pl3" style="top:[[line3]]px">Live in <em>3 weeks.</em></div>
        </div>
      </section>
      <section id="proof" class="clip" data-start="4.55" data-duration="1.4" data-track-index="2">
        <div class="proof-head" id="proofHead">Not our <span class="it">first build.</span></div>
        <div class="proof-sub" id="proofSub">Businesses in Johor Bahru already run on 4Skales websites.</div>
        <div class="case" id="caseCard"><span class="label">Live case study</span><b>See the results <em>on our page.</em></b>
          <div class="round-arrow"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#f4f3ef" stroke-width="1.8"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div></div>
      </section>
""" + END
AD3_JS = r"""
      // ---- the offer: price pulls back from a close-up, then three promises on the beat
      tl.fromTo('#price', { scale: 2.6, opacity: 0, transformOrigin: '35% 55%' }, { scale: 1, opacity: 1, duration: 1.1, ease: 'expo.out' }, 0);
      tl.fromTo('#offerCam', { scale: 1 }, { scale: 1.05, duration: 4.6, ease: 'none', transformOrigin: '30% 30%' }, 0);
      tl.fromTo('#pLabel', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.5);
      tl.fromTo('#pRule', { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: 'expo.out' }, 0.8);
      ['#pl1', '#pl2', '#pl3'].forEach((s, i) => tl.fromTo(s, { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, B * (4 + i)));
      tl.to('#hud', { opacity: 0, duration: 0.01 }, 0);
      tl.to('#hud', { opacity: 1, duration: 0.2 }, 4.55);

      // ---- proof
      wipe(B * 7 - 0.35);
      tl.fromTo('#proofHead', { y: 40, opacity: 0, scale: 1.08, transformOrigin: '0% 50%' }, { y: 0, opacity: 1, scale: 1, duration: 0.5, ease: 'expo.out' }, B * 7);
      tl.fromTo('#proofSub', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }, B * 7 + 0.2);
      tl.fromTo('#caseCard', { x: 1100, skewX: -10 }, { x: 0, skewX: 0, duration: 0.5, ease: 'expo.out' }, B * 7 + 0.35);
      wipe(B * 9 - 0.3);

      const E = B * 9;
""" + END_JS

ADS = {
    "ad1": dict(title="Missed calls", body=AD1_BODY, js=AD1_JS, vStart=2.05, vMedia=B * 3.5 - B * 4 + 2.05,
                vDur=3.2, endStart=B * 8, tag='Clinic websites that <span class="it">take bookings.</span>'),
    "ad2": dict(title="Three-tap booking", body=AD2_BODY, js=AD2_JS, vStart=0, vMedia=B * 3.5 - B * 1,
                vDur=B * 10.2 - (B * 3.5 - B * 1), endStart=B * 9,
                tag='RM 6,800. <span class="it">No retainer.</span>'),
    "ad3": dict(title="The offer", body=AD3_BODY, js=AD3_JS, vStart=0, vMedia=0, vDur=0, endStart=B * 9,
                tag='Clinic websites that <span class="it">take bookings.</span>'),
}


def build():
    for ad, a in ADS.items():
        for fmt, f in FORMATS.items():
            html = HEAD + a["body"] + '      <div class="wipe" id="wipe"></div>\n      <audio id="music" src="assets/music-' + ad + '.mp3" data-start="0" data-duration="7.5" data-volume="1" data-track-index="8"></audio>' + JS_HEAD + a["js"] + JS_TAIL
            vals = dict(f, TITLE=a["title"], TAG=a["tag"], vStart=round(a["vStart"], 4), vDur=round(a["vDur"], 4),
                        vMedia=round(a["vMedia"], 4), endStart=round(a["endStart"], 4), endDur=round(DUR - a["endStart"], 4),
                        phoneTw=f["phoneT"] - f["winT"], line1=f["line1"], line2=f["line1"] + f["lineGap"], line3=f["line1"] + 2 * f["lineGap"])
            for k, v in vals.items():
                html = html.replace(f"[[{k}]]", str(v))
            assert "[[" not in html, (ad, fmt, html[html.index("[["):html.index("[[") + 40])
            (ROOT / f"{ad}-{fmt}.html").write_text(html)
            if ad == "ad1" and fmt == "916":
                (ROOT / "index.html").write_text(html)  # default composition for Studio preview
            print("wrote", f"{ad}-{fmt}.html")


if __name__ == "__main__":
    build()
