import { useState, useEffect, useCallback } from 'react';
import { Activity } from 'lucide-react';
import { TickerSymbol, Prediction, LivePriceData, MarketIndexData, NewsHeadline, HistoricalLog } from './types';
import { marketService } from './services/marketService';
import { useMarketWebSocket } from './hooks/useMarketWebSocket';
import { Header } from './components/Header';
import { AlertBanner } from './components/AlertBanner';
import { MarketOverview } from './components/MarketOverview';
import { Watchlist } from './components/Watchlist';
import { NewsInput } from './components/NewsInput';
import { LiveNewsModal } from './components/LiveNewsModal';
import { PredictionCard } from './components/prediction/PredictionCard';
import { ConfidenceTimeline } from './components/ConfidenceTimeline';
import { PerformanceTable } from './components/PerformanceTable';

export default function App() {
  const [ticker, setTicker] = useState<TickerSymbol>('NVDA');
  const [headline, setHeadline] = useState('');
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [history, setHistory] = useState<HistoricalLog[]>([]);
  const [accuracy, setAccuracy] = useState(0);

  // Live market state
  const [livePrices, setLivePrices] = useState<Record<string, LivePriceData>>({});
  const [marketIndices, setMarketIndices] = useState<Record<string, MarketIndexData>>({});
  const [priceLastUpdated, setPriceLastUpdated] = useState('');
  const [fetchingPrices, setFetchingPrices] = useState(false);

  // Live news drawer state
  const [newsHeadlines, setNewsHeadlines] = useState<NewsHeadline[]>([]);
  const [fetchingNews, setFetchingNews] = useState(false);
  const [showNewsPanel, setShowNewsPanel] = useState(false);

  // WebSocket Connection
  const { isConnected: wsConnected } = useMarketWebSocket({
    onMessage: (newPrediction) => {
      setPredictions((prev) => [newPrediction, ...prev]);
      setLoading(false);
    }
  });

  // Fetch live quotes and index prices
  const fetchPrices = useCallback(async () => {
    setFetchingPrices(true);
    try {
      const [prices, indices] = await Promise.all([
        marketService.fetchLivePrices(),
        marketService.fetchMarketIndices()
      ]);
      setLivePrices(prices);
      setMarketIndices(indices);
      setPriceLastUpdated(new Date().toLocaleTimeString());
    } catch (e) {
      console.error('Failed to load market prices:', e);
    } finally {
      setFetchingPrices(false);
    }
  }, []);

  // Fetch live news from RSS
  const fetchNews = useCallback(async (sym: string) => {
    setFetchingNews(true);
    setShowNewsPanel(true);
    setNewsHeadlines([]);
    try {
      const headlines = await marketService.fetchLiveNews(sym);
      setNewsHeadlines(headlines);
    } catch (e) {
      console.error('Failed to load RSS news:', e);
    } finally {
      setFetchingNews(false);
    }
  }, []);

  // Load history & prices on mount
  useEffect(() => {
    marketService.fetchHistory()
      .then((data) => {
        setHistory(data.history);
        setAccuracy(data.accuracy);
      })
      .catch((e) => console.error('Failed to fetch prediction history:', e));

    fetchPrices();

    // Auto-refresh prices every 60 seconds
    const interval = setInterval(fetchPrices, 60000);
    return () => clearInterval(interval);
  }, [fetchPrices]);

  // Execute AI Prediction Pipeline
  const handleExecuteAI = async () => {
    if (!headline.trim()) return;
    setLoading(true);
    try {
      await marketService.triggerPrediction(ticker, headline);
    } catch (e) {
      console.error('Failed to trigger prediction:', e);
      setLoading(false);
    }
  };

  const latestPred = predictions[0];
  const displayPredictions = predictions.filter((p) => p.ticker === ticker);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-4 sm:p-6">
      {/* 1. HIGH CONFIDENCE ALERT BANNER */}
      <AlertBanner prediction={latestPred} selectedTicker={ticker} />

      {/* 2. LIVE MARKET OVERVIEW (INDICES + SENTIMENT) */}
      <MarketOverview
        indices={marketIndices}
        priceLastUpdated={priceLastUpdated}
        predictions={predictions}
        fetchingPrices={fetchingPrices}
        onRefreshPrices={fetchPrices}
      />

      {/* 3. APP HEADER */}
      <Header
        wsConnected={wsConnected}
        onExportCSV={marketService.exportPredictionsCSV}
      />

      {/* 4. MAIN WORKSPACE */}
      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT COLUMN: Watchlist & News Input Form */}
        <div className="lg:col-span-4 xl:col-span-3 space-y-6">
          <Watchlist
            selectedTicker={ticker}
            livePrices={livePrices}
            onSelectTicker={(newTicker) => {
              setTicker(newTicker);
              setShowNewsPanel(false);
            }}
          />

          <NewsInput
            ticker={ticker}
            headline={headline}
            loading={loading}
            fetchingNews={fetchingNews}
            onHeadlineChange={setHeadline}
            onFetchLiveNews={() => fetchNews(ticker)}
            onExecuteAI={handleExecuteAI}
          />
        </div>

        {/* RIGHT COLUMN: Live News Drawer & Signal Feed */}
        <div className="lg:col-span-8 xl:col-span-9 space-y-6">
          <LiveNewsModal
            show={showNewsPanel}
            ticker={ticker}
            headlines={newsHeadlines}
            fetchingNews={fetchingNews}
            onClose={() => setShowNewsPanel(false)}
            onSelectHeadline={(selectedTitle) => setHeadline(selectedTitle)}
          />

          <div className="flex items-center justify-between pb-1">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              Live {ticker} Signal Feed
            </h2>
            <span className="text-xs text-slate-500 font-mono">
              {displayPredictions.length} prediction{displayPredictions.length !== 1 ? 's' : ''} for {ticker}
            </span>
          </div>

          {displayPredictions.length === 0 ? (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center shadow-xl">
              <Activity className="w-12 h-12 text-slate-700 mx-auto mb-3 animate-pulse" />
              <div className="text-slate-400 font-bold mb-1">No Active Signals For {ticker}</div>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Select a live headline or type a rumor in the Feed News panel on the left, then click "Execute {ticker} AI".
              </p>
            </div>
          ) : (
            <div className="space-y-6">
              {displayPredictions.map((pred, i) => (
                <PredictionCard
                  key={`${pred.timestamp}-${i}`}
                  prediction={pred}
                  livePrice={livePrices[pred.ticker]?.price}
                />
              ))}
            </div>
          )}
        </div>
      </main>

      {/* 5. PREDICTION CONFIDENCE TIMELINE */}
      <ConfidenceTimeline predictions={predictions} />

      {/* 6. HISTORICAL MODEL PERFORMANCE TABLE */}
      <PerformanceTable
        history={history}
        accuracy={accuracy}
        onExportCSV={marketService.exportPredictionsCSV}
      />
    </div>
  );
}
