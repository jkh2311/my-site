한이네생활정보 V6.0 - 관리자 게시글 삭제 기능

추가 기능
- 기존 게시글 불러오기 후 '게시글 삭제' 버튼 표시
- 삭제 시 GitHub의 articles/<slug>.html 삭제
- article-index.json에서 제거
- articles.html 게시글 카드 제거
- sitemap.xml에서 해당 URL 제거

적용 순서
1) 이 ZIP의 사이트 파일을 기존 my-site에 덮어쓰기 후 Commit / Push origin
2) Cloudflare Worker의 worker.js를 admin-backend/src/index.js 내용 전체로 교체 후 배포
3) haninelife.com/admin.html 새로고침 후 로그인
4) 기존 게시글 선택 > 불러오기 > 게시글 삭제

주의
- 삭제는 실제 GitHub 파일을 삭제하므로 되돌리려면 GitHub 커밋 기록에서 복구해야 합니다.
- GITHUB_TOKEN, ADMIN_PASSWORD Secret은 기존 것을 그대로 사용합니다. 다시 만들 필요 없습니다.
