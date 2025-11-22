from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.utils.exceptions import BaseAPIException
import logging
import time
import json
import os

class JSONFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "data"):
            data = record.__dict__.get("data")
            if isinstance(data, dict):
                payload.update(data)
            else:
                payload["data"] = data
        return json.dumps(payload, ensure_ascii=False)

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

request_logger = logging.getLogger("request")
if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "").endswith("request.log") for h in request_logger.handlers):
    fh = logging.FileHandler(os.path.join(LOG_DIR, "request.log"))
    fh.setFormatter(JSONFormatter())
    request_logger.setLevel(logging.INFO)
    request_logger.addHandler(fh)

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
        
        level = logging.ERROR if response.status_code >= 400 else logging.INFO
        request_logger.log(level, "request", extra={"data": log_data})
        
        return response