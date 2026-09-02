한이네생활정보 V6.3 - RSS 자동관리

추가 기능
- 루트에 rss.xml 생성
- 관리자에서 새 글 발행 시 rss.xml 자동 추가
- 기존 글 수정 시 같은 RSS 항목을 갱신 (중복 추가 안 함)
- 게시글 삭제 시 RSS에서도 자동 제거
- robots.txt에 RSS 피드 위치 추가

설치
1. 이 폴더의 내용을 GitHub my-site 루트에 덮어쓰기
2. Commit / Push origin
3. https://haninelife.com/rss.xml 접속 확인
4. Cloudflare Worker의 코드를 WORKER_DELETE_CODE.js 내용으로 교체 후 배포
5. Google Search Console / Naver Search Advisor / Daum Seed URL에 RSS 주소 제출

RSS 주소: https://haninelife.com/rss.xml
