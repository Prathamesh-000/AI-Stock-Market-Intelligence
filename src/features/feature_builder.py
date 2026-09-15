import pandas as pd
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FeatureBuilder:
    """
    Merges NLP JSON data with Market CSV data based on synchronized timestamps.
    """
    
    @staticmethod
    def build_matrix(news_file: str, market_file: str) -> pd.DataFrame:
        """
        Loads the news NLP json and the market features CSV.
        Merges them using the 'market_reaction_time' from the news and 'Timestamp' from the market.
        """
        logger.info(f"Building Feature Matrix...")
        
        # 1. Load Market Data
        df_market = pd.read_csv(market_file)
        df_market['Timestamp'] = pd.to_datetime(df_market['Timestamp'], utc=True)
        
        # Ensure we only have one row per day (in case of duplicate timestamps in raw data)
        df_market = df_market.drop_duplicates(subset=['Timestamp']).set_index('Timestamp')
        
        # 2. Load News Data
        with open(news_file, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
            
        # Convert News JSON to DataFrame
        df_news = pd.DataFrame(news_data)
        
        if df_news.empty:
            logger.warning("News data is empty. Returning empty Feature Matrix.")
            return pd.DataFrame()
            
        # Convert reaction time to Datetime (ensure UTC)
        df_news['market_reaction_time'] = pd.to_datetime(df_news['market_reaction_time'], utc=True)
        
        # 3. The Merger
        # For every news event, grab the market features for that EXACT market_reaction_time
        # Since 'market_reaction_time' is perfectly aligned to market open, we can do an exact match or 
        # a forward merge to get the closest trading day context.
        
        # Sort both
        df_news = df_news.sort_values('market_reaction_time')
        df_market = df_market.sort_index()
        
        # Use merge_asof to match the news to the *closest* market data point at or just before the reaction time
        # This prevents lookahead bias by ensuring we only join market context known AT the moment of the news reaction.
        merged_df = pd.merge_asof(
            df_news, 
            df_market.reset_index(), 
            left_on='market_reaction_time', 
            right_on='Timestamp', 
            direction='backward'
        )
        
        # Drop rows where we couldn't find matching market data
        original_len = len(merged_df)
        merged_df = merged_df.dropna(subset=['Close'])
        
        logger.info(f"Merged {len(merged_df)} events with Market Context (dropped {original_len - len(merged_df)} due to missing market history).")
        
        return merged_df

