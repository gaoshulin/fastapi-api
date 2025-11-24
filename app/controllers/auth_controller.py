from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user import LoginRequest, TokenResponse
from app.schemas.common import BaseResponse
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserCreate
from app.utils.exceptions import ConflictException
from app.utils.auth import create_access_token, delete_token
from app.config.logs import get_json_logger
from app.utils.redis import RedisCache


app_logger = get_json_logger("app.log")
redis_cache = RedisCache()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=BaseResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    创建新用户
    """
    try:
        user_service = UserService(db)
        created_user = user_service.create_user(user)
        return BaseResponse(
            success=True,
            message="User register successfully",
            data=UserResponse.from_orm(created_user)
        )
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=BaseResponse)
def login(login: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_username(login.username)
    if not user or not user_service.verify_password(login.password, user.hashed_password):
        # 记录登录失败日志
        app_logger.error("login failed", extra={"data": {"username": login.username}})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    # 生成 JWT token
    token = create_access_token({"sub": str(user.id)})

    # 缓存 token 到 Redis
    redis_cache.set(f"user_token:{token}", token, expire_seconds=600)

    # 登录成功日志
    app_logger.info("login success", extra={"data": {"username": login.username, "token": token}})
    return BaseResponse(success=True, message="Login successful", data=TokenResponse(token=token))


@router.get("/logout", response_model=BaseResponse)
def logout(token: str = ""):
    """
    Logout user and invalidate JWT token.
    """
    # 删除 token
    delete_token(token)
    return BaseResponse(success=True, message="Logout successful")
    
