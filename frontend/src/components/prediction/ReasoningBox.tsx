import React from 'react';

interface ReasoningBoxProps {
  eventType: string;
  explanation: string;
  aiReasoning?: string[];
}

export const ReasoningBox: React.FC<ReasoningBoxProps> = ({
  eventType,
  explanation,
  aiReasoning
}) => {
  return (
    <div className="mb-6 p-4 bg-blue-900/10 border border-blue-900/30 rounded-lg">
      <div className="flex gap-2 mb-2">
        <span className="bg-blue-900/50 text-blue-400 text-xs font-bold px-2.5 py-1 rounded border border-blue-800/40 font-mono">
          Event: {eventType}
        </span>
      </div>

      <p className="text-sm text-slate-300 italic my-3 leading-relaxed">
        "{explanation}"
      </p>

      {aiReasoning && aiReasoning.length > 0 && (
        <div className="mt-4 pt-4 border-t border-blue-900/30">
          <div className="text-xs text-blue-400/80 font-bold mb-2 tracking-wider uppercase">
            AI Mathematical Reasoning
          </div>
          <ul className="list-disc list-inside text-xs text-slate-400 space-y-1.5 leading-normal">
            {aiReasoning.map((r, idx) => (
              <li key={idx} className="marker:text-blue-500">{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
