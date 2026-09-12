import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import argparse
import logging
import json
from config.settings import settings
from src.sentiment.finbert import FinBERTSentiment
from src.sentiment.event_classifier import EventClassifier
from src.sentiment.novelty import NoveltyDetector

logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run NLP Engine (Phase 3)")
    parser.add_argument("--ticker", type=str, default=settings.default_tickers.split(",")[0], help="Target stock ticker")
    args = parser.parse_args()
    
    logger.info(f"Starting NLP Engine for {args.ticker}")
    
    # 1. Load Cleaned News
    clean_news_file = settings.data_dir / "processed" / "news" / f"{args.ticker}_news_clean.json"
    if not clean_news_file.exists():
        logger.error(f"Clean news file not found: {clean_news_file}. Run Phase 2 first.")
        return
        
    with open(clean_news_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
        
    if not news_data:
        logger.warning("News file is empty.")
        return

    # 2. Initialize Models
    logger.info("Initializing AI Models...")
    finbert = FinBERTSentiment()
    event_classifier = EventClassifier()
    novelty_detector = NoveltyDetector()
    
    enriched_news = []
    
    # 3. Process each article
    logger.info(f"Processing {len(news_data)} articles. This may take a while depending on GPU/CPU...")
    for idx, article in enumerate(news_data):
        headline = article.get('headline', '')
        summary = article.get('summary', '')
        
        # Combine for sentiment
        full_text = f"{headline}. {summary}"
        
        # --- A. Sentiment Analysis ---
        sentiment_results = finbert.get_sentiment(full_text)
        article.update(sentiment_results)
        
        # --- B. Event Classification ---
        # We classify based purely on headline for sharper event categorization
        event_results = event_classifier.classify_event(headline)
        article.update(event_results)
        
        # --- C. Novelty Detection ---
        # Look back at the last 7 days of articles (assuming news_data is chronologically sorted from Phase 2)
        current_time = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
        lookback_limit = current_time - timedelta(days=7)
        
        recent_headlines = []
        for past_article in reversed(enriched_news):
            past_time = datetime.fromisoformat(past_article['published_at'].replace('Z', '+00:00'))
            if past_time < lookback_limit:
                break
            recent_headlines.append(past_article['headline'])
            
        novelty_score = novelty_detector.calculate_novelty(headline, recent_headlines)
        article['novelty_score'] = novelty_score
        
        enriched_news.append(article)
        
        if (idx + 1) % 10 == 0:
            logger.info(f"Processed {idx + 1}/{len(news_data)} articles...")
            
    # 4. Save Enriched Data
    output_dir = settings.data_dir / "processed" / "features"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{args.ticker}_news_nlp.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enriched_news, f, indent=4, ensure_ascii=False)
        
    logger.info(f"NLP Engine complete. Saved enriched data to {output_file}")

if __name__ == "__main__":
    main()
