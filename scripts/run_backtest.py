import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
import numpy as np
import joblib
from config.settings import settings
from src.models.xgboost_model import MarketImpactXGBoost
from src.backtesting.engine import BacktestEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_historical_signals(ticker: str) -> pd.DataFrame:
    """Loads the dataset and uses the trained AI to generate a signal for every row."""
    dataset_path = settings.data_dir / "processed" / f"{ticker}_final_dataset.csv"
    if not dataset_path.exists():
        logger.error(f"Dataset not found at {dataset_path}")
        sys.exit(1)
        
    df = pd.read_csv(dataset_path)
    logger.info(f"Loaded {len(df)} historical events for {ticker}")
    
    # Load Model and Calibrator
    model_dir = settings.project_root / "models" / "saved"
    xgb_model = MarketImpactXGBoost()
    xgb_model.load_model(str(model_dir / f"xgb_{ticker}_latest.json"))
    
    calibrator = None
    calib_path = model_dir / f"calibrator_{ticker}_latest.pkl"
    if calib_path.exists():
        calibrator = joblib.load(str(calib_path))

    # Preprocess features identical to training
    feature_cols = [c for c in df.columns if c not in [
        'event_id', 'headline', 'summary', 'url', 'publisher', 'source', 
        'published_at', 'duplicate_sources', 'Direction', 'CAR_1d', 'Impact_Score',
        'Fwd_Ret_1d', 'Fwd_Ret_1d_SPY', 'Timestamp', 'market_reaction_time', 'Target'
    ]]
    
    X = df[feature_cols].copy()
    if 'event_type' in X.columns:
        X = pd.get_dummies(X, columns=['event_type'], drop_first=True)
    X = X.select_dtypes(include=[np.number])
    
    # Predict
    logger.info("Generating AI predictions for all historical data...")
    raw_probs = xgb_model.predict_proba(X)
    
    if calibrator is not None and calibrator.calibrator is not None:
        final_probs = calibrator.predict_proba(X)
    else:
        final_probs = raw_probs
        
    # Generate Signals based on confidence thresholds
    signals = []
    for prob in final_probs:
        if prob > 0.60:
            signals.append("BUY")
        elif prob < 0.40:
            signals.append("SELL")
        else:
            signals.append("UNCERTAIN")
            
    df['AI_Signal'] = signals
    df['AI_Confidence'] = final_probs
    
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker to backtest")
    parser.add_argument("--capital", type=float, default=100000.0, help="Starting capital")
    args = parser.parse_args()

    logger.info(f"--- Starting Phase 13 Backtest Engine for {args.ticker} ---")
    
    # 1. Generate Signals
    df_with_signals = generate_historical_signals(args.ticker)
    
    # 2. Run Backtest
    engine = BacktestEngine(initial_capital=args.capital)
    metrics, trade_history = engine.run(df_with_signals, signal_col='AI_Signal', return_col='Fwd_Ret_1d')
    
    # 3. Print Results
    print("\n" + "="*40)
    print("--- AI BACKTEST RESULTS ---")
    print("="*40)
    for key, value in metrics.items():
        print(f"{key.ljust(20)}: {value}")
    print("="*40 + "\n")
    
    # Save equity curve for the dashboard later
    out_path = settings.data_dir / "processed" / f"{args.ticker}_backtest_results.csv"
    trade_history.to_csv(out_path, index=False)
    logger.info(f"Saved detailed trade history to {out_path}")
    logger.info("--- Phase 13 Complete ---")

if __name__ == "__main__":
    main()
