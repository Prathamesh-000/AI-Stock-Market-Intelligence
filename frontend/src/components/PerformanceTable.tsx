import React from 'react';
import { Database, Download } from 'lucide-react';
import { HistoricalLog } from '../types';

interface PerformanceTableProps {
  history: HistoricalLog[];
  accuracy: number;
  onExportCSV: () => void;
}

export const PerformanceTable: React.FC<PerformanceTableProps> = ({
  history,
  accuracy,
  onExportCSV
}) => {
  if (history.length === 0) return null;

  return (
    <div className="max-w-7xl mx-auto mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <Database className="w-5 h-5 text-purple-400" /> MODEL PERFORMANCE
        </h2>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-xs text-slate-500 font-bold block mb-1">HISTORICAL ACCURACY</span>
            <span className="text-xl font-black text-emerald-400 font-mono">{accuracy.toFixed(1)}%</span>
            <div className="text-[10px] text-slate-500 mt-1">(Directional Accuracy on Unseen Data)</div>
          </div>
          <button
            onClick={onExportCSV}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-400 hover:text-slate-200 text-sm transition-colors cursor-pointer"
          >
            <Download className="w-4 h-4" />
            Export
          </button>
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
                <td className="py-3 px-4 text-sm text-slate-400 font-mono">{row.date}</td>
                <td className="py-3 px-4 text-sm font-bold text-slate-300 font-mono">{row.ticker}</td>
                <td className="py-3 px-4 text-sm font-mono text-blue-400">{row.prediction}</td>
                <td className="py-3 px-4 text-sm font-mono text-slate-300">{parseFloat(row.actual).toFixed(1)}%</td>
                <td className="py-3 px-4 text-center">
                  {row.is_correct ? (
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 font-bold" title="Correct">✓</span>
                  ) : (
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-red-500/20 text-red-400 font-bold" title="Incorrect">✗</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

