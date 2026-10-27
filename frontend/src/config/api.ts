// Detect API base URL from Vite environment or default to localhost:8000
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_URL = `${API_BASE}/api/v1`;

// Calculate WebSocket URL dynamically based on current protocol and host
export const WS_URL = (() => {
  if (import.meta.env.VITE_WS_URL) {
    return import.meta.env.VITE_WS_URL;
  }
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    const isHttps = window.location.protocol === 'https:';
    return `${isHttps ? 'wss:' : 'ws:'}//${window.location.host}/ws`;
  }
  return 'ws://localhost:8000/ws';
})();

export const FALLBACK_PRICES: Record<string, { price: number; change: string }> = {
  NVDA: { price: 212.01, change: '+3.27%' },
  AMD:  { price: 164.20, change: '+1.92%' },
  AAPL: { price: 254.18, change: '-0.83%' },
  TSLA: { price: 421.52, change: '+2.11%' },
  MSFT: { price: 511.24, change: '+0.74%' },
};

export const SUPPORTED_TICKERS = ['NVDA', 'AMD', 'AAPL', 'TSLA', 'MSFT'] as const;
