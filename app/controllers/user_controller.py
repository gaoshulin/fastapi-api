from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import BaseResponse, PaginationResponse
from app.services.user_service import UserService
from app.utils.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/users", tags=["users"]) 


"""
用户控制器
"""
@router.get("/", response_model=BaseResponse)
def get_users(skip: int = 0, limit: int = 100, token: str = Header(None), db: Session = Depends(get_db)):
    """
    获取用户列表
    """
    user_service = UserService(db)
    users = user_service.get_users(skip=skip, limit=limit)
    total = len(users)
    
    pagination = PaginationResponse(
        items=[UserResponse.from_orm(user) for user in users],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )
    
    return BaseResponse(
        success=True,
        message="Users retrieved successfully",
        data=pagination
    )


@router.get("/{user_id}", response_model=BaseResponse)
def get_user(user_id: int, token: str = Header(None), db: Session = Depends(get_db)):
    """
    获取单个用户
    """
    try:
        user_service = UserService(db)
        user = user_service.get_user(user_id)
        return BaseResponse(
            success=True,
            message="User retrieved successfully",
            data=UserResponse.from_orm(user)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{user_id}", response_model=BaseResponse)
def update_user(user_id: int, user_update: UserUpdate, token: str = Header(None), db: Session = Depends(get_db)):
    """
    更新用户信息
    """
    try:
        user_service = UserService(db)
        updated_user = user_service.update_user(user_id, user_update)
        return BaseResponse(
            success=True,
            message="User updated successfully",
            data=UserResponse.from_orm(updated_user)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{user_id}", response_model=BaseResponse)
def delete_user(user_id: int, token: str = Header(None), db: Session = Depends(get_db)):
    """
    删除用户
    """
    try:
        user_service = UserService(db)
        user_service.delete_user(user_id)
        return BaseResponse(
            success=True,
            message="User deleted successfully"
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
