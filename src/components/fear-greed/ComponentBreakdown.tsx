import { useDashboardStore } from "../../store/useDashboardStore";

interface ComponentBarProps {
  label: string;
  value: number;
  color: string;
  contribution: number;
}

function ComponentBar({ label, value, color, contribution }: ComponentBarProps) {
  return (
    <div className="mb-4">
      <div className="flex justify-between mb-2">
        <span className="text-gray-300 font-medium">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-white font-bold">{Math.round(value)}</span>
          <span className="text-xs text-gray-500">
            ({contribution > 0 ? '+' : ''}{contribution.toFixed(1)} pts)
          </span>
        </div>
      </div>
      <div className="w-full bg-gray-600 rounded-full h-3 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000 ease-out"
          style={{
            width: `${value}%`,
            backgroundColor: color,
          }}
        />
      </div>
    </div>
  );
}

export default function ComponentBreakdown() {
  const components = useDashboardStore((state) => state.latestComponents);

  // Poids de chaque composante (aligné avec l'agrégateur backend)
  const weights = {
    momentum: 0.25,
    price_strength: 0.25,
    volume: 0.15,
    volatility: 0.15,
    equity_vs_bonds: 0.10,
    media_sentiment: 0.10,
  };

  // Calculer la contribution de chaque composante au score global
  const calculateContribution = (value: number, weight: number) => {
    // Contribution = (valeur - 50) * poids
    // Si valeur > 50 : contribution positive (vers Greed)
    // Si valeur < 50 : contribution négative (vers Fear)
    return (value - 50) * weight;
  };

  const componentData = [
    { 
      label: "Momentum", 
      value: components.momentum, 
      color: "#8b5cf6",
      contribution: calculateContribution(components.momentum, weights.momentum),
    },
    { 
      label: "Price Strength", 
      value: components.price_strength, 
      color: "#ec4899",
      contribution: calculateContribution(components.price_strength, weights.price_strength),
    },
    { 
      label: "Volume", 
      value: components.volume, 
      color: "#f59e0b",
      contribution: calculateContribution(components.volume, weights.volume),
    },
    { 
      label: "Volatility", 
      value: components.volatility, 
      color: "#ef4444",
      contribution: calculateContribution(components.volatility, weights.volatility),
    },
    { 
      label: "Equity vs Bonds", 
      value: components.equity_vs_bonds, 
      color: "#10b981",
      contribution: calculateContribution(components.equity_vs_bonds, weights.equity_vs_bonds),
    },
    { 
      label: "Media Sentiment", 
      value: components.media_sentiment, 
      color: "#3b82f6",
      contribution: calculateContribution(components.media_sentiment, weights.media_sentiment),
    },
  ];

  // Calculer la contribution totale
  const totalContribution = componentData.reduce((sum, c) => sum + c.contribution, 0);

  return (
    <div className="bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-700">
      <h2 className="text-2xl font-bold text-white mb-6">
        Détail des Composants
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {componentData.map((component) => (
          <ComponentBar
            key={component.label}
            label={component.label}
            value={component.value}
            color={component.color}
            contribution={component.contribution}
          />
        ))}
      </div>
      
      <div className="mt-6 pt-6 border-t border-gray-700">
        <div className="flex justify-between items-center mb-2">
          <p className="text-sm text-gray-400">
            Contribution totale au score
          </p>
          <p className="text-lg font-bold text-white">
            {totalContribution > 0 ? '+' : ''}{totalContribution.toFixed(1)} pts
          </p>
        </div>
        <p className="text-xs text-gray-500 text-center">
          Score neutre = 50 | Valeurs &gt; 50 poussent vers Greed | Valeurs &lt; 50 poussent vers Fear
        </p>
      </div>
    </div>
  );
}

