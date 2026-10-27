import { API_URL } from '../config/api';
import { MarketIndexData, LivePriceData, NewsHeadline, HistoricalLog } from '../types';

export const marketService = {
  async fetchLivePrices(): Promise<Record<string, LivePriceData>> {
    const res = await fetch(`${API_URL}/live-prices`);
    if (!res.ok) throw new Error('Failed to fetch live prices');
    const data = await res.json();
    return data.prices || {};
  },

  async fetchMarketIndices(): Promise<Record<string, MarketIndexData>> {
    const res = await fetch(`${API_URL}/market-indices`);
    if (!res.ok) throw new Error('Failed to fetch market indices');
    const data = await res.json();
    return data.indices || {};
  },

  async fetchLiveNews(ticker: string): Promise<NewsHeadline[]> {
    const res = await fetch(`${API_URL}/live-news/${ticker}`);
    if (!res.ok) throw new Error(`Failed to fetch live news for ${ticker}`);
    const data = await res.json();
    return data.headlines || [];
  },

  async fetchHistory(): Promise<{ history: HistoricalLog[]; accuracy: number }> {
    const res = await fetch(`${API_URL}/history`);
    if (!res.ok) throw new Error('Failed to fetch prediction history');
    const data = await res.json();
    return {
      history: data.history || [],
      accuracy: data.accuracy || 0
    };
  },

  async triggerPrediction(ticker: string, headline: string): Promise<void> {
    const res = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker, headline, summary: '' })
    });
    if (!res.ok) throw new Error('Failed to start prediction pipeline');
  },

  exportPredictionsCSV(): void {
    window.open(`${API_URL}/export-predictions`, '_blank');
  }
};

