한이네생활정보 V6.4 - 게시일/시간 자동 표시 패치

변경 내용
1. 생활정보 카드에 게시일 표시
2. 새 글은 Cloudflare Worker가 한국시간(Asia/Seoul) 기준 발행 시각을 자동 기록
3. 새 글 예: 게시일 2026년 9월 2일 16:30
4. 기존 8개 글은 과거 정확한 발행 시간이 저장되어 있지 않아 '게시일 2026년 9월 2일 · 시간 기록 없음'으로 표시
5. 새 글의 RSS에는 pubDate도 자동 기록

적용 방법
- 이 ZIP의 파일/폴더를 my-site 루트에 덮어쓰기
- GitHub Desktop에서 Commit → Push origin
- Cloudflare Worker에는 WORKER_DELETE_CODE.js 전체 코드를 다시 배포

주의
- robots.txt는 이 패치 ZIP에 포함하지 않았습니다. Daum 인증키가 들어간 현재 robots.txt를 보호하기 위한 것입니다.
