import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import pandas as pd
from config.settings import settings
from src.features.technical import TechnicalFeatures
from src.features.volatility import VolatilityFeatures
from src.features.volume import VolumeFeatures
from src.features.regime import MarketRegime
from src.features.relative_performance import RelativePerformance

logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run Market Engine (Phase 4)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0])
    parser.add_argument("--benchmark", type=str, default=settings.default_benchmark)
    parser.add_argument("--sector", type=str, default=settings.default_sector)
    parser.add_argument("--interval", type=str, default="1d")
    args = parser.parse_args()
    
    logger.info(f"Starting Market Engine for {args.ticker}")
    
    # Load clean market data
    stock_file = settings.data_dir / "processed" / "market" / f"{args.ticker}_{args.interval}_clean.csv"
    bench_file = settings.data_dir / "processed" / "market" / f"{args.benchmark}_{args.interval}_clean.csv"
    sector_file = settings.data_dir / "processed" / "market" / f"{args.sector}_{args.interval}_clean.csv"
    
    if not stock_file.exists():
        logger.error(f"Clean market file not found: {stock_file}")
        return
        
    df = pd.read_csv(stock_file)
    # Ensure Timestamp is parsed as datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    logger.info("Calculating Technical Indicators (RSI, SMA, MACD)...")
    df = TechnicalFeatures.add_sma(df, windows=[10, 20, 50, 200])
    df = TechnicalFeatures.add_rsi(df, window=14)
    df = TechnicalFeatures.add_macd(df)
    
    logger.info("Calculating Volatility Metrics (ATR, Bollinger Bands)...")
    df = VolatilityFeatures.add_atr(df, window=14)
    df = VolatilityFeatures.add_bollinger_bands(df, window=20)
    
    logger.info("Calculating Volume Anomalies (RVOL)...")
    df = VolumeFeatures.add_relative_volume(df, window=20)
    
    # Process Benchmarks if available
    if bench_file.exists():
        logger.info(f"Adding Macro Context vs {args.benchmark}...")
        df_bench = pd.read_csv(bench_file)
        df_bench['Timestamp'] = pd.to_datetime(df_bench['Timestamp'])
        
        # 1. Market Regime
        df_regime = MarketRegime.detect_regime(df_bench)
        df = pd.merge(df, df_regime, on='Timestamp', how='left')
        
        # 2. Relative Performance
        df_rp = RelativePerformance.calculate_relative_strength(df, df_bench, prefix=args.benchmark)
        df = pd.merge(df, df_rp, on='Timestamp', how='left')
        
    if sector_file.exists():
        logger.info(f"Adding Sector Context vs {args.sector}...")
        df_sector = pd.read_csv(sector_file)
        df_sector['Timestamp'] = pd.to_datetime(df_sector['Timestamp'])
        df_rp_sec = RelativePerformance.calculate_relative_strength(df, df_sector, prefix=args.sector)
        df = pd.merge(df, df_rp_sec, on='Timestamp', how='left')

    # Drop early rows that have NaNs due to rolling windows
    # Note: If we only downloaded 1 month of data, dropping NAs for a 200 SMA will drop everything!
    # For now, we will NOT dropna so you can inspect the data. ML pipeline will drop later.
    
    output_dir = settings.data_dir / "processed" / "features"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{args.ticker}_{args.interval}_market_features.csv"
    df.to_csv(output_file, index=False)
    
    logger.info(f"Market Engine complete! Generated {len(df.columns)} columns.")
    logger.info(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()

