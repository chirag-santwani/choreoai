from fastapi import APIRouter, HTTPException, Request
from app.schemas.requests import EmbeddingRequest
from app.schemas.responses import EmbeddingResponse
from app.adapters.factory import AdapterFactory

router = APIRouter()


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest, http_request: Request):
    """
    Create embeddings using the unified API.
    Supports multiple AI providers through adapter pattern.

    Request body:
        - model: Embedding model identifier (e.g., text-embedding-ada-002)
        - input: Text(s) to embed (string or array of strings)
        - encoding_format: Format for embeddings ("float" or "base64", default: "float")

    Returns:
        EmbeddingResponse with vector embeddings and token usage
    """
    try:
        # Get the appropriate adapter for the model
        adapter = AdapterFactory.get_adapter_for_model(request.model)

        # Set provider and model in request state for metrics/logging
        http_request.state.provider = adapter.__class__.__name__.replace("Adapter", "").lower()
        http_request.state.model = request.model

        # Convert request to dict for adapter
        request_dict = request.model_dump(exclude_none=True)

        # Create embeddings through the adapter
        response = await adapter.create_embedding(request_dict)

        # Store usage info in request state for metrics
        if 'usage' in response:
            http_request.state.usage = response['usage']

        return response

    except ValueError as e:
        # Handle validation errors (unknown model, missing API key, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
