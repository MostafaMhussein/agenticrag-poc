@echo off
REM Agentic RAG POC - Windows Run Script

echo ============================================
echo    Agentic RAG POC - Starting Services
echo ============================================
echo.

REM Check command line argument
if "%1"=="api" goto start_api
if "%1"=="docker" goto start_docker
if "%1"=="all" goto start_all
if "%1"=="ingest" goto run_ingest
if "%1"=="eval" goto run_eval
if "%1"=="stop" goto stop_services
if "%1"=="logs" goto show_logs
goto show_help

:start_api
echo Starting API server locally...
python api.py --host 0.0.0.0 --port 8000
goto end

:start_docker
echo Starting Docker services...
docker-compose up -d
echo.
echo Services started! Access points:
echo - API: http://localhost:8000
echo - Health: http://localhost:8000/health
goto end

:start_all
echo Starting all services including WebUI...
docker-compose --profile webui --profile observability up -d
echo.
echo Services started! Access points:
echo - API: http://localhost:8000
echo - OpenWebUI: http://localhost:3000
echo - Phoenix: http://localhost:6006
goto end

:run_ingest
echo Running document ingestion...
echo.
echo Step 1: Converting documents with Docling...
python src\data_ingestion\ingestion_docling.py
echo.
echo Step 2: Creating contextual embeddings...
python src\data_ingestion\ingest_contextual_rag.py
echo.
echo Ingestion complete!
goto end

:run_eval
echo Running RAGAS evaluation...
python src\evaluation\run_ragas_eval.py
goto end

:stop_services
echo Stopping all services...
docker-compose --profile webui --profile observability down
echo Services stopped.
goto end

:show_logs
echo Showing API logs...
docker logs -f rag-api
goto end

:show_help
echo.
echo Usage: run.bat [command]
echo.
echo Commands:
echo   api      - Start API server locally (requires Python)
echo   docker   - Start core Docker services (PostgreSQL + API)
echo   all      - Start all services including WebUI and Phoenix
echo   ingest   - Run document ingestion pipeline
echo   eval     - Run RAGAS evaluation
echo   stop     - Stop all Docker services
echo   logs     - Show API container logs
echo.
echo Examples:
echo   run.bat docker    - Start PostgreSQL and API
echo   run.bat ingest    - Process documents in data\raw\
echo   run.bat all       - Start everything
echo.
goto end

:end
