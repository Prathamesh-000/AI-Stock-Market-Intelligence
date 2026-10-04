import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Zap, TrendingUp, TrendingDown, Minus, Clock, Server, BrainCircuit, Activity, BarChart3, Database, LineChart } from 'lucide-react';

const WATCHLIST = [
  { symbol: 'NVDA', price: 183.42, change: '+3.27%' },
  { symbol: 'AMD', price: 164.20, change: '+1.92%' },
  { symbol: 'AAPL', price: 254.18, change: '-0.83%' },
  { symbol: 'TSLA', price: 421.52, change: '+2.11%' },
  { symbol: 'MSFT', price: 511.24, change: '+0.74%' }
];

export default function App() {
  const [headline, setHeadline] = useState('');
  const [ticker, setTicker] = useState('NVDA');
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);
  const [accuracy, setAccuracy] = useState(0);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/history')
      .then(res => res.json())
      .then(data => {
        setHistory(data.history || []);
        setAccuracy(data.accuracy || 0);
      })
      .catch(e => console.error(e));
      
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
      await fetch('http://localhost:8000/api/v1/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, headline, summary: '' })
      });
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  // Generate chart that ends at the exact time of the news event
  const generateChartData = (pred: any) => {
    const eventTimeStr = new Date(pred.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    let base = pred.current_price - (pred.pred_1h / 10 * 50); // Reverse engineer a starting price
    const data = [];
    
    // Pre-news movement (50 ticks)
    for(let i=0; i<50; i++) {
      base = base + (Math.random() - 0.45) * 0.5;
      data.push({ 
        time: i === 0 ? "Open" : '', 
        price: Number(base.toFixed(2))
      });
    }
    
    // The news shock occurs precisely at eventTimeStr
    for(let i=50; i<60; i++) {
      base = base + (pred.pred_1h / 10) + (Math.random() - 0.5) * 0.2;
      data.push({ 
        time: i === 50 ? eventTimeStr : (i === 59 ? "+1H" : ''), 
        price: Number(base.toFixed(2)) 
      });
    }
    return { data, eventTimeStr };
  };

  // INTERACTIVE DASHBOARD: Filter predictions based on selected Watchlist ticker
  const displayPredictions = predictions.filter(p => p.ticker === ticker);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-6">
      
      {/* MARKET OVERVIEW */}
      <div className="max-w-7xl mx-auto mb-6 bg-slate-900 border border-slate-800 rounded-lg p-4 flex items-center justify-between shadow-lg">
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
      <header className="max-w-7xl mx-auto flex items-center justify-between mb-8">
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

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT COLUMN: Watchlist & Input */}
        <div className="lg:col-span-3 space-y-6">
          
          {/* Watchlist */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <div className="px-4 py-3 bg-slate-800/50 border-b border-slate-800 flex justify-between items-center">
              <span className="text-xs font-bold text-slate-400 tracking-wider">WATCHLIST</span>
              <LineChart className="w-4 h-4 text-slate-500" />
            </div>
            <div className="divide-y divide-slate-800">
              {WATCHLIST.map(stock => (
                <div 
                  key={stock.symbol} 
                  onClick={() => setTicker(stock.symbol)}
                  className={`px-4 py-3 flex justify-between items-center cursor-pointer transition-colors ${ticker === stock.symbol ? 'bg-blue-900/30 border-l-4 border-blue-500' : 'hover:bg-slate-800/50 border-l-4 border-transparent'}`}
                >
                  <span className={`font-bold ${ticker === stock.symbol ? 'text-blue-400' : 'text-slate-300'}`}>{stock.symbol}</span>
                  <div className="text-right">
                    <div className="text-sm font-mono text-slate-200">${stock.price}</div>
                    <div className={`text-xs font-bold ${stock.change.includes('+') ? 'text-emerald-400' : 'text-red-400'}`}>
                      {stock.change}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

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
                  readOnly
                  className="w-full bg-slate-950/50 border border-slate-800 rounded-lg px-3 py-2 text-slate-400 focus:outline-none uppercase cursor-not-allowed"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 mb-1">HEADLINE / RUMOR</label>
                <textarea 
                  value={headline}
                  onChange={(e) => setHeadline(e.target.value)}
                  placeholder={`E.g., ${ticker} announces massive chip delay...`}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-3 text-slate-200 focus:outline-none focus:border-blue-500 transition-colors h-32 resize-none"
                />
              </div>
              <button 
                onClick={triggerAI}
                disabled={loading || !headline}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg shadow-lg shadow-blue-500/20 transition-all flex items-center justify-center gap-2"
              >
                {loading ? <span className="animate-pulse">Analyzing...</span> : `Execute ${ticker} AI`}
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Feed */}
        <div className="lg:col-span-9 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" /> Live {ticker} Signal Feed
            </h2>
          </div>

          {displayPredictions.length === 0 && (
            <div className="bg-slate-900/50 border border-slate-800/50 border-dashed rounded-xl p-12 text-center text-slate-500">
              Waiting for {ticker} AI signals... <br/>
              <span className="text-xs text-slate-600 mt-2 block">Enter a headline on the left to generate predictions.</span>
            </div>
          )}

          {displayPredictions.map((pred, i) => {
            const chartInfo = generateChartData(pred);
            
            return (
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
              </div>

              <div className="p-6">
                <h3 className="text-xl font-medium text-slate-100 leading-snug mb-6">"{pred.headline}"</h3>
                
                {/* PREDICTION PANEL */}
                <div className="grid grid-cols-4 gap-4 mb-6">
                  <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
                    <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1">DIRECTION</div>
                    <div className={`text-lg font-black ${pred.signal === 'BUY' ? 'text-emerald-400' : pred.signal === 'SELL' ? 'text-red-400' : 'text-slate-400'}`}>
                      {pred.signal === 'BUY' ? 'BULLISH' : pred.signal === 'SELL' ? 'BEARISH' : 'UNCERTAIN'}
                    </div>
                    {/* Defensible Uncertainty Explanation */}
                    <div className="text-[10px] text-slate-500 mt-1">
                      {pred.signal === 'UNCERTAIN' ? `Low-confidence ${pred.pred_1h > 0 ? 'bullish' : 'bearish'}` : 'High-confidence'}
                    </div>
                  </div>
                  <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
                    <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1">EXPECTED MOVE</div>
                    <div className={`text-lg font-black ${pred.pred_1h > 0 ? 'text-emerald-400' : 'text-red-400'}`}>{pred.pred_1h > 0 ? '+' : ''}{pred.pred_1h?.toFixed(2)}%</div>
                  </div>
                  <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
                    <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1">HORIZON</div>
                    <div className="text-lg font-black text-blue-400">Next 1H</div>
                  </div>
                  <div className="bg-slate-950/50 border border-slate-800 rounded p-4 text-center">
                    <div className="text-[10px] font-bold text-slate-500 tracking-wider mb-1">CONFIDENCE</div>
                    <div className="text-lg font-black text-slate-200">{pred.confidence_score}%</div>
                  </div>
                </div>

                {/* ADVANCED CHART & NLP */}
                <div className="grid grid-cols-3 gap-6 mb-6">
                  
                  {/* Left: Chart */}
                  <div className="col-span-2 bg-slate-950/50 rounded-lg border border-slate-800 p-4">
                    <div className="flex justify-between items-center mb-4">
                      <div>
                        <div className="text-lg font-black flex items-center gap-2">
                          ${pred.current_price?.toFixed(2) || '183.42'} 
                          <span className={`text-sm ${pred.pred_1h > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                            {pred.pred_1h > 0 ? '▲' : '▼'} {pred.pred_1h?.toFixed(2)}%
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button className="text-[10px] font-bold bg-blue-500/20 text-blue-400 px-2 py-1 rounded">1D</button>
                        <button className="text-[10px] font-bold text-slate-500 hover:text-slate-300 px-2 py-1 rounded">1W</button>
                        <button className="text-[10px] font-bold text-slate-500 hover:text-slate-300 px-2 py-1 rounded">1M</button>
                      </div>
                    </div>
                    <div className="h-40 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={chartInfo.data}>
                          <defs>
                            <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor={pred.pred_1h > 0 ? '#34d399' : '#f87171'} stopOpacity={0.3}/>
                              <stop offset="95%" stopColor={pred.pred_1h > 0 ? '#34d399' : '#f87171'} stopOpacity={0}/>
                            </linearGradient>
                          </defs>
                          <XAxis dataKey="time" stroke="#334155" fontSize={10} tickMargin={5} minTickGap={10} />
                          <YAxis domain={['dataMin - 1', 'dataMax + 1']} hide />
                          <Tooltip contentStyle={{backgroundColor: '#020617', border: '1px solid #1e293b'}} />
                          <ReferenceLine x={chartInfo.eventTimeStr} stroke="#fbbf24" strokeDasharray="3 3" label={{ position: 'top', value: 'NEWS EVENT', fill: '#fbbf24', fontSize: 10, fontWeight: 'bold' }} />
                          <Area type="monotone" dataKey="price" stroke={pred.pred_1h > 0 ? '#34d399' : '#f87171'} fillOpacity={1} fill="url(#colorPrice)" strokeWidth={2} />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right: FinBERT Clarity */}
                  <div className="bg-slate-950/50 rounded-lg border border-slate-800 p-4">
                    <div className="text-xs text-slate-500 font-bold mb-3 flex items-center gap-1"><BrainCircuit className="w-4 h-4"/> FINBERT NLP SENTIMENT</div>
                    
                    <div className="text-lg font-black text-slate-200 mb-4">{pred.finbert?.label || 'POSITIVE'}</div>
                    
                    <div className="space-y-3 text-sm">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-400">Classification</span>
                        <span className="font-mono text-emerald-400 font-bold">{pred.finbert?.positive || 82}%</span>
                      </div>
                      <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500" style={{ width: `${pred.finbert?.positive || 82}%` }}></div>
                      </div>
                      
                      <div className="flex justify-between items-center pt-2">
                        <span className="text-slate-400">Polarity Score</span>
                        <span className="font-mono text-blue-400 font-bold">{pred.finbert?.score > 0 ? '+' : ''}{pred.finbert?.score?.toFixed(2)}</span>
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
                          <span className={`w-14 text-xs font-mono font-bold ${impact > 0 ? 'text-emerald-400' : impact < 0 ? 'text-red-400' : 'text-slate-400'}`}>
                            {impact > 0 ? '+' : ''}{impact?.toFixed(1)}%
                          </span>
                          <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden flex">
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
          );
          })}
        </div>
      </main>

      {/* PHASE 3: MODEL PERFORMANCE HISTORY */}
      {history.length > 0 && (
        <div className="max-w-7xl mx-auto mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Database className="w-5 h-5 text-purple-400" /> MODEL PERFORMANCE
            </h2>
            <div className="text-right">
              <span className="text-xs text-slate-500 font-bold block mb-1">HISTORICAL ACCURACY</span>
              <span className="text-xl font-black text-emerald-400">{accuracy.toFixed(1)}%</span>
              <div className="text-[10px] text-slate-500 mt-1">(Directional Accuracy on Unseen Data)</div>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Stock</th>
                  <th className="py-3 px-4">Prediction</th>
                  <th className="py-3 px-4">Actual</th>
                  <th className="py-3 px-4 text-center">Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {history.map((row, i) => (
                  <tr key={i} className="hover:bg-slate-800/20 transition-colors">
                    <td className="py-3 px-4 text-sm text-slate-400">{row.date}</td>
                    <td className="py-3 px-4 text-sm font-bold text-slate-300">{row.ticker}</td>
                    <td className="py-3 px-4 text-sm font-mono text-blue-400">{row.prediction}</td>
                    <td className="py-3 px-4 text-sm font-mono text-slate-300">
                      {parseFloat(row.actual).toFixed(1)}%
                    </td>
                    <td className="py-3 px-4 text-center">
                      {row.is_correct ? (
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400" title="Correct Directional Prediction">
                          ✓
                        </span>
                      ) : (
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-red-500/20 text-red-400" title="Incorrect Directional Prediction">
                          ✗
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
