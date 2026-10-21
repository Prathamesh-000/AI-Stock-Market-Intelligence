# ML Pipeline Architecture

## Overview

The ML pipeline processes a raw news headline through multiple stages to produce a structured market prediction.

## Stage 1: LLM Feature Extraction

```
Input: headline (str), summary (str)
Model: GPT-4o-mini
Output: {
  "sentiment_score": float,      # -1.0 to 1.0
  "event_type": str,             # "earnings"|"merger"|"layoff"|...
  "severity": str,               # "HIGH"|"MEDIUM"|"LOW"
  "magnitude_estimate": float,   # 0.0 to 10.0
  "affected_sector": str,
  "key_entities": list[str]
}
```

**Prompt Engineering**:
The LLM is instructed to extract structured JSON, not generate text. Temperature is set to 0.1 for consistency.

## Stage 2: RAG Context Retrieval

```
Input: headline embedding (1536-dim from ada-002 or local)
Search: Cosine similarity against historical_news_embeddings.npy
Output: Top 5 historical analogues with their actual market outcomes
```

The RAG similarity score is then used as an additional feature for the XGBoost model.

## Stage 3: Technical Feature Assembly

```python
features = {
    # From LLM
    "polarity_score": llm_output["sentiment_score"],
    "severity_score": severity_to_float(llm_output["severity"]),
    "magnitude_estimate": llm_output["magnitude_estimate"],
    
    # From RAG
    "rag_similarity": rag_result["max_similarity"],
    "historical_direction": rag_result["most_common_direction"],
    
    # From yfinance (market context)
    "rsi_14": technicals["rsi"],
    "volume_ratio": technicals["volume_ratio"],
    "price_momentum_5d": technicals["momentum_5d"],
    
    # Engineered
    "is_earnings": int(event_type == "earnings"),
    "is_merger": int(event_type == "merger"),
    "is_layoff": int(event_type == "layoff"),
}
```

## Stage 4: XGBoost Prediction

Each ticker has its own trained model:
- `models/saved/xgb_NVDA_latest.json`
- `models/saved/xgb_AMD_latest.json`
- `models/saved/xgb_AAPL_latest.json`
- `models/saved/xgb_TSLA_latest.json`
- `models/saved/xgb_MSFT_latest.json`

The model outputs raw class probabilities [P_bearish, P_neutral, P_bullish].

## Stage 5: Probability Calibration

Raw XGBoost probabilities are calibrated using isotonic regression:
- `models/saved/calibrator_{ticker}_latest.pkl`

Calibration reduces overconfidence and improves reliability of probability estimates.

## Stage 6: Score Computation

```python
# Impact Score (0-10)
impact_score = magnitude_estimate * confidence

# Sentiment Score (-1 to +1)  
sentiment_score = polarity_score * severity_multiplier

# Confidence Score (0-100)
confidence = weighted_avg(model_prob, rag_similarity, severity)

# Volatility Risk (0-10)
volatility_risk = rsi_deviation * volume_ratio_anomaly

# Direction
direction = argmax(calibrated_probs)  # BULLISH / BEARISH / NEUTRAL
```

## Stage 7: Signal Generation

```python
if direction == "BULLISH" and impact_score > 7 and confidence > 75:
    signal = "🚀 STRONG BUY"
elif direction == "BULLISH" and impact_score > 5 and confidence > 60:
    signal = "📈 BUY"
elif direction == "BEARISH" and impact_score > 7 and confidence > 75:
    signal = "🔴 STRONG SELL"
elif direction == "BEARISH" and impact_score > 5 and confidence > 60:
    signal = "📉 SELL"
else:
    signal = "⚖️ HOLD"
```
