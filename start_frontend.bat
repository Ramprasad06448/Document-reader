@echo off
title DocuEase Frontend Server
echo ====================================================
echo Starting DocuEase Vite Frontend (Port 5173)...
echo ====================================================
cd /d "%~dp0frontend"
npm run dev
pause
