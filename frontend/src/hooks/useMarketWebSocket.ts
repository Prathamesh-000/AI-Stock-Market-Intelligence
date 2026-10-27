import { useState, useEffect, useRef } from 'react';
import { WS_URL } from '../config/api';
import { Prediction } from '../types';

interface UseMarketWebSocketOptions {
  onMessage?: (prediction: Prediction) => void;
}

export function useMarketWebSocket({ onMessage }: UseMarketWebSocketOptions = {}) {
  const [isConnected, setIsConnected] = useState(false);
  const onMessageRef = useRef(onMessage);
  onMessageRef.current = onMessage;

  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: ReturnType<typeof setTimeout>;

    function connect() {
      try {
        ws = new WebSocket(WS_URL);

        ws.onopen = () => {
          setIsConnected(true);
        };

        ws.onclose = () => {
          setIsConnected(false);
          // Auto-reconnect after 3 seconds if disconnected
          reconnectTimeout = setTimeout(connect, 3000);
        };

        ws.onerror = (err) => {
          console.error('WebSocket Error:', err);
          ws?.close();
        };

        ws.onmessage = (event) => {
          try {
            const data: Prediction = JSON.parse(event.data);
            if (onMessageRef.current) {
              onMessageRef.current(data);
            }
          } catch (e) {
            console.error('Failed to parse WebSocket message:', e);
          }
        };
      } catch (err) {
        console.error('WebSocket initialization error:', err);
        reconnectTimeout = setTimeout(connect, 3000);
      }
    }

    connect();

    return () => {
      clearTimeout(reconnectTimeout);
      if (ws) {
        ws.onclose = null; // Prevent reconnect on unmount
        ws.close();
      }
    };
  }, []);

  return { isConnected };
}

