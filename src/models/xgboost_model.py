import xgboost as xgb
import pandas as pd
import numpy as np
import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)

class MarketImpactXGBoost:
    """
    XGBoost Classifier to predict the binary direction of a stock post-news.
    1 = Up (Bullish), 0 = Down/Neutral (Bearish/Noise)
    """
    def __init__(self):
        # We use a relatively shallow tree to prevent overfitting on noisy financial data
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            objective='binary:logistic',
            eval_metric='auc',
            tree_method='hist', # Faster, natively supports NaN values (which we have in finance)
            random_state=42
        )
        self.features = []

    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Trains the XGBoost model.
        """
        logger.info(f"Training XGBoost on {len(X_train)} samples...")
        self.features = list(X_train.columns)
        self.model.fit(X_train, y_train)
        logger.info("Training complete.")

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """
        Predicts and evaluates performance on the test set.
        """
        if len(X_test) == 0:
            logger.warning("Test set is empty. Cannot evaluate.")
            return {}
            
        preds = self.model.predict(X_test)
        
        metrics = {
            "Accuracy": round(accuracy_score(y_test, preds), 4),
            "Precision": round(precision_score(y_test, preds, zero_division=0), 4),
            "Recall": round(recall_score(y_test, preds, zero_division=0), 4),
            "F1_Score": round(f1_score(y_test, preds, zero_division=0), 4)
        }
        
        logger.info("--- Model Evaluation ---")
        for k, v in metrics.items():
            logger.info(f"{k}: {v}")
            
        return metrics

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Returns the raw probability of the UP class.
        """
        return self.model.predict_proba(X)[:, 1]

    def save_model(self, filepath: str):
        """Saves the model weights"""
        self.model.save_model(filepath)
        logger.info(f"Model saved to {filepath}")
        
    def load_model(self, filepath: str):
        """Loads the model weights"""
        self.model.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")

