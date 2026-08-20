@echo off
echo ===================================================
echo Starting AI Code Review Assistant (Backend + Frontend)
echo ===================================================

start "AI Code Review - Backend (FastAPI)" cmd /k "cd backend && .\venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

timeout /t 2 >nul

start "AI Code Review - Frontend (Vite React)" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting!
echo - Backend API:  http://localhost:8000 (Swagger: http://localhost:8000/docs)
echo - Frontend UI:  http://localhost:5173
echo ===================================================
