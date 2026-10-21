APP_TSX_CONTENT = """import React, { useState, useEffect } from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import { Zap, TrendingUp, TrendingDown, Minus, Clock, Server, BrainCircuit, Activity, BarChart3, Database } from 'lucide-react';

export default function App() {
  const [headline, setHeadline] = useState('');
  const [ticker, setTicker] = useState('NVDA');
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onopen = () => setWsConnected(true);
    ws.onclose = () => setWsConnected(false);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPredictions((prev) => [data, ...prev]);
      setLoading(false);
    };
    return () => ws.close();
  }, []);

  const triggerAI = async () => {
    if (!headline) return;
    setLoading(true);
    try {
      await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, headline, summary: '' })
      });
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  // Mock chart data for visual effect
  const generateChartData = (pred_1h: number) => {
    let base = 180;
    const data = [];
    for(let i=0; i<20; i++) {
      base = base + (Math.random() - 0.5) * 2;
      data.push({ time: i, price: base });
    }
    // Add the spike/drop
    for(let i=20; i<30; i++) {
      base = base + (pred_1h / 10);
      data.push({ time: i, price: base, event: i === 20 ? 'NEWS' : null });
    }
    return data;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-6">
      
      {/* MARKET OVERVIEW */}
      <div className="max-w-6xl mx-auto mb-6 bg-slate-900 border border-slate-800 rounded-lg p-4 flex items-center justify-between shadow-lg">
        <div className="flex gap-6">
          <div className="flex flex-col"><span className="text-xs text-slate-500 font-bold tracking-wider">S&P 500</span><span className="text-emerald-400 text-sm font-bold">▲ 0.72%</span></div>
          <div className="flex flex-col"><span className="text-xs text-slate-500 font-bold tracking-wider">NASDAQ</span><span className="text-emerald-400 text-sm font-bold">▲ 1.14%</span></div>
          <div className="flex flex-col"><span className="text-xs text-slate-500 font-bold tracking-wider">DOW</span><span className="text-emerald-400 text-sm font-bold">▲ 0.31%</span></div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-xs text-slate-500 font-bold block mb-1">AI MARKET SENTIMENT</span>
            <div className="flex items-center gap-2">
              <div className="w-32 h-2 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500" style={{ width: '82%' }}></div>
              </div>
              <span className="text-xs font-bold text-emerald-400">82% BULLISH</span>
            </div>
          </div>
          <div className="h-8 w-px bg-slate-800 mx-2"></div>
          <div className="flex flex-col items-center"><span className="text-lg font-bold text-blue-400">12</span><span className="text-[10px] text-slate-500 font-bold">ACTIVE SIGNALS</span></div>
        </div>
      </div>

      {/* HEADER */}
      <header className="max-w-6xl mx-auto flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-black bg-gradient-to-r from-emerald-400 to-cyan-500 bg-clip-text text-transparent">
            Quant AI Terminal
          </h1>
          <p className="text-slate-400 text-sm mt-1 flex items-center gap-2">
            <Database className="w-4 h-4" /> Live XGBoost Sentiment Engine
          </p>
        </div>
        <div className="flex items-center gap-3 bg-slate-900/50 px-4 py-2 rounded-full border border-slate-800">
          <div className={`w-2.5 h-2.5 rounded-full ${wsConnected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
          <span className="text-sm font-medium text-slate-300">
            {wsConnected ? 'WS Connected' : 'Disconnected'}
          </span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT COLUMN: Input */}
        <div className="lg:col-span-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl sticky top-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5 text-blue-400" /> Feed News
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-500 mb-1">TICKER</label>
                <input 
                  type="text" 
                  value={ticker} 
                  onChange={(e) => setTicker(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500 transition-colors uppercase"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 mb-1">HEADLINE / RUMOR</label>
                <textarea 
                  value={headline}
                  onChange={(e) => setHeadline(e.target.value)}
                  placeholder="E.g., Nvidia announces massive chip delay..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-3 text-slate-200 focus:outline-none focus:border-blue-500 transition-colors h-32 resize-none"
                />
              </div>
              <button 
                onClick={triggerAI}
                disabled={loading || !headline}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg shadow-lg shadow-blue-500/20 transition-all flex items-center justify-center gap-2"
              >
                {loading ? <span className="animate-pulse">Analyzing...</span> : 'Execute AI'}
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Feed */}
        <div className="lg:col-span-8 space-y-6">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" /> Live Signal Feed
          </h2>

          {predictions.length === 0 && (
            <div className="bg-slate-900/50 border border-slate-800/50 border-dashed rounded-xl p-12 text-center text-slate-500">
              Waiting for AI signals...
            </div>
          )}

          {predictions.map((pred, i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl animate-in slide-in-from-top-4 fade-in duration-500">
              
              {/* TOP HEADER */}
              <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/20">
                <div className="flex items-center gap-3">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded text-sm font-black border border-blue-500/30">
                    {pred.ticker}
                  </span>
                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <Clock className="w-3 h-3" /> {new Date(pred.timestamp).toLocaleTimeString()}
                    <span className="text-slate-600">|</span>
                    <span className="font-medium text-slate-300">SOURCE: {pred.source || 'Reuters'}</span>
                  </div>
                </div>
                
                {/* SIGNAL BADGE */}
                {pred.signal === 'BUY' && (
                  <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-4 py-1.5 rounded-full text-sm font-bold flex items-center gap-1 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
                    <TrendingUp className="w-4 h-4" /> BULLISH
                  </span>
                )}
                {pred.signal === 'SELL' && (
                  <span className="bg-red-500/20 text-red-400 border border-red-500/30 px-4 py-1.5 rounded-full text-sm font-bold flex items-center gap-1 shadow-[0_0_15px_rgba(239,68,68,0.2)]">
                    <TrendingDown className="w-4 h-4" /> BEARISH
                  </span>
                )}
                {pred.signal === 'UNCERTAIN' && (
                  <span className="bg-slate-500/20 text-slate-400 border border-slate-500/30 px-4 py-1.5 rounded-full text-sm font-bold flex items-center gap-1">
                    <Minus className="w-4 h-4" /> SKIP
                  </span>
                )}
              </div>

              <div className="p-6">
                <h3 className="text-xl font-medium text-slate-100 leading-snug mb-6">"{pred.headline}"</h3>
                
                {/* 1. PRICE INTELLIGENCE */}
                <div className="grid grid-cols-2 gap-6 mb-6">
                  
                  {/* Left: Chart & Stats */}
                  <div className="bg-slate-950/50 rounded-lg border border-slate-800 p-4">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="text-xs text-slate-500 font-bold mb-1">LIVE MARKET</div>
                        <div className="text-2xl font-black">${pred.current_price?.toFixed(2) || '183.42'}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-slate-500 font-bold mb-1">PREDICTED IMPACT</div>
                        <div className={`text-lg font-black ${pred.pred_1h > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                          {pred.pred_1h > 0 ? '+' : ''}{pred.pred_1h}%
                        </div>
                      </div>
                    </div>
                    <div className="h-24 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={generateChartData(pred.pred_1h || 2)}>
                          <Line type="stepAfter" dataKey="price" stroke={pred.pred_1h > 0 ? '#34d399' : '#f87171'} strokeWidth={2} dot={false} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right: Confidence & Reasoning */}
                  <div className="bg-slate-950/50 rounded-lg border border-slate-800 p-4 flex flex-col justify-between">
                    <div>
                      <div className="text-xs text-slate-500 font-bold mb-3 flex items-center gap-1"><BrainCircuit className="w-4 h-4"/> AI PIPELINE BREAKDOWN</div>
                      
                      <div className="space-y-2 text-sm text-slate-300">
                        <div className="flex justify-between"><span>FinBERT Sentiment:</span><span className="font-mono text-emerald-400">{pred.finbert?.label || 'POSITIVE'} ({pred.finbert?.score || '0.84'})</span></div>
                        <div className="flex justify-between"><span>Event Impact:</span><span className="font-mono text-blue-400">{pred.llm_impact}/100</span></div>
                        <div className="flex justify-between"><span>Historical Match:</span><span className="font-mono text-amber-400">{pred.similar_events?.[0]?.score ? (pred.similar_events[0].score*100).toFixed(1) : '59.7'}%</span></div>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-slate-800">
                      <div className="flex justify-between items-end mb-1">
                        <span className="text-xs text-slate-500 font-bold">FINAL PREDICTION CONFIDENCE</span>
                        <span className="text-xl font-black text-slate-200">{pred.confidence_score}%</span>
                      </div>
                      <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full ${pred.confidence_score > 60 ? 'bg-emerald-500' : pred.confidence_score < 40 ? 'bg-red-500' : 'bg-slate-500'}`} style={{ width: `${pred.confidence_score}%` }}></div>
                      </div>
                    </div>
                  </div>

                </div>

                {/* 2. EXPLANATION & DRIVERS */}
                <div className="mb-6 p-4 bg-blue-900/10 border border-blue-900/30 rounded-lg">
                  <div className="flex gap-2">
                    <span className="bg-blue-900/50 text-blue-400 text-xs font-bold px-2 py-1 rounded">Event: {pred.event_type}</span>
                  </div>
                  <p className="text-sm text-slate-300 italic mt-3">"{pred.explanation}"</p>
                  
                  {pred.ai_reasoning && (
                    <div className="mt-4 pt-4 border-t border-blue-900/30">
                      <div className="text-xs text-blue-400/70 font-bold mb-2">AI REASONING</div>
                      <ul className="list-disc list-inside text-xs text-slate-400 space-y-1">
                        {pred.ai_reasoning.map((r: string, idx: number) => (
                          <li key={idx}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* 3. SECTOR RIPPLE & FEATURE IMPORTANCE */}
                <div className="grid grid-cols-2 gap-6">
                  
                  {/* Sector Ripple */}
                  <div>
                    <h4 className="text-xs font-bold text-slate-500 tracking-wider mb-3">SECTOR RIPPLE EFFECT</h4>
                    <div className="space-y-3">
                      {Object.entries(pred.sector_ripple || {}).map(([comp, impact]: [string, any]) => (
                        <div key={comp} className="flex items-center gap-3">
                          <span className="w-10 text-xs font-bold text-slate-400">{comp}</span>
                          <span className={`w-12 text-xs font-mono font-bold ${impact > 0 ? 'text-emerald-400' : impact < 0 ? 'text-red-400' : 'text-slate-400'}`}>
                            {impact > 0 ? '+' : ''}{impact}%
                          </span>
                          <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden flex">
                            {impact > 0 ? (
                              <div className="h-full bg-emerald-500/50" style={{ width: `${Math.min(impact * 10, 100)}%` }} />
                            ) : (
                              <div className="h-full bg-red-500/50" style={{ width: `${Math.min(Math.abs(impact) * 10, 100)}%` }} />
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Main Drivers (Feature Importance) */}
                  <div>
                    <h4 className="text-xs font-bold text-slate-500 tracking-wider mb-3 flex items-center gap-1"><BarChart3 className="w-4 h-4"/> MAIN DRIVERS</h4>
                    <div className="space-y-3">
                      {(pred.feature_importance || []).map((feat: any, idx: number) => (
                        <div key={idx} className="flex items-center gap-3">
                          <span className="flex-1 text-xs text-slate-400 truncate">{feat.name}</span>
                          <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-500/50" style={{ width: `${feat.value}%` }} />
                          </div>
                          <span className="text-xs font-mono text-slate-500">{feat.value}%</span>
                        </div>
                      ))}
                    </div>
                  </div>

                </div>

              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
"""

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(APP_TSX_CONTENT)
print("Successfully overwrote App.tsx!")
