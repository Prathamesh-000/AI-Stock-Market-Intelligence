# Project Proposal — AI Stock Market Intelligence

**Project Title**: AI-Powered Stock Market Intelligence Terminal  
**Author**: Prathamesh  
**Date**: September 2026

---

## 1. Problem Statement

Financial markets react rapidly to news events, but human traders cannot process the volume and velocity of modern financial news. A single earnings miss, regulatory announcement, or supply chain disruption can move a stock 10-30% within minutes. Retail and institutional traders need tools that can:

1. Ingest and understand financial news in real-time
2. Predict the likely directional impact on specific stocks
3. Quantify confidence and risk before executing trades
4. Provide explainable signals, not black-box outputs

---

## 2. Proposed Solution

Build an end-to-end AI terminal that:
- Uses OpenAI GPT-4o-mini to extract structured features from news headlines
- Runs XGBoost classifiers (one per ticker) to predict market direction
- Implements RAG (Retrieval-Augmented Generation) to find historical analogues
- Displays everything in a Bloomberg Terminal-inspired React UI

---

## 3. Technical Approach

### 3.1 NLP Pipeline
- Input: Raw news headline + summary
- Processing: GPT-4o-mini extracts `sentiment_score`, `event_type`, `severity`, `magnitude_estimate`
- Output: Structured feature vector

### 3.2 ML Model
- Algorithm: XGBoost (gradient boosted trees)
- Features: 15+ engineered features from price data + NLP output
- Target: 3-class (Bullish / Bearish / Neutral)
- Validation: Walk-forward cross-validation

### 3.3 RAG System
- Embeddings: Stored in NumPy array (historical_news_embeddings.npy)
- Search: Cosine similarity lookup
- Purpose: Find 5 most similar historical news events and their outcomes

---

## 4. Expected Deliverables

1. FastAPI backend with REST + WebSocket endpoints
2. React TypeScript frontend (Bloomberg-style)
3. Trained XGBoost models for NVDA, AMD, AAPL, TSLA, MSFT
4. RAG vector database with historical news
5. Docker deployment configuration
6. Complete documentation

---

## 5. Timeline

| Week | Tasks |
|------|-------|
| 1-2 | Data collection, preprocessing |
| 3-4 | Feature engineering, model training |
| 5-6 | API development, RAG implementation |
| 7-8 | Frontend development |
| 9-10 | Testing, bug fixes, deployment |

---

## 6. Success Criteria

- Directional accuracy > 60% on held-out test set
- API response time < 10 seconds per prediction
- Frontend loads and displays live data without errors
- Docker deployment works on clean machine
