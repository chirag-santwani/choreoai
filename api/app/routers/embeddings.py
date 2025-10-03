from fastapi import APIRouter, HTTPException
from app.schemas.requests import EmbeddingRequest
from app.schemas.responses import EmbeddingResponse

router = APIRouter()


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest):
    """
    Create embeddings using the unified API.
    Supports multiple AI providers through adapter pattern.
    """
    try:
        # TODO: Implement adapter selection and request routing
        raise HTTPException(
            status_code=501,
            detail="Embeddings endpoint not yet implemented"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
