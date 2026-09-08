@echo off
chcp 65001 >nul
cd /d %~dp0
where py >nul 2>nul
if %errorlevel%==0 (
  py update_gov24_data.py
) else (
  python update_gov24_data.py
)
echo.
pause
