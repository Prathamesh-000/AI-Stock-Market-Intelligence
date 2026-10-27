import React from 'react';
import { BrainCircuit } from 'lucide-react';
import { FinBERTMetrics } from '../../types';

interface SentimentGaugeProps {
  finbert: FinBERTMetrics;
}

export const SentimentGauge: React.FC<SentimentGaugeProps> = ({ finbert }) => {
  const isPos = finbert.score >= 0;

  return (
    <div className="bg-slate-950/50 rounded-lg border border-slate-800 p-4 flex flex-col justify-between">
      <div>
        <div className="text-xs text-slate-500 font-bold mb-3 flex items-center gap-1.5">
          <BrainCircuit className="w-4 h-4 text-cyan-400" /> FINBERT NLP SENTIMENT
        </div>
        <div className={`text-lg font-black tracking-wide mb-4 ${isPos ? 'text-emerald-400' : 'text-red-400'}`}>
          {finbert.label || 'POSITIVE'}
        </div>
      </div>

      <div className="space-y-3 text-sm">
        <div className="flex justify-between items-center">
          <span className="text-slate-400 text-xs">Dominant Conviction</span>
          <span className={`font-mono font-bold text-xs ${isPos ? 'text-emerald-400' : 'text-red-400'}`}>
            {finbert.positive || 82}%
          </span>
        </div>

        <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${isPos ? 'bg-emerald-500' : 'bg-red-500'}`}
            style={{ width: `${finbert.positive || 82}%` }}
          />
        </div>

        <div className="flex justify-between items-center pt-2 border-t border-slate-900">
          <span className="text-slate-400 text-xs">Polarity Index</span>
          <span className="font-mono text-blue-400 font-bold text-xs">
            {finbert.score > 0 ? '+' : ''}{finbert.score?.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  );
};

