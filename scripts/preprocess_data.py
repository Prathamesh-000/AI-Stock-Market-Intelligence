import sys
import os
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import json
import pandas as pd
from config.settings import settings
from src.preprocessing.market_cleaner import MarketCleaner
from src.preprocessing.news_cleaner import NewsCleaner
from src.preprocessing.deduplication import NewsDeduplicator
from src.preprocessing.timestamp_sync import TimestampSynchronizer

logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Clean and Synchronize Market and News Data (Phase 2)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0], help="Target stock ticker")
    parser.add_argument("--interval", type=str, default="1d", help="Market data interval to clean")
    
    args = parser.parse_args()
    
    logger.info(f"Starting Phase 2 Preprocessing for {args.ticker}")
    
    # --- 1. Process Market Data ---
    raw_market_file = settings.raw_market_dir / f"{args.ticker}_{args.interval}.csv"
    if raw_market_file.exists():
        df = pd.read_csv(raw_market_file)
        clean_df = MarketCleaner.clean_data(df)
        
        proc_market_dir = settings.data_dir / "processed" / "market"
        proc_market_dir.mkdir(parents=True, exist_ok=True)
        
        clean_file = proc_market_dir / f"{args.ticker}_{args.interval}_clean.csv"
        clean_df.to_csv(clean_file, index=False)
        logger.info(f"Cleaned Market Data saved to {clean_file}")
    else:
        logger.warning(f"Raw market file {raw_market_file} not found.")

    # --- 2. Process News Data ---
    raw_news_file = settings.raw_news_dir / f"{args.ticker}_news.json"
    if raw_news_file.exists():
        with open(raw_news_file, 'r', encoding='utf-8') as f:
            raw_news = json.load(f)
            
        # Step A: Clean Text
        cleaned_news = NewsCleaner.clean_news_list(raw_news)
        
        # Step B: Deduplicate
        dedup_news = NewsDeduplicator.deduplicate(cleaned_news, time_window_hours=12)
        
        # Step C: Timestamp Synchronization
        for item in dedup_news:
            # Create a new field that tells us exactly when the market reacts
            item['market_reaction_time'] = TimestampSynchronizer.align_to_market_reaction_time(item['published_at'])
            
        proc_news_dir = settings.data_dir / "processed" / "news"
        proc_news_dir.mkdir(parents=True, exist_ok=True)
        
        clean_news_file = proc_news_dir / f"{args.ticker}_news_clean.json"
        with open(clean_news_file, 'w', encoding='utf-8') as f:
            json.dump(dedup_news, f, indent=4, ensure_ascii=False)
            
        logger.info(f"Cleaned News Data (Synchronized) saved to {clean_news_file}")
    else:
        logger.warning(f"Raw news file {raw_news_file} not found.")

    logger.info("Phase 2 Preprocessing completed successfully.")

if __name__ == "__main__":
    main()

