import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { Prediction } from '../types';

interface AlertBannerProps {
  prediction?: Prediction;
  selectedTicker: string;
}

export const AlertBanner: React.FC<AlertBannerProps> = ({ prediction, selectedTicker }) => {
  if (!prediction) return null;

  const isHighConfidence =
    prediction.ticker === selectedTicker &&
    prediction.confidence_score > 75 &&
    prediction.signal !== 'UNCERTAIN';

  if (!isHighConfidence) return null;

  const isBuy = prediction.signal === 'BUY';

  return (
    <div
      className={`max-w-7xl mx-auto mb-4 px-5 py-3 rounded-lg border flex items-center gap-3 animate-pulse shadow-lg ${
        isBuy
          ? 'bg-emerald-900/30 border-emerald-500/50 text-emerald-400'
          : 'bg-red-900/30 border-red-500/50 text-red-400'
      }`}
    >
      <AlertTriangle className="w-5 h-5 flex-shrink-0" />
      <span className="font-bold text-sm tracking-wide">
        HIGH CONFIDENCE {prediction.signal} SIGNAL — {selectedTicker} | {prediction.confidence_score.toFixed(1)}% confidence | Expected Move: {prediction.pred_1h > 0 ? '+' : ''}{prediction.pred_1h?.toFixed(2)}% (1H)
      </span>
    </div>
  );
};

