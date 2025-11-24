"use client";

import { useState, useEffect } from "react";
import { useDashboardStore } from "../../../src/store/useDashboardStore";

function getSentimentColor(score: number | undefined): string {
  if (!score) return "text-gray-400";
  if (score > 10) return "text-green-600";
  if (score > -10) return "text-yellow-600";
  return "text-red-600";
}

function getSentimentEmoji(score: number | undefined): string {
  if (!score) return "😐";
  if (score > 10) return "😊";
  if (score > -10) return "😐";
  return "😟";
}

function getSentimentLabel(score: number | undefined): string {
  if (!score) return "Neutre";
  if (score > 10) return "Positif";
  if (score > -10) return "Neutre";
  return "Négatif";
}

export default function SentimentFeed() {
  const mediaFeed = useDashboardStore((state) => state.mediaSentimentFeed);
  const [articles, setArticles] = useState<any[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // Utiliser uniquement les données réelles du backend
    if (mediaFeed && mediaFeed.length > 0) {
      setArticles(mediaFeed);
      console.log('✅ Articles média chargés:', mediaFeed.length);
    } else {
      // Pas de données de démo - afficher liste vide
      setArticles([]);
      console.warn('⚠️ Aucun article média disponible');
    }
  }, [mediaFeed]);

  if (!mounted) {
    return null; // Rendu silencieux pendant l'hydration
  }

  return (
    <div className="bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">
          📰 Sentiment Média
        </h2>
        <span className="text-sm text-gray-500 bg-gray-600 px-3 py-1 rounded-full">
          {articles.length} articles
        </span>
      </div>
      
      <div className="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
        {articles.length === 0 ? (
          <div className="text-center text-gray-500 py-12">
            <div className="text-4xl mb-3">📭</div>
            <p>Aucun article disponible</p>
            <p className="text-xs mt-2">Lancez le pipeline pour scraper les news</p>
          </div>
        ) : (
          articles.slice(0, 15).map((article, index) => {
            const sentimentScore = article.sentiment_score ?? article.sentimentScore;
            const publishedDate = article.published_at ?? article.publishedAt;
            
            return (
              <a
                key={article.id || index}
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block bg-gray-700 rounded-lg p-4 border border-gray-700 hover:bg-blue-50 hover:border-blue-300 transition-all cursor-pointer"
              >
                <div className="flex items-start gap-3 mb-2">
                  <span className="text-2xl flex-shrink-0">
                    {getSentimentEmoji(sentimentScore)}
                  </span>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-white font-medium text-sm line-clamp-2 mb-1">
                      {article.title}
                    </h3>
                    {article.summary && (
                      <p className="text-xs text-gray-400 line-clamp-2">
                        {article.summary}
                      </p>
                    )}
                  </div>
                  <span
                    className={`text-xs font-bold flex-shrink-0 ${getSentimentColor(sentimentScore)}`}
                  >
                    {sentimentScore !== null && sentimentScore !== undefined ? sentimentScore.toFixed(1) : 'N/A'}
                  </span>
                </div>
                
                <div className="flex justify-between items-center text-xs text-gray-500">
                  <span className="font-medium uppercase">{article.source}</span>
                  <span>
                    {publishedDate ? new Date(publishedDate).toLocaleDateString('fr-FR', { 
                      day: '2-digit', 
                      month: 'short',
                      hour: '2-digit',
                      minute: '2-digit'
                    }) : 'Date inconnue'}
                  </span>
                </div>
              </a>
            );
          })
        )}
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #f1f1f1;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #888;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #555;
        }
        .line-clamp-2 {
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
      `}</style>
    </div>
  );
}
