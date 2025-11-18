from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        errors: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "message": message,
                "errors": errors
            }
        )

class NotFoundException(BaseAPIException):
    def __init__(self, resource: str, identifier: Any = None):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with identifier {identifier} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message
        )

class BadRequestException(BaseAPIException):
    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            errors=errors
        )

class UnauthorizedException(BaseAPIException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message
        )

class ForbiddenException(BaseAPIException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message
        )

class ConflictException(BaseAPIException):
    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            errors=errors
        )

class InternalServerErrorException(BaseAPIException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message
        )