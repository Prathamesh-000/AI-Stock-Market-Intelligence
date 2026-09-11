import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class NewsDeduplicator:
    """
    Groups duplicate or highly similar news articles published around the same time 
    into a single canonical event to prevent inflating event significance.
    """
    @staticmethod
    def deduplicate(news_list: List[Dict[str, Any]], time_window_hours: int = 12) -> List[Dict[str, Any]]:
        if not news_list:
            return []
            
        # Sort chronologically
        sorted_news = sorted(news_list, key=lambda x: x['published_at'])
        
        canonical_events = []
        
        for current_news in sorted_news:
            current_time = datetime.fromisoformat(current_news['published_at'].replace('Z', '+00:00'))
            current_headline = current_news['headline'].lower()
            
            is_duplicate = False
            
            # Check backwards through recent canonical events
            # We look in reverse to find the most recent matching event
            for canonical in reversed(canonical_events):
                canon_time = datetime.fromisoformat(canonical['published_at'].replace('Z', '+00:00'))
                
                # If we've looked past the time window, stop checking
                if (current_time - canon_time).total_seconds() > (time_window_hours * 3600):
                    break
                    
                canon_headline = canonical['headline'].lower()
                
                # Very basic exact headline match or highly similar subset
                # In Phase 3, this can be upgraded to semantic embedding similarity
                if current_headline == canon_headline or current_headline in canon_headline or canon_headline in current_headline:
                    is_duplicate = True
                    # Append this source to the canonical event's source list
                    if 'duplicate_sources' not in canonical:
                        canonical['duplicate_sources'] = []
                    canonical['duplicate_sources'].append({
                        'publisher': current_news['publisher'],
                        'url': current_news['url'],
                        'published_at': current_news['published_at']
                    })
                    break
            
            if not is_duplicate:
                canonical_events.append(current_news)
                
        logger.info(f"Deduplication: Reduced {len(news_list)} raw items to {len(canonical_events)} canonical events.")
        return canonical_events

