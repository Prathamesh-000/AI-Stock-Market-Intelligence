"""API routing and WebSocket manager package."""

from backend.api.websocket import websocket_router
from backend.api.routes.stocks import router as stocks_router
from backend.api.routes.news import router as news_router
from backend.api.routes.predictions import router as predictions_router

__all__ = [
    "websocket_router",
    "stocks_router",
    "news_router",
    "predictions_router",
]

