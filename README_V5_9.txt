한이네생활정보 V5.9 - 관리자 자동 GitHub 발행

[중요] 이 버전은 사이트 파일을 GitHub에 한 번 올린 뒤, Cloudflare Worker를 1회 설정해야 자동 발행이 작동합니다.
GitHub 토큰/관리자 비밀번호는 절대 HTML 파일에 넣지 않습니다. Worker Secret에만 저장합니다.

1) 이 ZIP의 사이트 파일을 기존 my-site에 덮어쓰기 (admin-backend 폴더 포함 가능)
2) GitHub Desktop Commit -> Push origin
3) GitHub에서 fine-grained Personal Access Token 생성: jkh2311/my-site 저장소만 선택, Contents 권한 Read and write
4) Cloudflare 계정 생성/로그인
5) PC 터미널에서 admin-backend 폴더로 이동
   npm install
   npx wrangler login
   npx wrangler secret put GITHUB_TOKEN
   (3번 토큰 입력)
   npx wrangler secret put ADMIN_PASSWORD
   (원하는 관리자 비밀번호 입력)
   npm run deploy
6) 배포 후 표시되는 https://haninelife-admin.XXXXX.workers.dev 주소를 복사
7) https://haninelife.com/admin.html 접속
8) 관리자 API 주소 + ADMIN_PASSWORD 입력 -> 로그인
9) 새 글 작성 후 'GitHub에 바로 발행'

자동 발행 시:
- articles/<slug>.html 생성 또는 수정
- article-index.json 갱신 (게시글 조회 검색)
- sitemap.xml에 새 URL이 없을 때만 1회 추가
- articles.html 목록에 새 글 추가/기존 글 카드 수정
- GitHub main 브랜치에 커밋되므로 기존 GitHub Pages 설정에서 사이트가 자동 갱신

주의:
- admin.html은 noindex이며 메뉴에 노출하지 않지만 URL을 아는 사람은 페이지 자체에 접근할 수 있습니다. 실제 발행은 Worker의 관리자 비밀번호가 맞아야 가능합니다.
- 관리자 비밀번호와 GitHub 토큰을 다른 사람에게 공유하지 마세요.
- 기존 8개 글 수정은 본문(article 영역)을 불러와 편집할 수 있습니다. 복잡한 기존 레이아웃은 편집기에서 모양이 다르게 보일 수 있으므로 처음에는 작은 수정으로 테스트하세요.
