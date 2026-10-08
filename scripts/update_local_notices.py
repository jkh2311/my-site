#!/usr/bin/env python3
"""Validate and publish reviewed official notices from local-notices/source-notices.json.
No scraping or synthetic notices. Only direct https official government source URLs.
"""
import json,datetime,pathlib,urllib.parse
root=pathlib.Path(__file__).resolve().parents[1]/'local-notices'
source=root/'source-notices.json'; dest=root/'notices.json'
allowed={'지원금','무료 교육','주민 모집','생활 공지'}
if not source.exists():
    print('No reviewed source-notices.json; preserving current data'); raise SystemExit(0)
data=json.loads(source.read_text(encoding='utf-8'))
items=[]
for item in data.get('items',[]):
    if not all(isinstance(item.get(k),str) and item[k].strip() for k in ('title','province','category','agency','published','url')): continue
    u=urllib.parse.urlsplit(item['url']); host=(u.hostname or '').lower()
    if u.scheme!='https' or not (host=='go.kr' or host.endswith('.go.kr')) or item['category'] not in allowed: continue
    if not (len(item['published'])==10 and item['published'][4]=='-' and item['published'][7]=='-'):continue
    items.append({k:item.get(k,'') for k in ('title','province','district','category','agency','published','deadline','url')})
items=sorted(items,key=lambda x:x['published'],reverse=True)[:2000]
dest.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':items},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Published {len(items)} reviewed notices')
