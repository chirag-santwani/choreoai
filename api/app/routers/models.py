from fastapi import APIRouter, HTTPException
from app.schemas.responses import ModelsResponse
from app.adapters.factory import AdapterFactory
from app.config import settings

router = APIRouter()


@router.get("/models")
async def list_models():
    """
    List all available models across all configured providers.
    Returns models from providers that have API keys configured.
    """
    try:
        all_models = []

        # Define provider configs with their API key checks
        providers = []

        if settings.OPENAI_API_KEY:
            providers.append("openai")
        if settings.ANTHROPIC_API_KEY:
            providers.append("claude")
        if settings.GEMINI_API_KEY:
            providers.append("gemini")
        if settings.GROK_API_KEY:
            providers.append("grok")
        if settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT:
            providers.append("azure")
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            providers.append("bedrock")

        # Fetch models from each configured provider
        for provider in providers:
            try:
                adapter = AdapterFactory.get_adapter(provider)
                models_response = await adapter.list_models()

                # Handle response format
                if isinstance(models_response, dict):
                    if "data" in models_response:
                        all_models.extend(models_response["data"])
                    else:
                        all_models.append(models_response)

            except Exception as e:
                # Log error but continue with other providers
                print(f"Warning: Could not fetch models from {provider}: {e}")
                continue

        return {
            "object": "list",
            "data": all_models
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
