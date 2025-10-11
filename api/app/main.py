from datetime import datetime
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.config import settings
from app.routers import chat, embeddings, models
from app.middleware.logging import LoggingMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.utils.logger import setup_logging

# Initialize logging
logger = setup_logging(settings.LOG_LEVEL)

app = FastAPI(
    title="ChoreoAI",
    description="A unified API orchestration platform for multiple AI providers",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware (order matters: metrics -> logging -> CORS)
app.add_middleware(MetricsMiddleware)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(embeddings.router, prefix="/v1", tags=["embeddings"])
app.include_router(models.router, prefix="/v1", tags=["models"])


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and orchestration"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/")
async def root():
    return {
        "service": "ChoreoAI",
        "version": "1.0.0",
        "description": "Unified API orchestration for multiple AI providers"
    }
