@echo off
title DocuEase Launcher
echo ========================================================
echo        DocuEase - AI Document Simplification System
echo ========================================================
echo.
echo 1. Launching Backend Server on http://127.0.0.1:5000 ...
start "DocuEase Backend" cmd /k "cd /d "%~dp0backend" && venv\Scripts\python.exe app.py"

echo 2. Waiting 3 seconds for Backend to initialize...
timeout /t 3 /nobreak >nul

echo 3. Launching Frontend Server on http://localhost:5173 ...
start "DocuEase Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo 4. Waiting 2 seconds for Vite dev server...
timeout /t 2 /nobreak >nul

echo 5. Opening DocuEase in your default browser...
start http://localhost:5173

echo.
echo ========================================================
echo  DocuEase is now running!
echo  - Frontend: http://localhost:5173
echo  - Backend API: http://127.0.0.1:5000
echo  - Health Endpoint: http://127.0.0.1:5000/api/health
echo ========================================================
echo.
echo Keep the backend and frontend terminal windows open.
echo Press any key to exit this launcher window.
pause >nul
