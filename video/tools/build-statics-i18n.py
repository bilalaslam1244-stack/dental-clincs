"""Bahasa Malaysia and Chinese versions of the static ads.

Reads statics/statics.html (English), swaps every on-screen string, and writes
statics/statics-ms.html and statics/statics-zh.html. Fails loudly when an
English string is missing, so translations can't drift from the English build.
tools/build-motion.py then builds the -ms / -zh motion ads from these files.

Chinese uses Noto Serif SC / Noto Sans SC subsets downloaded from Google Fonts
for exactly the characters used (saved as *-statics-subset.woff2, separate
from the main ad's subsets).
"""
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

# (English, Bahasa Malaysia, Chinese). Each English string must appear at least once; all copies are replaced.
T = [
    ('<html lang="en">', '<html lang="ms">', '<html lang="zh-Hans">'),
    ("<title>4Skales static ads</title>", "<title>4Skales iklan statik</title>", "<title>4Skales 静态广告</title>"),
    ('<div class="eyebrow">For dental clinic owners</div>', '<div class="eyebrow">Untuk pemilik klinik pergigian</div>', '<div class="eyebrow">专为牙科诊所老板</div>'),
    # hook
    ('<h1><span class="lead">Is your clinic</span>struggling to get <em>dental bookings?</em></h1>',
     '<h1><span class="lead">Klinik pergigian anda</span>susah dapat <em>tempahan pesakit?</em></h1>',
     '<h1><span class="lead">你的牙科诊所</span>预约<em>总是不够？</em></h1>'),
    ("<b>This week</b>", "<b>Minggu ini</b>", "<b>本周</b>"),
    ("<span>1 booking</span>", "<span>1 tempahan</span>", "<span>仅 1 个预约</span>"),
    ('<div class="k">Scaling</div>', '<div class="k">Cuci gigi</div>', '<div class="k">洗牙</div>'),
    ('<div class="d">MON</div><div class="d">TUE</div><div class="d">WED</div><div class="d">THU</div><div class="d">FRI</div><div class="d">SAT</div>',
     '<div class="d">ISN</div><div class="d">SEL</div><div class="d">RAB</div><div class="d">KHA</div><div class="d">JUM</div><div class="d">SAB</div>',
     '<div class="d">周一</div><div class="d">周二</div><div class="d">周三</div><div class="d">周四</div><div class="d">周五</div><div class="d">周六</div>'),
    ("<div>9AM</div>", "<div>9:00</div>", "<div>9:00</div>"),
    ("<div>10AM</div>", "<div>10:00</div>", "<div>10:00</div>"),
    ("<div>11AM</div>", "<div>11:00</div>", "<div>11:00</div>"),
    ("<div>2PM</div>", "<div>14:00</div>", "<div>14:00</div>"),
    ("<div>4PM</div>", "<div>16:00</div>", "<div>16:00</div>"),
    # week
    ("<h1>Turn empty slots into <em>booked ones.</em></h1>", "<h1>Penuhkan slot kosong dengan <em>tempahan.</em></h1>", "<h1>把空档变成<em>满档。</em></h1>"),
    ('<div class="tag before">BEFORE</div>', '<div class="tag before">SEBELUM</div>', '<div class="tag before">之前</div>'),
    ('<div class="tag after">AFTER</div>', '<div class="tag after">SELEPAS</div>', '<div class="tag after">之后</div>'),
    ("<span>2 bookings</span>", "<span>2 tempahan</span>", "<span>2 个预约</span>"),
    ("<span>Fully booked</span>", "<span>Penuh ditempah</span>", "<span>全部约满</span>"),
    # lock
    ("<h1>Wake up to <em>bookings.</em></h1>", "<h1>Bangun pagi, <em>tempahan dah masuk.</em></h1>", "<h1>一觉醒来，<em>预约已到。</em></h1>"),
    ('<div class="date">Saturday, 11 October</div>', '<div class="date">Sabtu, 11 Oktober</div>', '<div class="date">10月11日 星期六</div>'),
    ("<span>now</span>", "<span>kini</span>", "<span>现在</span>"),
    ("<span>6m</span>", "<span>6 min</span>", "<span>6分钟前</span>"),
    ("<span>14m</span>", "<span>14 min</span>", "<span>14分钟前</span>"),
    ("<p>Hi! I'd like to book a <b>braces consultation</b>, Saturday morning.</p>",
     "<p>Hi! Saya nak tempah <b>konsultasi braces</b>, Sabtu pagi.</p>",
     "<p>你好！我想预约<b>牙套咨询</b>，星期六早上。</p>"),
    ("<p><b>Scaling &amp; polish</b> tomorrow evening, any slots?</p>",
     "<p><b>Cuci &amp; gilap gigi</b> esok petang, ada slot?</p>",
     "<p>明天傍晚可以<b>洗牙</b>吗？还有位吗？</p>"),
    ("<p>Can I come in for an <b>implant consult</b> this week?</p>",
     "<p>Boleh saya datang untuk <b>konsultasi implan</b> minggu ini?</p>",
     "<p>这周可以来做<b>种植牙咨询</b>吗？</p>"),
    # offer band + CTA
    ("<h3>2 weeks of patient enquiries, <em>free.</em></h3>", "<h3>2 minggu pertanyaan pesakit, <em>percuma.</em></h3>", "<h3>两周病人咨询，<em>完全免费。</em></h3>"),
    ("<p>We even pay the ad spend. No card, no contract.</p>", "<p>Kos iklan pun kami tanggung. Tiada kad, tiada kontrak.</p>", "<p>连广告费都由我们承担。不用信用卡，不签合约。</p>"),
    ("Claim 2 free weeks on WhatsApp <b>→</b>", "Tuntut 2 minggu percuma di WhatsApp <b>→</b>", "WhatsApp 领取两周免费 <b>→</b>"),
    # offer
    ('<div class="big">2 weeks<small>of patient enquiries.</small></div>', '<div class="big">2 minggu<small>pertanyaan pesakit.</small></div>', '<div class="big">两周<small>病人咨询。</small></div>'),
    ('<div class="free">Free.<br>We even pay the ad spend.</div>', '<div class="free">Percuma.<br>Kos iklan pun kami tanggung.</div>', '<div class="free">免费。<br>广告费也由我们出。</div>'),
    ('<p id="yes"><b>Like the results?</b> Keep going.</p>', '<p id="yes"><b>Suka hasilnya?</b> Teruskan.</p>', '<p id="yes"><b>满意效果？</b>继续合作。</p>'),
    ('<p id="no"><b>Not for you?</b> Walk away.</p>', '<p id="no"><b>Tak sesuai?</b> Berhenti saja.</p>', '<p id="no"><b>不适合？</b>随时停止。</p>'),
    ("<p><b>No card. No contract.</b> Just message us.</p>", "<p><b>Tiada kad. Tiada kontrak.</b> WhatsApp sahaja.</p>", "<p><b>不用信用卡，不签合约。</b>直接 WhatsApp 我们。</p>"),
]

