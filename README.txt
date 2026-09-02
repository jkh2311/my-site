한이네생활정보 V5.7

변경사항
- 모든 게시글 제목 마지막에 '총정리' 통일
- 페이지 상단에 '게시글 조회' 검색창 추가
- 2글자 이상 입력하면 제목/설명/카테고리를 검색
- 검색 결과를 클릭하면 해당 게시글로 바로 이동
- Enter 키와 조회 버튼 둘 다 지원
- 정적 HTML/JavaScript 방식이라 GitHub Pages에서 그대로 작동
- 기존 V5.6 내용은 유지
- style.css?v=57

적용:
ZIP 압축 해제 → 기존 my-site 폴더에 전부 덮어쓰기
.git 폴더는 삭제하지 않기
Live Server → Ctrl+F5 → GitHub Desktop Commit → Push origin

[V5.8 추가 기능]
- contact.html 문의 폼 활성화: 수신 jhh271@naver.com, 별도 서버 저장 없이 사용자의 이메일 앱(mailto)으로 전송
- admin.html 게시글 작성 도구 추가: 제목/카테고리/기준일/본문 편집, 브라우저 임시저장, HTML 파일 생성
- admin.html은 검색엔진 noindex 처리 및 공개 메뉴에 링크하지 않음
- GitHub Pages는 정적 호스팅이라 admin.html에서 저장소를 직접 수정할 수 없음. GitHub 토큰을 공개 코드에 넣지 않기 위해 안전한 파일 생성 방식으로 구현
- 완전한 '발행 버튼 → GitHub 자동 반영'을 원하면 별도 로그인/백엔드 또는 안전한 CMS 인증 구성이 필요함
