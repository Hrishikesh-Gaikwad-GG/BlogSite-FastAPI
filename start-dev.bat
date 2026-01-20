@echo off
echo ============================================
echo   BlogSite - Starting Development Servers
echo ============================================
echo.

echo Starting Backend Server...
start "FastAPI Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd app && uvicorn main:app --reload --port 8000"

timeout /t 3

echo Starting Frontend Server...
start "React Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ============================================
echo   Servers Started!
echo ============================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Press any key to exit this window...
pause > nul
