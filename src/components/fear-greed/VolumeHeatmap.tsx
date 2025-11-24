import { useState, useEffect } from "react";
import { useDashboardStore } from "../../store/useDashboardStore";

function getHeatmapColor(normalizedVolume: number): string {
  // normalizedVolume est autour de 100 (moyenne)
  if (normalizedVolume < 70) return "bg-blue-500/30";
  if (normalizedVolume < 90) return "bg-green-500/50";
  if (normalizedVolume < 110) return "bg-yellow-500/70";
  return "bg-red-500/90";
}

export default function VolumeHeatmap() {
  const volumeData = useDashboardStore((state) => state.volumeHeatmap);
  const [heatmapData, setHeatmapData] = useState<any[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Utiliser uniquement les données réelles du backend
    if (volumeData && Array.isArray(volumeData) && volumeData.length > 0) {
      setHeatmapData(volumeData);
      console.log('✅ Données volume chargées:', volumeData.length, 'jours');
    } else {
      setHeatmapData([]);
      if (volumeData !== undefined) {
        console.warn('⚠️ Aucune donnée de volume disponible', { volumeData });
      }
    }
  }, [volumeData]);

  if (!mounted) {
    return null; // Rendu silencieux pendant l'hydration
  }

  if (heatmapData.length === 0) {
    return (
      <div className="bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-700">
        <h2 className="text-2xl font-bold text-white mb-6">
          📊 Volume de Trading (30 jours)
        </h2>
        <div className="text-center text-gray-500 py-12">
          <div className="text-4xl mb-3">📊</div>
          <p>Aucune donnée de volume disponible</p>
          <p className="text-xs mt-2">Lancez le pipeline pour collecter les données</p>
        </div>
      </div>
    );
  }

  // Organiser les données en grille (7 colonnes pour une semaine)
  const rows: any[][] = [];
  for (let i = 0; i < heatmapData.length; i += 7) {
    rows.push(heatmapData.slice(i, i + 7));
  }

  return (
    <div className="bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">
          📊 Volume de Trading
        </h2>
        <span className="text-sm text-gray-500 bg-gray-600 px-3 py-1 rounded-full">
          {heatmapData.length} jours
        </span>
      </div>
      
      <div className="space-y-2">
        {rows.map((row, rowIndex) => (
          <div key={rowIndex} className="flex gap-2">
            {row.map((day, colIndex) => {
              const date = new Date(day.date);
              const dayOfMonth = date.getDate();
              const monthShort = date.toLocaleDateString('fr-FR', { month: 'short' });
              
              // Gérer les valeurs null/undefined
              const closeValue = day.close ?? day.Close ?? null;
              const changePercent = day.change_percent ?? day.changePercent ?? 0;
              const volumeValue = day.volume ?? day.Volume ?? 0;
              const normalizedVolume = day.normalized_volume ?? day.normalizedVolume ?? 100;
              
              // Construire le tooltip en gérant les valeurs nulles
              const tooltip = [
                date.toLocaleDateString('fr-FR'),
                `Volume: ${volumeValue.toLocaleString()}`,
                `Normalisé: ${normalizedVolume.toFixed(0)}%`,
                closeValue !== null ? `Clôture: ${closeValue.toFixed(2)}` : 'Clôture: N/A',
                `Variation: ${changePercent !== null && changePercent !== undefined ? changePercent.toFixed(2) : 'N/A'}%`
              ].join('\n');
              
              return (
                <div
                  key={colIndex}
                  className={`flex-1 min-w-[80px] h-20 rounded-lg ${getHeatmapColor(
                    normalizedVolume
                  )} flex flex-col items-center justify-center text-white transition-all hover:scale-105 cursor-pointer shadow-sm`}
                  title={tooltip}
                >
                  <div className="text-xs font-bold opacity-90">
                    {dayOfMonth} {monthShort}
                  </div>
                  <div className="text-lg font-bold mt-1">
                    {Math.round(normalizedVolume)}
                  </div>
                  {changePercent !== null && changePercent !== undefined && (
                    <div className={`text-xs font-medium mt-1 ${
                      changePercent > 0 ? 'text-green-200' : 
                      changePercent < 0 ? 'text-red-200' : 
                      'text-gray-200'
                    }`}>
                      {changePercent > 0 ? '↑' : changePercent < 0 ? '↓' : '→'} 
                      {Math.abs(changePercent).toFixed(1)}%
                    </div>
                  )}
                </div>
              );
            })}
            {/* Remplir les cases vides pour la dernière ligne */}
            {row.length < 7 && Array.from({ length: 7 - row.length }).map((_, i) => (
              <div key={`empty-${i}`} className="flex-1 min-w-[80px] h-20"></div>
            ))}
          </div>
        ))}
      </div>
      
      {/* Légende */}
      <div className="mt-6 flex flex-wrap justify-center items-center gap-4 text-xs">
        <span className="text-gray-400 font-semibold">Volume (normalisé):</span>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-blue-500/30 rounded"></div>
          <span className="text-gray-400">&lt; 70% (Faible)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500/50 rounded"></div>
          <span className="text-gray-400">70-90% (Moyen)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-yellow-500/70 rounded"></div>
          <span className="text-gray-400">90-110% (Normal)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500/90 rounded"></div>
          <span className="text-gray-400">&gt; 110% (Élevé)</span>
        </div>
      </div>

      {/* Statistiques */}
      {heatmapData.length > 0 && (() => {
        const volumes = heatmapData.map(d => d.volume ?? d.Volume ?? 0).filter(v => v > 0);
        if (volumes.length === 0) return null;
        
        const avgVolume = volumes.reduce((sum, v) => sum + v, 0) / volumes.length;
        const maxVolume = Math.max(...volumes);
        const minVolume = Math.min(...volumes);
        
        return (
          <div className="mt-6 pt-6 border-t border-gray-700">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-xs text-gray-500 mb-1">Volume Moyen</div>
                <div className="text-lg font-bold text-white">
                  {avgVolume.toLocaleString('fr-FR', { maximumFractionDigits: 0 })}
                </div>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Volume Max</div>
                <div className="text-lg font-bold text-white">
                  {maxVolume.toLocaleString('fr-FR', { maximumFractionDigits: 0 })}
                </div>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Volume Min</div>
                <div className="text-lg font-bold text-white">
                  {minVolume.toLocaleString('fr-FR', { maximumFractionDigits: 0 })}
                </div>
              </div>
            </div>
          </div>
        );
      })()}
    </div>
  );
}

