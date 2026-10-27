import React from 'react';
import { Zap, Newspaper } from 'lucide-react';
import { TickerSymbol } from '../types';

interface NewsInputProps {
  ticker: TickerSymbol;
  headline: string;
  loading: boolean;
  fetchingNews: boolean;
  onHeadlineChange: (val: string) => void;
  onFetchLiveNews: () => void;
  onExecuteAI: () => void;
}

export const NewsInput: React.FC<NewsInputProps> = ({
  ticker,
  headline,
  loading,
  fetchingNews,
  onHeadlineChange,
  onFetchLiveNews,
  onExecuteAI
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl sticky top-6">
      <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4">
        <Zap className="w-5 h-5 text-blue-400" /> Feed News
      </h2>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase tracking-wider">
            ACTIVE TICKER
          </label>
          <div className="w-full bg-slate-950/70 border border-slate-800 rounded-lg px-3.5 py-2.5 text-blue-400 font-mono font-bold text-sm">
            {ticker}
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase tracking-wider">
            HEADLINE / RUMOR
          </label>
          <textarea
            value={headline}
            onChange={(e) => onHeadlineChange(e.target.value)}
            placeholder={`E.g., ${ticker} unveils next-generation enterprise chip with record power efficiency...`}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-3 text-slate-200 text-sm focus:outline-none focus:border-blue-500 transition-colors h-28 resize-none shadow-inner"
          />
        </div>

        <button
          onClick={onFetchLiveNews}
          disabled={fetchingNews}
          className="w-full border border-slate-700/80 hover:border-blue-500 text-slate-300 hover:text-blue-400 font-medium py-2.5 rounded-lg transition-all flex items-center justify-center gap-2 text-sm bg-slate-950/40 hover:bg-slate-800/40 cursor-pointer disabled:opacity-50"
        >
          <Newspaper className={`w-4 h-4 ${fetchingNews ? 'animate-pulse text-blue-400' : ''}`} />
          {fetchingNews ? 'Fetching Headlines...' : `Fetch Live ${ticker} News`}
        </button>

        <button
          onClick={onExecuteAI}
          disabled={loading || !headline.trim()}
          className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg shadow-lg shadow-blue-500/20 transition-all flex items-center justify-center gap-2 cursor-pointer"
        >
          {loading ? (
            <span className="animate-pulse flex items-center gap-2">
              <Zap className="w-4 h-4 animate-spin" /> Analyzing Intelligence...
            </span>
          ) : (
            `Execute ${ticker} AI`
          )}
        </button>
      </div>
    </div>
  );
};

