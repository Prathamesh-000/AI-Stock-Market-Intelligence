# Data Flow Architecture

## High-Level Data Flow

```
External Sources                  Processing                    Storage
──────────────                    ──────────                    ───────
RSS News Feeds ──────────────────► LLM Processor ─────────────► SQLite DB
Yahoo Finance ───────────────────► Feature Engineering ────────► Vector Store
OpenAI API ──────────────────────► XGBoost Models ─────────────► JSON Models
                                           │
                                           ▼
                                    FastAPI Backend
                                           │
                              ┌────────────┴────────────┐
                              │                         │
                         REST API                  WebSocket
                              │                         │
                         React Frontend ◄───────────────┘
```

## Request Flow (Prediction)

```
1. User enters headline in UI
2. POST /api/v1/predict
3. Backend:
   a. LLM extracts structured features
   b. RAG retrieves historical analogues  
   c. Fetch yfinance technicals
   d. Assemble feature vector
   e. XGBoost predicts direction + probs
   f. Calibrator refines probabilities
   g. Compute 5 scores
   h. Generate trading signal
   i. Log to SQLite
   j. Broadcast via WebSocket
4. Return JSON response to frontend
5. Frontend animates score cards
6. History chart updates
```

## Live Price Flow

```
1. Frontend polls /api/v1/live-prices every 15s
2. Backend fetches yfinance.download() for all tickers
3. Returns {ticker: {price, change, change_pct}}
4. Frontend updates price ticker bar
```

## WebSocket Flow

```
1. Frontend connects to /ws/prices
2. Backend streams price updates every 5s
3. Frontend receives {ticker, price, timestamp}
4. Real-time chart updates
```

## Data Storage Schema

### SQLite: market_intelligence.db

**prediction_logs table**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| ticker | TEXT | Stock ticker |
| headline | TEXT | News headline |
| direction | TEXT | BULLISH/BEARISH/NEUTRAL |
| impact_score | REAL | 0-10 |
| sentiment_score | REAL | -1 to +1 |
| confidence_score | REAL | 0-100 |
| volatility_risk | REAL | 0-10 |
| rag_similarity | REAL | 0-100 |
| signal | TEXT | BUY/SELL/HOLD/etc |
| created_at | DATETIME | Timestamp |

### Vector Store: data/vector_store/

- `historical_news_embeddings.npy` — numpy array (N × 1536)
- `historical_news_metadata.json` — list of {headline, ticker, date, direction, return_pct}
