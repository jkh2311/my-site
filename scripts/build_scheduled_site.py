from pathlib import Path
from datetime import datetime, timezone
import shutil, json, re, csv, os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
SCHEDULE={
'/articles/energy-voucher-eligibility.html': datetime(2026,10,7,7,20,tzinfo=timezone.utc),
'/articles/childbirth-parenting-benefits.html': datetime(2026,10,7,11,20,tzinfo=timezone.utc),
'/articles/medical-expense-cap-refund.html': datetime(2026,10,7,15,20,tzinfo=timezone.utc),
'/articles/msafer-mobile-identity-theft-check.html': datetime(2026,10,7,19,20,tzinfo=timezone.utc),
}
# For deterministic local testing: RELEASE_NOW=2026-10-07T11:20:00+00:00
raw=os.environ.get('RELEASE_NOW')
NOW=datetime.fromisoformat(raw) if raw else datetime.now(timezone.utc)
if NOW.tzinfo is None: NOW=NOW.replace(tzinfo=timezone.utc)
NOW=NOW.astimezone(timezone.utc)
visible={u for u,t in SCHEDULE.items() if NOW>=t}
future=set(SCHEDULE)-visible

if OUT.exists(): shutil.rmtree(OUT)
ignore=shutil.ignore_patterns('.git','.github','_site','scripts','*.zip')
shutil.copytree(ROOT,OUT,ignore=ignore)
for url in future:
    p=OUT/url.lstrip('/')
    if p.exists(): p.unlink()

# Update article index and embedded JSON fallbacks.
idx=OUT/'article-index.json'
if idx.exists():
    data=json.loads(idx.read_text(encoding='utf-8'))
    data=[x for x in data if x.get('url') not in future]
    idx.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    filtered_json=json.dumps(data,ensure_ascii=False,separators=(',',':'))
else: filtered_json='[]'

# HTML: remove any anchor/card pointing to a future URL; replace embedded ARTICLE_INDEX.
for p in OUT.rglob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    if not any(u in txt for u in future) and 'let ARTICLE_INDEX =' not in txt:
        continue
    soup=BeautifulSoup(txt,'html.parser')
    changed=False
    for a in list(soup.find_all('a',href=True)):
        href=a.get('href','')
        if href in future or ('https://haninelife.com'+href) in future:
            # Cards/list links disappear; inline related links become plain text to avoid broken links.
            cls=' '.join(a.get('class',[]))
            if 'card' in cls or 'article-card' in cls or p.name in ('site-index.html',):
                a.decompose()
            else:
                a.replace_with(a.get_text(' ',strip=True))
            changed=True
    out=str(soup)
    out=re.sub(r'let ARTICLE_INDEX\s*=\s*\[.*?\];', 'let ARTICLE_INDEX = '+filtered_json+';', out, count=1, flags=re.S)
    p.write_text(out,encoding='utf-8')

# Sitemap: remove future URLs.
sp=OUT/'sitemap.xml'
if sp.exists():
    tree=ET.parse(sp); root=tree.getroot(); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    for node in list(root):
        loc=node.find(ns+'loc')
        if loc is not None and loc.text:
            path=loc.text.replace('https://haninelife.com','')
            if path in future: root.remove(node)
    tree.write(sp,encoding='utf-8',xml_declaration=True)

# RSS: remove future items and use exact release timestamps for visible scheduled posts.
rp=OUT/'rss.xml'
if rp.exists():
    tree=ET.parse(rp); root=tree.getroot(); channel=root.find('channel')
    from email.utils import format_datetime
    for item in list(channel.findall('item')):
        link=item.findtext('link','').replace('https://haninelife.com','')
        if link in future:
            channel.remove(item)
        elif link in SCHEDULE:
            pd=item.find('pubDate')
            if pd is not None: pd.text=format_datetime(SCHEDULE[link])
    lb=channel.find('lastBuildDate')
    if lb is not None: lb.text=format_datetime(NOW)
    tree.write(rp,encoding='utf-8',xml_declaration=True)

# Naver submit list CSV: drop future article URLs.
cp=OUT/'naver-submit-list.csv'
if cp.exists():
    rows=list(csv.reader(cp.open(encoding='utf-8-sig',newline='')))
    kept=[]
    for row in rows:
        joined=' '.join(row)
        if any(('https://haninelife.com'+u) in joined or u in joined for u in future): continue
        kept.append(row)
    with cp.open('w',encoding='utf-8-sig',newline='') as f: csv.writer(f).writerows(kept)

# Remove internal audit/source-only files from public artifact.
for p in list(OUT.iterdir()):
    if p.is_file() and (p.name.startswith('V') and p.suffix.lower() in {'.txt','.csv','.json'}):
        p.unlink()

print('Build time UTC:',NOW.isoformat())
print('Published scheduled URLs:',sorted(visible))
print('Held scheduled URLs:',sorted(future))
