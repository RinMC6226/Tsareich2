@echo off
chcp 65001 >nul
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js not found. Please install from https://nodejs.org/
  pause
  exit /b 1
)
node server.mjs
pause
