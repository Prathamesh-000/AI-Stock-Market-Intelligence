# Data Directory

This directory contains all project data files.

## Structure

```
data/
├── raw/            # Original, unprocessed data (gitignored except .gitkeep)
│   ├── news/       # Raw news JSON from yfinance/RSS
│   └── prices/     # Raw OHLCV price data
├── processed/      # Cleaned and feature-engineered data
│   ├── features/   # NLP feature JSONs
│   └── *.csv       # Final datasets per ticker
├── external/       # Third-party data (market indices, etc.)
└── vector_store/   # RAG embeddings
    ├── historical_news_embeddings.npy
    └── historical_news_metadata.json
```

## Important Notes

- Raw and processed CSV data is gitignored (large files)
- Vector store files ARE committed (required for RAG to work)
- Never commit `.env` or API keys
- The `trade_logs.db` SQLite file is gitignored (runtime data)
