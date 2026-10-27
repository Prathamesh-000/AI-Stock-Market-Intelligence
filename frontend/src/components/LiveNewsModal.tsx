import React from 'react';
import { Newspaper, ArrowRight } from 'lucide-react';
import { NewsHeadline, TickerSymbol } from '../types';

interface LiveNewsModalProps {
  show: boolean;
  ticker: TickerSymbol;
  headlines: NewsHeadline[];
  fetchingNews: boolean;
  onClose: () => void;
  onSelectHeadline: (headline: string) => void;
}

export const LiveNewsModal: React.FC<LiveNewsModalProps> = ({
  show,
  ticker,
  headlines,
  fetchingNews,
  onClose,
  onSelectHeadline
}) => {
  if (!show) return null;

  return (
    <div className="bg-slate-900 border border-slate-700/80 rounded-xl p-5 shadow-2xl animate-in fade-in duration-300">
      <div className="flex justify-between items-center mb-4 pb-2 border-b border-slate-800">
        <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
          <Newspaper className="w-4 h-4 text-blue-400" />
          Live {ticker} Headlines — Yahoo Finance Feed
        </h3>
        <button
          onClick={onClose}
          className="text-slate-500 hover:text-slate-300 text-xs px-2 py-1 rounded hover:bg-slate-800 transition-colors cursor-pointer"
        >
          ✕ Close
        </button>
      </div>

      {fetchingNews ? (
        <div className="text-slate-400 text-sm py-4 text-center animate-pulse flex items-center justify-center gap-2">
          <Newspaper className="w-4 h-4 animate-spin text-blue-400" /> Fetching latest RSS headlines...
        </div>
      ) : headlines.length === 0 ? (
        <div className="text-slate-500 text-sm py-4 text-center">No recent headlines found for {ticker}.</div>
      ) : (
        <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
          {headlines.map((item, i) => (
            <div
              key={i}
              className="border border-slate-800 rounded-lg p-3 hover:bg-slate-800/40 hover:border-slate-700 transition-all flex justify-between items-start gap-3 group"
            >
              <div className="flex-1">
                <button
                  onClick={() => onSelectHeadline(item.title)}
                  className="text-sm text-slate-200 hover:text-blue-400 text-left font-medium leading-snug transition-colors cursor-pointer block"
                >
                  {item.title}
                </button>
                <div className="text-[10px] text-slate-500 mt-1 font-mono">
                  {item.published} • {item.source || 'Yahoo Finance'}
                </div>
              </div>

              <button
                onClick={() => onSelectHeadline(item.title)}
                className="flex-shrink-0 text-xs bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 px-2.5 py-1.5 rounded border border-blue-500/30 transition-colors flex items-center gap-1 cursor-pointer font-medium"
              >
                Use <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

