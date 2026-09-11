import pandas as pd
import pytz
from datetime import datetime, timedelta

class TimestampSynchronizer:
    """
    Aligns UTC news publication timestamps to the exact active US market trading hours (EST).
    Handles pre-market, after-hours, and weekends to prevent lookahead bias.
    """
    
    # Standard US Market Hours
    MARKET_OPEN = "09:30"
    MARKET_CLOSE = "16:00"
    EST_TZ = pytz.timezone('US/Eastern')
    
    @staticmethod
    def align_to_market_reaction_time(pub_time_utc: str) -> str:
        """
        Takes a UTC ISO string (e.g. '2024-01-12T20:30:00+00:00') and returns the 
        UTC ISO string representing when the market will officially react to it.
        """
        # Parse UTC time
        dt_utc = datetime.fromisoformat(pub_time_utc.replace('Z', '+00:00'))
        
        # Convert to US Eastern Time (EST/EDT)
        dt_est = dt_utc.astimezone(TimestampSynchronizer.EST_TZ)
        
        reaction_dt = dt_est
        
        # 1. Check Weekends (Saturday=5, Sunday=6)
        if dt_est.weekday() >= 5:
            days_to_add = 7 - dt_est.weekday() # Shift to Monday
            reaction_dt = dt_est + timedelta(days=days_to_add)
            # Set to exactly Market Open
            reaction_dt = reaction_dt.replace(hour=9, minute=30, second=0, microsecond=0)
            
        # 2. Check Weekday Time
        else:
            time_str = dt_est.strftime("%H:%M")
            
            if time_str < TimestampSynchronizer.MARKET_OPEN:
                # Pre-market news reacts at open today
                reaction_dt = dt_est.replace(hour=9, minute=30, second=0, microsecond=0)
                
            elif time_str >= TimestampSynchronizer.MARKET_CLOSE:
                # After-hours news reacts at open tomorrow
                reaction_dt = dt_est + timedelta(days=1)
                
                # If 'tomorrow' is Saturday, shift to Monday
                if reaction_dt.weekday() == 5:
                    reaction_dt = reaction_dt + timedelta(days=2)
                    
                reaction_dt = reaction_dt.replace(hour=9, minute=30, second=0, microsecond=0)
                
            else:
                # Intraday news reacts immediately (no shift needed)
                pass
                
        # Convert back to UTC for standard database storage
        reaction_dt_utc = reaction_dt.astimezone(pytz.utc)
        return reaction_dt_utc.isoformat()

