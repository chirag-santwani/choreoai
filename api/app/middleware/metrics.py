import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge
from app.utils.logger import logger


# Define Prometheus metrics
request_counter = Counter(
    "choreoai_requests_total",
    "Total number of API requests",
    ["provider", "model", "endpoint", "status", "method"],
)

request_duration = Histogram(
    "choreoai_request_duration_seconds",
    "Request duration in seconds",
    ["provider", "endpoint", "method"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
)

token_counter = Counter(
    "choreoai_tokens_total",
    "Total tokens processed",
    ["provider", "model", "type"],  # type: input/output
)

error_counter = Counter(
    "choreoai_errors_total",
    "Total number of errors",
    ["provider", "error_type", "endpoint"],
)

active_connections = Gauge(
    "choreoai_active_connections",
    "Current number of active connections",
)

streaming_requests = Counter(
    "choreoai_streaming_requests_total",
    "Total number of streaming requests",
    ["provider", "model"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting Prometheus metrics"""

    async def dispatch(self, request: Request, call_next):
        # Increment active connections
        active_connections.inc()

        # Track request start time
        start_time = time.time()

        # Extract request info
        method = request.method
        endpoint = request.url.path

        # Initialize provider and model (will be set by router if available)
        provider = "unknown"
        model = "unknown"

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Get provider and model from request state (set by routers)
            provider = getattr(request.state, "provider", "unknown")
            model = getattr(request.state, "model", "unknown")

            # Record request metrics
            request_counter.labels(
                provider=provider,
                model=model,
                endpoint=endpoint,
                status=response.status_code,
                method=method,
            ).inc()

            request_duration.labels(
                provider=provider, endpoint=endpoint, method=method
            ).observe(duration)

            # Track token usage if available
            if hasattr(request.state, "usage"):
                usage = request.state.usage
                if hasattr(usage, "prompt_tokens"):
                    token_counter.labels(
                        provider=provider, model=model, type="input"
                    ).inc(usage.prompt_tokens)
                if hasattr(usage, "completion_tokens"):
                    token_counter.labels(
                        provider=provider, model=model, type="output"
                    ).inc(usage.completion_tokens)

            # Track streaming requests
            if hasattr(request.state, "is_streaming") and request.state.is_streaming:
                streaming_requests.labels(provider=provider, model=model).inc()

            return response

        except Exception as e:
            # Calculate duration even on error
            duration = time.time() - start_time

            # Get provider from request state if available
            provider = getattr(request.state, "provider", "unknown")

            # Record error metrics
            error_counter.labels(
                provider=provider, error_type=type(e).__name__, endpoint=endpoint
            ).inc()

            # Log error
            logger.error(
                f"Request error: {str(e)}",
                extra={
                    "provider": provider,
                    "endpoint": endpoint,
                    "error_type": type(e).__name__,
                    "duration": round(duration, 3),
                },
            )

            # Re-raise exception
            raise

        finally:
            # Decrement active connections
            active_connections.dec()
