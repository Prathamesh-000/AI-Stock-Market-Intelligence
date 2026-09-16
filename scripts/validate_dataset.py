import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
from config.settings import settings
from src.validation.leakage import LeakageDetector
from src.validation.splitter import TimeSeriesSplitter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Validate Dataset for ML Training (Phase 6)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0])
    args = parser.parse_args()
    
    logger.info(f"--- Starting Validation Checkpoint for {args.ticker} ---")
    
    dataset_file = settings.data_dir / "processed" / f"{args.ticker}_final_dataset.csv"
    
    if not dataset_file.exists():
        logger.error(f"Dataset not found: {dataset_file}")
        return
        
    df = pd.read_csv(dataset_file)
    
    # 1. Check Target Leakage
    logger.info("Running Target Leakage Checks...")
    target = 'Impact_Score'
    leaks = LeakageDetector.check_target_leakage(df, target_col=target)
    
    if leaks:
        logger.error(f"Validation FAILED: The following columns contain future data and must be removed: {leaks}")
        # Automatically drop leaked columns for safety (excluding targets)
        cols_to_drop = [col for col in leaks if col not in ['CAR_1d', 'Direction']]
        df = df.drop(columns=cols_to_drop)
        logger.info(f"Dropped {cols_to_drop} for safety.")
        
    # 2. Check Chronology
    logger.info("Running Lookahead Bias Checks...")
    LeakageDetector.check_chronological_order(df)
    
    # 3. Check Target Integrity
    LeakageDetector.check_missing_targets(df, target_col=target)
    
    # 4. Demonstrate Purged Split
    logger.info("Running Time-Series Embargo Split Test...")
    train_df, test_df = TimeSeriesSplitter.purged_split(df, test_size=0.2, purge_days=20)
    
    if len(test_df) == 0:
        logger.warning("Test dataset is completely empty after purging! You need a longer history of data.")
    
    logger.info("--- Validation Checkpoint Complete ---")
    logger.info("If all checks passed, the dataset is certified for Machine Learning Training!")

if __name__ == "__main__":
    main()

