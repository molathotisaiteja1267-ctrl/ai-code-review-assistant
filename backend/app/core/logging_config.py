import logging
import sys
import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("ai_code_review")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"
        logger.info(f"START {request.method} {request.url.path} from {client_host}")
        
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            logger.info(f"END   {request.method} {request.url.path} status={response.status_code} duration={process_time:.2f}ms")
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"FAIL  {request.method} {request.url.path} error={str(e)} duration={process_time:.2f}ms")
            raise e
