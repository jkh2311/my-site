#!/usr/bin/env python3
import json, os, sys, urllib.parse, urllib.request, getpass, time
from pathlib import Path
from datetime import datetime, timezone

BASE='https://api.odcloud.kr/api/gov24/v3'
OUT=Path(__file__).resolve().parent/'data'/'services.json'
PAGE_SIZE=1000
TIMEOUT=90

COND_LABELS={
 'JA0101':'남성','JA0102':'여성',
 'JA0201':'중위소득 0~50%','JA0202':'중위소득 51~75%','JA0203':'중위소득 76~100%','JA0204':'중위소득 101~200%','JA0205':'중위소득 200% 초과',
 'JA0301':'예비부모/난임','JA0302':'임산부','JA0303':'출산/입양','JA0313':'농업인','JA0314':'어업인','JA0315':'축산업인','JA0316':'임업인',
 'JA0317':'초등학생','JA0318':'중학생','JA0319':'고등학생','JA0320':'대학생/대학원생','JA0326':'근로자/직장인','JA0327':'구직자/실업자',
 'JA0328':'장애인','JA0329':'국가보훈대상자','JA0330':'질병/질환자',
 'JA0401':'다문화가족','JA0402':'북한이탈주민','JA0403':'한부모가정/조손가정','JA0404':'1인가구','JA0411':'다자녀가구','JA0412':'무주택세대','JA0413':'신규전입','JA0414':'확대가족',
 'JA1101':'예비창업자','JA1102':'영업중','JA1103':'생계곤란/폐업예정자','JA1201':'음식점업','JA1202':'제조업','JA1299':'기타업종',
 'JA2101':'중소기업','JA2102':'사회복지시설','JA2103':'기관/단체','JA2201':'제조업','JA2202':'농업·임업·어업','JA2203':'정보통신업','JA2299':'기타업종'
}

def truthy(v):
    return str(v).strip() not in ('','0','N','n','false','False','None','null')

def request_json(ep,key,page,per_page=PAGE_SIZE,retries=4):
    params={'page':page,'perPage':per_page,'returnType':'JSON','serviceKey':key}
    url=f"{BASE}/{ep}?{urllib.parse.urlencode(params)}"
    last=None
    for attempt in range(retries):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'HanineSupportDataUpdater/1.1'})
            with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
                return json.load(r)
        except Exception as e:
            last=e
            if attempt+1<retries:
                time.sleep(2*(attempt+1))
    raise RuntimeError(f'{ep} page {page} 요청 실패: {last}')

def fetch_all(ep,key):
    first=request_json(ep,key,1)
    total=int(first.get('matchCount') or first.get('totalCount') or len(first.get('data',[])))
    rows=list(first.get('data',[]))
    pages=max(1,(total+PAGE_SIZE-1)//PAGE_SIZE)
    print(f'  {ep}: 총 {total:,}건 / {pages}페이지')
    for page in range(2,pages+1):
        data=request_json(ep,key,page)
        rows.extend(data.get('data',[]))
        print(f'    {page}/{pages} 페이지 완료 ({len(rows):,}건)', flush=True)
        time.sleep(0.15)
    # 서비스ID 기준 중복 제거
    out={}
    for row in rows:
        sid=str(row.get('서비스ID','')).strip()
        if sid: out[sid]=row
    return out, total

def clean(v):
    if v is None: return ''
    if isinstance(v,(int,float)): return v
    return str(v).replace('\r\n','\n').replace('\r','\n').strip()

def main():
    key=os.getenv('GOV24_API_KEY') or getpass.getpass('공공데이터포털 일반 인증키 입력(화면에 표시되지 않음): ').strip()
    if not key: sys.exit('인증키가 없습니다.')
    print('정부24 공공서비스 데이터 동기화를 시작합니다.')
    listing, list_total=fetch_all('serviceList',key)
    details, detail_total=fetch_all('serviceDetail',key)
    conds, cond_total=fetch_all('supportConditions',key)

    services=[]
    max_updated=''
    for sid,x in listing.items():
        d=details.get(sid,{})
        c=conds.get(sid,{})
        labels=[label for code,label in COND_LABELS.items() if truthy(c.get(code,''))]
        age1=c.get('JA0110'); age2=c.get('JA0111')
        age1=None if age1 in ('',None) else age1
        age2=None if age2 in ('',None) else age2
        if age1 is not None or age2 is not None:
            labels.append(f'연령 {age1 if age1 is not None else ""}~{age2 if age2 is not None else ""}세')
        updated=clean(x.get('수정일시') or d.get('수정일시'))
        if updated>max_updated: max_updated=updated
        services.append({
            'id':sid,
            'name':clean(x.get('서비스명') or d.get('서비스명')),
            'summary':clean(x.get('서비스목적요약') or d.get('서비스목적')),
            'target':clean(x.get('지원대상') or d.get('지원대상')),
            'criteria':clean(x.get('선정기준') or d.get('선정기준')),
            'benefit':clean(x.get('지원내용') or d.get('지원내용')),
            'method':clean(x.get('신청방법') or d.get('신청방법')),
            'deadline':clean(x.get('신청기한') or d.get('신청기한')),
            'detailUrl':clean(x.get('상세조회URL')),
            'applyUrl':clean(d.get('온라인신청사이트URL')),
            'documents':clean(d.get('구비서류')),
            'agency':clean(x.get('소관기관명') or d.get('소관기관명')),
            'agencyType':clean(x.get('소관기관유형')),
            'userType':clean(x.get('사용자구분')),
            'field':clean(x.get('서비스분야')),
            'contact':clean(x.get('전화문의') or d.get('문의처')),
            'registeredAt':clean(x.get('등록일시')),
            'updatedAt':updated,
            'conditions':labels,
            'ageMin':age1,
            'ageMax':age2
        })

    services.sort(key=lambda z: (z.get('updatedAt',''), z.get('name','')), reverse=True)
    payload={
        'source':'행정안전부_대한민국 공공서비스(혜택) 정보',
        'sourcePage':'https://www.data.go.kr/data/15113968/openapi.do',
        'generatedAt':datetime.now(timezone.utc).isoformat(),
        'sourceUpdatedMax':max_updated,
        'count':len(services),
        'apiCounts':{'serviceList':list_total,'serviceDetail':detail_total,'supportConditions':cond_total},
        'services':services
    }
    if len(services)<1000:
        sys.exit(f'검증 실패: 서비스가 {len(services):,}건뿐이라 기존 파일을 교체하지 않습니다.')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    tmp=OUT.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    tmp.replace(OUT)
    mb=OUT.stat().st_size/1024/1024
    print(f'완료: {len(services):,}개 → {OUT} ({mb:.1f} MB)')
    print(f'원천 데이터 최신 수정일시(최대값): {max_updated or "확인 불가"}')

if __name__=='__main__':
    main()
