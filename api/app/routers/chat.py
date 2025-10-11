from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.schemas.requests import ChatCompletionRequest
from app.schemas.responses import ChatCompletionResponse
from app.adapters.factory import AdapterFactory
import json

router = APIRouter()


@router.post("/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest, http_request: Request):
    """
    Create a chat completion using the unified API.
    Supports multiple AI providers through adapter pattern.
    Supports both streaming and non-streaming responses.
    """
    try:
        # Get the appropriate adapter for the model
        adapter = AdapterFactory.get_adapter_for_model(request.model)

        # Set provider and model in request state for metrics/logging
        http_request.state.provider = adapter.__class__.__name__.replace("Adapter", "").lower()
        http_request.state.model = request.model
        http_request.state.is_streaming = request.stream

        # Convert request to dict for adapter
        request_dict = request.model_dump(exclude_none=True)

        # Handle streaming requests
        if request.stream:
            async def stream_generator():
                try:
                    async for chunk in adapter.chat_completion_stream(request_dict):
                        yield f"data: {json.dumps(chunk)}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    error_data = {
                        "error": {
                            "message": str(e),
                            "type": "stream_error"
                        }
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"

            return StreamingResponse(
                stream_generator(),
                media_type="text/event-stream"
            )

        # Handle non-streaming requests
        response = await adapter.chat_completion(request_dict)

        # Store usage info in request state for metrics
        if hasattr(response, 'usage'):
            http_request.state.usage = response.usage

        return response

    except ValueError as e:
        # Handle validation errors (unknown model, missing API key, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
