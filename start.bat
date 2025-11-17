@echo off
REM Site-Steward MVP - Quick Start Script for Windows

echo ========================================
echo Site-Steward MVP - Docker Setup
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and set:
    echo   - POSTGRES_PASSWORD
    echo   - JWT_SECRET
    echo   - SMTP credentials
    echo.
    pause
)

echo Building Docker images...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for database to be ready...
timeout /t 10 /nobreak > nul

echo.
echo Initializing database...
docker-compose exec api python database/init_db.py

echo.
echo ========================================
echo Services are running!
echo ========================================
echo Admin Portal: http://localhost:8501
echo Field App:    http://localhost:8502
echo API:          http://localhost:5000
echo ========================================
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose down
echo.
pause
