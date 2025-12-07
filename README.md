# 🤖 Agentic RAG POC

[![CrewAI](https://img.shields.io/badge/CrewAI-%F0%9F%9A%A2-blue?style=for-the-badge&logo=docker&logoColor=white)](https://crewai.com)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-%F0%9F%A6%99-green?style=for-the-badge&logo=python&logoColor=white)](https://llamaindex.ai)
[![Ollama](https://img.shields.io/badge/Ollama-%F0%9F%A6%99-orange?style=for-the-badge&logo=llama&logoColor=white)](https://ollama.ai)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%F0%9F%90%98-blue?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-%F0%9F%90%B3-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

**🎯 An intelligent agentic RAG system with multi-agent workflows, powered by CrewAI and local LLMs**

**✅ Compatible with Windows, macOS, and Linux**

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Agent Workflow** | Specialized agents for research & synthesis using CrewAI |
| 🦙 **Local LLM Integration** | Ollama with Gemma 3 (131K context window) |
| 🎯 **Contextual RAG** | AI-generated context for each document chunk |
| 📊 **Smart Document Processing** | PDF/DOCX parsing with Docling |
| 🚀 **Vector Search** | PostgreSQL + pgvector for fast retrieval |
| 💬 **OpenWebUI Integration** | Beautiful chat interface |
| 🔗 **OpenAI-Compatible API** | Standard REST endpoints |
| 📈 **RAGAS Evaluation** | Quality metrics for RAG performance |
| 🐦 **Phoenix Observability** | Request tracing and monitoring |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                    (OpenWebUI / API Client)                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Server                             │
│                (OpenAI-Compatible Endpoints)                    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CrewAI Orchestrator                         │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │  Document Researcher │───▶│  Insight Synthesizer │           │
│  │  - Vector Search     │    │  - Response Generation│          │
│  │  - Hybrid Retrieval  │    │  - Source Attribution │          │
│  └─────────────────────┘    └─────────────────────┘            │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Retrieval Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │ PostgreSQL +    │  │ Ollama LLM      │  │ Ollama         │  │
│  │ pgvector        │  │ (Gemma 3)       │  │ Embeddings     │  │
│  │ 768-dim vectors │  │ 131K context    │  │ nomic-embed    │  │
│  └─────────────────┘  └─────────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

| Component | Requirement | Download |
|-----------|-------------|----------|
| 🐳 Docker | Docker Desktop | [Download](https://www.docker.com/products/docker-desktop) |
| 🦙 Ollama | Local LLM inference | [Download](https://ollama.ai/download) |
| 🐍 Python | 3.10+ (for local dev) | [Download](https://www.python.org/downloads/) |
| 💻 System | 8GB+ RAM, 50GB+ disk | - |

---

## ⚡ Quick Start (Windows)

### 1️⃣ Install Prerequisites

1. **Install Docker Desktop for Windows**
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Enable WSL 2 backend during installation
   - Start Docker Desktop

2. **Install Ollama for Windows**
   - Download from [ollama.ai/download](https://ollama.ai/download)
   - Run the installer

3. **Install Python 3.10+** (for local development)
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation

### 2️⃣ Setup Ollama

Open **Command Prompt** or **PowerShell**:

```cmd
:: Pull required models
ollama pull gemma3:4b
ollama pull nomic-embed-text

:: Verify models are installed
ollama list
```

### 3️⃣ Clone & Configure

```cmd
:: Clone repository (or extract the ZIP file)
cd C:\Projects
git clone https://github.com/yourusername/agentic-rag-poc.git
cd agentic-rag-poc

:: Copy environment file
copy .env.example .env

:: Or use the setup script
setup-windows.bat
```

### 4️⃣ Start Services with Docker

```cmd
:: Start PostgreSQL and RAG API
docker-compose up -d

:: Check services are running
docker ps

:: View logs if needed
docker logs rag-api
```

### 5️⃣ Ingest Documents

```cmd
:: Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Place your PDF/DOCX files in data\raw\ folder
:: Then run ingestion
python src\data_ingestion\ingestion_docling.py
python src\data_ingestion\ingest_contextual_rag.py
```

### 6️⃣ Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| ⚡ RAG API | http://localhost:8000 | API endpoints |
| 📋 API Docs | http://localhost:8000/docs | Swagger UI |
| 🏥 Health Check | http://localhost:8000/health | Service status |

### 7️⃣ (Optional) Add OpenWebUI

```cmd
:: Start with OpenWebUI chat interface
docker-compose --profile webui up -d

:: Access at http://localhost:3000
```

---

## 🖥️ Windows Helper Scripts

### setup-windows.bat
Run this first to check prerequisites and configure the environment:
```cmd
setup-windows.bat
```

### run.bat
Use this for common operations:
```cmd
run.bat docker    :: Start core services
run.bat all       :: Start all services including WebUI
run.bat ingest    :: Run document ingestion
run.bat stop      :: Stop all services
run.bat logs      :: View API logs
```

---

## 📖 Usage

### Via API (PowerShell)

```powershell
# List models
Invoke-RestMethod -Uri "http://localhost:8000/v1/models"

# Chat completion
$body = @{
    model = "crew-ai-rag"
    messages = @(
        @{role = "user"; content = "What are the key procurement requirements?"}
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/v1/chat/completions" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Via API (curl - if installed)

```cmd
curl http://localhost:8000/v1/models

curl -X POST http://localhost:8000/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\": \"crew-ai-rag\", \"messages\": [{\"role\": \"user\", \"content\": \"What are the HR policies?\"}]}"
```

### Via CLI

```cmd
:: Activate virtual environment first
venv\Scripts\activate

:: Interactive mode
python main.py

:: Single query
python main.py "What are the HR policies?"

:: Simple mode (single agent)
python main.py --simple "Quick question about leave policy"
```

### Via OpenWebUI

1. Open http://localhost:3000
2. Go to **Settings** → **Connections** → **OpenAI API**
3. Set API Base URL: `http://rag-api:8000/v1`
4. Leave API Key empty
5. Select "crew-ai-rag" model and start chatting!

---

## 📁 Project Structure

```
agentic-rag-poc\
├── src\
│   ├── config\              # Configuration settings
│   │   └── settings.py
│   ├── data_ingestion\      # Document processing
│   │   ├── ingestion_docling.py    # Docling converter
│   │   └── ingest_contextual_rag.py # Contextual RAG indexer
│   ├── rag_system\          # Core RAG implementation
│   │   ├── agents.py        # CrewAI agent definitions
│   │   ├── crew.py          # Workflow orchestration
│   │   └── tools.py         # Retrieval tools
│   └── evaluation\          # Quality evaluation
│       └── run_ragas_eval.py
├── data\
│   ├── raw\                 # Place your documents here
│   ├── processed\           # Converted files
│   └── evaluation\          # Eval datasets
├── api.py                   # FastAPI server
├── main.py                  # CLI entry point
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container build
├── requirements.txt         # Python dependencies
├── setup-windows.bat        # Windows setup script
├── run.bat                  # Windows run script
└── README.md                # This file
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | http://localhost:11434 | Ollama server URL |
| `OLLAMA_LLM_MODEL` | gemma3:4b | LLM model name |
| `OLLAMA_EMBEDDING_MODEL` | nomic-embed-text | Embedding model |
| `DB_HOST` | localhost | PostgreSQL host |
| `DB_PORT` | 5432 | PostgreSQL port |
| `CHUNK_SIZE` | 512 | Document chunk size |
| `SIMILARITY_TOP_K` | 5 | Number of results to retrieve |

---

## 🐛 Troubleshooting (Windows)

### Docker Desktop not starting
- Enable virtualization in BIOS
- Enable WSL 2: `wsl --install`
- Restart your computer

### "host.docker.internal" not resolving
- This should work automatically on Docker Desktop for Windows
- If issues persist, check Docker Desktop settings → Resources → WSL Integration

### Ollama connection refused
```cmd
:: Check if Ollama is running
ollama list

:: If not running, start it
ollama serve
```

### Port already in use
```cmd
:: Find what's using port 8000
netstat -ano | findstr :8000

:: Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Python module not found
```cmd
:: Make sure you're in the project directory
cd C:\Projects\agentic-rag-poc

:: Activate virtual environment
venv\Scripts\activate

:: Reinstall dependencies
pip install -r requirements.txt
```

### View Docker logs
```cmd
docker logs rag-api
docker logs rag-postgres
```

---

## 📊 Evaluation

Run RAGAS evaluation to measure RAG quality:

```cmd
:: Activate virtual environment
venv\Scripts\activate

:: Create sample evaluation dataset
python src\evaluation\run_ragas_eval.py --create-sample

:: Run evaluation
python src\evaluation\run_ragas_eval.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) - Multi-agent orchestration
- [LlamaIndex](https://llamaindex.ai) - Document processing & retrieval
- [Ollama](https://ollama.ai) - Local LLM inference
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity search
- [OpenWebUI](https://openwebui.com) - Chat interface
- [Arize Phoenix](https://phoenix.arize.com) - Observability

---

**⭐ Star this repo if it helped you! ⭐**
