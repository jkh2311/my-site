#!/usr/bin/env python3
import json, os, sys, urllib.parse, urllib.request, getpass
from pathlib import Path
BASE='https://api.odcloud.kr/api/gov24/v3'
OUT=Path(__file__).resolve().parent/'data'/'services.json'
COND_LABELS={'JA0101':'남성','JA0102':'여성','JA0301':'예비부모/난임','JA0302':'임산부','JA0303':'출산/입양','JA0313':'농업인','JA0314':'어업인','JA0315':'축산업인','JA0316':'임업인','JA0317':'초등학생','JA0318':'중학생','JA0319':'고등학생','JA0320':'대학생/대학원생','JA0326':'근로자/직장인','JA0327':'구직자/실업자','JA0328':'장애인','JA0329':'국가보훈대상자','JA0330':'질병/질환자','JA0401':'다문화가족','JA0402':'북한이탈주민','JA0403':'한부모가정/조손가정','JA0404':'1인가구','JA0411':'다자녀가구','JA0412':'무주택세대','JA0413':'신규전입','JA0414':'확대가족','JA1101':'예비창업자','JA1102':'영업중','JA1103':'생계곤란/폐업예정자','JA2101':'중소기업','JA2102':'사회복지시설','JA2103':'기관/단체'}
def fetch(ep,key):
    q=urllib.parse.urlencode({'page':1,'perPage':20000,'returnType':'JSON','serviceKey':key})
    req=urllib.request.Request(f'{BASE}/{ep}?{q}',headers={'User-Agent':'HanineSupportDataUpdater/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r:return json.load(r)
def main():
    key=os.getenv('GOV24_API_KEY') or getpass.getpass('공공데이터포털 일반 인증키 입력(화면에 표시되지 않음): ').strip()
    if not key:sys.exit('인증키가 없습니다.')
    listing=fetch('serviceList',key); cond=fetch('supportConditions',key)
    cmap={str(x.get('서비스ID','')):x for x in cond.get('data',[])}
    services=[]
    for x in listing.get('data',[]):
        sid=str(x.get('서비스ID','')); c=cmap.get(sid,{})
        labels=[label for code,label in COND_LABELS.items() if str(c.get(code,'')).strip() not in ('','0','N','n','false','False','None')]
        age1=c.get('JA0110'); age2=c.get('JA0111')
        if age1 is not None or age2 is not None: labels.append(f'연령 {age1 if age1 is not None else ""}~{age2 if age2 is not None else ""}세')
        services.append({'id':sid,'name':x.get('서비스명',''),'summary':x.get('서비스목적요약',''),'target':x.get('지원대상',''),'criteria':x.get('선정기준',''),'benefit':x.get('지원내용',''),'method':x.get('신청방법',''),'deadline':x.get('신청기한',''),'detailUrl':x.get('상세조회URL',''),'agency':x.get('소관기관명',''),'agencyType':x.get('소관기관유형',''),'userType':x.get('사용자구분',''),'field':x.get('서비스분야',''),'contact':x.get('전화문의',''),'registeredAt':x.get('등록일시',''),'updatedAt':x.get('수정일시',''),'conditions':labels})
    from datetime import datetime, timezone
    payload={'source':'행정안전부_대한민국 공공서비스(혜택) 정보','generatedAt':datetime.now(timezone.utc).isoformat(),'count':len(services),'services':services}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(f'완료: {len(services):,}개 → {OUT}')
if __name__=='__main__':main()
