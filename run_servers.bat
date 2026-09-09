@echo off
echo ======================================================
echo Starting BIS Saathi (Backend + Frontend)
echo ======================================================

start "BIS Saathi Backend (FastAPI)" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

start "BIS Saathi Frontend (Vite React)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Backend running at: http://127.0.0.1:8000
echo Frontend running at: http://localhost:5173
echo.
pause
