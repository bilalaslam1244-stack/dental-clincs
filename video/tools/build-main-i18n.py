"""Bahasa Malaysia and Chinese versions of the main ad.

Run after tools/build-main.py. Reads main-916.html / main-45.html (English),
swaps every on-screen string, and writes main-916-ms.html, main-45-ms.html,
main-916-zh.html, main-45-zh.html. Fails loudly if any English string is
missing, so the translations can't silently drift from the English build.

Chinese uses Noto Serif SC / Noto Sans SC, downloaded from Google Fonts as
subsets containing only the characters in the video (small, crisp, offline).
The recorded demo site in step 2 and the deliberately dated old site stay in
English.
"""
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

# (English fragment as it appears in the built HTML, Bahasa Malaysia, Chinese)
T = [
    ('<html lang="en">', '<html lang="ms">', '<html lang="zh-Hans">'),
    ('<title>4Skales · Redesign + 2 free weeks</title>', '<title>4Skales · Reka semula + 2 minggu percuma</title>', '<title>4Skales · 网站改版 + 免费两周</title>'),
    ('hook-lead">Is your clinic</span>struggling to get <span class="it">dental bookings?</span>',
     'hook-lead">Adakah klinik anda</span>sukar mendapat <span class="it">tempahan pesakit?</span>',
     'hook-lead">你的牙科诊所</span>还在为<span class="it">预约太少</span>发愁？'),
    ('<b>This week</b>', '<b>Minggu ini</b>', '<b>本周预约</b>'),
    ('<div>MON</div>', '<div>ISN</div>', '<div>周一</div>'),
    ('<div>TUE</div>', '<div>SEL</div>', '<div>周二</div>'),
    ('<div>WED</div>', '<div>RAB</div>', '<div>周三</div>'),
    ('<div>THU</div>', '<div>KHA</div>', '<div>周四</div>'),
    ('<div>FRI</div>', '<div>JUM</div>', '<div>周五</div>'),
    ('<div>SAT</div>', '<div>SAB</div>', '<div>周六</div>'),
    ('slot-booked">Scaling<', 'slot-booked">Cuci gigi<', 'slot-booked">洗牙<'),
    ('slot-booked">Filling<', 'slot-booked">Tampalan<', 'slot-booked">补牙<'),
    ('2 of 30 slots filled', 'Hanya 2 daripada 30 slot terisi', '30 个时段，只约满 2 个'),
    ('id="stamp" data-layout-allow-overlap>Call only<', 'id="stamp" data-layout-allow-overlap>Telefon sahaja<', 'id="stamp" data-layout-allow-overlap>只限电话<'),
    ('id="baBefore">BEFORE<', 'id="baBefore">SEBELUM<', 'id="baBefore">改版前<'),
    ("Your website isn't <span class=\"it\">bringing in leads.</span>",
     'Laman web anda <span class="it">tidak menarik pesakit.</span>',
     '你的网站<span class="it">带不来新病人。</span>'),
    ("Here's how we fix it. <span class=\"it\">Three steps.</span>",
     'Ini cara kami atasinya. <span class="it">Tiga langkah.</span>',
     '我们这样解决：<span class="it">三个步骤。</span>'),
    ('<b>Step 1</b> of 3', '<b>Langkah 1</b> daripada 3', '<b>第 1 步</b> · 共 3 步'),
    ('<b>Step 2</b> of 3', '<b>Langkah 2</b> daripada 3', '<b>第 2 步</b> · 共 3 步'),
    ('<b>Step 3</b> of 3', '<b>Langkah 3</b> daripada 3', '<b>第 3 步</b> · 共 3 步'),
    ('<span class="t">We run ads to patients <span class="it">near your clinic.</span></span>',
     '<span class="t">Kami siarkan iklan kepada pesakit <span class="it">berhampiran klinik anda.</span></span>',
     '<span class="t">我们投放广告，<span class="it" style="display:block">触达诊所附近的病人。</span></span>'),
    ('<span class="t">They book on your new site <span class="it">in three taps.</span></span>',
     '<span class="t">Mereka tempah di laman web baharu <span class="it">dengan tiga ketikan.</span></span>',
     '<span class="t">他们在你的新网站上，<span class="it" style="display:block">点三下就能预约。</span></span>'),
    ('<span class="t">The booking lands in <span class="it">your WhatsApp.</span></span>',
     '<span class="t">Tempahan terus masuk ke <span class="it">WhatsApp anda.</span></span>',
     '<span class="t">预约直接发到<span class="it" style="display:block">你的 WhatsApp。</span></span>'),
    # Instagram-style feed
    ('<b>Home</b>', '<b>Utama</b>', '<b>首页</b>'),
    ('<span>Sponsored</span>', '<span>Ditaja</span>', '<span>赞助内容</span>'),
    ('class="big" data-layout-allow-overlap>Check-up &amp; scaling, <em>booked in three taps.</em>',
     'class="big" data-layout-allow-overlap>Pemeriksaan &amp; cuci gigi, <em data-layout-allow-overlap>tempah dalam tiga ketikan.</em>',
     'class="big" data-layout-allow-overlap>检查与洗牙，<em data-layout-allow-overlap style="display:block">点三下就能预约。</em>'),
    ('<b>OPEN WEEKENDS</b>Reserve on WhatsApp', '<b>BUKA HUJUNG MINGGU</b>Tempah melalui WhatsApp', '<b>周末照常营业</b>WhatsApp 预约'),
    ('<span>Book now</span>', '<span>Tempah sekarang</span>', '<span>立即预约</span>'),
    ('<b>lumendental.jb</b> Unhurried dental care in Mount Austin. Pick a treatment and a time, and it goes straight to our WhatsApp. <span>more</span>',
     '<b>lumendental.jb</b> Rawatan pergigian yang tenang di Mount Austin. Pilih rawatan dan masa, terus ke WhatsApp kami. <span>lagi</span>',
     '<b>lumendental.jb</b> Mount Austin 的从容牙科护理。选好项目和时间，直接发到我们的 WhatsApp。<span>更多</span>'),
    # WhatsApp
    ('<span>online</span>', '<span>dalam talian</span>', '<span>在线</span>'),
    ("class=\"bub out\">Hi Lumen Dental, I'm Mei Ling. I'd like to reserve: Check-up &amp; scaling. Preferred: Saturday, morning.",
     'class="bub out">Hai Lumen Dental, saya Mei Ling. Saya nak tempah: Pemeriksaan &amp; cuci gigi. Masa pilihan: Sabtu, pagi.',
     'class="bub out">你好 Lumen Dental，我是 Mei Ling。我想预约：检查与洗牙。希望时间：星期六上午。'),
    ('id="bubIn">Hello Mei Ling, Saturday at 10:00am is available. Shall we confirm?',
     'id="bubIn">Hai Mei Ling, Sabtu jam 10:00 pagi masih kosong. Boleh kami sahkan?',
     'id="bubIn">你好 Mei Ling，星期六上午 10 点有空位。要帮你确认吗？'),
    ('<b>New booking · Mei Ling</b><span>Check-up &amp; scaling · Sat morning</span>',
     '<b>Tempahan baharu · Mei Ling</b><span>Cuci gigi · Sabtu pagi</span>',
     '<b>新预约 · Mei Ling</b><span>检查与洗牙 · 星期六上午</span>'),
    # offer
    ('id="oLabel">Try it<', 'id="oLabel">Cuba dulu<', 'id="oLabel">先试试<'),
    ('id="oHead">2 weeks of leads.<', 'id="oHead">2 minggu pesakit baharu.<', 'id="oHead">两周的新病人询问。<'),
    ('id="free">Free.<', 'id="free">Percuma.<', 'id="free">免费。<'),
    (re.compile(r'(id="ol1" style="top:\d+px">)Like the results\? <em>Keep going.</em>'),
     r'\1Suka hasilnya? <em>Teruskan.</em>', r'\1效果满意？<em>继续合作。</em>'),
    (re.compile(r'(id="ol2" style="top:\d+px">)Not for you\? <em>Walk away.</em>'),
     r'\1Tak sesuai? <em>Berhenti sahaja.</em>', r'\1不适合？<em>随时退出。</em>'),
    # end card
    ('id="endTag">Redesigned to <span class="it">get you booked.</span>',
     'id="endTag">Direka semula untuk <span class="it">penuhkan tempahan.</span>',
     'id="endTag">重新设计，<span class="it" style="display:block">让预约满档。</span>'),
    ('<b>CLAIM 2 FREE WEEKS</b><span>Tap Send Message</span>',
     '<b>DAPATKAN 2 MINGGU PERCUMA</b><span>Tekan Hantar Mesej</span>',
     '<b>免费领取两周</b><span>点击“发送消息”</span>'),
    ('Johor Bahru · Kuala Lumpur', 'Johor Bahru · Kuala Lumpur', '新山 · 吉隆坡'),
]

