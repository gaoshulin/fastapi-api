# /Applications/project/python/echosell-api/app/middleware/auth.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.auth import decode_token
from app.config.database import SessionLocal
from app.models import User

# 允许的路径，无需认证
EXEMPT_PATHS = {
    "/docs", "/redoc", "/openapi.json", "/health",
    "/api/v1/auth/login",
    "/api/v1/auth/register"
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()
        # 允许注册开放
        if path in EXEMPT_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        token_header = request.headers.get("x-token") or request.headers.get("token")
        token = None
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1]
        elif token_header:
            token = token_header

        if not token:
            return JSONResponse(status_code=401, content={"success": False, "message": "Unauthorized", "errors": None})

        try:
            payload = decode_token(token)
            sub = payload.get("sub")
            if not sub:
                return JSONResponse(status_code=401, content={"success": False, "message": "Unauthorized", "errors": None})
        except Exception:
            return JSONResponse(status_code=401, content={"success": False, "message": "Unauthorized", "errors": None})

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == int(sub)).first()
            if not user or not user.is_active:
                return JSONResponse(status_code=401, content={"success": False, "message": "Unauthorized", "errors": None})
            request.state.user = user
        finally:
            db.close()

        return await call_next(request)