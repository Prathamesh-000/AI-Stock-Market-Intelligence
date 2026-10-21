"""FastAPI route definitions for stocks, news, and prediction models."""

from backend.api.routes.stocks import router as stocks_router
from backend.api.routes.news import router as news_router
from backend.api.routes.predictions import router as predictions_router

__all__ = ["stocks_router", "news_router", "predictions_router"]