# Per-language layout adjustments, appended to the page's styles.
CSS = {
    "ms": """
      .hook-cap { font-size: 100px; }
      .step-cap span.t { font-size: 64px; }
      .ig-img .big { font-size: 80px; }
      .o-head { font-size: 104px; }
      #free, #ol1, #ol2 { margin-top: 110px; }
      .o-line { font-size: 58px; }
      .end-tag { font-size: 80px; }
      .cta b { font-size: 30px; letter-spacing: .06em; }
""",
    "zh": """
      :root { --serif: 'Newsreader', 'Noto Serif SC', Georgia, serif; --sans: 'Jost', 'Noto Sans SC', sans-serif; }
      #feed { font-family: 'Jost', 'Noto Sans SC', sans-serif; }
      .it, em { font-style: normal; }
      .hook-cap { font-size: 96px; line-height: 1.15; white-space: nowrap; }
      .hook-lead { font-size: 60px; }
      .cap, .step-cap span.t { line-height: 1.2; }
      .label { letter-spacing: .2em; }
      .ig-img .big { font-size: 66px; line-height: 1.2; }
      .o-head { font-size: 96px; line-height: 1.1; white-space: nowrap; }
      .end-tag { line-height: 1.15; }
""",
}


def zh_fonts(text):
    """Download Noto Serif SC / Noto Sans SC subsets covering `text`; return @font-face CSS."""
    chars = "".join(sorted(set(c for c in text if ord(c) > 0x2E7F)))
    faces = []
    for fam, weights, stem in (("Noto Serif SC", (300, 500), "NotoSerifSC"), ("Noto Sans SC", (400, 500), "NotoSansSC")):
        for w in weights:
            q = urllib.parse.urlencode({"family": f"{fam}:wght@{w}", "text": chars})
            css = urllib.request.urlopen(urllib.request.Request(f"https://fonts.googleapis.com/css2?{q}", headers={"User-Agent": UA})).read().decode()
            url = re.search(r"url\((https://[^)]+)\)", css).group(1)
            out = FONTS / f"{stem}-{w}-subset.woff2"
            out.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read())
            faces.append(f"@font-face {{ font-family: '{fam}'; font-weight: {w}; font-style: normal; src: url('assets/fonts/{out.name}') format('woff2'); }}")
    return "\n      ".join(faces)


def translate(html, lang):
    i = {"ms": 1, "zh": 2}[lang]
    for row in T:
        src, dst = row[0], row[i]
        if isinstance(src, re.Pattern):
            html, n = src.subn(dst, html)
        else:
            n = html.count(src)
            html = html.replace(src, dst)
        assert n == 1, f"{lang}: expected exactly one match for {src!r}, found {n}"
    return html


def main():
    built = {fmt: (ROOT / f"main-{fmt}.html").read_text() for fmt in ("916", "45")}
    zh_text = "".join(translate(h, "zh") for h in built.values())
    faces = zh_fonts(zh_text)
    for lang in ("ms", "zh"):
        for fmt, html in built.items():
            out = translate(html, lang)
            extra = CSS[lang]
            if lang == "zh":
                extra = "\n      " + faces + "\n" + extra
            out = out.replace("    </style>", extra + "    </style>", 1)
            (ROOT / f"main-{fmt}-{lang}.html").write_text(out)
            print("wrote", f"main-{fmt}-{lang}.html")


if __name__ == "__main__":
    main()
