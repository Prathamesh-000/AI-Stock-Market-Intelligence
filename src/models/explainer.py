import shap
import pandas as pd
import numpy as np
import logging
import xgboost as xgb

logger = logging.getLogger(__name__)

class ModelExplainer:
    """
    Uses SHAP (SHapley Additive exPlanations) to open the 'Black Box' of the XGBoost model.
    It explains exactly WHICH features drove the model to make a specific prediction.
    """
    
    def __init__(self, model):
        """
        Accepts the fitted XGBoost model object.
        """
        # SHAP specifically expects the raw XGBoost model, not our custom wrapper
        # If the user passes our custom wrapper, extract the inner model
        if hasattr(model, 'model'):
            self.xgb_model = model.model
        else:
            self.xgb_model = model
            
        logger.info("Initializing SHAP TreeExplainer...")
        self.explainer = shap.TreeExplainer(self.xgb_model)
        
    def get_global_importance(self, X: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Calculates the overall feature importance across the entire dataset.
        Tells us what the model cares about most in general (e.g., Sentiment vs RSI).
        """
        logger.info("Calculating Global SHAP values...")
        shap_values = self.explainer.shap_values(X)
        
        # Calculate mean absolute SHAP value for each feature
        # This tells us the average impact magnitude of the feature
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        
        importance_df = pd.DataFrame({
            'Feature': X.columns,
            'SHAP_Importance': mean_abs_shap
        }).sort_values('SHAP_Importance', ascending=False).reset_index(drop=True)
        
        return importance_df.head(top_n)
        
    def explain_single_prediction(self, X_row: pd.DataFrame) -> dict:
        """
        Explains a single specific news event prediction.
        Returns the top features that pushed the prediction UP and the top features that pushed it DOWN.
        """
        # Ensure it's a 1-row dataframe
        if len(X_row) != 1:
            logger.error("explain_single_prediction expects a DataFrame with exactly 1 row.")
            return {}
            
        shap_values = self.explainer.shap_values(X_row)[0]
        base_value = self.explainer.expected_value
        
        # Create a mapping of feature to its SHAP impact
        impacts = []
        for i, col in enumerate(X_row.columns):
            impacts.append({
                'Feature': col,
                'Value': X_row.iloc[0, i],
                'Impact': shap_values[i]
            })
            
        # Sort by impact
        # Positive impact = pushed the prediction towards BUY
        # Negative impact = pushed the prediction towards SELL
        impacts.sort(key=lambda x: x['Impact'], reverse=True)
        
        # Get top 3 bullish drivers and top 3 bearish drivers
        bullish_drivers = [x for x in impacts if x['Impact'] > 0][:3]
        bearish_drivers = [x for x in impacts if x['Impact'] < 0][-3:]
        bearish_drivers.reverse() # Most negative first
        
        return {
            "Base_Value": float(base_value),
            "Final_SHAP_Sum": float(base_value + np.sum(shap_values)),
            "Top_Bullish_Drivers": bullish_drivers,
            "Top_Bearish_Drivers": bearish_drivers
        }
