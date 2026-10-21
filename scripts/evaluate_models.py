"""
scripts/evaluate_models.py
--------------------------
Evaluate all saved XGBoost models and print performance metrics.
Loads each ticker's model and runs predictions on test data.
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
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
TARGET_COL = 'direction_label'
LABEL_MAP = {0: 'Bearish', 1: 'Neutral', 2: 'Bullish'}


def evaluate_ticker(ticker: str) -> dict | None:
    """Evaluate saved model for a ticker."""
    model_path = MODELS_DIR / f'xgb_{ticker}_latest.json'
    csv_path = DATA_DIR / f'{ticker}_final_dataset.csv'

    if not model_path.exists():
        logger.warning(f"No model found for {ticker}: {model_path}")
        return None

    if not csv_path.exists():
        logger.warning(f"No dataset found for {ticker}: {csv_path}")
        return None

    # Load model
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    logger.info(f"Loaded model: {model_path}")

    # Load data (use last 20% as test set)
    df = pd.read_csv(csv_path)
    available_features = [c for c in FEATURE_COLS if c in df.columns]

    if TARGET_COL not in df.columns:
        logger.warning(f"No target column in {ticker} dataset")
        return None

    split_idx = int(len(df) * 0.8)
    test_df = df.iloc[split_idx:]

    X_test = test_df[available_features].fillna(0)
    y_test = test_df[TARGET_COL]

    if len(X_test) == 0:
        logger.warning(f"Empty test set for {ticker}")
        return None

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=list(LABEL_MAP.values()), output_dict=True)

    return {
        'ticker': ticker,
        'test_samples': len(X_test),
        'accuracy': round(accuracy, 4),
        'precision_macro': round(report['macro avg']['precision'], 4),
        'recall_macro': round(report['macro avg']['recall'], 4),
        'f1_macro': round(report['macro avg']['f1-score'], 4),
    }


def main():
    logger.info("Evaluating all saved models...\n")
    results = []

    for ticker in TICKERS:
        result = evaluate_ticker(ticker)
        if result:
            results.append(result)

    logger.info("\n" + "="*70)
    logger.info(f"{'Ticker':<8} {'Acc':>8} {'Prec':>8} {'Recall':>8} {'F1':>8} {'N Test':>8}")
    logger.info("="*70)
    for r in results:
        logger.info(
            f"{r['ticker']:<8} {r['accuracy']:>8.3f} {r['precision_macro']:>8.3f} "
            f"{r['recall_macro']:>8.3f} {r['f1_macro']:>8.3f} {r['test_samples']:>8}"
        )


if __name__ == '__main__':
    main()
