import React from 'react';
import { BarChart3 } from 'lucide-react';
import { FeatureDriver } from '../../types';

interface FeatureDriversProps {
  featureImportance: FeatureDriver[];
}

export const FeatureDrivers: React.FC<FeatureDriversProps> = ({ featureImportance }) => {
  return (
    <div>
      <h4 className="text-xs font-bold text-slate-500 tracking-wider mb-3 flex items-center gap-1.5 uppercase">
        <BarChart3 className="w-4 h-4 text-blue-400" /> MAIN DRIVERS
      </h4>

      <div className="space-y-3">
        {(featureImportance || []).map((feat, idx) => (
          <div key={idx} className="flex items-center gap-3">
            <span className="flex-1 text-xs text-slate-400 truncate">{feat.name}</span>
            <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500/60 transition-all duration-500"
                style={{ width: `${Math.min(feat.value, 100)}%` }}
              />
            </div>
            <span className="text-xs font-mono text-slate-500 w-8 text-right">{feat.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};
