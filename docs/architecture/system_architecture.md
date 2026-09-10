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
