@echo off
chcp 65001 >nul
if "%~1"=="" (
  echo 사용법: indexnow-submit.bat articles/new-post/
  echo 또는: indexnow-submit.bat https://haninelife.com/articles/new-post/
  pause
  exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0indexnow-submit.ps1" -Url %*
pause
