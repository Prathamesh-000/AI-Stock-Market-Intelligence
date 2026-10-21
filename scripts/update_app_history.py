import os

app_path = 'frontend/src/App.tsx'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add states for history
state_code = """  const [predictions, setPredictions] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);
  const [accuracy, setAccuracy] = useState(0);"""
content = content.replace("  const [predictions, setPredictions] = useState<any[]>([]);", state_code)

# Add fetch for history
effect_code = """  useEffect(() => {
    fetch('http://localhost:8000/api/v1/history')
      .then(res => res.json())
      .then(data => {
        setHistory(data.history || []);
        setAccuracy(data.accuracy || 0);
      })
      .catch(e => console.error(e));
      
    const ws = new WebSocket('ws://localhost:8000/ws');"""
content = content.replace("  useEffect(() => {\n    const ws = new WebSocket('ws://localhost:8000/ws');", effect_code)

# Add UI at the bottom
ui_code = """
        </div>
      </main>

      {/* PHASE 3: MODEL PERFORMANCE HISTORY */}
      {history.length > 0 && (
        <div className="max-w-6xl mx-auto mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Database className="w-5 h-5 text-purple-400" /> MODEL PERFORMANCE
            </h2>
            <div className="text-right">
              <span className="text-xs text-slate-500 font-bold block mb-1">HISTORICAL ACCURACY</span>
              <span className="text-xl font-black text-emerald-400">{accuracy.toFixed(1)}%</span>
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
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400">
                          ✓
                        </span>
                      ) : (
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-red-500/20 text-red-400">
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
}"""

content = content.replace("        </div>\n      </main>\n    </div>\n  );\n}", ui_code)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated App.tsx with Model Performance!")
