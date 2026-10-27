import React from 'react';
import { RefreshCw } from 'lucide-react';
import { MarketIndexData, Prediction } from '../types';

interface MarketOverviewProps {
  indices: Record<string, MarketIndexData>;
  priceLastUpdated: string;
  predictions: Prediction[];
  fetchingPrices: boolean;
  onRefreshPrices: () => void;
}

export const MarketOverview: React.FC<MarketOverviewProps> = ({
  indices,
  priceLastUpdated,
  predictions,
  fetchingPrices,
  onRefreshPrices
}) => {
  // Market sentiment calculated from recent live predictions
  const recentPredictions = predictions.slice(0, 10);
  const avgConfidence =
    recentPredictions.length > 0
      ? recentPredictions.reduce((sum, p) => sum + (p.confidence_score || 50), 0) / recentPredictions.length
      : 65;

  const bullishPct = Math.round(avgConfidence);
  const sentimentLabel = bullishPct > 55 ? 'BULLISH' : bullishPct < 45 ? 'BEARISH' : 'NEUTRAL';
  const sentimentColor = bullishPct > 55 ? 'text-emerald-400' : bullishPct < 45 ? 'text-red-400' : 'text-slate-400';
  const barColor = bullishPct > 55 ? 'bg-emerald-500' : bullishPct < 45 ? 'bg-red-500' : 'bg-slate-400';

  const hasIndices = Object.keys(indices).length > 0;

  return (
    <div className="max-w-7xl mx-auto mb-6 bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
      <div className="flex flex-wrap items-center gap-6">
        {hasIndices ? (
          Object.entries(indices).map(([name, data]) => (
            <div key={name} className="flex flex-col">
              <span className="text-xs text-slate-500 font-bold tracking-wider">{name}</span>
              <span className={`text-sm font-bold font-mono ${data.change_pct >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {data.change_pct >= 0 ? '▲' : '▼'} {Math.abs(data.change_pct).toFixed(2)}%
              </span>
            </div>
          ))
        ) : (
          <>
            <div className="flex flex-col"><span className="text-xs text-slate-500 font-bold tracking-wider">S&P 500</span><span className="text-slate-500 text-sm font-bold animate-pulse">Loading...</span></div>
            <div className="flex flex-col"><span className="text-xs text-slate-500 font-bold tracking-wider">NASDAQ</span><span className="text-slate-500 text-sm font-bold animate-pulse">Loading...</span></div>
            <div className="flex flex-col"><span className="text-xs text-slate-500 font-bold tracking-wider">DOW</span><span className="text-slate-500 text-sm font-bold animate-pulse">Loading...</span></div>
          </>
        )}

        {priceLastUpdated && (
          <div className="hidden sm:flex flex-col justify-end">
            <span className="text-[10px] text-slate-600 font-mono">Synced {priceLastUpdated}</span>
          </div>
        )}
      </div>

      <div className="flex items-center justify-between md:justify-end gap-5">
        <div className="text-right">
          <span className="text-xs text-slate-500 font-bold block mb-1">AI MARKET SENTIMENT</span>
          <div className="flex items-center gap-2">
            <div className="w-28 sm:w-32 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div className={`h-full transition-all duration-500 ${barColor}`} style={{ width: `${bullishPct}%` }}></div>
            </div>
            <span className={`text-xs font-bold font-mono ${sentimentColor}`}>{bullishPct}% {sentimentLabel}</span>
          </div>
        </div>

        <div className="h-8 w-px bg-slate-800 hidden sm:block"></div>

        <div className="flex items-center gap-3">
          <div className="flex flex-col items-center">
            <span className="text-lg font-bold text-blue-400 font-mono leading-none">{predictions.length}</span>
            <span className="text-[10px] text-slate-500 font-bold tracking-wider mt-0.5">SIGNALS</span>
          </div>

          <button
            onClick={onRefreshPrices}
            disabled={fetchingPrices}
            title="Refresh real-time prices & indices"
            className="p-2 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition-colors disabled:opacity-50 cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${fetchingPrices ? 'animate-spin text-blue-400' : ''}`} />
          </button>
        </div>
      </div>
    </div>
  );
};
