import asyncio
import logging
import yfinance as yf
from datetime import datetime, timezone, timedelta
from src.database.db import SessionLocal
from src.database.models import PredictionLog

logger = logging.getLogger(__name__)

async def start_market_tracker():
    """
    Background daemon that runs continuously.
    Objective 6: High-Frequency Continuous Evaluation.
    Tracks actual market reaction vs predicted impact at 15m, 30m, 1h, and 1d intervals.
    """
    logger.info("Starting High-Frequency Market Tracker (Objective 6)...")
    
    while True:
        try:
            await track_pending_predictions()
        except Exception as e:
            logger.error(f"Market Tracker encountered an error: {e}")
            
        # Run every 60 seconds
        await asyncio.sleep(60)

async def track_pending_predictions():
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        
        # We only want to track predictions made in the last 24 hours that aren't fully resolved yet
        cutoff = now - timedelta(days=2)
        pending = db.query(PredictionLog).filter(
            PredictionLog.created_at >= cutoff,
            PredictionLog.actual_1d_return == None
        ).all()
        
        if not pending:
            return
            
        tickers = list(set([p.ticker for p in pending]))
        logger.info(f"Market Tracker checking {len(pending)} pending predictions across {tickers}")
        
        # Fetch current price for all tickers in one go to save API calls
        live_prices = {}
        for ticker in tickers:
            try:
                # yf.Ticker(ticker).fast_info['last_price'] is fast and doesn't download huge history
                info = yf.Ticker(ticker).fast_info
                live_prices[ticker] = info['last_price']
            except Exception as e:
                logger.warning(f"Could not fetch live price for {ticker}: {e}")
                
        # Process each pending prediction
        for p in pending:
            current_price = live_prices.get(p.ticker)
            if not current_price:
                continue
                
            # If price_at_prediction is missing (just generated), set it now
            if p.price_at_prediction is None:
                p.price_at_prediction = current_price
                db.commit()
                continue
                
            # Calculate elapsed time in minutes
            # Since created_at is naive UTC from datetime.utcnow(), we must ensure we compare correctly.
            # In models.py we used datetime.now(timezone.utc) but SQLAlchemy often strips timezone.
            # Let's handle naive datetimes if necessary.
            p_time = p.created_at
            if p_time.tzinfo is None:
                p_time = p_time.replace(tzinfo=timezone.utc)
                
            elapsed_mins = (now - p_time).total_seconds() / 60.0
            
            # Calculate current return %
            ret_pct = ((current_price - p.price_at_prediction) / p.price_at_prediction) * 100.0
            
            updated = False
            
            # 15 Minute Check
            if elapsed_mins >= 15 and p.actual_15m_return is None:
                p.actual_15m_return = round(ret_pct, 4)
                updated = True
                
            # 30 Minute Check
            if elapsed_mins >= 30 and p.actual_30m_return is None:
                p.actual_30m_return = round(ret_pct, 4)
                updated = True
                
            # 1 Hour Check
            if elapsed_mins >= 60 and p.actual_1h_return is None:
                p.actual_1h_return = round(ret_pct, 4)
                updated = True
                
            # 1 Day (24 Hour) Check
            if elapsed_mins >= 1440 and p.actual_1d_return is None:
                p.actual_1d_return = round(ret_pct, 4)
                
                # Check if model was correct
                # E.g., if predicted BUY (positive impact) and return is > 0, it was correct
                if (p.signal == 'BUY' and ret_pct > 0) or (p.signal == 'SELL' and ret_pct < 0):
                    p.is_correct = 1
                elif p.signal == 'UNCERTAIN':
                    p.is_correct = None
                else:
                    p.is_correct = 0
                    
                updated = True
                logger.info(f"Prediction Resolved! [{p.ticker}] Signal: {p.signal}, Actual 1D Return: {p.actual_1d_return}%, Correct: {p.is_correct}")

            if updated:
                db.commit()

    finally:
        db.close()
