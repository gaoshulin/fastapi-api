from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user import LoginRequest, TokenResponse
from app.schemas.common import BaseResponse
from app.services.user_service import UserService
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=BaseResponse)
def login(login: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_username(login.username)
    if not user or not user_service.verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    token = create_access_token({"sub": str(user.id)})
    return BaseResponse(success=True, message="Login successful", data=TokenResponse(token=token))