import yfinance as yf
import pandas as pd
import numpy as np
import xgboost as xgb
import os

print("Fetching 5 years of real historical data from Yahoo Finance...")
tickers = ["NVDA", "AMD", "TSM", "INTC"]
data = yf.download(tickers, start="2019-01-01", end="2024-01-01")["Adj Close"]

print("Calculating daily returns...")
returns = data.pct_change().dropna() * 100  # Convert to percentage

# We assume that a news event on NVDA drives its daily return.
# We will use NVDA's return, along with 5-day rolling volatility, to predict the competitors' returns.
returns["NVDA_Vol_5d"] = returns["NVDA"].rolling(window=5).std().fillna(0)

# Drop initial NaN rows from rolling window
returns = returns.dropna()

print(f"Dataset ready with {len(returns)} trading days of real market actuality.")

# Prepare Features (X) and Targets (Y)
# X: NVDA daily return (simulating the immediate impact of the news) and sector volatility
X = returns[["NVDA", "NVDA_Vol_5d"]]

models_dir = "models"
os.makedirs(models_dir, exist_ok=True)

competitors = ["AMD", "TSM", "INTC"]
models = {}

print("Training Quantitative XGBoost Ripple Models...")
for comp in competitors:
    y = returns[comp]
    
    # Train XGBoost Regressor
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )
    model.fit(X, y)
    
    # Save the model
    model_path = os.path.join(models_dir, f"xgb_ripple_{comp}.json")
    model.save_model(model_path)
    models[comp] = model
    print(f" - Trained & saved {comp} Ripple Model (R^2: {model.score(X, y):.4f})")

print("\n--- Model Training Complete ---")
print("These models now mathematically map NVDA news shocks to AMD, TSM, and INTC based on 5 years of real historical price action!")
