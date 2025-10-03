from fastapi import APIRouter, HTTPException
from app.schemas.requests import ChatCompletionRequest
from app.schemas.responses import ChatCompletionResponse

router = APIRouter()


@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """
    Create a chat completion using the unified API.
    Supports multiple AI providers through adapter pattern.
    """
    try:
        # TODO: Implement adapter selection and request routing
        raise HTTPException(
            status_code=501,
            detail="Chat completion endpoint not yet implemented"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
