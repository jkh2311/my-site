한이네생활정보 IndexNow 설정

1) 사이트 전체 파일을 먼저 업로드합니다.
2) 사이트 루트에 있는 IndexNow 키 파일이 https://haninelife.com/<키>.txt 로 열리는지 확인합니다.
3) 새 글/수정 글을 배포한 뒤 tools/indexnow-submit.bat 에 URL을 넘겨 실행합니다.
   예: tools\indexnow-submit.bat articles/new-post/
4) HTTP 200이 나오면 네이버 IndexNow 접수가 정상입니다.

주의:
- IndexNow는 새로 생성/수정/삭제된 URL을 빠르게 알리는 용도이며 색인을 보장하지 않습니다.
- 기존 전체 게시글을 매번 재전송하지 않습니다.
- sitemap.xml, rss.xml, 내부링크, 네이버 웹 페이지 수집 요청은 기존 방식대로 유지합니다.
