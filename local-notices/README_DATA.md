# 전국 생활 알림판 데이터 안내

`notices.json`은 사이트에 노출되는 검증된 공고 데이터입니다. 초기값은 빈 목록이며 가짜 공고는 표시하지 않습니다.

공고를 추가하려면 `source-notices.json`에 `{ "items": [{ "title": "...", "province": "충청북도", "district": "청주시", "category": "지원금", "agency": "청주시", "published": "2026-10-08", "deadline": "", "url": "https://...go.kr/..." }] }` 형태로 공식 원문 확인 후 입력하세요.

`python scripts/update_local_notices.py` 실행 시 `notices.json`을 생성합니다. 출처 URL은 HTTPS `go.kr` 도메인만 허용합니다.

**주의:** 자동 수집 API는 아직 연결되지 않았습니다. GitHub Actions만으로 전국 지자체 공고를 자동으로 확보할 수 없으므로, 공공데이터 API 접근 권한 및 실제 제공 데이터 구조 확인 후 연동해야 합니다.
