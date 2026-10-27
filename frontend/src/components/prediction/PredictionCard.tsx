import React from 'react';
import { Clock, ShieldCheck } from 'lucide-react';
import { Prediction } from '../../types';
import { PriceChart } from './PriceChart';
import { SentimentGauge } from './SentimentGauge';
import { ReasoningBox } from './ReasoningBox';
import { SectorRipple } from './SectorRipple';
import { FeatureDrivers } from './FeatureDrivers';
import { EvidentiarySources } from './EvidentiarySources';

interface PredictionCardProps {
  prediction: Prediction;
  livePrice?: number;
}

export const PredictionCard: React.FC<PredictionCardProps> = ({
  prediction,
  livePrice
}) => {
  const isBuy = prediction.signal === 'BUY';
  const isSell = prediction.signal === 'SELL';
  const directionText = isBuy ? 'BULLISH' : isSell ? 'BEARISH' : 'UNCERTAIN';
  const directionColor = isBuy ? 'text-emerald-400' : isSell ? 'text-red-400' : 'text-slate-400';
  const expectedMoveColor = prediction.pred_1h > 0 ? 'text-emerald-400' : 'text-red-400';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl animate-in slide-in-from-top-4 fade-in duration-500">
      {/* TOP HEADER */}
      <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/20">
        <div className="flex items-center gap-3">
          <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded text-sm font-black border border-blue-500/30 font-mono">
            {prediction.ticker}
          </span>
          <div className="flex items-center gap-2.5 text-xs text-slate-400">
            <Clock className="w-3 h-3 text-slate-500" />
            <span>{new Date(prediction.timestamp).toLocaleTimeString()}</span>
            <span className="text-slate-600">|</span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-[11px] font-bold">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>{prediction.sources?.primary_news?.publisher || prediction.source || 'Institutional Financial Wire'}</span>
            </span>
          </div>
        </div>
      </div>

      <div className="p-6">
        <h3 className="text-xl font-medium text-slate-100 leading-snug mb-6">
          "{prediction.headline}"
        </h3>

        {/* 4-METRIC SCORE ROW */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
          <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
            <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1 uppercase">
              DIRECTION
            </div>
            <div className={`text-lg font-black ${directionColor}`}>
              {directionText}
            </div>
            <div className="text-[10px] text-slate-500 mt-1">
              {prediction.signal === 'UNCERTAIN'
                ? `Low-confidence ${prediction.pred_1h > 0 ? 'bullish' : 'bearish'}`
                : 'High-confidence'}
            </div>
          </div>

          <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
            <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1 uppercase">
              EXPECTED MOVE
            </div>
            <div className={`text-lg font-black font-mono ${expectedMoveColor}`}>
              {prediction.pred_1h > 0 ? '+' : ''}{prediction.pred_1h?.toFixed(2)}%
            </div>
            <div className="text-[10px] text-slate-500 mt-1">1-Hour Forecast</div>
          </div>

          <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
            <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1 uppercase">
              HORIZON
            </div>
            <div className="text-lg font-black text-blue-400 font-mono">Next 1H</div>
            <div className="text-[10px] text-slate-500 mt-1">Next Day: {prediction.pred_1d > 0 ? '+' : ''}{prediction.pred_1d?.toFixed(1)}%</div>
          </div>

          <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
            <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1 uppercase">
              CONFIDENCE
            </div>
            <div className="text-lg font-black text-slate-200 font-mono">
              {prediction.confidence_score}%
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Platt Calibrated</div>
          </div>
        </div>

        {/* CHART & NLP SENTIMENT */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <PriceChart prediction={prediction} livePrice={livePrice} />
          </div>
          <div>
            <SentimentGauge finbert={prediction.finbert} />
          </div>
        </div>

        {/* EXPLANATION & AI REASONING */}
        <ReasoningBox
          eventType={prediction.event_type}
          explanation={prediction.explanation}
          aiReasoning={prediction.ai_reasoning}
        />

        {/* SECTOR RIPPLE & FEATURE IMPORTANCE */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SectorRipple sectorRipple={prediction.sector_ripple} />
          <FeatureDrivers featureImportance={prediction.feature_importance} />
        </div>

        {/* EVIDENTIARY SOURCES */}
        <EvidentiarySources prediction={prediction} />
      </div>
    </div>
  );
};

