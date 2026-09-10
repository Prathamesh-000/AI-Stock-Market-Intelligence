# System Architecture & Tech Stack

This document outlines the end-to-end architecture, technology stack, and step-by-step implementation layout for the **AI-Powered Real-Time Market Impact & Stock Intelligence System**.

## 🏗️ System Architecture Flowchart

```text
                  ┌─────────────────────┐
                  │     DATA SOURCES    │
                  └──────────┬──────────┘
                             │
              ┌──────────────┴──────────────┐
              ↓                             ↓
       MARKET DATA                       NEWS
              │                             │
              ↓                             ↓
       Cleaning & Validation        Cleaning & Validation
              │                             │
              └──────────────┬──────────────┘
                             ↓
                  Timestamp Synchronization
                             │
              ┌──────────────┴──────────────┐
              ↓                             ↓
        MARKET ENGINE                  NLP ENGINE
              │                             │
       ┌──────┼───────┐             ┌──────┼────────┐
       ↓      ↓       ↓             ↓      ↓        ↓
   Technical Relative Regime     FinBERT Event   Novelty
   Indicators Performance        Sentiment Severity Detection
       │      │       │             │      │        │
       └──────┴───────┴─────────────┴──────┴────────┘
                             ↓
                    FEATURE ENGINEERING
                             ↓
                     LEAKAGE CHECK
                             ↓
                  TIME-SERIES DATA SPLIT
                             ↓
                ┌────────────┴────────────┐
                ↓                         ↓
          IMPACT MODEL              DIRECTION MODEL
           XGBoost/LightGBM          XGBoost/LightGBM
                ↓                         ↓
          CAR / Impact             UP/DOWN/NEUTRAL
                └───────────┬─────────────┘
                            ↓
                    CONFIDENCE LAYER
                            ↓
                         SHAP
                            ↓
                  MARKET INTELLIGENCE
                            ↓
             ┌──────────────┴─────────────┐
             ↓                            ↓
          FastAPI                     WebSocket
             │                            │
             └──────────────┬─────────────┘
                            ↓
                     PostgreSQL
                            ↓
                 React + Tailwind
                            ↓
                 Monitoring & Backtesting
                            ↓
                     MLflow + Docker
```

## 📅 Implementation Roadmap (15 Phases)

We will build the system iteratively following this exact 15-phase sequence:

```text
PHASE 1
Environment & Data Ingestion
        ↓
PHASE 2
Cleaning & Timestamp Synchronization
        ↓
PHASE 3
NLP Engine
 ├── FinBERT
 ├── Event Classification
 ├── Event Severity
 └── Novelty Detection
        ↓
PHASE 4
Market Engine
 ├── Technical Indicators
 ├── ATR
 ├── Historical Volatility
 ├── Relative Volume
 ├── Relative Performance
 └── Market Regime
        ↓
PHASE 5
Feature Engineering & Target Creation
 ├── Feature Matrix
 ├── CAR 15m
 ├── CAR 30m
 ├── CAR 1h
 ├── CAR 1d
 ├── Impact Score
 └── Direction Label
        ↓
PHASE 6
Leakage Prevention & Time-Series Validation
        ↓
PHASE 7
ML Models
 ├── Baselines
 ├── Direction Model
 └── Impact Model
        ↓
PHASE 8
Confidence & Uncertainty
        ↓
PHASE 9
SHAP Explainability
        ↓
PHASE 10
FastAPI + WebSockets
        ↓
PHASE 11
PostgreSQL + MLflow
        ↓
PHASE 12
React Dashboard
        ↓
PHASE 13
Backtesting & Model Evaluation
        ↓
PHASE 14
Monitoring / Drift Detection
        ↓
PHASE 15
Docker + Deployment
```

## 🛠️ Complete Technology Stack

| Layer | Technologies | Purpose |
| :--- | :--- | :--- |
| **Environment** | Python 3.14, Virtualenv | Core development environment. |
| **Data Ingestion** | `yfinance`, `beautifulsoup4`, `feedparser`, `requests` | Fetching historical/live market data and news. |
| **Data Processing** | `pandas`, `numpy`, `pandas-ta` | Time-series manipulation, technical indicators, and cleaning. |
| **NLP Engine** | `transformers` (Hugging Face), `torch` | FinBERT sentiment analysis and zero-shot event classification. |
| **Machine Learning** | `xgboost` / `lightgbm`, `scikit-learn` | Dual-model architecture for Regression (Impact) and Classification (Direction). |
| **Explainability** | `shap` | Extracting feature importance and causality. |
| **Backend API** | `fastapi`, `uvicorn`, `websockets` | Serving REST APIs and real-time WebSocket feeds. |
| **Database** | PostgreSQL, `SQLAlchemy` | Persisting model predictions and market data. |
| **Frontend UI** | React.js, Tailwind CSS, Recharts | End-user Stock Intelligence Dashboard. |
| **MLOps & DevOps** | `mlflow`, Docker, GitHub Actions | Model monitoring, experiment tracking, and containerization. |

