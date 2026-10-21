"""Test client for the real-time WebSocket market streaming endpoint."""

import asyncio
import json
import logging
import websockets

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ws_tester")

WS_URL = "ws://localhost:8000/api/v1/ws"

async def test_websocket_feed(duration_seconds: int = 15):
    """Connects to the WebSocket endpoint and listens for real-time market updates."""
    logger.info(f"Connecting to WebSocket: {WS_URL}...")
    try:
        async with websockets.connect(WS_URL) as ws:
            logger.info("Connected successfully! Listening for live ticker frames...")
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < duration_seconds:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    data = json.loads(message)
                    logger.info(f"[STREAM PACKET] Ticker: {data.get('ticker', 'N/A')} | Price: ${data.get('price', 0):.2f} | Change: {data.get('change_pct', 0):+.2f}%")
                except asyncio.TimeoutError:
                    logger.warning("Heartbeat timeout waiting for message. Sending ping...")
                    await ws.ping()
                    
    except ConnectionRefusedError:
        logger.error(f"Could not connect to {WS_URL}. Ensure the FastAPI server is running via 'uvicorn src.api.main:app --port 8000'")
    except Exception as e:
        logger.error(f"WebSocket test encountered error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_feed())

