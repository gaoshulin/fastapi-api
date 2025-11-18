from app.controllers.user_controller import router as user_router
from app.controllers.item_controller import router as item_router
from app.controllers.auth_controller import router as auth_router

__all__ = ["user_router", "item_router", "auth_router"]
