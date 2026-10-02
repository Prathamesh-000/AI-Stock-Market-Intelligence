import { useState, useEffect, useRef, FormEvent } from 'react';
import { Zap, Activity, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface Prediction {
  ticker: string;
  headline: string;
  signal: 'BUY' | 'SELL' | 'UNCERTAIN';
  confidence_score: number;
  timestamp: string;
}

function App() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [ticker, setTicker] = useState("NVDA");
  const [headline, setHeadline] = useState("");
  const [loading, setLoading] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const connectWebSocket = () => {
    ws.current = new WebSocket("ws://127.0.0.1:8000/ws");
    
    ws.current.onopen = () => setIsConnected(true);
    ws.current.onclose = () => {
      setIsConnected(false);
      setTimeout(connectWebSocket, 3000);
    };
    
    ws.current.onmessage = (event) => {
      const data: Prediction = JSON.parse(event.data);
      setPredictions(prev => [data, ...prev]);
      setLoading(false);
    };
  };

  const triggerPrediction = async (e: FormEvent) => {
    e.preventDefault();
    if (!headline) return;
    
    setLoading(true);
    
    try {
      await fetch("http://127.0.0.1:8000/api/v1/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker,
          headline,
          summary: headline
        })
      });
      setHeadline("");
    } catch (err) {
      console.error("Failed to trigger API", err);
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <header className="flex justify-between items-center mb-10 pb-4 border-b border-slate-700">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            Quant AI Terminal
          </h1>
          <p className="text-slate-400 text-sm mt-1">Live XGBoost Sentiment Engine</p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-sm font-medium text-slate-300">
            {isConnected ? 'WS Connected' : 'Disconnected'}
          </span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="col-span-1">
          <div className="bg-cardBg p-6 rounded-xl border border-slate-700 shadow-xl">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-white">
              <Zap className="w-5 h-5 text-blue-400" /> Feed News
            </h2>
            <form onSubmit={triggerPrediction} className="flex flex-col gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wider">Ticker</label>
                <input 
                  type="text" 
                  value={ticker}
                  onChange={e => setTicker(e.target.value.toUpperCase())}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white focus:outline-none focus:border-blue-500 font-mono"
                  placeholder="NVDA"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wider">Headline / Rumor</label>
                <textarea 
                  value={headline}
                  onChange={e => setHeadline(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white focus:outline-none focus:border-blue-500 min-h-[100px]"
                  placeholder="E.g., Nvidia announces massive chip delay..."
                  required
                ></textarea>
              </div>
              <button 
                type="submit" 
                disabled={loading || !isConnected}
                className={`w-full font-bold rounded-lg p-3 transition-all ${
                  loading 
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]'
                }`}
              >
                {loading ? 'Analyzing...' : 'Execute AI'}
              </button>
            </form>
          </div>
        </div>

        <div className="col-span-1 md:col-span-2">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-white">
            <Activity className="w-5 h-5 text-emerald-400" /> Live Signal Feed
          </h2>
          
          <div className="flex flex-col gap-4">
            {predictions.length === 0 && (
              <div className="bg-cardBg/50 border border-slate-800 border-dashed rounded-xl p-10 text-center text-slate-500">
                Waiting for AI signals...
              </div>
            )}
            
            {predictions.map((pred, idx) => (
              <div key={idx} className="bg-cardBg p-5 rounded-xl border border-slate-700 shadow-lg transform transition-all hover:scale-[1.01] animate-slide-in">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex items-center gap-3">
                    <span className="bg-slate-900 text-blue-400 font-mono font-bold px-3 py-1 rounded-md border border-slate-700">
                      {pred.ticker}
                    </span>
                    <span className="text-xs text-slate-400">
                      {new Date(pred.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  
                  {pred.signal === 'BUY' && (
                    <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" /> BUY
                    </span>
                  )}
                  {pred.signal === 'SELL' && (
                    <span className="bg-red-500/20 text-red-400 border border-red-500/30 px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                      <TrendingDown className="w-4 h-4" /> SELL
                    </span>
                  )}
                  {pred.signal === 'UNCERTAIN' && (
                    <span className="bg-slate-500/20 text-slate-400 border border-slate-500/30 px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                      <Minus className="w-4 h-4" /> SKIP
                    </span>
                  )}
                </div>
                
                <p className="text-slate-200 text-lg font-medium leading-relaxed mb-4">
                  "{pred.headline}"
                </p>
                
                <div className="flex items-center justify-between border-t border-slate-700 pt-3">
                  <div className="text-sm text-slate-400">AI Confidence Level</div>
                  <div className="text-lg font-bold text-white">
                    {pred.confidence_score}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
