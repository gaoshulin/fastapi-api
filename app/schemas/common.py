from pydantic import BaseModel
from typing import Any, Optional, Dict

class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[Dict[str, Any]] = None

class PaginationResponse(BaseModel):
    items: list
    total: int
    page: int
    size: int
    pages: int
    
class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Optional[Dict[str, Any]] = None
    status_code: int