## ?? Codebase Mapping

This structure ensures separation of concerns, mapping every step of the 15-phase roadmap directly to specific folders and files.

### ??? Phase 1: Environment & Data Ingestion
*   **Config:** config/settings.py, .env.example
*   **Ingestion:** src/data/market_data.py, src/data/news_data.py
*   **Data Access Layer:** src/data/data_provider.py, src/data/validators.py
*   **CLI Trigger:** scripts/download_data.py

### ?? Phase 2: Cleaning & Timestamp Synchronization
*   **Cleaning:** src/preprocessing/market_cleaner.py, src/preprocessing/news_cleaner.py
*   **Synchronization:** src/preprocessing/timestamp_sync.py, src/preprocessing/deduplication.py
*   **CLI Trigger:** scripts/preprocess_data.py

### ?? Phase 3: NLP Engine
*   **Sentiment & Event:** src/sentiment/finbert.py, src/sentiment/event_classifier.py
*   **Context:** src/sentiment/severity.py, src/sentiment/novelty.py, src/sentiment/entity_linking.py
*   **CLI Trigger:** scripts/run_nlp.py

### ?? Phase 4: Market Engine
*   **Technical & Volatility:** src/features/technical.py, src/features/volatility.py
*   **Context:** src/features/volume.py, src/features/relative_performance.py, src/features/regime.py

### ?? Phase 5: Feature Engineering & Target Creation
*   **Matrix Assembly:** src/features/feature_builder.py, src/features/event_features.py
*   **Targets ($ labels):** src/targets/abnormal_returns.py, src/targets/impact_score.py, src/targets/direction.py
*   **CLI Trigger:** scripts/build_features.py

### ??? Phase 6: Leakage Prevention & Time-Series Validation
*   **Validation Rules:** src/validation/leakage.py, src/validation/time_split.py, src/validation/walk_forward.py

### ?? Phase 7: ML Models (Dual-Model Architecture)
*   **Classification:** src/models/direction_model.py (UP/DOWN/NEUTRAL)
*   **Regression:** src/models/impact_model.py (0-100 Impact Score)
*   **Training & Baselines:** src/models/trainer.py, src/models/evaluator.py, src/models/baselines/
*   **CLI Trigger:** scripts/train_models.py

### ?? Phase 8: Confidence & Uncertainty
*   **Logic:** src/prediction/confidence.py, src/prediction/calibration.py

### ?? Phase 9: SHAP Explainability
*   **Explainability:** src/prediction/shap_explainer.py
*   **Final Inference:** src/prediction/predictor.py

### ?? Phase 10: FastAPI + WebSockets
*   **REST API:** ackend/api/routes/predictions.py, ackend/api/routes/news.py, ackend/api/routes/stocks.py
*   **Live Feed:** ackend/api/websocket.py
*   **Services:** ackend/services/prediction_service.py, ackend/main.py

### ?? Phase 11: PostgreSQL + MLflow
*   **Database Schema:** ackend/database/models.py, ackend/database/session.py, ackend/database/repositories.py
*   **MLOps Tracking:** mlruns/

### ??? Phase 12: React Dashboard
*   **Frontend UI:** rontend/src/components/, rontend/src/pages/, rontend/src/charts/

### ?? Phase 13: Backtesting & Model Evaluation
*   **Simulation:** src/backtesting/backtest.py, src/backtesting/metrics.py
*   **CLI Trigger:** scripts/evaluate_models.py

### ?? Phase 14: Monitoring / Drift Detection
*   **Monitoring:** Handled via MLflow tracking logs and src/models/evaluator.py

### ?? Phase 15: Docker + Deployment
*   **Containerization:** docker/Dockerfile.backend, docker/Dockerfile.frontend, docker/docker-compose.yml
*   **CI/CD:** .github/workflows/ci.yml

