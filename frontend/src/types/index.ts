export type TickerSymbol = 'NVDA' | 'AMD' | 'AAPL' | 'TSLA' | 'MSFT';
export type Timeframe = '1D' | '1W' | '1M';
export type SignalType = 'BUY' | 'SELL' | 'UNCERTAIN';

export interface MarketIndexData {
  price: number;
  change_pct: number;
  change_str: string;
}

export interface LivePriceData {
  price: number;
  prev_close?: number;
  change_pct: number;
  change_str: string;
}

export interface FinBERTMetrics {
  score: number;
  label: string;
  positive: number;
  negative: number;
  neutral: number;
}

export interface FeatureDriver {
  name: string;
  value: number;
}

export interface HistoricalPrecedent {
  headline: string;
  date: string;
  event_type?: string;
  similarity?: number;
  actual_return_1d: number;
  source?: string;
}

export interface TechnicalMetric {
  name: string;
  value: string;
  detail: string;
}

export interface EvidentiarySources {
  primary_news?: {
    headline?: string;
    publisher?: string;
    type?: string;
    verification_status?: string;
    ticker?: string;
    quote_url?: string;
    timestamp?: string;
  };
  market_data?: {
    provider?: string;
    live_quote?: string;
    metrics?: TechnicalMetric[];
  };
  historical_rag?: HistoricalPrecedent[];
  quant_model?: {
    classifier?: string;
    calibrator?: string;
    training_corpus?: string;
    features_vector?: string;
  };
  nlp_models?: {
    event_extractor?: string;
    sentiment_classifier?: string;
  };
  sector_ripple?: {
    models?: string[];
    basis?: string;
  };
}

export interface Prediction {
  ticker: TickerSymbol;
  headline: string;
  signal: SignalType;
  confidence_score: number;
  explanation: string;
  event_type: string;
  llm_impact: number;
  similar_events?: HistoricalPrecedent[];
  sector_ripple: Record<string, number>;
  timestamp: string;
  current_price: number;
  pred_1h: number;
  pred_1d: number;
  finbert: FinBERTMetrics;
  ai_reasoning: string[];
  feature_importance: FeatureDriver[];
  source?: string;
  sources?: EvidentiarySources;
}

export interface NewsHeadline {
  title: string;
  summary?: string;
  published: string;
  link?: string;
  source?: string;
}

export interface HistoricalLog {
  date: string;
  ticker: string;
  prediction: string;
  actual: string;
  is_correct: boolean;
}

export interface ChartPoint {
  time: string;
  price: number;
}

export interface ChartDataResult {
  data: ChartPoint[];
  eventMarker: string;
  changePct: number;
  delta: number;
  currentPrice: number;
  periodLabel: string;
}
