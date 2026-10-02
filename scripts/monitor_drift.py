import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
from config.settings import settings
from src.validation.drift import DriftDetector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker to monitor")
    args = parser.parse_args()

    logger.info(f"--- Starting Phase 14 Drift Monitoring for {args.ticker} ---")
    
    dataset_path = settings.data_dir / "processed" / f"{args.ticker}_final_dataset.csv"
    if not dataset_path.exists():
        logger.error(f"Dataset not found at {dataset_path}")
        sys.exit(1)
        
    df = pd.read_csv(dataset_path)
    
    # Simulate Production Environment
    # We will split our data in half. 
    # First half = "Training Data". Second half = "Live Production Data"
    midpoint = len(df) // 2
    reference_data = df.iloc[:midpoint]
    current_data = df.iloc[midpoint:]
    
    logger.info(f"Comparing Reference Data (First {len(reference_data)} rows) against Live Data (Last {len(current_data)} rows)")
    
    detector = DriftDetector(p_value_threshold=0.05)
    
    # Features to monitor for drift (we'll check a mix of NLP and Market features)
    features_to_monitor = [
        'sentiment_score', 
        'RSI', 
        'MACD', 
        'ATR'
    ]
    
    # 1. Feature Drift
    drift_results = detector.detect_feature_drift(reference_data, current_data, features_to_monitor)
    
    print("\n" + "="*50)
    print("--- DATA DRIFT ANALYSIS ---")
    print("="*50)
    
    if drift_results["drift_detected"]:
        print("STATUS: WARNING! Market conditions have shifted.")
    else:
        print("STATUS: STABLE. No significant drift detected.")
        
    print("\nFeature Breakdown (Kolmogorov-Smirnov Test):")
    for feature, stats in drift_results["feature_details"].items():
        status_text = "DRIFTING [X]" if stats["is_drifting"] else "STABLE [OK]"
        p_val = stats["p_value"]
        print(f" - {feature.ljust(15)} : {status_text} (p-value: {p_val:.4f})")
        
    print("="*50 + "\n")
    
    logger.info("--- Phase 14 Complete ---")

if __name__ == "__main__":
    main()
