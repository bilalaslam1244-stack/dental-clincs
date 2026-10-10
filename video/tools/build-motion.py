"""Short motion ads (7.5 s, 92 BPM) built from the static ads in statics/statics.html.

Each motion ad animates one static concept and lands on exactly the static's
layout, so the static PNG doubles as the video's poster frame.
  lock  : lock screen, WhatsApp enquiries drop in one by one
  week  : before week, then the after week fills slot by slot
  offer : 2 weeks free, line by line, then the CTA
Writes motion-<name>-<916|45>.html, plus -ms / -zh versions from
statics/statics-<ms|zh>.html (made by tools/build-statics-i18n.py) when they
exist. Music: tools/compose-music-motion.py.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMATS = {"916": 1920, "45": 1350}
LANGS = {"en": "statics.html", "ms": "statics-ms.html", "zh": "statics-zh.html"}


def section(src, cid):
    return re.search(rf'<section class="ad" id="{cid}">(.*?)</section>', src, re.S).group(1).replace("../assets/", "assets/")


COMMON_JS = r"""
      tl.fromTo(S + ' .gridbg', { y: 0 }, { y: -120, duration: DUR, ease: 'none' }, 0);
      tl.fromTo(S + ' .head', { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, 0);
      tl.fromTo(S + ' .eyebrow', { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' }, 0.1);
"""
HEADLINE_JS = r"""
      tl.fromTo(S + ' h1', { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.8, ease: 'expo.out' }, 0.18);
      tl.fromTo(S + ' h1 em', { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'power1.out' }, 0.62);
"""
DEAL_JS = r"""
      tl.fromTo(S + ' .deal', { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.65, ease: 'expo.out' }, DEAL);
      tl.fromTo(S + ' .deal .go', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5, ease: 'expo.out' }, DEAL + 0.3);
      tl.fromTo(S + ' .deal .go b', { x: 0 }, { x: 10, duration: B / 2, repeat: 7, yoyo: true, ease: 'sine.inOut' }, DEAL + 0.9);
"""

ADS = {
    "lock": dict(title="Wake up to bookings", deal=6, js=HEADLINE_JS + r"""
      tl.fromTo(S + ' .lock', { opacity: 0, y: 140, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.9, ease: 'expo.out' }, 1.5 * B - 0.3);
      // newest on top: the bottom notification arrives first
      ['3', '2', '1'].forEach((n, i) => {
        tl.fromTo(S + ' .note:nth-of-type(' + (Number(n) + 2) + ')', { opacity: 0, y: -36, scale: 0.94 },
                  { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(1.7)' }, (3 + i) * B - 0.06);
      });
"""),
    "week": dict(title="Turn empty slots into booked ones", deal=6.5, js=HEADLINE_JS + r"""
      tl.fromTo(S + ' .book:nth-of-type(1)', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.7, ease: 'expo.out' }, 2 * B - 0.25);
      tl.fromTo(S + ' .book:nth-of-type(2)', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.7, ease: 'expo.out' }, 3 * B - 0.25);
      tl.fromTo(S + ' .book:nth-of-type(2) .k', { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(2)', stagger: 0.075 }, 3.5 * B);
      tl.fromTo(S + ' .book:nth-of-type(2) .book-head span', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 6 * B);
"""),
    "offer": dict(title="2 weeks of patient enquiries, free", deal=6, js=r"""
      tl.fromTo(S + ' .big', { opacity: 0, scale: 1.5, transformOrigin: '0% 60%' }, { opacity: 1, scale: 1, duration: 1.0, ease: 'expo.out' }, 0);
      tl.fromTo(S + ' .big small', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 0.75);
      tl.fromTo(S + ' .free', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 2 * B - 0.1);
      tl.fromTo(S + ' #yes', { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: 'expo.out' }, 3 * B);
      tl.fromTo(S + ' #no', { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: 'expo.out' }, 4 * B);
      tl.fromTo(S + ' #terms', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 5 * B);
      tl.fromTo(S + ' .cta', { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.6, ease: 'expo.out' }, 6 * B - 0.1);
      tl.fromTo(S + ' .cta b', { x: 0 }, { x: 10, duration: B / 2, repeat: 7, yoyo: true, ease: 'sine.inOut' }, 6 * B + 0.6);
"""),
    "calls": dict(title="Every missed call is a patient booking elsewhere", deal=6, js=HEADLINE_JS + r"""
      tl.fromTo(S + ' .recents', { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.7, ease: 'expo.out' }, 1.5 * B - 0.25);
      tl.fromTo(S + ' .call', { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.4, ease: 'expo.out', stagger: B }, 2 * B - 0.05);
      tl.fromTo(S + ' .recents .rh span', { opacity: 0, scale: 1.4, transformOrigin: '100% 50%' }, { opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)' }, 5.5 * B);
"""),
    "site": dict(title="Your website might be losing you patients", deal=6, js=HEADLINE_JS + r"""
      tl.fromTo(S + ' .browser', { opacity: 0, y: 80, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'expo.out' }, 1.5 * B - 0.3);
      ['#f1', '#f2', '#f3'].forEach((id, i) => {
        tl.fromTo(S + ' ' + id, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: 'back.out(2.2)' }, (3 + i) * B - 0.04);
      });
"""),
    "steps": dict(title="3 steps to a fuller appointment book", deal=6, js=HEADLINE_JS + r"""
      tl.fromTo(S + ' .step', { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.6, ease: 'expo.out', stagger: 1.25 * B }, 2 * B - 0.1);
      tl.fromTo(S + ' .step b', { scale: 0.6, transformOrigin: '0% 80%' }, { scale: 1, duration: 0.6, ease: 'back.out(2)', stagger: 1.25 * B }, 2 * B - 0.1);
"""),
    "claim": dict(title="Claim your 2 free weeks", deal=6, js=r"""
      tl.fromTo(S + ' .claim', { opacity: 0, scale: 1.35, transformOrigin: '0% 60%' }, { opacity: 1, scale: 1, duration: 1.0, ease: 'expo.out' }, 0.1);
      tl.fromTo(S + ' .free', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 1.5 * B - 0.1);
      tl.fromTo(S + ' .checks p', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: 'expo.out', stagger: B / 2 }, 2.5 * B - 0.05);
      tl.fromTo(S + ' .cta', { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.6, ease: 'expo.out' }, 5.5 * B - 0.1);
      tl.fromTo(S + ' .tapnote', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 6.2 * B);
      tl.fromTo(S + ' .cta b', { x: 0 }, { x: 10, duration: B / 2, repeat: 7, yoyo: true, ease: 'sine.inOut' }, 6 * B);
"""),
}


def build():
  for lang, name in LANGS.items():
    path = ROOT / "statics" / name
    if not path.exists():
        continue
    src = path.read_text()
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1).replace("../assets/", "assets/")
    html_lang = re.search(r'<html lang="([^"]+)"', src).group(1)
    suffix = "" if lang == "en" else f"-{lang}"
    for cid, a in ADS.items():
        for fmt, h in FORMATS.items():
            deal_js = DEAL_JS if 'class="deal"' in section(src, cid) else ""
            html = f"""<!doctype html>
<html lang="{html_lang}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height={h}" />
    <title>4Skales · {a['title']}</title>
    <script src="assets/gsap.min.js"></script>
    <style>{css}
  html, body {{ width: 1080px; height: {h}px; overflow: hidden; }}
  #root {{ position: relative; width: 1080px; height: {h}px; overflow: hidden; }}
  .clip {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body class="f{fmt}">
    <div id="root" data-composition-id="main" data-start="0" data-duration="7.5" data-width="1080" data-height="{h}">
      <section class="ad on clip" id="{cid}" data-start="0" data-duration="7.5" data-track-index="0">{section(src, cid)}</section>
      <audio id="music" src="assets/music-motion-{cid}.mp3" data-start="0" data-duration="7.5" data-volume="1" data-track-index="8"></audio>
    </div>
    <script>
      const B = 60 / 92, DUR = 7.5, S = '#{cid}', DEAL = {a['deal']} * B;
      const tl = gsap.timeline({{ paused: true }});
{COMMON_JS}{a['js']}{deal_js}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
            (ROOT / f"motion-{cid}-{fmt}{suffix}.html").write_text(html)
            print("wrote", f"motion-{cid}-{fmt}{suffix}.html")


if __name__ == "__main__":
    build()
