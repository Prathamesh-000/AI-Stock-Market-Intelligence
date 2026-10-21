"""
scripts/train_models.py
-----------------------
Train XGBoost models for all tickers using processed dataset CSVs.
Saves trained models to models/saved/xgb_{TICKER}_latest.json
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.calibration import CalibratedClassifierCV
import joblib

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

TICKERS = ['NVDA', 'AMD', 'AAPL', 'TSLA', 'MSFT']
DATA_DIR = Path('data/processed')
MODELS_DIR = Path('models/saved')

FEATURE_COLS = [
    'polarity_score', 'subjectivity', 'compound_score',
    'severity_score', 'magnitude_estimate', 'rag_similarity',
    'is_earnings', 'is_merger', 'is_layoff', 'is_regulatory',
    'rsi_14', 'macd_signal', 'volume_ratio', 'price_momentum_5d',
]
TARGET_COL = 'direction_label'  # 0=Bearish, 1=Neutral, 2=Bullish

XGB_PARAMS = {
    'n_estimators': 300,
    'max_depth': 5,
    'learning_rate': 0.05,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective': 'multi:softprob',
    'num_class': 3,
    'eval_metric': 'mlogloss',
    'random_state': 42,
    'n_jobs': -1,
}


def train_ticker(ticker: str) -> dict:
    """Train XGBoost model for a single ticker."""
    csv_path = DATA_DIR / f'{ticker}_final_dataset.csv'
    if not csv_path.exists():
        logger.warning(f"No dataset found for {ticker} at {csv_path}")
        return {}

    df = pd.read_csv(csv_path)
    available_features = [c for c in FEATURE_COLS if c in df.columns]

    if TARGET_COL not in df.columns:
        logger.warning(f"No target column '{TARGET_COL}' in {ticker} dataset")
        return {}

    X = df[available_features].fillna(0)
    y = df[TARGET_COL]

    logger.info(f"Training {ticker}: {len(X)} samples, {len(available_features)} features")

    # Cross-validation
    model = xgb.XGBClassifier(**XGB_PARAMS)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    logger.info(f"{ticker} CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # Final fit
    model.fit(X, y)

    # Save model
    model_path = MODELS_DIR / f'xgb_{ticker}_latest.json'
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model.save_model(model_path)
    logger.info(f"Saved model: {model_path}")

    # Calibrate probabilities
    calibrated = CalibratedClassifierCV(model, cv='prefit', method='isotonic')
    calibrated.fit(X, y)
    cal_path = MODELS_DIR / f'calibrator_{ticker}_latest.pkl'
    joblib.dump(calibrated, cal_path)
    logger.info(f"Saved calibrator: {cal_path}")

    # Evaluate
    y_pred = model.predict(X)
    train_acc = accuracy_score(y, y_pred)

    return {
        'ticker': ticker,
        'samples': len(X),
        'features': len(available_features),
        'cv_accuracy_mean': round(float(cv_scores.mean()), 4),
        'cv_accuracy_std': round(float(cv_scores.std()), 4),
        'train_accuracy': round(float(train_acc), 4),
    }


def main():
    logger.info("Starting model training for all tickers...")
    results = []

    for ticker in TICKERS:
        result = train_ticker(ticker)
        if result:
            results.append(result)

    logger.info("\n" + "="*60)
    logger.info("TRAINING SUMMARY")
    logger.info("="*60)
    for r in results:
        logger.info(
            f"{r['ticker']}: CV={r['cv_accuracy_mean']:.3f}±{r['cv_accuracy_std']:.3f} "
            f"| Train={r['train_accuracy']:.3f} | N={r['samples']}"
        )


if __name__ == '__main__':
    main()

