import React from 'react';
import { LineChart as LineChartIcon } from 'lucide-react';
import { TickerSymbol, LivePriceData } from '../types';
import { SUPPORTED_TICKERS, FALLBACK_PRICES } from '../config/api';

interface WatchlistProps {
  selectedTicker: TickerSymbol;
  livePrices: Record<string, LivePriceData>;
  onSelectTicker: (ticker: TickerSymbol) => void;
}

export const Watchlist: React.FC<WatchlistProps> = ({
  selectedTicker,
  livePrices,
  onSelectTicker
}) => {
  const getPrice = (sym: string): LivePriceData => {
    if (livePrices[sym]) return livePrices[sym];
    const fb = FALLBACK_PRICES[sym];
    return {
      price: fb?.price || 0,
      change_str: fb?.change || 'N/A',
      change_pct: 0
    };
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      <div className="px-4 py-3 bg-slate-800/50 border-b border-slate-800 flex justify-between items-center">
        <span className="text-xs font-bold text-slate-400 tracking-wider">WATCHLIST</span>
        <LineChartIcon className="w-4 h-4 text-slate-500" />
      </div>

      <div className="divide-y divide-slate-800/80">
        {SUPPORTED_TICKERS.map((sym) => {
          const p = getPrice(sym);
          const isPos = (p.change_pct ?? 0) >= 0;
          const isSelected = selectedTicker === sym;

          return (
            <div
              key={sym}
              onClick={() => onSelectTicker(sym)}
              className={`px-4 py-3.5 flex justify-between items-center cursor-pointer transition-all ${
                isSelected
                  ? 'bg-blue-900/30 border-l-4 border-blue-500 shadow-inner'
                  : 'hover:bg-slate-800/50 border-l-4 border-transparent'
              }`}
            >
              <div className="flex flex-col">
                <span className={`font-bold font-mono text-sm ${isSelected ? 'text-blue-400' : 'text-slate-200'}`}>
                  {sym}
                </span>
                <span className="text-[10px] text-slate-500">
                  {sym === 'NVDA' ? 'NVIDIA Corp' :
                   sym === 'AMD' ? 'Advanced Micro' :
                   sym === 'AAPL' ? 'Apple Inc' :
                   sym === 'TSLA' ? 'Tesla Inc' : 'Microsoft Corp'}
                </span>
              </div>

              <div className="text-right">
                <div className="text-sm font-mono font-bold text-slate-200">
                  ${p.price?.toFixed(2) || '—'}
                </div>
                <div className={`text-xs font-bold font-mono ${isPos ? 'text-emerald-400' : 'text-red-400'}`}>
                  {p.change_str || '—'}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