LANG_CSS = {
    "ms": """
  /* Bahasa Malaysia runs longer: slightly smaller display type */
  h1 { font-size: 90px; }
  .f45 h1 { font-size: 80px; }
  h1 .lead { font-size: 58px; }
  .f45 h1 .lead { font-size: 50px; }
  .big { font-size: 210px; }
  .f45 .big { font-size: 186px; }
  .deal h3 { font-size: 42px; }
  .f45 .deal h3 { font-size: 36px; }
  .deal .go { font-size: 22px; letter-spacing: .12em; }
  .f45 .deal .go { font-size: 19px; }
  .go-big { font-size: 24px; letter-spacing: .14em; padding: 28px 36px; }
  .free { font-size: 74px; }
  .f45 .free { font-size: 64px; }
  .f45 .go-big { font-size: 22px; }
""",
    "zh": """
  /* Chinese: Noto Serif SC / Noto Sans SC behind the Latin faces, upright accents, tighter tracking */
  [[FACES]]
  :root { --serif: Newsreader, 'Noto Serif SC', serif; --sans: Jost, 'Noto Sans SC', sans-serif; }
  em { font-style: normal; }
  h1 { font-weight: 300; letter-spacing: 0; line-height: 1.12; font-size: 88px; }
  .f45 h1 { font-size: 80px; }
  .eyebrow { letter-spacing: .24em; }
  .free { font-style: normal; }
  .big { letter-spacing: -.02em; }
  .deal .go, .cta { letter-spacing: .1em; }
  .tag { letter-spacing: .2em; }
""",
}


def zh_fonts(text):
    """Download Noto Serif SC / Noto Sans SC subsets covering `text`; return @font-face CSS."""
    chars = "".join(sorted(set(c for c in text if ord(c) > 0x2E7F)))
    faces = []
    for fam, weights, stem in (("Noto Serif SC", (300,), "NotoSerifSC"), ("Noto Sans SC", (400, 500), "NotoSansSC")):
        for w in weights:
            q = urllib.parse.urlencode({"family": f"{fam}:wght@{w}", "text": chars})
            css = urllib.request.urlopen(urllib.request.Request(f"https://fonts.googleapis.com/css2?{q}", headers={"User-Agent": UA})).read().decode()
            url = re.search(r"url\((https://[^)]+)\)", css).group(1)
            out = FONTS / f"{stem}-{w}-statics-subset.woff2"
            out.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read())
            faces.append(f"@font-face {{ font-family: '{fam}'; font-weight: {w}; src: url(../assets/fonts/{out.name}); }}")
    return "\n  ".join(faces)


def translate(html, lang):
    i = {"ms": 1, "zh": 2}[lang]
    for row in T:
        assert row[0] in html, f"missing English string: {row[0][:70]}"
        html = html.replace(row[0], row[i])
    return html


def main():
    src = (ROOT / "statics" / "statics.html").read_text()
    for lang in ("ms", "zh"):
        html = translate(src, lang)
        css = LANG_CSS[lang]
        if lang == "zh":
            css = css.replace("[[FACES]]", zh_fonts(html))
        html = html.replace("</style>", css + "</style>", 1)
        out = ROOT / "statics" / f"statics-{lang}.html"
        out.write_text(html)
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
