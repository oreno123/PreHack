@echo off
cd /d "%~dp0"
start "server" /min python -m http.server 8899 --bind 127.0.0.1
timeout /t 1 >nul
start "" "http://localhost:8899/hybrid.html?auto=1&beat=1&shape=ding"
