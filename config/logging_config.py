"""Structured logging configuration for AI Stock Market Intelligence."""

import os
import sys
import logging
from pathlib import Path

def setup_logging(level: str = "INFO", log_to_file: bool = True) -> logging.Logger:
    """
    Configures standard structured logging across all terminal,
    data pipeline, and API components.
    """
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_to_file:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        handlers.append(file_handler)
        
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True
    )
    
    logger = logging.getLogger("market_intelligence")
    logger.setLevel(numeric_level)
    return logger

logger = setup_logging()

