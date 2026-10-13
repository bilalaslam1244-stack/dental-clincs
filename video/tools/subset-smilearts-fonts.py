"""Downloads Noto Sans SC (500, 700) and Noto Serif SC (700) subsets from Google Fonts covering exactly the
Chinese characters in smilearts/kd-ads.html. Run after changing any Chinese copy there.
Writes assets/fonts/<Family>-<weight>-smilearts-subset.woff2.
"""
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

html = (ROOT / "smilearts" / "kd-ads.html").read_text(encoding="utf-8")
zh = html[html.index("  zh: {"):html.index("const u = q.get('u')")]
chars = "".join(sorted(set(ch for ch in re.sub(r"<[^>]+>", "", zh) if ord(ch) > 0x2E80)))
print(len(chars), "characters")
for family, stem, weight in [("Noto Sans SC", "NotoSansSC", 500), ("Noto Sans SC", "NotoSansSC", 700), ("Noto Serif SC", "NotoSerifSC", 700)]:
    q = urllib.parse.urlencode({"family": f"{family}:wght@{weight}", "text": chars})
    css = urllib.request.urlopen(urllib.request.Request(f"https://fonts.googleapis.com/css2?{q}", headers={"User-Agent": UA})).read().decode()
    data = urllib.request.urlopen(re.search(r"url\((\S+?)\)", css).group(1)).read()
    out = ROOT / "assets" / "fonts" / f"{stem}-{weight}-smilearts-subset.woff2"
    out.write_bytes(data)
    print("wrote", out.name, len(data))
