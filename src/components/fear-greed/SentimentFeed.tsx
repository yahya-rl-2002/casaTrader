import { useState, useEffect } from "react";
import { useDashboardStore } from "../../store/useDashboardStore";

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

export default function SentimentFeed() {
  const mediaFeed = useDashboardStore((state) => state.mediaSentimentFeed);
  const [articles, setArticles] = useState<any[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // Utiliser uniquement les données réelles du backend
    if (mediaFeed && Array.isArray(mediaFeed) && mediaFeed.length > 0) {
      setArticles(mediaFeed);
      console.log('✅ Articles média chargés:', mediaFeed.length);
    } else {
      // Pas de données de démo - afficher liste vide
      setArticles([]);
      if (mediaFeed !== undefined) {
        console.warn('⚠️ Aucun article média disponible', { mediaFeed });
      }
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
            // S'assurer que le titre est toujours affiché
            const articleTitle = article.title || article.Title || 'Titre non disponible';
            const articleSummary = article.summary || article.Summary || article.summary;
            const articleSource = article.source || article.Source || 'Source inconnue';
            const articleUrl = article.url || article.Url || '#';
            
            return (
              <a
                key={article.id || index}
                href={articleUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block bg-gray-700 rounded-lg p-4 border border-gray-700 hover:bg-blue-900 hover:border-blue-300 transition-all cursor-pointer"
              >
                <div className="flex items-start gap-3 mb-2">
                  <span className="text-2xl flex-shrink-0" title={`Sentiment: ${sentimentScore !== null && sentimentScore !== undefined ? sentimentScore.toFixed(1) : 'N/A'}`}>
                    {getSentimentEmoji(sentimentScore)}
                  </span>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-white font-semibold text-sm line-clamp-2 mb-1 leading-tight">
                      {articleTitle}
                    </h3>
                    {articleSummary && (
                      <p className="text-xs text-gray-400 line-clamp-2 mt-1">
                        {articleSummary}
                      </p>
                    )}
                  </div>
                  <span
                    className={`text-xs font-bold flex-shrink-0 ${getSentimentColor(sentimentScore)}`}
                    title={`Score: ${sentimentScore !== null && sentimentScore !== undefined ? sentimentScore.toFixed(1) : 'N/A'}`}
                  >
                    {sentimentScore !== null && sentimentScore !== undefined ? sentimentScore.toFixed(1) : 'N/A'}
                  </span>
                </div>
                
                <div className="flex justify-between items-center text-xs text-gray-500 mt-2 pt-2 border-t border-gray-600">
                  <span className="font-medium uppercase bg-gray-600 px-2 py-1 rounded">
                    {articleSource}
                  </span>
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

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #374151;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #6b7280;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #9ca3af;
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

