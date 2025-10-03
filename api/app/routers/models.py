from fastapi import APIRouter, HTTPException
from app.schemas.responses import ModelsResponse

router = APIRouter()


@router.get("/models", response_model=ModelsResponse)
async def list_models():
    """
    List all available models across all configured providers.
    """
    try:
        # TODO: Implement model listing from all adapters
        raise HTTPException(
            status_code=501,
            detail="Models listing endpoint not yet implemented"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
