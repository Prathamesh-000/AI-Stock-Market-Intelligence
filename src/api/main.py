import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from src.api.routes import router as prediction_router
from src.api.ws_manager import manager
from config.settings import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Stock Market Intelligence",
    description="High-speed prediction server",
    version="1.0.0"
)

# Allow React dashboard to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST routes
app.include_router(prediction_router, prefix="/api/v1")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    The main WebSocket endpoint that the React dashboard will connect to.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, wait for client messages (if any)
            data = await websocket.receive_text()
            logger.info(f"Received WS message from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/health")
def health_check():
    return {"status": "online", "model_version": "xgboost_v1"}

if __name__ == "__main__":
    logger.info("Starting production prediction server...")
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)
