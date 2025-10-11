from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.utils.logger import setup_logging

logger = setup_logging(settings.LOG_LEVEL)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to authenticate API requests using Bearer token authentication.

    In development mode (ENVIRONMENT=development), all API keys are accepted.
    In production mode, implement proper validation against a database or key store.
    """

    # Public endpoints that don't require authentication
    PUBLIC_ENDPOINTS = {
        "/",
        "/health",
        "/metrics",
        "/docs",
        "/redoc",
        "/openapi.json",
    }

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public endpoints
        if request.url.path in self.PUBLIC_ENDPOINTS:
            return await call_next(request)

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return self._error_response(
                message="Missing Authorization header",
                error_type="authentication_error",
                code="missing_authorization",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Validate Bearer scheme
        try:
            scheme, api_key = auth_header.split(" ", 1)
        except ValueError:
            return self._error_response(
                message="Malformed Authorization header",
                error_type="authentication_error",
                code="malformed_authorization",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if scheme.lower() != "bearer":
            return self._error_response(
                message="Invalid authentication scheme. Use Bearer authentication",
                error_type="authentication_error",
                code="invalid_auth_scheme",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Validate API key
        if not self._validate_api_key(api_key):
            logger.warning(f"Invalid API key attempt from {request.client.host}")
            return self._error_response(
                message="Invalid API key provided",
                error_type="authentication_error",
                code="invalid_api_key",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Store API key in request state for potential use in route handlers
        request.state.api_key = api_key

        # Log successful authentication
        logger.debug(f"Authenticated request to {request.url.path} from {request.client.host}")

        return await call_next(request)

    def _validate_api_key(self, api_key: str) -> bool:
        """
        Validate the provided API key.

        In development mode, accepts any non-empty key.
        In production, implement proper validation:
        - Check against database
        - Verify key hasn't expired
        - Check if key is revoked
        - Validate key permissions for the requested endpoint

        Args:
            api_key: The API key to validate

        Returns:
            True if key is valid, False otherwise
        """
        # Basic validation: key must not be empty
        if not api_key or not api_key.strip():
            return False

        # Development mode: accept all non-empty keys
        if settings.ENVIRONMENT == "development":
            return True

        # Production mode: implement proper validation
        # TODO: Implement production API key validation
        # - Query database for key existence
        # - Check expiration date
        # - Verify key is not revoked
        # - Check rate limits
        # Example:
        # return await self._check_key_in_database(api_key)

        # For now, require keys to have a minimum length in production
        if len(api_key) < 32:
            return False

        # Placeholder: In production, you should validate against a database
        logger.warning("Production mode using basic API key validation. Implement proper key management!")
        return True

    def _error_response(
        self,
        message: str,
        error_type: str,
        code: str,
        status_code: int
    ) -> JSONResponse:
        """
        Return a standardized error response for authentication failures.

        Args:
            message: Human-readable error message
            error_type: Type of error (e.g., "authentication_error")
            code: Machine-readable error code
            status_code: HTTP status code

        Returns:
            JSONResponse with error details
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "message": message,
                    "type": error_type,
                    "code": code
                }
            }
        )
