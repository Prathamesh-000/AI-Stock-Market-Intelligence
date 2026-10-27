import React from 'react';
import { Activity } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts';
import { Prediction } from '../types';

interface ConfidenceTimelineProps {
  predictions: Prediction[];
}

export const ConfidenceTimeline: React.FC<ConfidenceTimelineProps> = ({ predictions }) => {
  if (predictions.length <= 1) return null;

  const timelineData = [...predictions].reverse().map((p, i) => ({
    index: i + 1,
    confidence: p.confidence_score,
    ticker: p.ticker,
    signal: p.signal
  }));

  return (
    <div className="max-w-7xl mx-auto mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4">
        <Activity className="w-5 h-5 text-blue-400" /> Prediction Confidence Timeline
        <span className="text-xs font-normal text-slate-500 ml-2">
          — how signal confidence has evolved across your predictions
        </span>
      </h2>
      <div className="h-40">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={timelineData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="index"
              stroke="#475569"
              fontSize={11}
              label={{ value: 'Prediction #', position: 'insideBottomRight', offset: -5, fill: '#475569', fontSize: 11 }}
            />
            <YAxis domain={[0, 100]} stroke="#475569" fontSize={11} tickFormatter={(v) => `${v}%`} />
            <Tooltip
              contentStyle={{ backgroundColor: '#020617', border: '1px solid #1e293b' }}
              formatter={(val: any) => [`${Number(val).toFixed(1)}%`, 'Confidence']}
              labelFormatter={(label) => `Prediction #${label}`}
            />
            <ReferenceLine y={60} stroke="#34d399" strokeDasharray="3 3" label={{ value: 'BUY threshold', fill: '#34d399', fontSize: 10 }} />
            <ReferenceLine y={40} stroke="#f87171" strokeDasharray="3 3" label={{ value: 'SELL threshold', fill: '#f87171', fontSize: 10 }} />
            <Line type="monotone" dataKey="confidence" stroke="#60a5fa" strokeWidth={2} dot={{ fill: '#60a5fa', r: 4 }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

