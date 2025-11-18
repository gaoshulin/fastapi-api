from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.user import ItemResponse, ItemCreate, ItemUpdate
from app.schemas.common import BaseResponse, PaginationResponse
from app.services.item_service import ItemService
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/items", tags=["items"]) 


"""
商品控制器
"""
@router.post("/", response_model=BaseResponse)
def create_item(item: ItemCreate, owner_id: int, token: str = Header(None), db: Session = Depends(get_db)):
    """
    创建新商品
    """
    item_service = ItemService(db)
    created_item = item_service.create_item(item, owner_id)
    return BaseResponse(
        success=True,
        message="Item created successfully",
        data=ItemResponse.from_orm(created_item)
    )


@router.get("/", response_model=BaseResponse)
def get_items(skip: int = 0, limit: int = 100, token: str = Header(None), db: Session = Depends(get_db)):
    """
    获取商品列表
    """
    item_service = ItemService(db)
    items = item_service.get_all_items(skip=skip, limit=limit)
    total = len(items)
    
    pagination = PaginationResponse(
        items=[ItemResponse.from_orm(item) for item in items],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )
    
    return BaseResponse(
        success=True,
        message="Items retrieved successfully",
        data=pagination
    )


@router.get("/owner/{owner_id}", response_model=BaseResponse)
def get_items_by_owner(owner_id: int, skip: int = 0, limit: int = 100, token: str = Header(None), db: Session = Depends(get_db)):
    """
    获取用户所有商品
    """
    item_service = ItemService(db)
    items = item_service.get_items_by_owner(owner_id, skip=skip, limit=limit)
    total = len(items)
    
    pagination = PaginationResponse(
        items=[ItemResponse.from_orm(item) for item in items],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )
    
    return BaseResponse(
        success=True,
        message="Items retrieved successfully",
        data=pagination
    )


@router.get("/{item_id}", response_model=BaseResponse)
def get_item(item_id: int, token: str = Header(None), db: Session = Depends(get_db)):
    """
    获取单个商品
    """
    try:
        item_service = ItemService(db)
        item = item_service.get_item(item_id)
        return BaseResponse(
            success=True,
            message="Item retrieved successfully",
            data=ItemResponse.from_orm(item)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{item_id}", response_model=BaseResponse)
def update_item(item_id: int, item_update: ItemUpdate, token: str = Header(None), db: Session = Depends(get_db)):
    """
    更新商品信息
    """
    try:
        item_service = ItemService(db)
        updated_item = item_service.update_item(item_id, item_update)
        return BaseResponse(
            success=True,
            message="Item updated successfully",
            data=ItemResponse.from_orm(updated_item)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{item_id}", response_model=BaseResponse)
def delete_item(item_id: int, token: str = Header(None), db: Session = Depends(get_db)):
    """
    删除商品
    """
    try:
        item_service = ItemService(db)
        item_service.delete_item(item_id)
        return BaseResponse(
            success=True,
            message="Item deleted successfully"
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        