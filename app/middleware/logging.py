from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.utils.exceptions import BaseAPIException
import logging
import time
import json

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()
        content_type = request.headers.get("content-type", "")
        content_length = request.headers.get("content-length")
        body = b""
        
        # 读取请求体（保持不变）
        if content_length and content_type.startswith("application/json"):
            try:
                if int(content_length) <= 10240:
                    body = await request.body()
            except Exception:
                body = b""
        
        # 关键修改：通过自定义 receive 方法重构请求，无需 Body 类
        async def receive():
            # 模拟请求体接收，返回原始 body（Starlette 0.27.0 兼容写法）
            return {"type": "http.request", "body": body, "more_body": False}
        
        # 用新的 receive 方法创建请求对象
        new_request = Request(request.scope, receive=receive)
        
        # 继续处理请求
        response = await call_next(new_request)
        
        # 日志处理逻辑（保持不变）
        process_time = time.time() - start_time
        log_data = {
            "method": new_request.method,
            "url": str(new_request.url),
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s"
        }
        
        if body:
            try:
                log_data["request_body"] = json.loads(body.decode())
            except:
                log_data["request_body"] = "Unable to parse"
        
        if response.status_code >= 400:
            logger.error(f"Request failed: {log_data}")
        else:
            logger.info(f"Request completed: {log_data}")
        
        return response