import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
import numpy as np
import xgboost as xgb
from config.settings import settings
from src.models.xgboost_model import MarketImpactXGBoost
from src.models.explainer import ModelExplainer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run SHAP Explainer (Phase 9)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0])
    args = parser.parse_args()
    
    logger.info(f"--- Starting SHAP Explainability Engine for {args.ticker} ---")
    
    # 1. Load the Model
    model_path = settings.project_root / "models" / "saved" / f"xgb_{args.ticker}_latest.json"
    if not model_path.exists():
        logger.error("Trained model not found. Run train_model.py first.")
        return
        
    wrapper = MarketImpactXGBoost()
    wrapper.load_model(str(model_path))
    
    # 2. Load the Dataset (for the feature columns)
    dataset_file = settings.data_dir / "processed" / f"{args.ticker}_final_dataset.csv"
    if not dataset_file.exists():
        logger.error("Dataset not found.")
        return
        
    df = pd.read_csv(dataset_file)
    
    # Match the exact preprocessing from train_model.py to get the exact feature columns
    cols_to_drop = [
        'event_id', 'headline', 'summary', 'url', 'publisher', 'source', 
        'published_at', 'duplicate_sources', 'Direction', 'CAR_1d', 'Impact_Score',
        'Fwd_Ret_1d', 'Fwd_Ret_1d_SPY', 'Timestamp', 'market_reaction_time'
    ]
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    if 'event_type' in df.columns:
        df = pd.get_dummies(df, columns=['event_type'], drop_first=True)
        
    df = df.select_dtypes(include=[np.number])
    
    # Assume target was dropped, but it might not be in this clean df if we didn't add it.
    # In train_model.py, we created 'Target'. Let's just drop it if it exists.
    if 'Target' in df.columns:
        df = df.drop(columns=['Target'])
        
    # We now have pure features X
    X = df
    
    if len(X) == 0:
        logger.error("No features found after preprocessing.")
        return
        
    # 3. Initialize Explainer
    explainer = ModelExplainer(wrapper)
    
    # 4. Global Explanation
    logger.info("\n=== GLOBAL FEATURE IMPORTANCE ===")
    logger.info("What does the AI care about the most overall?")
    global_imp = explainer.get_global_importance(X, top_n=5)
    for idx, row in global_imp.iterrows():
        logger.info(f"{idx+1}. {row['Feature']}: {row['SHAP_Importance']:.4f} impact magnitude")
        
    # 5. Local Explanation (Explain the very last event)
    logger.info("\n=== LOCAL PREDICTION EXPLANATION ===")
    logger.info("Why did the AI make its prediction on the most recent news event?")
    
    # Take the last row
    latest_event = X.iloc[[-1]]
    explanation = explainer.explain_single_prediction(latest_event)
    
    if explanation:
        logger.info(f"Base Output (Average Prediction): {explanation['Base_Value']:.4f}")
        logger.info(f"Final Model Output for this event: {explanation['Final_SHAP_Sum']:.4f}")
        
        logger.info("\nTop Factors pushing the AI to BUY (Bullish):")
        for f in explanation['Top_Bullish_Drivers']:
            logger.info(f"  + {f['Feature']} = {f['Value']:.2f} (Impact: +{f['Impact']:.4f})")
            
        logger.info("\nTop Factors pushing the AI to SELL (Bearish):")
        for f in explanation['Top_Bearish_Drivers']:
            logger.info(f"  - {f['Feature']} = {f['Value']:.2f} (Impact: {f['Impact']:.4f})")
            
    logger.info("\n--- Phase 9 Complete ---")

if __name__ == "__main__":
    main()

