import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface IndexScore {
  as_of: string;
  score: number;
}

export interface ComponentScores {
  as_of: string;
  momentum: number;
  price_strength: number;
  volume: number;
  volatility: number;
  equity_vs_bonds: number;
  media_sentiment: number;
}

export interface MediaArticle {
  title: string;
  summary: string;
  url: string;
  source: string;
  published_at: string;
}

export function useApi() {
  const [latestScore, setLatestScore] = useState<IndexScore | null>(null);
  const [components, setComponents] = useState<ComponentScores | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLatestScore = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/index/latest`);
      if (!response.ok) throw new Error('Failed to fetch latest score');
      const data = await response.json();
      setLatestScore(data);
    } catch (err) {
      console.error('Error fetching latest score:', err);
      setError('Failed to fetch latest score');
    }
  };

  const fetchComponents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/components/latest`);
      if (!response.ok) throw new Error('Failed to fetch components');
      const data = await response.json();
      setComponents(data);
    } catch (err) {
      console.error('Error fetching components:', err);
      setError('Failed to fetch components');
    }
  };

  const fetchAll = async () => {
    setLoading(true);
    setError(null);
    
    await Promise.all([
      fetchLatestScore(),
      fetchComponents()
    ]);
    
    setLoading(false);
  };

  useEffect(() => {
    fetchAll();
    
    // Refresh every 5 minutes
    const interval = setInterval(fetchAll, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return {
    latestScore,
    components,
    loading,
    error,
    refetch: fetchAll
  };
}