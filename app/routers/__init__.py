from fastapi import APIRouter
from app.controllers import user_router, item_router, auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(item_router)
