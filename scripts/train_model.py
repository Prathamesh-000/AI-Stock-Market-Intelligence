import sys
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
import numpy as np
from config.settings import settings
from src.validation.splitter import TimeSeriesSplitter
from src.models.xgboost_model import MarketImpactXGBoost

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Train XGBoost Model (Phase 7)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0])
    args = parser.parse_args()
    
    logger.info(f"--- Starting Model Training for {args.ticker} ---")
    
    # 1. Load Dataset
    dataset_file = settings.data_dir / "processed" / f"{args.ticker}_final_dataset.csv"
    if not dataset_file.exists():
        logger.error(f"Dataset not found: {dataset_file}")
        return
        
    df = pd.read_csv(dataset_file)
    
    if len(df) < 50:
        logger.error("Dataset is too small to train a model. Download more historical data.")
        return

    # 2. Preprocessing
    logger.info("Preprocessing features...")
    
    # Map Target: 1 (Up) remains 1. -1 (Down) and 0 (Neutral) become 0.
    # XGBoost binary classification requires 0 and 1.
    df['Target'] = np.where(df['Direction'] == 1, 1, 0)
    
    # Drop columns that are text, future data (CAR_1d, Impact_Score, Direction), or identifiers
    cols_to_drop = [
        'event_id', 'headline', 'summary', 'url', 'publisher', 'source', 
        'published_at', 'duplicate_sources', 'Direction', 'CAR_1d', 'Impact_Score',
        'Fwd_Ret_1d', 'Fwd_Ret_1d_SPY', 'Timestamp'
    ]
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    # One-Hot Encode Categorical 'event_type'
    if 'event_type' in df.columns:
        df = pd.get_dummies(df, columns=['event_type'], drop_first=True)
        
    # 3. Split Data
    # Attempt strict purged split first
    train_df, test_df = TimeSeriesSplitter.purged_split(df, test_size=0.2, purge_days=20)
    
    # Fallback for testing on small datasets (like 1 month) where purge deletes the whole test set
    if len(test_df) == 0:
        logger.warning("Dataset too small for strict Embargo Purge. Falling back to basic chronological split (WARNING: May contain leakage, for testing only!)")
        train_end_idx = int(len(df) * 0.8)
        train_df = df.iloc[:train_end_idx]
        test_df = df.iloc[train_end_idx:]
        
    # Now that it's split, we can safely select only numeric columns for XGBoost
    train_df = train_df.select_dtypes(include=[np.number])
    test_df = test_df.select_dtypes(include=[np.number])
    
    # Separate Features (X) and Target (y)
    X_train = train_df.drop(columns=['Target'])
    y_train = train_df['Target']
    
    X_test = test_df.drop(columns=['Target'])
    y_test = test_df['Target']
    
    # 4. Train Model
    model = MarketImpactXGBoost()
    model.train(X_train, y_train)
    
    # 5. Evaluate
    metrics = model.evaluate(X_test, y_test)
    
    # 6. Save Model
    model_dir = settings.project_root / "models" / "saved"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = model_dir / f"xgb_{args.ticker}_latest.json"
    model.save_model(str(save_path))
    
    logger.info("--- Phase 7 Complete ---")

if __name__ == "__main__":
    main()
