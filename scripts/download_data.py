import argparse
import logging
import json
import os
from datetime import datetime, timedelta
from config.settings import settings
from src.data.market_data import YFinanceMarketProvider
from src.data.news_data import FinnhubNewsProvider, YahooNewsProvider

# Configure basic logging for the script
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Download Market and News Data (Phase 1)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0], help="Target stock ticker (e.g., NVDA)")
    parser.add_argument("--benchmark", type=str, default=settings.default_benchmark, help="Broad market benchmark (e.g., SPY)")
    parser.add_argument("--sector", type=str, default=settings.default_sector, help="Sector benchmark (e.g., XLK)")
    parser.add_argument("--start", type=str, help="Start date YYYY-MM-DD", default=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
    parser.add_argument("--end", type=str, help="End date YYYY-MM-DD", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--interval", type=str, default="1d", help="Market data interval (1d, 1h, 15m)")
    
    args = parser.parse_args()
    
    logger.info(f"Starting Data Download for {args.ticker}")
    logger.info(f"Context: Benchmark={args.benchmark}, Sector={args.sector}")
    logger.info(f"Period: {args.start} to {args.end} | Interval: {args.interval}")
    
    # 1. Market Data Collection
    market_provider = YFinanceMarketProvider()
    market_data = market_provider.fetch_market_and_benchmarks(
        ticker=args.ticker,
        benchmark=args.benchmark,
        sector=args.sector,
        start_date=args.start,
        end_date=args.end,
        interval=args.interval
    )
    
    # Save Market Data
    for symbol, df in market_data.items():
        if not df.empty:
            file_path = settings.raw_market_dir / f"{symbol}_{args.interval}.csv"
            df.to_csv(file_path, index=False)
            logger.info(f"Saved {symbol} market data ({len(df)} rows) to {file_path}")
        else:
            logger.warning(f"No market data retrieved for {symbol}")

    # 2. News Data Collection
    all_news = []
    
    # Finnhub
    if settings.finnhub_api_key and settings.finnhub_api_key != "your_finnhub_api_key_here":
        finnhub_provider = FinnhubNewsProvider(api_key=settings.finnhub_api_key)
        finnhub_news = finnhub_provider.fetch_news(args.ticker, args.start, args.end)
        all_news.extend(finnhub_news)
    else:
        logger.warning("FINNHUB_API_KEY not set in .env. Skipping Finnhub news collection.")
        
    # Yahoo
    yahoo_provider = YahooNewsProvider()
    yahoo_news = yahoo_provider.fetch_news(args.ticker, args.start, args.end)
    all_news.extend(yahoo_news)
    
    # Deduplication Step (Basic matching on URL/Headline)
    unique_news = {}
    for item in all_news:
        unique_news[item['event_id']] = item
    
    final_news_list = list(unique_news.values())
    
    # Save News Data
    if final_news_list:
        news_file_path = settings.raw_news_dir / f"{args.ticker}_news.json"
        with open(news_file_path, 'w', encoding='utf-8') as f:
            json.dump(final_news_list, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(final_news_list)} unique news events to {news_file_path}")
    else:
        logger.warning(f"No news data retrieved for {args.ticker}")
        
    logger.info("Download completed successfully.")

if __name__ == "__main__":
    main()

