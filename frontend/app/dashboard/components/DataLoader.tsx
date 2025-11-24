"use client";

import { useEffect } from "react";
import { useDashboardStore } from "../../../src/store/useDashboardStore";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export default function DataLoader() {
  const { setLatestScore, setComponents, setSimplifiedScore, setMediaFeed, setVolumeHeatmap, setLoading, setError } = useDashboardStore();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        // Fetch all data in parallel
        const [scoreResponse, componentsResponse, historyResponse, simplifiedResponse, mediaResponse, volumeResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/index/latest`),
          fetch(`${API_BASE_URL}/components/latest`),
          fetch(`${API_BASE_URL}/index/history?range=90d`),
          fetch(`${API_BASE_URL}/simplified-v2/score`),
          fetch(`${API_BASE_URL}/media/latest`),
          fetch(`${API_BASE_URL}/volume/latest`),
        ]);

        // Latest score
        if (scoreResponse.ok) {
          const scoreData = await scoreResponse.json();
          console.log('[DataLoader] Latest score:', scoreData);
          setLatestScore(scoreData.score);
        } else {
          console.warn('[DataLoader] Failed to fetch latest score', scoreResponse.status);
        }

        // Components
        if (componentsResponse.ok) {
          const componentsData = await componentsResponse.json();
          console.log('[DataLoader] Components:', componentsData);
          setComponents({
            momentum: componentsData.momentum,
            price_strength: componentsData.price_strength,
            volume: componentsData.volume,
            volatility: componentsData.volatility,
            equity_vs_bonds: componentsData.equity_vs_bonds,
            media_sentiment: componentsData.media_sentiment,
          });
        } else {
          console.warn('[DataLoader] Failed to fetch components', componentsResponse.status);
        }

        // History (for the chart)
        if (historyResponse.ok) {
          const historyData = await historyResponse.json();
          console.log('[DataLoader] Historical data:', historyData.data?.length || 0, 'records');
          if (typeof window !== 'undefined') {
            window.localStorage.setItem('fear_greed_history', JSON.stringify(historyData.data));
          }
        } else {
          console.warn('[DataLoader] Failed to fetch history', historyResponse.status);
        }

        // Simplified score
        if (simplifiedResponse.ok) {
          const simplifiedData = await simplifiedResponse.json();
          console.log('[DataLoader] Simplified score:', simplifiedData);
          setSimplifiedScore(simplifiedData);
        } else {
          console.warn('[DataLoader] Failed to fetch simplified score', simplifiedResponse.status);
        }

        // Media feed
        if (mediaResponse.ok) {
          const mediaData = await mediaResponse.json();
          console.log('[DataLoader] Media feed:', mediaData.data?.length || 0, 'articles');
          setMediaFeed(mediaData.data || []);
        } else {
          console.warn('[DataLoader] Failed to fetch media feed', mediaResponse.status);
        }

        // Volume heatmap
        if (volumeResponse.ok) {
          const volumeData = await volumeResponse.json();
          console.log('[DataLoader] Volume heatmap:', volumeData.data?.length || 0, 'points');
          setVolumeHeatmap(volumeData.data || []);
        } else {
          console.warn('[DataLoader] Failed to fetch volume heatmap', volumeResponse.status);
        }

      } catch (error) {
        console.error('[DataLoader] Error fetching data:', error);
        setError('Failed to load data from API');
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

