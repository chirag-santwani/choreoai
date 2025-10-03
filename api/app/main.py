from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import chat, embeddings, models

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

# Include routers
app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(embeddings.router, prefix="/v1", tags=["embeddings"])
app.include_router(models.router, prefix="/v1", tags=["models"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "service": "ChoreoAI",
        "version": "1.0.0",
        "description": "Unified API orchestration for multiple AI providers"
    }
