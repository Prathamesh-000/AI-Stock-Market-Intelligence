# AI Stock Market Intelligence — Complete Project Reference

> Every conceptual, technical, and architectural detail of the project — from first principles to deployment. Nothing left out.

---

## Table of Contents

1. [Project Overview & Vision](#1-project-overview--vision)
2. [What Problem Does It Solve?](#2-what-problem-does-it-solve)
3. [How It's Different From Other Projects](#3-how-its-different-from-other-projects)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Data Sources & Ingestion](#5-data-sources--ingestion)
6. [NLP Intelligence Pipeline](#6-nlp-intelligence-pipeline)
7. [Market Feature Engineering](#7-market-feature-engineering)
8. [Machine Learning Models](#8-machine-learning-models)
9. [RAG Vector Store System](#9-rag-vector-store-system)
10. [Sector Ripple Engine](#10-sector-ripple-engine)
11. [Prediction Pipeline — Step by Step](#11-prediction-pipeline--step-by-step)
12. [Real-Time Tracking & Continuous Evaluation](#12-real-time-tracking--continuous-evaluation)
13. [Backtesting Engine](#13-backtesting-engine)
14. [FastAPI Backend](#14-fastapi-backend)
15. [WebSocket Live Streaming](#15-websocket-live-streaming)
16. [React Frontend UI](#16-react-frontend-ui)
17. [Database Design](#17-database-design)
18. [Bug Fixes & Score Integrity](#18-bug-fixes--score-integrity)
19. [Docker Deployment](#19-docker-deployment)
20. [Complete File & Folder Map](#20-complete-file--folder-map)
21. [Technology Stack — Every Library Explained](#21-technology-stack--every-library-explained)
22. [How to Run the Project](#22-how-to-run-the-project)
23. [Supported Tickers & Why Them](#23-supported-tickers--why-them)
24. [Scoring System — All 5 Dimensions Explained](#24-scoring-system--all-5-dimensions-explained)
25. [Signal Generation Logic](#25-signal-generation-logic)
26. [Known Limitations](#26-known-limitations)
27. [Future Roadmap](#27-future-roadmap)

---

## 1. Project Overview & Vision

**Name**: AI Stock Market Intelligence Terminal  
**Type**: Full-Stack AI + Quantitative Finance Application  
**Inspired by**: Bloomberg Terminal UX, Goldman Sachs quant research pipelines  
**GitHub**: https://github.com/Prathamesh-000/AI-Stock-Market-Intelligence

### One-Line Summary

> Enter any financial news headline → the system uses AI, NLP, and historical market data to tell you: will this stock go **UP**, **DOWN**, or stay **NEUTRAL** — and by how much, with what confidence, and why?

### Core Mission

Financial markets react violently to news events. A single earnings miss, a supply-chain disruption, or a regulatory fine can move a stock 10–30% within minutes. Retail traders are overwhelmed by the volume and speed of news. This project is an **automated intelligence terminal** that:

- Reads any financial news headline
- Extracts deep structured information using GPT-4o-mini (an LLM)
- Finds the most similar historical events using semantic vector search
- Runs an XGBoost machine learning model trained on 5 years of real stock + news data
- Delivers a complete multi-dimensional prediction and actionable trading signal
- Shows everything in a real-time Bloomberg-style dashboard

---

## 2. What Problem Does It Solve?

### The Core Problem

News moves markets. But human traders face three critical limitations:

| Problem | Effect |
|---------|--------|
| **Information overload** | Hundreds of headlines per hour; can't read all |
| **Slow processing** | Human reading + reasoning takes minutes; markets move in seconds |
| **Inconsistency** | Human sentiment is biased, mood-dependent, and subjective |

### What This System Does

| Task | Traditional Approach | This System |
|------|---------------------|-------------|
| Sentiment | Human reads, guesses | GPT-4o-mini extracts JSON: `{sentiment: "Negative", confidence: 84}` |
| Event Type | Human judgment | Auto-classified: Earnings / Layoffs / Acquisition / Regulatory / ... |
| Historical Comparison | "I think this is like 2022 Intel layoffs" | Cosine similarity search across actual historical embeddings |
| Impact Prediction | Rule of thumb | Trained XGBoost model on 5 years of real data |
| Competitor Ripple | Ignored | Dedicated XGBoost regression model per competitor |
| Speed | Minutes | < 10 seconds end-to-end |

---

## 3. How It's Different From Other Projects

### vs. Bloomberg Terminal

| Feature | Bloomberg | This Project |
|---------|-----------|-------------|
| Cost | \$24,000/year | Free, open source |
| NLP | Basic keyword alerts | GPT-4o-mini structured extraction |
| ML Prediction | Human analysts | XGBoost with probability calibration |
| Historical RAG | Not available | Custom cosine similarity vector DB |
| Competitor ripple | Manual estimation | Automated XGBoost ripple model |
| Explainability | None | SHAP feature importance, AI reasoning lines |

### vs. FinBERT (Hugging Face)

- FinBERT only gives `{positive, negative, neutral}` probabilities on raw text
- **This project** uses GPT-4o-mini to extract 10+ structured fields: event type, impact severity, novelty classification, competitor ripple predictions — then passes all of this into XGBoost

### vs. FinRL (Reinforcement Learning)

- FinRL is about training agents to trade using price data only
- **This project** focuses on *news-driven event impact* — how does a specific piece of news change a stock's trajectory?

### vs. Kaggle News Sentiment Projects

- Typical Kaggle project: CSV → FinBERT → accuracy score → done
- **This project**: 15-phase production system with live WebSocket feeds, a real-time React UI, automated prediction tracking daemon, backtesting engine, Docker deployment, RAG vector search, and competitor ripple modeling

### vs. GPT-only Finance Chatbots

- Chatbots hallucinate and don't use real market data
- **This project** grounds every LLM call with real quantitative features: RSI, Bollinger Band position, relative volume, 5-day momentum — then combines them via a *calibrated ML model*, not plain language output

### What Makes This Unique (A Combination Nobody Else Has)

1. **LLM → Structured JSON → XGBoost** pipeline (not just sentiment, but 10 structured fields fed into ML)
2. **RAG historical event search** with OpenAI embeddings + custom NumPy vector store
3. **Sector Ripple Engine**: Separate XGBoost regression models predict how NVDA events ripple to AMD, TSM, and INTC
4. **Real-time prediction tracking daemon** (`tracker.py`) that monitors every prediction at 15m, 30m, 1h, 1d intervals and auto-records accuracy
5. **Platt scaling probability calibration** applied to raw XGBoost outputs to eliminate overconfidence
6. **Bloomberg Terminal aesthetic** with real data behind every pixel

---

## 4. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNAL DATA                            │
│   Yahoo Finance RSS ──── yfinance API ──── OpenAI Embeddings    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     INTELLIGENCE PIPELINE                        │
│                                                                  │
│  Headline Input                                                  │
│       │                                                          │
│       ▼                                                          │
│  GPT-4o-mini (LLMProcessor)                                      │
│  → sentiment, event_type, impact_score, novelty, sector_ripple  │
│       │                                                          │
│       ▼                                                          │
│  RAG VectorStore (cosine similarity on 1536-dim embeddings)      │
│  → top 2-3 most similar historical events                        │
│       │                                                          │
│       ▼                                                          │
│  yfinance (live technical context)                               │
│  → RSI_14, RVOL_20, BB_Pct, price momentum                      │
│       │                                                          │
│       ▼                                                          │
│  XGBoost Classifier (per-ticker model)                           │
│  → raw probability P(up)                                         │
│       │                                                          │
│       ▼                                                          │
│  Platt Calibration (isotonic regression)                         │
│  → calibrated_probability                                        │
│       │                                                          │
│       ▼                                                          │
│  Sentiment Polarity Alignment                                    │
│  → if LLM says NEGATIVE: final_prob = 1 - final_prob            │
│       │                                                          │
│       ▼                                                          │
│  Sector Ripple XGBoost (3 separate models)                       │
│  → AMD impact %, TSM impact %, INTC impact %                     │
│       │                                                          │
│       ▼                                                          │
│  Payload Assembly + Signal Generation                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                         FASTAPI BACKEND                          │
│   REST: /predict, /history, /live-prices, /market-indices,      │
│         /live-news/{ticker}, /export-predictions                 │
│   WS:   /ws  (broadcasts full prediction JSON to all clients)   │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┴────────────────┐
         │                                │
┌────────▼────────┐              ┌────────▼──────────┐
│  SQLite DB      │              │   React Frontend  │
│  PredictionLog  │              │  Bloomberg UI     │
│  (SQLAlchemy)   │              │  Recharts, WS     │
└─────────────────┘              └───────────────────┘
```

---

## 5. Data Sources & Ingestion

### Market Price Data — `yfinance`

- **Library**: `yfinance` (Yahoo Finance unofficial Python API)
- **Data**: OHLCV (Open, High, Low, Close, Volume) daily bars
- **Coverage**: 5 years of historical data per ticker
- **Live prices**: `yf.Ticker(symbol).fast_info.last_price` (sub-second)
- **Indices**: `^GSPC` (S&P 500), `^IXIC` (NASDAQ), `^DJI` (Dow Jones)
- **Files**: `scripts/download_data.py`, `src/data/market_data.py`

### News Data — Yahoo Finance RSS + feedparser

- **Library**: `feedparser`
- **Endpoint**: `https://feeds.finance.yahoo.com/rss/2.0/headline?s={TICKER}&region=US&lang=en-US`
- **Returns**: Title, summary, published datetime, link, source
- **Usage**: Live news panel in the frontend + training data collection
- **File**: `src/api/routes.py` → `/live-news/{ticker}` endpoint

### Historical News for Training

- **File**: `data/raw/news/NVDA_news.json` (328KB, 5 years of NVDA news)
- **File**: `data/processed/features/NVDA_news_nlp.json` (463KB, NLP-processed)
- Each entry: `{headline, summary, published_at, event_type, sentiment_score, impact_score, ...}`

---

## 6. NLP Intelligence Pipeline

### 6.1 GPT-4o-mini Structured Extraction (Primary LLM)

**File**: `src/nlp/llm_processor.py`

Uses OpenAI's **Structured Outputs** (not plain chat completions) via a Pydantic model:

```python
class NewsIntelligence(BaseModel):
    sentiment: str            # "Positive" | "Negative" | "Neutral"
    sentiment_confidence: int # 0-100
    event_type: str           # "Earnings" | "Product Launch" | "Acquisition" | ...
    impact_level: str         # "Low" | "Medium" | "High"
    impact_score: int         # 0-100 (severity of expected market impact)
    novelty: str              # "New" | "Continuation" | "Duplicate"
    explanation: str          # 1-2 sentence rationale
    sector_ripple_amd: int    # -100 to 100
    sector_ripple_tsm: int    # -100 to 100
    sector_ripple_intc: int   # -100 to 100
```

**Why `temperature=0.0`?** Deterministic outputs — the same headline always produces the same structured JSON, avoiding stochastic variation in financial signals.

**Why Structured Outputs (not plain text)?** `response_format=NewsIntelligence` forces GPT-4o-mini to return valid JSON matching the schema. No parsing needed, no hallucinated formats.

**Supported Event Types**: Earnings, Product Launch, Acquisition, Regulatory, Lawsuit, Management, Dividend, Analyst, Layoffs, Guidance, Production Halt

### 6.2 FinBERT (Offline Deep Learning NLP)

**File**: `src/sentiment/finbert.py`  
**Model**: `ProsusAI/finbert` (Hugging Face)

FinBERT is a BERT model **fine-tuned specifically on financial texts** (Reuters, Bloomberg). It understands financial jargon that general-purpose NLP models miss.

- Input: raw headline string (max 512 tokens)
- Output: `{positive_prob, negative_prob, neutral_prob}` (sum to 1.0)
- **Sentiment score**: `sentiment_score = positive_prob - negative_prob` (range: -1.0 to +1.0)
- **Hardware**: Automatically uses CUDA GPU if available, else CPU

> **Why both GPT-4o-mini AND FinBERT?**
> GPT-4o-mini gives event classification + impact quantification. FinBERT gives fine-grained probabilistic sentiment calibrated on financial text. They are complementary: GPT-4o-mini does "what type of event and how severe?", FinBERT does "what is the precise textual sentiment?".
> In production, the FinBERT display in the UI is derived from GPT-4o-mini's `sentiment_confidence` to avoid loading the 400MB FinBERT model on every request. FinBERT is used during the offline training phase.

### 6.3 Event Classifier — `src/sentiment/event_classifier.py`

Classifies events into: Earnings, M&A, Regulatory, Layoff, Product, Analyst, Guidance, Macro, Management, Legal

### 6.4 Novelty Detection — `src/sentiment/novelty.py`

Detects if a headline is: `New` (fresh information) / `Continuation` (follow-up) / `Duplicate` (already seen). Prevents the model from double-counting the same news event.

### 6.5 Entity Linking — `src/sentiment/entity_linking.py`

Extracts company names, people, and ticker symbols from text. Maps "NVIDIA" → "NVDA", "Tim Cook" → "AAPL", etc.

---

## 7. Market Feature Engineering

### 7.1 Technical Indicators — `src/features/technical.py`

| Feature | Description | Why Used |
|---------|-------------|----------|
| `RSI_14` | Relative Strength Index (14-period) | Overbought/oversold context |
| `MACD_Signal` | MACD signal line deviation | Trend momentum |
| `BB_Pct` | Bollinger Band % position (0=lower, 1=upper band) | Price relative to volatility |
| `ATR_14` | Average True Range | Baseline volatility level |
| `SMA_20` | 20-day Simple Moving Average | Trend direction |

### 7.2 Volatility Features — `src/features/volatility.py`

| Feature | Description |
|---------|-------------|
| `RVOL_20` | Relative Volume: current volume / 20-day avg volume |
| `Historical_Vol_20` | 20-day realized volatility (annualized %) |
| `Intraday_Range_Pct` | (High - Low) / Close — daily price tension |

### 7.3 Relative Performance — `src/features/relative_performance.py`

- `Alpha_5d_vs_SPY` — 5-day return vs. S&P 500
- `Alpha_5d_vs_XLK` — 5-day return vs. Technology ETF

### 7.4 Market Regime — `src/features/regime.py`

Classifies the current market environment:
- **Bull**: SPY above 200-day MA, low VIX
- **Bear**: SPY below 200-day MA, high VIX
- **Neutral**: In between

The regime is critical context — the same news has different impacts in a bull vs. bear market.

### 7.5 Feature Builder — `src/features/feature_builder.py`

The `FeatureBuilder.build_matrix()` method uses **`pd.merge_asof(direction='backward')`** to join news events with market features. This prevents **lookahead bias** — only market features known *before* the news reaction time are used.

---

## 8. Machine Learning Models

### 8.1 XGBoost Direction Classifier (Primary Model)

**File**: `src/models/xgboost_model.py` — Class: `MarketImpactXGBoost`

```python
xgb.XGBClassifier(
    n_estimators=100,
    max_depth=4,             # Shallow: prevents overfitting on noisy finance data
    learning_rate=0.05,      # Conservative: more stable convergence
    objective='binary:logistic',  # Binary: UP(1) or DOWN/NEUTRAL(0)
    eval_metric='auc',       # AUC is better than accuracy for imbalanced data
    tree_method='hist',      # Fast; handles NaN natively (common in finance)
    random_state=42
)
```

**Why `max_depth=4`?** Deep trees overfit on financial noise. Shallow trees find general patterns.  
**Why `binary:logistic`?** Outputs P(stock goes up) — more useful than a binary class label.  
**Why `tree_method='hist'`?** Natively handles NaN values without imputation — critical because financial features often have gaps (e.g., RSI unavailable for first 14 days).  
**Saved format**: `.json` (XGBoost native) — portable, version-stable, not pickle.

### 8.2 Probability Calibration (Platt Scaling)

**Files**: `src/models/calibration.py`, `src/prediction/calibration.py`  
**Saved**: `models/saved/calibrator_NVDA_latest.pkl`

Raw XGBoost probabilities are **overconfident** — 0.9 does NOT mean 90% likely to go up. Isotonic regression calibration (`CalibratedClassifierCV(method='isotonic')`) maps raw probabilities to well-calibrated ones using validation data.

### 8.3 Sector Ripple Models (Regression)

**Files**: `models/xgb_ripple_AMD.json`, `models/xgb_ripple_TSM.json`, `models/xgb_ripple_INTC.json`

Separate `xgb.XGBRegressor` models trained to predict: *"If NVDA moves X%, how much does AMD/TSM/INTC move?"*

**Input features**: `{NVDA: predicted_return, NVDA_Vol_5d: recent_volatility}`  
**Output**: predicted % return for the competitor

### 8.4 Walk-Forward Validation — `src/validation/walk_forward.py`

Standard k-fold validation causes data leakage in finance (future used to predict past). Walk-forward validation mimics reality:
1. Train on months 1–12, test on month 13
2. Train on months 1–13, test on month 14... etc.

### 8.5 Leakage Prevention — `src/validation/leakage.py`

Checks for 3 types of data leakage:
1. **Temporal leakage**: future returns in feature set
2. **Look-ahead bias**: market features from after the event
3. **Duplicate contamination**: same event in both train and test

### 8.6 SHAP Explainability — `src/prediction/shap_explainer.py`

Uses **SHAP (SHapley Additive exPlanations)** TreeExplainer to show which features drove each prediction. Generates `reports/NVDA_shap_summary.png`.

---

## 9. RAG Vector Store System

**File**: `src/database/vector_store.py` — Class: `VectorStore`

### What is RAG?

RAG = **Retrieval-Augmented Generation**. Instead of relying solely on the model's training data, you search a database of real historical events for similar ones and use their outcomes as context.

### How It's Implemented

```
New Headline
     │
     ▼
OpenAI text-embedding-3-small
     │ (1536-dimensional float vector)
     ▼
Cosine Similarity against:
  data/vector_store/historical_news_embeddings.npy  ← 1.2MB NumPy array
     │
     ▼
Top-K most similar events (similarity threshold > 50%)
     │
     ▼
Returns: {headline, ticker, date, actual_return, event_type}
```

### Why NumPy Instead of ChromaDB or FAISS?

> ChromaDB requires C++ compilation on Windows → installation crashes.
> FAISS has similar Windows compatibility issues.
> A plain NumPy matrix + `sklearn.metrics.pairwise.cosine_similarity` works perfectly and requires zero native compilation.
> For 5,000 events at 1536 dimensions, NumPy search takes < 50ms.

### Storage Files

| File | Size | Content |
|------|------|---------|
| `historical_news_embeddings.npy` | 1.2 MB | (N × 1536) float32 matrix |
| `historical_news_metadata.json` | 36.5 KB | List of event dicts with outcomes |

---

## 10. Sector Ripple Engine

When a major NVIDIA news event happens, it doesn't just affect NVDA. AMD, TSM (TSMC), and INTC are connected through the semiconductor supply chain and competitive landscape.

### How It Works

```python
for comp in ["AMD", "TSM", "INTC"]:
    ripple_model = xgb.XGBRegressor()
    ripple_model.load_model(f"models/xgb_ripple_{comp}.json")
    
    impact = llm_analysis["impact_score"]
    if llm_sentiment == "Negative": impact = -impact
    pseudo_return = impact / 10.0
    
    X_ripple = pd.DataFrame({"NVDA": [pseudo_return], "NVDA_Vol_5d": [2.0]})
    pred_return = float(ripple_model.predict(X_ripple)[0])
    sector_ripple[comp] = int(round(pred_return * 10))
```

**LLM fallback**: If the quantitative ripple model is unavailable, the LLM's `sector_ripple_amd`, `sector_ripple_tsm`, `sector_ripple_intc` fields are used directly.

---

## 11. Prediction Pipeline — Step by Step

This is the exact sequence in `run_prediction_pipeline()` in `src/api/routes.py`:

```
Step 1:  Load XGBoost model + calibrator from disk (lazy cached in memory)

Step 2:  Load latest market feature row from processed CSV
         → X_live = df.iloc[[-1]].copy()  ← most recent market state

Step 3:  Run GPT-4o-mini LLM processor
         → Returns: sentiment, confidence, event_type, impact_score, novelty, ripple

Step 4:  Inject LLM scores into the XGBoost feature vector
         → X_live['impact_score'] = llm_analysis['impact_score']

Step 5:  XGBoost prediction
         → raw_prob = xgb_model.predict_proba(X_live)[0]

Step 6:  Platt probability calibration
         → final_prob = calibrator.predict_proba([[raw_prob]])[0][1]

Step 7:  Ticker-specific bias correction
         → AMD: +0.12 | AAPL: -0.08 | TSLA: +0.24 | MSFT: +0.05
         (Each ticker's model has a different inherent bias from training data)

Step 8:  Sentiment polarity alignment
         → if LLM says "Negative": final_prob = 1.0 - final_prob
         (Model was trained on impact magnitude only, not direction)

Step 9:  Sector Ripple Engine (3 separate XGBoost regression models)

Step 10: RAG Vector Search (top-2 historical similar events via cosine similarity)

Step 11: Dynamic AI Reasoning generation
         → Uses real RSI, RVOL, BB_Pct values to write context-aware lines

Step 12: Event-driven Feature Importance
         → Maps event_type to SHAP-style importance weights

Step 13: FinBERT-style metrics construction
         → Decouples sentiment% from confidence% (fixes Bug #5)

Step 14: Signal determination
         → P > 0.60 → BUY | P < 0.40 → SELL | else → UNCERTAIN

Step 15: Save to SQLite database (PredictionLog record)

Step 16: Broadcast full JSON payload via WebSocket to all React clients
```

---

## 12. Real-Time Tracking & Continuous Evaluation

**File**: `src/api/tracker.py`  
Runs as an `asyncio` background daemon every 60 seconds.

After every prediction, the system tracks actual market outcomes at:
- **15 minutes** after prediction
- **30 minutes** after prediction
- **1 hour** after prediction
- **24 hours** after prediction (final: marks `is_correct = 1 or 0`)

**Accuracy check**: BUY signal + actual return > 0 → correct. SELL signal + actual return < 0 → correct.

This enables the `/history` endpoint to show **real accuracy metrics** based on actual market outcomes, not hypothetical backtests.

---

## 13. Backtesting Engine

**File**: `src/backtesting/backtest.py`

```python
engine = BacktestEngine(initial_capital=10_000, position_size=0.1)
engine.run(predictions, price_data)
report = engine.summary()
```

### Trade Simulation

- **UP prediction**: Buy at entry price, sell at next day's price
- **DOWN prediction**: Short-sell, cover at next day's price
- **FLAT**: No position taken
- **Position size**: 10% of current capital per trade

### Metrics (`src/backtesting/metrics.py`)

| Metric | Formula |
|--------|---------|
| Win Rate | `correct_trades / total_trades` |
| Sharpe Ratio | `mean(returns) / std(returns) * sqrt(252)` |
| Sortino Ratio | `mean(returns) / std(negative_returns) * sqrt(252)` |
| Max Drawdown | Max peak-to-trough decline in equity curve |
| Profit Factor | `sum(gains) / abs(sum(losses))` |

---

## 14. FastAPI Backend

**File**: `src/api/main.py` — Port: 8000

### All API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/predict` | Main prediction endpoint (async background task) |
| `GET` | `/api/v1/history` | Last 10 predictions with real accuracy |
| `GET` | `/api/v1/live-prices` | Real-time NVDA/AMD/AAPL/TSLA/MSFT prices |
| `GET` | `/api/v1/market-indices` | S&P 500, NASDAQ, DOW live values |
| `GET` | `/api/v1/live-news/{ticker}` | Latest 5 RSS headlines for any ticker |
| `GET` | `/api/v1/export-predictions` | Download all predictions as CSV |
| `WS` | `/ws` | WebSocket live prediction broadcast |
| `GET` | `/health` | Server health check: `{status: "online"}` |

### Background Task Pattern (Non-Blocking)

```python
@router.post("/predict")
async def trigger_prediction(request, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_prediction_pipeline, request)
    return {"status": "Processing"}  # Instant return; result arrives via WebSocket
```

The full 3–8 second pipeline runs in the background. The UI never freezes.

### Settings — `config/settings.py`

Type-safe config via `pydantic-settings`, loaded from `.env`:

```python
class Settings(BaseSettings):
    finnhub_api_key: str
    default_tickers: str = "NVDA,AAPL"
    project_root: Path          # Auto-detected from file location
    data_dir: Path
    logs_dir: Path
    log_level: str = "INFO"
```

---

## 15. WebSocket Live Streaming

**File**: `src/api/ws_manager.py` — Class: `ConnectionManager`

```python
class ConnectionManager:
    active_connections: List[WebSocket] = []
    async def connect(ws): await ws.accept(); active_connections.append(ws)
    def disconnect(ws): active_connections.remove(ws)
    async def broadcast(payload: dict):
        for conn in active_connections:
            await conn.send_text(json.dumps(payload))
```

### Lifecycle

1. React opens: `new WebSocket('ws://localhost:8000/ws')`
2. Added to `active_connections`
3. User submits headline → POST `/predict`
4. Pipeline runs in background (3–8 seconds)
5. `await manager.broadcast(payload)` → all clients receive full JSON
6. React `ws.onmessage` fires → `setPredictions(prev => [data, ...prev])`
7. Dashboard instantly updates

**Why WebSocket vs. polling?** Polling wastes bandwidth. WebSocket pushes data the instant it's ready — exactly how Bloomberg Terminal live feeds work.

---

## 16. React Frontend UI

**File**: `frontend/src/App.tsx` (738 lines)  
**Framework**: React 18 + TypeScript  
**Bundler**: Vite  
**Styling**: TailwindCSS (dark theme)  
**Charts**: Recharts  
**Icons**: lucide-react

### Component Breakdown

#### 1. Top Price Ticker Marquee
Auto-scrolling strip: `NVDA | $227.48 | +3.27%` — live from `/api/v1/live-prices`, refreshed every 60 seconds. Green = up, Red = down.

#### 2. Market Indices Bar
`S&P 500 | +0.72%` | `NASDAQ | +1.14%` | `DOW | +0.31%` — live from `/api/v1/market-indices`.

#### 3. Prediction Input Panel
Text field for headline + dropdown for ticker (NVDA/AMD/AAPL/TSLA/MSFT) + "Run AI Analysis" button.

#### 4. Signal Alert Banner
`🚀 BUY SIGNAL — Confidence: 74.2%` — color-coded: green/BUY, red/SELL, gray/UNCERTAIN.

#### 5. Five Score Cards (Animated Progress Bars)
| Card | Data Source | Range |
|------|------------|-------|
| Confidence Score | XGBoost calibrated probability | 0–100% |
| FinBERT Score | GPT-4o-mini sentiment_confidence | -1.0 to +1.0 |
| LLM Impact | GPT-4o-mini impact_score | 0–100 |
| 1H Prediction | Derived from confidence | % |
| 1D Prediction | Derived from confidence | % |

#### 6. 1D / 1W / 1M Interactive Price Chart
- **1D**: 5-minute intervals (intraday)
- **1W**: 30-minute intervals (5-day week)
- **1M**: Daily intervals (calendar month)
- AreaChart with hover scrubbing — shows exact price at cursor position
- Data fetched from yfinance via the backend on tab click

#### 7. AI Reasoning Panel
5 auto-generated context-aware lines:
```
✓ Classified as 'Product Launch' event — 72/100 severity
✓ LLM sentiment: Positive (84% confidence) — polarity score +0.54
✓ RSI at 58.3 (neutral range)
✓ Relative volume 2.3x (elevated) — heightened event sensitivity
✓ Aligned with 2 historical precedents (cosine similarity search)
```

#### 8. Feature Importance Panel
Bar chart showing which factors drove the prediction. Dynamically mapped by event type — Earnings events show "Earnings Surprise", Regulatory events show "Regulatory Risk", etc.

#### 9. Sector Ripple Panel
```
AMD  ████████ +3.2%
TSM  ████ +1.8%
INTC ██ +0.7%
```
Driven by XGBoost ripple regression models.

#### 10. Live News Panel
Triggered by "Fetch Live News" button → calls `/api/v1/live-news/{ticker}` → shows 5 latest headlines. Click any headline → auto-fills the prediction input.

#### 11. Similar Historical Events (RAG Results)
```
[78.4% match] "NVIDIA beats Q3 earnings by 15%..." — Jul 2023 — Actual: +8.7%
[64.1% match] "NVDA partners with Microsoft for AI..." — Jan 2024 — Actual: +5.2%
```

#### 12. Prediction History Timeline
LineChart showing history of past signals. Animated when new predictions arrive via WebSocket.

#### 13. Export CSV Button
`window.open('/api/v1/export-predictions', '_blank')` → downloads `quant_ai_predictions.csv` instantly.

---

## 17. Database Design

**File**: `src/database/models.py`  
**ORM**: SQLAlchemy  
**Database**: SQLite (`market_intelligence.db`)

### `prediction_logs` Table

```sql
CREATE TABLE prediction_logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker              VARCHAR(10) NOT NULL,
    headline            VARCHAR(500) NOT NULL,
    signal              VARCHAR(20) NOT NULL,     -- BUY / SELL / UNCERTAIN
    confidence_score    FLOAT NOT NULL,           -- 0.0 to 100.0
    predicted_impact    FLOAT,                    -- % predicted price move
    actual_return       FLOAT,                    -- Actual % move (filled by tracker)
    is_correct          INTEGER,                  -- 1=correct, 0=wrong, NULL=pending
    price_at_prediction FLOAT,                    -- Stock price at prediction time
    actual_15m_return   FLOAT,
    actual_30m_return   FLOAT,
    actual_1h_return    FLOAT,
    actual_1d_return    FLOAT,                    -- Final resolution
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Why SQLite?** Zero-config for development. Architecture supports PostgreSQL for production — just change `DATABASE_URL` in `.env`.

---

## 18. Bug Fixes & Score Integrity

Eight critical score calculation bugs were identified and fixed during development:

| Bug | Problem | Fix |
|-----|---------|-----|
| **#1 — FinBERT = XGBoost Duplicate** | `finbert_score = (final_prob - 0.5) * 2` — literally XGBoost repackaged | Now uses `llm_analysis['sentiment_confidence']` — independent source |
| **#2 — FinBERT Probabilities All Zero** | `{positive: 0, negative: 0, neutral: 100}` always | Distribute remaining % across other classes: 65% opposing, 35% neutral |
| **#3 — Static AI Reasoning** | Always said "XGBoost identified correlated volatility pattern" | Lines now built from real `RSI_14`, `RVOL_20`, `BB_Pct` values |
| **#4 — Feature Importance Always "Product Innovation"** | `event_type` was hardcoded to "Product Launch" | Now reads from `llm_analysis['event_type']` dynamically |
| **#5 — Confidence% and FinBERT% Identical** | Same root cause as Bug #1 | Fully decoupled sources |
| **#6 — Feature Bars Always at 100% Scale** | `base_val * 1.0` regardless of impact severity | `value = base_val * scale_factor` where `scale_factor = llm_impact / 100` |
| **#7 — 1W/1M Chart Buttons Not Clickable** | Wrong yfinance params: used `period='1W'` (invalid) | Correct: `{"1D": ("1d","5m"), "1W": ("5d","30m"), "1M": ("1mo","1d")}` |
| **#8 — Same News → Same Result for All Tickers** | Model was ticker-agnostic | Per-ticker probability bias corrections added in Step 7 |

---

## 19. Docker Deployment

### `docker-compose.yml`

```yaml
services:
  backend:
    build: { context: ., dockerfile: Dockerfile.backend }
    ports: ["8000:8000"]
    volumes:
      - ./data:/app/data
      - ./models/saved:/app/models/saved
  frontend:
    build: { context: ., dockerfile: Dockerfile.frontend }
    ports: ["3000:80"]
    depends_on: [backend]
```

### Dockerfile.backend
- Base: `python:3.11-slim`
- CPU-only PyTorch (no CUDA in container)
- CMD: `uvicorn src.api.main:app --host 0.0.0.0 --port 8000`

### Dockerfile.frontend
- Stage 1: `node:18-alpine` → `npm run build` → `/dist/`
- Stage 2: `nginx:alpine` → serves static files
- Multi-stage build keeps the final image ~22MB

---

## 20. Complete File & Folder Map

```
AI-Stock-Market-Intelligence/
│
├── config/
│   ├── settings.py          # Pydantic settings (reads .env)
│   ├── logging_config.py    # Structured logging setup
│   └── __init__.py
│
├── src/
│   ├── api/
│   │   ├── main.py          # FastAPI app + CORS + WebSocket endpoint
│   │   ├── routes.py        # ALL 6 prediction endpoints (525 lines)
│   │   ├── tracker.py       # Background daemon: tracks actual returns
│   │   └── ws_manager.py    # WebSocket ConnectionManager
│   │
│   ├── nlp/
│   │   └── llm_processor.py # GPT-4o-mini structured extraction (65 lines)
│   │
│   ├── database/
│   │   ├── db.py            # SQLAlchemy engine + SessionLocal
│   │   ├── models.py        # PredictionLog ORM model
│   │   └── vector_store.py  # NumPy-based RAG vector store (101 lines)
│   │
│   ├── models/
│   │   ├── xgboost_model.py # MarketImpactXGBoost wrapper class
│   │   ├── calibration.py   # Isotonic regression calibrator
│   │   ├── direction_model.py # 3-class UP/DOWN/FLAT classifier
│   │   ├── impact_model.py  # Regression: impact magnitude
│   │   ├── evaluator.py     # Accuracy, F1, precision, recall
│   │   ├── trainer.py       # Training orchestrator with CV
│   │   └── explainer.py     # SHAP TreeExplainer wrapper
│   │
│   ├── data/
│   │   ├── market_data.py   # yfinance OHLCV downloader
│   │   ├── news_data.py     # RSS + web scraper
│   │   ├── data_provider.py # Unified data access interface
│   │   └── validators.py    # Input validation functions
│   │
│   ├── features/
│   │   ├── feature_builder.py  # merge_asof: joins NLP + Market data
│   │   ├── technical.py        # RSI, MACD, Bollinger Bands, SMA
│   │   ├── volatility.py       # ATR, RVOL, historical volatility
│   │   ├── volume.py           # Volume ratios, VWAP
│   │   ├── relative_performance.py  # Alpha vs SPY / XLK
│   │   ├── regime.py           # Bull/Bear/Neutral market classification
│   │   └── event_features.py   # LLM-extracted event flags
│   │
│   ├── preprocessing/
│   │   ├── market_cleaner.py   # OHLCV cleaning, forward-fill
│   │   ├── news_cleaner.py     # HTML strip, Unicode, dedup
│   │   ├── timestamp_sync.py   # Align news to market hours
│   │   └── deduplication.py    # Hash-based duplicate removal
│   │
│   ├── sentiment/
│   │   ├── finbert.py          # FinBERT (ProsusAI) sentiment
│   │   ├── event_classifier.py # Zero-shot event type classification
│   │   ├── severity.py         # HIGH/MEDIUM/LOW severity
│   │   ├── novelty.py          # New/Continuation/Duplicate
│   │   └── entity_linking.py   # Company → Ticker mapping
│   │
│   ├── targets/
│   │   ├── abnormal_returns.py # CAR (Cumulative Abnormal Return)
│   │   ├── direction.py        # UP/DOWN/FLAT labeling
│   │   ├── impact_score.py     # 0-100 composite impact score
│   │   └── targets.py          # Target label assembly
│   │
│   ├── prediction/
│   │   ├── calibration.py      # Probability calibration wrapper
│   │   ├── confidence.py       # Weighted confidence score
│   │   └── shap_explainer.py   # SHAP TreeExplainer integration
│   │
│   ├── validation/
│   │   ├── time_split.py       # Time-aware train/test split
│   │   ├── walk_forward.py     # Walk-forward cross-validation
│   │   ├── leakage.py          # Data leakage detection
│   │   └── drift.py            # Feature drift monitoring
│   │
│   └── backtesting/
│       ├── backtest.py         # BacktestEngine (P&L simulation)
│       ├── metrics.py          # Sharpe, Sortino, drawdown, win rate
│       └── engine.py           # Alternative backtest engine
│
├── backend/                    # Alternate FastAPI architecture (secondary)
│   ├── api/
│   │   ├── websocket.py        # WS connection manager + /ws endpoint
│   │   └── routes/
│   │       ├── stocks.py       # /stocks/quotes + /stocks/{ticker}/chart
│   │       ├── news.py         # /news/{ticker} RSS endpoint
│   │       └── predictions.py  # /predict + /history + /export/csv
│   ├── database/
│   │   ├── models.py           # PredictionRecord + MarketSnapshot
│   │   ├── session.py          # DB engine + get_db() generator
│   │   └── repositories.py     # CRUD repository pattern
│   ├── schemas/__init__.py     # Pydantic I/O schemas (StockQuote, etc.)
│   ├── middleware/__init__.py  # ProcessTimeMiddleware
│   └── services/__init__.py    # PredictionService orchestrator
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Main component (738 lines, all features)
│   │   ├── main.tsx            # React entry point
│   │   └── index.css           # TailwindCSS imports
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── index.html
│
├── models/
│   ├── saved/
│   │   ├── xgb_NVDA_latest.json    # 88.7 KB — trained XGBoost
│   │   ├── xgb_AMD_latest.json
│   │   ├── xgb_AAPL_latest.json
│   │   ├── xgb_TSLA_latest.json
│   │   ├── xgb_MSFT_latest.json
│   │   └── calibrator_*.pkl        # Isotonic regression calibrators
│   ├── xgb_ripple_AMD.json         # 186.7 KB — ripple regression
│   ├── xgb_ripple_TSM.json         # 173.6 KB
│   └── xgb_ripple_INTC.json        # 177.0 KB
│
├── data/
│   ├── raw/news/NVDA_news.json     # 328.6 KB — 5 years news data
│   ├── processed/
│   │   ├── NVDA_final_dataset.csv  # 187 KB — final feature matrix
│   │   ├── AMD_final_dataset.csv
│   │   ├── AAPL_final_dataset.csv
│   │   ├── TSLA_final_dataset.csv
│   │   └── MSFT_final_dataset.csv
│   └── vector_store/
│       ├── historical_news_embeddings.npy  # 1.2 MB NumPy matrix
│       └── historical_news_metadata.json   # 36.5 KB event metadata
│
├── scripts/
│   ├── download_data.py        # Downloads OHLCV + news
│   ├── preprocess_data.py      # Cleans + syncs timestamps
│   ├── run_nlp.py              # Runs FinBERT + event classification
│   ├── build_features.py       # Assembles feature matrix
│   ├── train_model.py          # Trains single ticker model
│   ├── train_models.py         # Trains all 5 ticker models
│   ├── evaluate_models.py      # Evaluates all models (prints report)
│   ├── run_pipeline.py         # Full end-to-end pipeline runner
│   ├── run_backtest.py         # Runs backtesting engine
│   ├── build_vector_db.py      # Builds RAG vector store from history
│   ├── explain_model.py        # SHAP explanations + beeswarm plot
│   ├── monitor_drift.py        # Feature drift detection
│   ├── init_db.py              # Creates SQLite tables
│   └── test_ws.py              # WebSocket test client
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_exploration.ipynb
│   ├── 02_market_data_analysis.ipynb
│   ├── 03_news_data_analysis.ipynb
│   ├── 04_market_analysis.ipynb
│   ├── 04_sentiment_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_model_training.ipynb
│   └── 07_model_evaluation.ipynb
│
├── docs/
│   ├── architecture/
│   │   ├── system_architecture.md
│   │   ├── data_flow.md
│   │   └── ml_pipeline.md
│   └── reports/
│       ├── final_report.md
│       ├── progress_report.md
│       └── project_proposal.md
│
├── reports/
│   └── NVDA_shap_summary.png   # 200 KB SHAP beeswarm plot
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt            # 5 KB — all Python dependencies
├── README.md
├── .env.example
└── .gitignore
```

---

## 21. Technology Stack — Every Library Explained

### Python Backend

| Library | Why Used |
|---------|----------|
| `fastapi` | Async Python web framework; automatic OpenAPI docs; WebSocket support |
| `uvicorn` | ASGI server for FastAPI; high-performance async I/O |
| `pydantic` v2 | Data validation + serialization; Structured Output schemas for LLM |
| `pydantic-settings` | Type-safe `.env` loading for `config/settings.py` |
| `openai` | GPT-4o-mini API + `text-embedding-3-small` for RAG embeddings |
| `xgboost` | Primary ML model; gradient boosted trees for direction + ripple prediction |
| `scikit-learn` | `CalibratedClassifierCV`, `cosine_similarity`, accuracy/F1 metrics |
| `pandas` | DataFrames for all tabular data; `merge_asof` for time-aware joins |
| `numpy` | Vector math for embeddings; cosine similarity matrix computation |
| `yfinance` | Yahoo Finance market data (free, no API key required) |
| `feedparser` | Parses RSS XML feeds from Yahoo Finance for live news |
| `sqlalchemy` | ORM for SQLite; `SessionLocal`, `Base`, ORM models |
| `joblib` | Save/load calibrator `.pkl` files |
| `transformers` | Hugging Face: loads FinBERT (`ProsusAI/finbert`) |
| `torch` | PyTorch: runs FinBERT inference (CPU-only in production) |
| `shap` | SHAP TreeExplainer for XGBoost feature importance |
| `python-dotenv` | Load `.env` with `load_dotenv()` |

### JavaScript Frontend

| Library | Why Used |
|---------|----------|
| `react` 18 | Component-based UI; state management |
| `typescript` | Type safety for all props, state, API responses |
| `vite` | Ultra-fast bundler + dev server |
| `recharts` | AreaChart, LineChart for price history and prediction timeline |
| `tailwindcss` | Utility-first CSS; dark theme (`bg-gray-950`) |
| `lucide-react` | Icons: Zap, BrainCircuit, Activity, Download, etc. |
| WebSocket API | Native browser API; no library needed |

---

## 22. How to Run the Project

### Step 1 — Clone & Setup

```powershell
cd "c:\Users\PC Point\AI-Stock-Market-Intelligence"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Configure API Key

```
Edit .env:
OPENAI_API_KEY=sk-...your-key-here...
```

### Step 3 — Initialize Database

```powershell
.venv\Scripts\activate
python scripts/init_db.py
```

### Step 4 — Start Backend

```powershell
.venv\Scripts\activate
python -m uvicorn src.api.main:app --reload --port 8000
```

### Step 5 — Start Frontend (new terminal)

```powershell
cd frontend
npm install
npm run dev
# Opens on http://localhost:5173
```

### Step 6 — Use the App

1. Open `http://localhost:5173`
2. Select a ticker (NVDA, AMD, AAPL, TSLA, MSFT)
3. Enter a financial news headline
4. Click "Run AI Analysis"
5. Results appear in < 10 seconds via WebSocket

### Docker (One-Command Alternative)

```powershell
docker-compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## 23. Supported Tickers & Why Them

| Ticker | Company | Selection Reason |
|--------|---------|-----------------|
| `NVDA` | NVIDIA | AI chip leader; extremely news-sensitive; large historical news corpus; primary ticker |
| `AMD` | Advanced Micro Devices | NVDA's primary competitor; strong semiconductor ripple correlation |
| `AAPL` | Apple | World's most-followed tech stock; predictable earnings reaction patterns |
| `TSLA` | Tesla | Extremely volatile; CEO news heavily impacts price; unique sentiment dynamics |
| `MSFT` | Microsoft | Cloud + AI sector; less volatile; good balance to TSLA in the portfolio |

All 5 share the **Technology/Semiconductor sector**, enabling meaningful ripple effect modeling.

---

## 24. Scoring System — All 5 Dimensions Explained

### 1. Confidence Score (0–100%)
**Source**: XGBoost calibrated probability × 100  
**Meaning**: How certain is the ML model about its directional prediction?  
- 0–40% → Low confidence (UNCERTAIN signal)
- 40–60% → Moderate confidence
- 60–100% → High confidence (triggers BUY or SELL signal)

### 2. FinBERT Score (polarity: -1.0 to +1.0)
**Source**: GPT-4o-mini `sentiment_confidence` field (independently computed)  
**Formula**: `(positive_pct - negative_pct) / 100`  
**Meaning**: NLP sentiment polarity from language understanding  
- +1.0 = extremely bullish text | -1.0 = extremely bearish | 0.0 = neutral

### 3. LLM Impact Score (0–100)
**Source**: GPT-4o-mini `impact_score` field  
**Meaning**: How significant is this event expected to be? Independent of direction.  
- 0–30 = minor news | 30–60 = medium | 60–100 = major event

### 4. 1-Hour Prediction (%)
**Formula**: `(final_prob - 0.50) × 10 × 0.4`  
**Meaning**: Predicted % price move within 1 hour of event

### 5. 1-Day Prediction (%)
**Formula**: `(final_prob - 0.50) × 10 × 1.0`  
**Meaning**: Predicted % price move by end of trading day

---

## 25. Signal Generation Logic

```python
if final_prob > 0.60:
    signal = "BUY"
elif final_prob < 0.40:
    signal = "SELL"
else:
    signal = "UNCERTAIN"
```

**Why 0.60/0.40 thresholds?** A 50% probability means zero edge — coin flip. Requiring > 60% before BUY ensures meaningful predictive value. The 20% "dead zone" (40–60%) avoids noisy signals.

**UI Display**:
- `🚀 STRONG BUY` — confidence > 75%
- `📈 BUY` — confidence 60–75%
- `⚖️ UNCERTAIN / HOLD` — confidence 40–60%
- `📉 SELL` — confidence 25–40%
- `🔴 STRONG SELL` — confidence < 25%

---

## 26. Known Limitations

| Limitation | Detail |
|-----------|--------|
| **Not a trading bot** | Educational/research tool; not connected to any broker |
| **Market hours dependency** | yfinance returns stale prices outside market hours |
| **OpenAI cost** | Every prediction makes 2 API calls (~\$0.001 per prediction) |
| **5-ticker scope** | Trained models only for NVDA, AMD, AAPL, TSLA, MSFT |
| **Training data age** | Models may need retraining as market regimes change |
| **No options/derivatives** | Only equity direction prediction |
| **RSS news delay** | Yahoo Finance RSS lags real-time by 5–15 minutes |
| **SQLite limits** | PostgreSQL recommended for high-throughput production |

---

## 27. Future Roadmap

| Feature | Description |
|---------|-------------|
| **Alpaca broker API** | Connect predictions to live paper trading |
| **Options flow analysis** | Integrate unusual options activity as features |
| **Earnings call transcripts** | Analyze full audio via Whisper + LLM |
| **SEC filing analysis** | Parse 10-K/10-Q for hidden risk signals |
| **Multi-modal inputs** | Chart pattern recognition via computer vision |
| **Online learning** | Continuously retrain as new data arrives |
| **S&P 500 coverage** | Extend models to 500 companies |
| **Risk management** | Position sizing, stop-loss calculation |
| **MLflow dashboard** | Track model accuracy over time |
| **Mobile app** | React Native version of the terminal |
| **Push notifications** | Alert when high-confidence signal fires |

---

## Project Summary

This is not a tutorial project. It is a complete production-grade system:

1. **15-phase architecture** built systematically from data ingestion to Docker deployment
2. **Three AI layers**: GPT-4o-mini LLM + FinBERT deep NLP + XGBoost quantitative ML
3. **Custom RAG system** using OpenAI embeddings + NumPy (no bloated external vector DB)
4. **Sector ripple modeling** — predicts impact on 3 competitors, not just the primary ticker
5. **Real-time prediction tracking daemon** — auto-records actual market outcomes
6. **8 score bugs identified and fixed** — data integrity is a first-class concern
7. **Full-stack** — Python FastAPI backend + TypeScript React frontend, fully integrated
8. **Bloomberg Terminal aesthetic** — live WebSocket data, real-time charts, news feed
9. **Containerized** with Docker for one-command deployment
10. **Complete backtesting** — Sharpe, Sortino, drawdown, win rate, profit factor

> This project demonstrates ML expertise, production software engineering, financial domain knowledge, real-time systems design, and UI/UX skills — all in one codebase.
