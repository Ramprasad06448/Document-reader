@echo off
title DocuEase Backend Server
echo ====================================================
echo Starting DocuEase Flask Backend API (Port 5000)...
echo ====================================================
cd /d "%~dp0backend"
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe app.py
) else (
    python app.py
)
pause
