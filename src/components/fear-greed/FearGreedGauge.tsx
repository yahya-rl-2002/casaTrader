import { useMemo } from "react";
import { useDashboardStore } from "../../store/useDashboardStore";

function clampScore(score: number): number {
  return Math.max(0, Math.min(100, score));
}

function getStatus(score: number): string {
  if (score >= 70) return "EXTREME GREED";
  if (score >= 55) return "GREED";
  if (score >= 45) return "NEUTRAL";
  if (score >= 30) return "FEAR";
  return "EXTREME FEAR";
}

function getColor(score: number): string {
  if (score >= 70) return "#10b981"; // green-500
  if (score >= 55) return "#84cc16"; // lime-500
  if (score >= 45) return "#fbbf24"; // amber-400
  if (score >= 30) return "#f97316"; // orange-500
  return "#ef4444"; // red-500
}

export default function FearGreedGauge() {
  const latestScore = useDashboardStore((state) => state.latestScore);
  const score = clampScore(latestScore);
  const status = useMemo(() => getStatus(score), [score]);
  const color = useMemo(() => getColor(score), [score]);
  const displayScore = score.toFixed(2); // Afficher avec 2 décimales (ex: 52.30)
  const position = score; // Position en pourcentage (0-100)

  return (
    <div className="bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-700">
      <h2 className="text-2xl font-bold text-white mb-8 text-center">
        Fear & Greed Index
      </h2>
      
      {/* Score principal */}
      <div className="text-center mb-8">
        <div className="text-7xl font-bold mb-3" style={{ color }}>
          {displayScore}
        </div>
        <div className="text-2xl font-semibold text-gray-300 mb-1">
          {status}
        </div>
      </div>

      {/* Barre avec dégradé */}
      <div className="relative w-full mb-8">
        {/* Barre de fond avec dégradé */}
        <div 
          className="relative w-full h-16 rounded-xl overflow-hidden shadow-lg"
          style={{
            background: 'linear-gradient(to right, #ef4444 0%, #f97316 25%, #fbbf24 50%, #84cc16 75%, #10b981 100%)'
          }}
        >
          {/* Labels sur la barre */}
          <div className="absolute inset-0 flex justify-between items-center px-6 text-sm font-bold text-white/95 pointer-events-none">
            <span className="drop-shadow-lg">FEAR</span>
            <span className="drop-shadow-lg">NEUTRAL</span>
            <span className="drop-shadow-lg">GREED</span>
          </div>
          
          {/* Indicateur de position */}
          <div 
            className="absolute top-0 bottom-0 w-1 bg-white shadow-2xl transition-all duration-1000 ease-out"
            style={{ left: `${position}%` }}
          >
            {/* Cercle supérieur */}
            <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-5 h-5 bg-white rounded-full shadow-xl border-4 border-gray-900"></div>
            
            {/* Cercle inférieur */}
            <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-5 h-5 bg-white rounded-full shadow-xl border-4 border-gray-900"></div>
          </div>
        </div>

        {/* Valeurs de référence sous la barre */}
        <div className="flex justify-between mt-3 text-xs text-gray-400 px-2">
          <span>0</span>
          <span>25</span>
          <span>50</span>
          <span>75</span>
          <span>100</span>
        </div>
      </div>
      
      {/* Légende détaillée */}
      <div className="grid grid-cols-5 gap-3 text-xs text-center mt-8">
        <div className="p-3 rounded-lg bg-gray-700/50">
          <div className="w-full h-3 bg-red-500 rounded-full mb-2 shadow-md"></div>
          <span className="text-gray-300 font-medium">Extreme Fear</span>
          <div className="text-gray-500 mt-1">0-25</div>
        </div>
        <div className="p-3 rounded-lg bg-gray-700/50">
          <div className="w-full h-3 bg-orange-500 rounded-full mb-2 shadow-md"></div>
          <span className="text-gray-300 font-medium">Fear</span>
          <div className="text-gray-500 mt-1">25-45</div>
        </div>
        <div className="p-3 rounded-lg bg-gray-700/50">
          <div className="w-full h-3 bg-amber-400 rounded-full mb-2 shadow-md"></div>
          <span className="text-gray-300 font-medium">Neutral</span>
          <div className="text-gray-500 mt-1">45-55</div>
        </div>
        <div className="p-3 rounded-lg bg-gray-700/50">
          <div className="w-full h-3 bg-lime-500 rounded-full mb-2 shadow-md"></div>
          <span className="text-gray-300 font-medium">Greed</span>
          <div className="text-gray-500 mt-1">55-70</div>
        </div>
        <div className="p-3 rounded-lg bg-gray-700/50">
          <div className="w-full h-3 bg-green-500 rounded-full mb-2 shadow-md"></div>
          <span className="text-gray-300 font-medium">Extreme Greed</span>
          <div className="text-gray-500 mt-1">70-100</div>
        </div>
      </div>
    </div>
  );
}

