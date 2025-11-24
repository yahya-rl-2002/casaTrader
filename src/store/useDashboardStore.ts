import { create } from "zustand";

type ComponentScores = Record<string, number>;

export type MediaArticle = {
  id?: number;
  title: string;
  summary?: string;
  url: string;
  source: string;
  published_at?: string;
  publishedAt?: string; // Alias pour compatibilité
  sentiment_score?: number | null;
  sentimentScore?: number; // Alias pour compatibilité
  sentiment_label?: string | null;
  sentimentLabel?: string; // Alias pour compatibilité
  scraped_at?: string;
};

export type VolumePoint = {
  date: string;
  volume: number;
  normalized_volume: number;
  close?: number | null;
  change_percent?: number | null;
};

export type SimplifiedScore = {
  score: number;
  volume_moyen: number;
  sentiment_news: number;
  performance_marche: number;
  nombre_actions: number;
  date: string;
  formule: string;
  interpretation: string;
};

type DashboardState = {
  latestScore: number;
  latestComponents: ComponentScores;
  simplifiedScore: SimplifiedScore | null;
  mediaSentimentFeed: MediaArticle[];
  volumeHeatmap: VolumePoint[];
  loading: boolean;
  error: string | null;
  setLatestScore: (score: number) => void;
  setComponents: (components: ComponentScores) => void;
  setSimplifiedScore: (score: SimplifiedScore) => void;
  setMediaFeed: (articles: MediaArticle[]) => void;
  setVolumeHeatmap: (points: VolumePoint[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
};

export const useDashboardStore = create<DashboardState>()((set) => ({
  latestScore: 50, // Default score
  latestComponents: {
    momentum: 50,
    price_strength: 50,
    volume: 50,
    volatility: 50,
    equity_vs_bonds: 50,
    media_sentiment: 50,
  },
  simplifiedScore: null,
  mediaSentimentFeed: [],
  volumeHeatmap: [],
  loading: false,
  error: null,
  setLatestScore: (score) => set({ latestScore: score }),
  setComponents: (components) => set({ latestComponents: components }),
  setSimplifiedScore: (score) => set({ simplifiedScore: score }),
  setMediaFeed: (articles) => set({ mediaSentimentFeed: articles }),
  setVolumeHeatmap: (points) => set({ volumeHeatmap: points }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));

