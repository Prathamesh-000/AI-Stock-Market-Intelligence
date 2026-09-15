import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
from config.settings import settings
from src.features.feature_builder import FeatureBuilder
from src.targets.targets import TargetCreator

logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Build Final ML Feature Matrix (Phase 5)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0])
    parser.add_argument("--interval", type=str, default="1d")
    args = parser.parse_args()
    
    logger.info(f"Starting Phase 5 for {args.ticker}")
    
    news_file = settings.data_dir / "processed" / "features" / f"{args.ticker}_news_nlp.json"
    market_file = settings.data_dir / "processed" / "features" / f"{args.ticker}_{args.interval}_market_features.csv"
    
    if not news_file.exists() or not market_file.exists():
        logger.error("Missing necessary NLP JSON or Market CSV files.")
        return
        
    # 1. Merge the streams
    matrix_df = FeatureBuilder.build_matrix(str(news_file), str(market_file))
    
    if matrix_df.empty:
        logger.error("Feature Matrix is empty after merge.")
        return
        
    # 2. Calculate Targets (The y-variables)
    logger.info("Calculating Targets (CAR, Impact Score, Direction)...")
    
    # Target calculations require the raw market df so we can look at forward returns.
    # Since matrix_df already has the market columns appended for each event, we can calculate targets directly on it.
    # However, since multiple news events might happen on the same day, they will have the same forward returns.
    
    matrix_df = TargetCreator.calculate_abnormal_return(matrix_df, target_prefix='SPY')
    matrix_df = TargetCreator.calculate_impact_score(matrix_df)
    matrix_df = TargetCreator.calculate_direction(matrix_df)
    
    # Drop rows at the very end of the dataset where forward return couldn't be calculated
    matrix_df = matrix_df.dropna(subset=['Impact_Score'])
    
    # 3. Save Final Dataset
    output_dir = settings.data_dir / "processed"
    output_file = output_dir / f"{args.ticker}_final_dataset.csv"
    
    matrix_df.to_csv(output_file, index=False)
    
    logger.info(f"Phase 5 Complete! Master Feature Matrix saved to {output_file}")
    logger.info(f"Final shape: {matrix_df.shape[0]} events, {matrix_df.shape[1]} features/targets.")

if __name__ == "__main__":
    main()
