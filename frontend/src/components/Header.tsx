import React from 'react';
import { Database, Download } from 'lucide-react';

interface HeaderProps {
  wsConnected: boolean;
  onExportCSV: () => void;
}

export const Header: React.FC<HeaderProps> = ({ wsConnected, onExportCSV }) => {
  return (
    <header className="max-w-7xl mx-auto flex items-center justify-between mb-8">
      <div>
        <h1 className="text-3xl font-black bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-500 bg-clip-text text-transparent tracking-tight">
          Quant AI Terminal
        </h1>
        <p className="text-slate-400 text-sm mt-1 flex items-center gap-2">
          <Database className="w-4 h-4 text-cyan-400" /> Live XGBoost Sentiment & Market Intelligence Engine
        </p>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={onExportCSV}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-slate-300 text-sm font-medium transition-colors shadow-sm cursor-pointer"
          title="Download all predictions as CSV"
        >
          <Download className="w-4 h-4 text-slate-400" />
          Export CSV
        </button>

        <div className="flex items-center gap-2.5 bg-slate-900/60 px-4 py-2 rounded-full border border-slate-800 shadow-sm">
          <div className={`w-2.5 h-2.5 rounded-full ${wsConnected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
          <span className="text-xs font-semibold text-slate-300 font-mono">
            {wsConnected ? 'WS CONNECTED' : 'OFFLINE'}
          </span>
        </div>
      </div>
    </header>
  );
};
