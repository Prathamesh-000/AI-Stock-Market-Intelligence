import React from 'react';

interface SectorRippleProps {
  sectorRipple: Record<string, number>;
}

export const SectorRipple: React.FC<SectorRippleProps> = ({ sectorRipple }) => {
  const rippleEntries = Object.entries(sectorRipple || {}) as [string, number][];
  const maxAbs = Math.max(...rippleEntries.map(([, v]) => Math.abs(v)), 1);

  return (
    <div>
      <h4 className="text-xs font-bold text-slate-500 tracking-wider mb-3 uppercase">
        SECTOR RIPPLE EFFECT
      </h4>

      <div className="space-y-3">
        {rippleEntries.map(([comp, impact]) => {
          const isPos = impact > 0;
          const isNeg = impact < 0;

          return (
            <div key={comp} className="flex items-center gap-3">
              <span className="w-10 text-xs font-bold text-slate-400 font-mono">{comp}</span>
              <span className={`w-14 text-xs font-mono font-bold ${isPos ? 'text-emerald-400' : isNeg ? 'text-red-400' : 'text-slate-400'}`}>
                {isPos ? '+' : ''}{impact?.toFixed(1)}%
              </span>
              <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-500 ${isPos ? 'bg-emerald-500/60' : 'bg-red-500/60'}`}
                  style={{ width: `${Math.min((Math.abs(impact) / maxAbs) * 100, 100)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

