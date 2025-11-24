export type FearGreedOverview = {
  asOf: string;
  score: number;
};

export type ComponentBreakdown = {
  asOf: string;
  components: Record<string, number>;
};

export type MediaArticle = {
  title: string;
  summary: string;
  source: string;
  url: string;
  publishedAt: string;
};



