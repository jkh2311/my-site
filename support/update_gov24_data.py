#!/usr/bin/env python3
import json, os, sys, urllib.parse, urllib.request, urllib.error, time, subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE='https://api.odcloud.kr/api/gov24/v3'
AUTH_MODE=None
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

def _read_http_error(e):
    try:
        body=e.read().decode('utf-8','replace').strip()
    except Exception:
        body=''
    return body[:1200]

def _build_url(ep,key,page,per_page):
    # Swagger에서 실제 성공한 요청과 동일하게 serviceKey를 query에 직접 붙인다.
    # 인증키는 이미 포털이 발급한 문자열이므로 별도 Authorization 헤더를 사용하지 않는다.
    safe_key=key.strip().strip('\"').strip("'")
    if not safe_key:
        raise RuntimeError('인증키가 비어 있습니다.')
    params=f"page={int(page)}&perPage={int(per_page)}&serviceKey={safe_key}"
    return f"{BASE}/{ep}?{params}"

def request_json(ep,key,page,per_page=PAGE_SIZE,retries=3):
    url=_build_url(ep,key,page,per_page)
    headers={'User-Agent':'HanineSupportDataUpdater/1.3','Accept':'application/json'}
    last=None
    for attempt in range(retries):
        try:
            req=urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last=e
            body=_read_http_error(e)
            if e.code in (401,403):
                raise RuntimeError(
                    f'{ep} page {page} 인증 실패: HTTP {e.code} {body}\n'
                    'Swagger에서 성공한 것과 동일하게 serviceKey query 방식으로 요청했습니다. '
                    '인증키를 다시 복사해 입력해 주세요.'
                )
            if attempt+1<retries:
                time.sleep(2*(attempt+1))
        except Exception as e:
            last=e
            if attempt+1<retries:
                time.sleep(2*(attempt+1))
    raise RuntimeError(f'{ep} page {page} 요청 실패: {last}')

def verify_key(key):
    print('인증키를 Swagger와 동일한 serviceKey query 방식으로 확인합니다...')
    data=request_json('serviceList',key,1,10,retries=1)
    rows=data.get('data',[])
    total=int(data.get('matchCount') or data.get('totalCount') or len(rows))
    print(f'  인증 성공: HTTP 200 / 공공서비스 총 {total:,}건')
    return total

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

def sanitize_key(value):
    # Windows의 숨김 입력(getpass)에서 Ctrl+V가 실제 붙여넣기 대신
    # 제어문자(\x16)로 들어오는 문제를 피하고, 복사 과정의 줄바꿈/공백도 제거한다.
    value = '' if value is None else str(value)
    value = ''.join(ch for ch in value if ch.isprintable())
    return value.strip().strip('\"').strip("'")

def read_clipboard_windows():
    if os.name != 'nt':
        return ''
    try:
        r=subprocess.run(
            ['powershell','-NoProfile','-Command','Get-Clipboard -Raw'],
            capture_output=True,text=True,timeout=10
        )
        if r.returncode==0:
            return sanitize_key(r.stdout)
    except Exception:
        pass
    return ''

def get_api_key():
    env_key=sanitize_key(os.getenv('GOV24_API_KEY',''))
    if env_key:
        print('환경변수 GOV24_API_KEY에서 인증키를 읽었습니다.')
        return env_key

    if os.name=='nt':
        print('공공데이터포털 일반 인증키를 먼저 복사(Ctrl+C)해 두세요.')
        print('※ 이 창에서는 Ctrl+V를 누르지 마세요. 이전 오류의 \x16은 Ctrl+V 제어문자였습니다.')
        input('인증키를 복사한 상태라면 Enter를 누르세요: ')
        clip=read_clipboard_windows()
        if clip:
            print('Windows 클립보드에서 인증키를 읽었습니다(화면에는 표시하지 않음).')
            return clip
        print('클립보드를 읽지 못했습니다. 아래 입력은 화면에 보일 수 있습니다.')

    return sanitize_key(input('공공데이터포털 일반 인증키 입력: '))

def main():
    key=get_api_key()
    if not key:
        sys.exit('인증키가 없습니다. 공공데이터포털의 일반 인증키를 복사한 뒤 다시 실행해 주세요.')
    if any(ord(ch)<32 or ord(ch)==127 for ch in key):
        sys.exit('인증키에 제어문자가 포함되어 있습니다. 인증키를 다시 복사해 주세요.')
    print('정부24 공공서비스 데이터 동기화를 시작합니다.')
    verify_key(key)
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
