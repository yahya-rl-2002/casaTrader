import { useEffect } from "react";
import { useDashboardStore } from "../../store/useDashboardStore";

// Utilise le proxy Vite - pas besoin de spécifier localhost:8001
const API_BASE_URL = '/api/v1';

export default function DataLoader() {
  const { setLatestScore, setComponents, setSimplifiedScore, setMediaFeed, setVolumeHeatmap, setLoading, setError } = useDashboardStore();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      // Fonction helper pour gérer les requêtes individuellement
      const fetchWithErrorHandling = async (url: string, name: string) => {
        try {
          const response = await fetch(url);
          if (response.ok) {
            return await response.json();
          } else {
            console.warn(`[DataLoader] Failed to fetch ${name}:`, response.status, response.statusText);
            return null;
          }
        } catch (error) {
          console.warn(`[DataLoader] Error fetching ${name}:`, error);
          return null;
        }
      };

      try {
        // Fetch all data in parallel avec gestion d'erreur individuelle
        const [scoreData, componentsData, historyData, simplifiedData, mediaData, volumeData] = await Promise.allSettled([
          fetchWithErrorHandling(`${API_BASE_URL}/index/latest`, 'latest score'),
          fetchWithErrorHandling(`${API_BASE_URL}/components/latest`, 'components'),
          fetchWithErrorHandling(`${API_BASE_URL}/index/history?range=90d`, 'history'),
          fetchWithErrorHandling(`${API_BASE_URL}/simplified-v2/score`, 'simplified score'),
          fetchWithErrorHandling(`${API_BASE_URL}/media/latest`, 'media feed'),
          fetchWithErrorHandling(`${API_BASE_URL}/volume/latest`, 'volume heatmap'),
        ]);

        // Latest score
        if (scoreData.status === 'fulfilled' && scoreData.value) {
          console.log('[DataLoader] Latest score:', scoreData.value);
          setLatestScore(scoreData.value.score);
        }

        // Components
        if (componentsData.status === 'fulfilled' && componentsData.value) {
          console.log('[DataLoader] Components:', componentsData.value);
          setComponents({
            momentum: componentsData.value.momentum,
            price_strength: componentsData.value.price_strength,
            volume: componentsData.value.volume,
            volatility: componentsData.value.volatility,
            equity_vs_bonds: componentsData.value.equity_vs_bonds,
            media_sentiment: componentsData.value.media_sentiment,
          });
        }

        // History (for the chart)
        if (historyData.status === 'fulfilled' && historyData.value) {
          console.log('[DataLoader] Historical data:', historyData.value.data?.length || 0, 'records');
          if (typeof window !== 'undefined' && historyData.value.data) {
            window.localStorage.setItem('fear_greed_history', JSON.stringify(historyData.value.data));
          }
        }

        // Simplified score
        if (simplifiedData.status === 'fulfilled' && simplifiedData.value) {
          console.log('[DataLoader] Simplified score:', simplifiedData.value);
          setSimplifiedScore(simplifiedData.value);
        }

        // Media feed
        if (mediaData.status === 'fulfilled' && mediaData.value) {
          const articles = mediaData.value.data || [];
          console.log('[DataLoader] Media feed:', articles.length, 'articles');
          if (articles.length > 0) {
            setMediaFeed(articles);
          } else {
            console.warn('[DataLoader] Media feed vide ou structure invalide:', mediaData.value);
          }
        } else if (mediaData.status === 'rejected') {
          console.warn('[DataLoader] Erreur lors du chargement des articles média');
        }

        // Volume heatmap
        if (volumeData.status === 'fulfilled' && volumeData.value) {
          const points = volumeData.value.data || [];
          console.log('[DataLoader] Volume heatmap:', points.length, 'points');
          if (points.length > 0) {
            setVolumeHeatmap(points);
          } else {
            console.warn('[DataLoader] Volume heatmap vide ou structure invalide:', volumeData.value);
          }
        } else if (volumeData.status === 'rejected') {
          console.warn('[DataLoader] Erreur lors du chargement des données de volume');
        }

      } catch (error) {
        console.error('[DataLoader] Unexpected error:', error);
        setError('Failed to load some data from API');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Refresh every 5 minutes
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [setLatestScore, setComponents, setSimplifiedScore, setMediaFeed, setVolumeHeatmap, setLoading, setError]);

  return null; // This component doesn't render anything
}

