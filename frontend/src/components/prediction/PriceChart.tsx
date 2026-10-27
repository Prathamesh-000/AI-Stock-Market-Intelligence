import React, { useState } from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts';
import { Prediction, Timeframe } from '../../types';
import { generateChartData } from '../../utils/chartUtils';

interface PriceChartProps {
  prediction: Prediction;
  livePrice?: number;
}

export const PriceChart: React.FC<PriceChartProps> = ({ prediction, livePrice }) => {
  const [chartTimeframe, setChartTimeframe] = useState<Timeframe>('1D');
  const [hoveredPoint, setHoveredPoint] = useState<{ price: number; time?: string } | null>(null);

  const chartInfo = generateChartData(prediction, chartTimeframe, livePrice);
  const isBullish = prediction.signal === 'BUY' || (prediction.signal === 'UNCERTAIN' && prediction.pred_1h >= 0);

  return (
    <div className="bg-slate-950/50 rounded-lg border border-slate-800 p-4">
      <div className="flex justify-between items-center mb-4">
        <div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black font-mono">
              ${(hoveredPoint?.price ?? chartInfo.currentPrice).toFixed(2)}
            </span>
            <span className={`text-sm font-bold font-mono ${chartInfo.changePct >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {chartInfo.changePct >= 0 ? '▲' : '▼'} {chartInfo.delta >= 0 ? '+' : ''}${chartInfo.delta.toFixed(2)} ({Math.abs(chartInfo.changePct).toFixed(2)}%)
            </span>
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
              {hoveredPoint?.time ? `@ ${hoveredPoint.time}` : chartInfo.periodLabel}
            </span>
          </div>
        </div>

        <div className="flex gap-1 bg-slate-900 border border-slate-800 p-0.5 rounded-lg">
          {(['1D', '1W', '1M'] as const).map((tf) => (
            <button
              key={tf}
              onClick={() => { setChartTimeframe(tf); setHoveredPoint(null); }}
              className={`text-[10px] font-bold px-2.5 py-1 rounded transition-all cursor-pointer ${
                chartTimeframe === tf
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      <div className="h-40 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart 
            data={chartInfo.data}
            onMouseMove={(e: any) => {
              if (e?.activePayload && e.activePayload.length > 0) {
                setHoveredPoint({
                  price: e.activePayload[0].payload.price,
                  time: e.activePayload[0].payload.time || undefined
                });
              }
            }}
            onMouseLeave={() => setHoveredPoint(null)}
          >
            <defs>
              <linearGradient id={`colorPrice-${prediction.ticker}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={isBullish ? '#34d399' : '#f87171'} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={isBullish ? '#34d399' : '#f87171'} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="time" stroke="#334155" fontSize={10} tickMargin={5} minTickGap={10} />
            <YAxis domain={['dataMin - 1', 'dataMax + 1']} hide />
            <Tooltip contentStyle={{ backgroundColor: '#020617', border: '1px solid #1e293b' }} />
            <ReferenceLine
              x={chartInfo.eventMarker}
              stroke="#fbbf24"
              strokeDasharray="3 3"
              label={{ position: 'top', value: 'NEWS EVENT', fill: '#fbbf24', fontSize: 10, fontWeight: 'bold' }}
            />
            <Area
              type="monotone"
              dataKey="price"
              stroke={isBullish ? '#34d399' : '#f87171'}
              fillOpacity={1}
              fill={`url(#colorPrice-${prediction.ticker})`}
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
