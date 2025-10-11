from fastapi import APIRouter, HTTPException, Request
from app.schemas.requests import EmbeddingRequest
from app.schemas.responses import EmbeddingResponse

router = APIRouter()


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest, http_request: Request):
    """
    Create embeddings using the unified API.
    Supports multiple AI providers through adapter pattern.
    """
    try:
        # Set provider and model in request state for metrics/logging
        http_request.state.provider = "embeddings"
        http_request.state.model = request.model

        # TODO: Implement adapter selection and request routing
        raise HTTPException(
            status_code=501,
            detail="Embeddings endpoint not yet implemented"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
