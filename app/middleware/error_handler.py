from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.exceptions import BaseAPIException
import logging
import traceback

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseAPIException as exc:
            logger.error(f"API Exception: {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail
            )
        except StarletteHTTPException as exc:
            logger.error(f"HTTP Exception: {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "message": exc.detail,
                    "errors": None
                }
            )
        except Exception as exc:
            logger.error(f"Unhandled Exception: {str(exc)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal server error",
                    "errors": {"detail": str(exc)}
                }
            )