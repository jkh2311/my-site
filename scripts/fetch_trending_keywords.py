"""Build a sourced Korean trending-search list for the static Pages artifact."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
import xml.etree.ElementTree as ET
import json

OUTPUT = Path(__file__).resolve().parents[1] / "_site" / "trending-keywords.json"
FEED = "https://trends.google.com/trending/rss?geo=KR"
payload = {"source": "Google Trends", "sourceUrl": "https://trends.google.com/trending?geo=KR", "updatedAt": None, "items": []}
try:
    req = Request(FEED, headers={"User-Agent": "Mozilla/5.0 (compatible; HanineLife/1.0)"})
    with urlopen(req, timeout=18) as res:
        root = ET.fromstring(res.read())
    ns = {"ht": "https://trends.google.com/trending/rss"}
    seen = set()
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        if not title or title.casefold() in seen:
            continue
        seen.add(title.casefold())
        traffic = item.findtext("ht:approx_traffic", default="", namespaces=ns)
        payload["items"].append({"keyword": title, "traffic": traffic, "url": "https://www.google.com/search?q=" + quote(title)})
        if len(payload["items"]) == 10:
            break
    if payload["items"]:
        payload["updatedAt"] = datetime.now(timezone.utc).isoformat()
except Exception as exc:
    print("Trending feed unavailable; no unsourced keywords will be shown:", exc)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("Trending keywords:", len(payload["items"]))
