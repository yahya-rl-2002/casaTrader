"use client";

import { useDashboardStore } from "../../../src/store/useDashboardStore";

export default function SimplifiedScoreCard() {
  const simplifiedScore = useDashboardStore((state) => state.simplifiedScore);

  if (!simplifiedScore) {
    return null;
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 shadow-lg border border-blue-100">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">📐 Formule Simplifiée</h3>
        <span className="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded-full">
          {simplifiedScore.date}
        </span>
      </div>

      {/* Score principal */}
      <div className="text-center mb-6">
        <div className="text-5xl font-bold text-indigo-600 mb-2">
          {simplifiedScore.score.toFixed(2)}
        </div>
        <div className="text-sm text-gray-400">{simplifiedScore.interpretation}</div>
      </div>

      {/* Formule */}
      <div className="bg-gray-800 rounded-lg p-4 mb-4">
        <div className="text-xs text-gray-500 mb-2">Calcul :</div>
        <div className="font-mono text-sm text-gray-300 break-all">
          {simplifiedScore.formule}
        </div>
      </div>

      {/* Composantes */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="bg-gray-800 rounded-lg p-3 text-center">
          <div className="text-xs text-gray-500 mb-1">Volume</div>
          <div className="text-lg font-bold text-blue-600">
            {simplifiedScore.volume_moyen.toFixed(1)}
          </div>
        </div>
        <div className="bg-gray-800 rounded-lg p-3 text-center">
          <div className="text-xs text-gray-500 mb-1">Sentiment</div>
          <div className="text-lg font-bold text-green-600">
            {simplifiedScore.sentiment_news.toFixed(1)}
          </div>
        </div>
        <div className="bg-gray-800 rounded-lg p-3 text-center">
          <div className="text-xs text-gray-500 mb-1">Performance</div>
          <div className="text-lg font-bold text-purple-600">
            {simplifiedScore.performance_marche.toFixed(1)}
          </div>
        </div>
      </div>

      {/* Diviseur */}
      <div className="text-center text-xs text-gray-500">
        ÷ {simplifiedScore.nombre_actions} actions MASI
      </div>
    </div>
  );
}







