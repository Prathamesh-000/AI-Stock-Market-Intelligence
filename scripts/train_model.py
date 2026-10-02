import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
import numpy as np
from config.settings import settings
from src.models.xgboost_model import MarketImpactXGBoost
from src.models.calibration import ConfidenceCalibrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Train and Calibrate XGBoost Model (Phases 7 & 8)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0])
    args = parser.parse_args()
    
    logger.info(f"--- Starting Advanced Training Pipeline for {args.ticker} ---")
    
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
    df['Target'] = np.where(df['Direction'] == 1, 1, 0)
    cols_to_drop = [
        'event_id', 'headline', 'summary', 'url', 'publisher', 'source', 
        'published_at', 'duplicate_sources', 'Direction', 'CAR_1d', 'Impact_Score',
        'Fwd_Ret_1d', 'Fwd_Ret_1d_SPY', 'Timestamp'
    ]
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    if 'event_type' in df.columns:
        df = pd.get_dummies(df, columns=['event_type'], drop_first=True)
        
    # Ensure chronological order for splitting
    if 'market_reaction_time' in df.columns:
        df['market_reaction_time'] = pd.to_datetime(df['market_reaction_time'])
        df = df.sort_values('market_reaction_time')
        df = df.drop(columns=['market_reaction_time'])
        
    df = df.select_dtypes(include=[np.number])
    
    # 3. Time-Series Split (Train 60% | Validation 20% | Test 20%)
    # Because this is a test environment with a tiny dataset, we use basic chronological splits
    n = len(df)
    train_df = df.iloc[:int(n*0.6)]
    val_df = df.iloc[int(n*0.6):int(n*0.8)]
    test_df = df.iloc[int(n*0.8):]
    
    X_train, y_train = train_df.drop(columns=['Target']), train_df['Target']
    X_val, y_val = val_df.drop(columns=['Target']), val_df['Target']
    X_test, y_test = test_df.drop(columns=['Target']), test_df['Target']
    
    logger.info(f"Split sizes: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
    
    # 4. Train Base XGBoost
    model = MarketImpactXGBoost()
    model.train(X_train, y_train)
    
    # 5. Calibrate Probabilities (Phase 8)
    # We calibrate using the Validation set to avoid overfitting the train set
    calibrator = ConfidenceCalibrator(method='sigmoid')
    
    # The CalibratedClassifierCV expects an sklearn-compatible estimator. 
    # Our custom XGB wrapper hides the inner sklearn API slightly, so we pass model.model
    calibrator.fit(model.model, X_val, y_val)
    
    # 6. Evaluate Confidence on Test Set
    logger.info("Evaluating Calibrated Predictions on Test Set...")
    calibrated_probs = calibrator.predict_proba(X_test)
    
    # Analyze how many trades we actually take vs skip
    trade_stats = calibrator.filter_actionable_trades(calibrated_probs, lower_threshold=0.40, upper_threshold=0.60)
    
    logger.info("--- Uncertainty Filter Results ---")
    for k, v in trade_stats.items():
        logger.info(f"{k}: {v}")
        
    # 7. Save Artifacts
    model_dir = settings.project_root / "models" / "saved"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model.save_model(str(model_dir / f"xgb_{args.ticker}_latest.json"))
    calibrator.save(str(model_dir / f"calibrator_{args.ticker}_latest.pkl"))
    
    logger.info("--- Phases 7 & 8 Complete ---")

if __name__ == "__main__":
    main()
