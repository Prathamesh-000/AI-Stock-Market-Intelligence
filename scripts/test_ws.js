/**
 * Node.js WebSocket test client for AI Stock Market Intelligence
 * Run with: node scripts/test_ws.js
 */

const WebSocket = require('ws');

const WS_URL = 'ws://localhost:8000/api/v1/ws';
console.log(`[INFO] Attempting to connect to ${WS_URL}...`);

const ws = new WebSocket(WS_URL);

ws.on('open', function open() {
  console.log('[SUCCESS] Connected to live market streaming server.');
});

ws.on('message', function incoming(data) {
  try {
    const payload = JSON.parse(data.toString());
    console.log(`[LIVE FEED] ${payload.ticker || 'SYS'}: $${Number(payload.price || 0).toFixed(2)} (${payload.change_pct || '+0.00%'})`);
  } catch (err) {
    console.log(`[RAW PACKET] ${data}`);
  }
});

ws.on('error', function error(err) {
  console.error('[ERROR] WebSocket connection error:', err.message);
  console.log('[TIP] Make sure the backend server is running on http://localhost:8000');
});

ws.on('close', function close() {
  console.log('[CLOSED] Disconnected from market stream.');
});

