import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # API Keys
    finnhub_api_key: str = Field(default="")
    
    # Defaults
    default_tickers: str = Field(default="NVDA,AAPL")
    default_benchmark: str = Field(default="SPY")
    default_sector: str = Field(default="XLK")
    
    # Project Root and Paths
    project_root: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = Field(default=project_root / "data")
    logs_dir: Path = Field(default=project_root / "logs")
    
    # Logging
    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def raw_market_dir(self) -> Path:
        path = self.data_dir / "raw" / "market"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def raw_news_dir(self) -> Path:
        path = self.data_dir / "raw" / "news"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def processed_dir(self) -> Path:
        path = self.data_dir / "processed"
        path.mkdir(parents=True, exist_ok=True)
        return path

settings = Settings()

