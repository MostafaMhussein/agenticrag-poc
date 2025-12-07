"""
FastAPI Server for Agentic RAG
Provides OpenAI-compatible API endpoints for integration with OpenWebUI and other clients.
Compatible with Windows, macOS, and Linux.
"""
import os
import sys
import time
import uuid
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# Add project root to path (cross-platform compatible)
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import RAG components
from src.rag_system.crew import RAGCrewManager, run_query
from src.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agentic RAG API",
    description="OpenAI-compatible API for Agentic RAG with CrewAI",
    version="1.0.0"
)

# Add CORS middleware for web interface access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG manager
rag_manager = RAGCrewManager(use_simple_mode=False)


# ============== Pydantic Models ==============

class Message(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request"""
    model: str = Field(default="crew-ai-rag", description="Model identifier")
    messages: List[Message] = Field(..., description="List of messages")
    temperature: Optional[float] = Field(default=0.1, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=4096, description="Maximum tokens in response")
    stream: Optional[bool] = Field(default=False, description="Enable streaming")
    top_p: Optional[float] = Field(default=1.0, description="Top-p sampling")
    frequency_penalty: Optional[float] = Field(default=0.0)
    presence_penalty: Optional[float] = Field(default=0.0)


class ChatCompletionChoice(BaseModel):
    """Chat completion choice"""
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    """Token usage information"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """OpenAI-compatible chat completion response"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


class ModelInfo(BaseModel):
    """Model information"""
    id: str
    object: str = "model"
    created: int
    owned_by: str


class ModelsResponse(BaseModel):
    """List of available models"""
    object: str = "list"
    data: List[ModelInfo]


# ============== API Endpoints ==============

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Agentic RAG API",
        "version": "1.0.0",
        "description": "OpenAI-compatible API for document Q&A with CrewAI agents",
        "endpoints": {
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "running",
            "database": "configured",
            "ollama": settings.ollama.base_url
        }
    }


@app.get("/v1/models", response_model=ModelsResponse)
async def list_models():
    """
    List available models.
    Returns models that can be selected in OpenWebUI.
    """
    models = [
        ModelInfo(
            id="crew-ai-rag",
            object="model",
            created=int(time.time()),
            owned_by="agentic-rag-poc"
        ),
        ModelInfo(
            id="rag-model",
            object="model",
            created=int(time.time()),
            owned_by="agentic-rag-poc"
        ),
        ModelInfo(
            id="simple-rag",
            object="model",
            created=int(time.time()),
            owned_by="agentic-rag-poc"
        )
    ]
    
    return ModelsResponse(object="list", data=models)


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint.
    
    Supports multiple model types:
    - crew-ai-rag: Full multi-agent workflow (research + synthesis)
    - rag-model: Alias for crew-ai-rag
    - simple-rag: Single-agent Q&A mode
    """
    try:
        start_time = time.time()
        
        # Extract the user's query from messages
        user_messages = [m for m in request.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message provided")
        
        query = user_messages[-1].content
        logger.info(f"Processing query: {query[:100]}...")
        
        # Determine mode based on model selection
        use_simple_mode = request.model == "simple-rag"
        
        # Create manager with appropriate mode
        manager = RAGCrewManager(use_simple_mode=use_simple_mode)
        
        # Execute query
        result = manager.query(query)
        
        if not result.get("success", False):
            answer = result.get("answer", "Failed to process query")
            logger.error(f"Query failed: {result.get('error', 'Unknown error')}")
        else:
            answer = result.get("answer", "")
            
            # Add source attribution if available
            sources = result.get("sources", [])
            if sources:
                answer += f"\n\n**Sources:** {', '.join(sources)}"
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(f"Query processed in {processing_time:.2f}s")
        
        # Estimate token counts (rough estimation)
        prompt_tokens = sum(len(m.content.split()) * 1.3 for m in request.messages)
        completion_tokens = len(answer.split()) * 1.3
        
        # Build response
        response = ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content=answer),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=int(prompt_tokens),
                completion_tokens=int(completion_tokens),
                total_tokens=int(prompt_tokens + completion_tokens)
            )
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/embeddings")
async def create_embeddings(request: Dict[str, Any]):
    """
    Embeddings endpoint (placeholder for compatibility).
    The actual embeddings are handled internally by the RAG system.
    """
    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": [0.0] * 768,  # Placeholder
                "index": 0
            }
        ],
        "model": "nomic-embed-text",
        "usage": {
            "prompt_tokens": 0,
            "total_tokens": 0
        }
    }


@app.get("/v1/models/{model_id}")
async def get_model(model_id: str):
    """Get information about a specific model"""
    valid_models = ["crew-ai-rag", "rag-model", "simple-rag"]
    
    if model_id not in valid_models:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
    
    return ModelInfo(
        id=model_id,
        object="model",
        created=int(time.time()),
        owned_by="agentic-rag-poc"
    )


# ============== Error Handlers ==============

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": str(exc),
                "type": type(exc).__name__,
                "code": 500
            }
        }
    )


# ============== Main Entry Point ==============

def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run the Agentic RAG API server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
