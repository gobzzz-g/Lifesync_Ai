@echo off
title LifeSync AI Launcher
echo ========================================================
echo          Starting LifeSync AI Servers
echo ========================================================
echo.
echo Starting FastAPI Backend on port 8000...
start "LifeSync AI Backend" cmd /k "cd /d ""%~dp0backend"" && call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting Vite Frontend on port 5173...
start "LifeSync AI Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm run dev -- --host"

echo.
echo ========================================================
echo   LifeSync AI is launching!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000/docs
echo ========================================================
