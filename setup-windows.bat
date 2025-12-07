@echo off
REM Agentic RAG POC - Windows Setup Script
REM Run this script as Administrator

echo ============================================
echo    Agentic RAG POC - Windows Setup
echo ============================================
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop for Windows from:
    echo https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo [OK] Docker is installed and running
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.ai/download
    echo After installation, run: ollama pull gemma3:4b
    echo                          ollama pull nomic-embed-text
    echo.
) else (
    echo [OK] Ollama is installed
    echo.
    echo Pulling required models...
    ollama pull gemma3:4b
    ollama pull nomic-embed-text
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo [OK] Created .env file - please review and customize if needed
) else (
    echo [OK] .env file already exists
)

echo.
echo ============================================
echo    Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Start the services: docker-compose up -d
echo 3. Access the API at: http://localhost:8000
echo.
echo For OpenWebUI (optional):
echo    docker-compose --profile webui up -d
echo    Access at: http://localhost:3000
echo.
pause
