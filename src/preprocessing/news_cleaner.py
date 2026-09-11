import re
import html
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class NewsCleaner:
    """
    Cleans financial news text, removing HTML, weird unicode, and standardizing format.
    """
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Unescape HTML entities (e.g. &amp; -> &)
        text = html.unescape(text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove excessive whitespace/newlines
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def clean_news_list(news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned_list = []
        for item in news_list:
            cleaned_item = item.copy()
            cleaned_item['headline'] = NewsCleaner.clean_text(item.get('headline', ''))
            cleaned_item['summary'] = NewsCleaner.clean_text(item.get('summary', ''))
            
            # Skip items with no real content
            if not cleaned_item['headline']:
                continue
                
            cleaned_list.append(cleaned_item)
            
        logger.info(f"Cleaned {len(news_list)} news items. Kept {len(cleaned_list)} valid items.")
        return cleaned_list
