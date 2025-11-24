"use client";

import { useDashboardStore } from "../../../src/store/useDashboardStore";

export default function ComponentBreakdownChart() {
  const components = useDashboardStore((state) => state.latestComponents);

  const componentLabels: Record<string, string> = {
    momentum: "Momentum MASI",
    price_strength: "Force des Prix",
    volume: "Volume",
    volatility: "Volatilité",
    equity_vs_bonds: "Actions vs Obligations",
    media_sentiment: "Sentiment Média",
  };

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-800 p-6 shadow">
      <h2 className="text-xl font-semibold mb-4">Détail des composantes</h2>
      <div className="space-y-4">
        {Object.entries(components).map(([key, value]) => (
          <div key={key} className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-300">{componentLabels[key] || key}</span>
              <span className="text-white font-semibold">{value.toFixed(1)}</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${value}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

