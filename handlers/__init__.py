from .commands import router as commands_router
from .callback import router as callback_router
from .messages import router as messages_router
from .admin import router as admin_router

__all__ = ['commands_router', 'callback_router', 'messages_router', 'admin_router']