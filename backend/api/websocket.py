"""WebSocket router for live ticker streaming and client broadcast management."""

import json
import asyncio
import logging
from typing import List, Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("backend.websocket")
websocket_router = APIRouter()

class ConnectionManager:
    """Tracks active WebSocket connections and handles broadcasts."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: Dict):
        payload = json.dumps(message)
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                disconnected.append(connection)
        for dead_conn in disconnected:
            self.disconnect(dead_conn)

ws_manager = ConnectionManager()

@websocket_router.websocket("/ws")
@websocket_router.websocket("/ws/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str = "ALL"):
    """Streams live market prices and prediction alerts to connected frontend clients."""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep-alive heartbeat & ping receiver
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.debug(f"WebSocket exception: {e}")
        ws_manager.disconnect(websocket)
