"use client";

import FearGreedGauge from "./components/FearGreedGauge";
import HistoricalChart from "./components/HistoricalChart";
import ComponentBreakdown from "./components/ComponentBreakdown";
import SimplifiedScoreCard from "./components/SimplifiedScoreCard";
import SentimentFeed from "./components/SentimentFeed";
import VolumeHeatmap from "./components/VolumeHeatmap";
import DataLoader from "./components/DataLoader";
import RefreshButton from "./components/RefreshButton";

export default function DashboardPage() {
  return (
    <div className="min-h-screen p-8 bg-gray-900" style={{ 
      fontFamily: 'Arial, sans-serif'
    }}>
      <DataLoader />
      <div className="max-w-7xl mx-auto">
        {/* Header avec indicateur de statut et bouton d'actualisation */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">
              📊 Fear & Greed Index
            </h1>
            <p className="text-gray-400 text-lg">
              Bourse de Casablanca - Sentiment du marché en temps réel
            </p>
          </div>
          <div className="flex flex-col items-end gap-3">
            {/* Bouton d'actualisation */}
            <RefreshButton />
            
            {/* Indicateur de statut */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-300">Système actif</span>
              </div>
              <div className="text-sm text-gray-400" suppressHydrationWarning>
                Mis à jour: {new Date().toLocaleTimeString("fr-MA", { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        </div>
        
        {/* Gauge principal et graphique historique */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-8">
          <div className="xl:col-span-2">
            <FearGreedGauge />
          </div>
          <div>
            <SimplifiedScoreCard />
          </div>
        </div>

        {/* Graphique historique */}
        <div className="mb-8">
          <HistoricalChart />
        </div>
        
        {/* Breakdown des composants */}
        <div className="mb-8">
          <ComponentBreakdown />
        </div>
        
        {/* Composants secondaires */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <SentimentFeed />
          <VolumeHeatmap />
        </div>

        {/* Footer */}
        <div className="mt-12 pt-8 border-t border-gray-700">
          <div className="text-center text-sm text-gray-400">
            <p>
              Données en temps réel de la Bourse de Casablanca
            </p>
            <p className="mt-2">
              Sources : MASI, Medias24, BourseNews.ma, Challenge.ma, La Vie Éco
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

