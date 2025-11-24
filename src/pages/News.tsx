import { useState, useEffect, useMemo, useCallback } from "react";
import { Navigation } from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";
import { RefreshCw, Search, Calendar, Tag } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { format } from "date-fns";
import { fr } from "date-fns/locale";

interface Article {
  id: string;
  title: string;
  description: string | null;
  content: string | null;
  source: string;
  source_url: string;
  image_url: string | null;
  published_at: string | null;
  category: string | null;
  tags: string[] | null;
}

type AutoUpdateStats = {
  total_articles: number;
  active_sources: number;
  articles_last_hour: number;
  articles_last_24h: number;
  latest_article_date: string | null;
  oldest_article_date: string | null;
};

type ScrapeResp = {
  success: boolean;
  articlesCount?: number;
  errors?: { source: string; error: string }[];
  error?: string;
  processed?: string[];
  totalTargets?: number;
  nextOffset?: number | null;
};

type DateRange = "all" | "24h" | "7d" | "30d";

export default function News() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [filteredArticles, setFilteredArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);
  // Variables d'auto-update supprimées pour garantir l'affichage stable
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedSource, setSelectedSource] = useState<string>("all");
  const [dateRange, setDateRange] = useState<DateRange>("all");
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [statsLoading, setStatsLoading] = useState<boolean>(false);
  // Pagination
  const PAGE_SIZE = 500;
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const { toast } = useToast();

  const fetchArticles = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) {
        setLoading(true);
      }
      
      // Utiliser l'API FastAPI directement au lieu de Supabase
      // Utiliser le proxy Vite qui redirige /api/v1 vers http://localhost:8001/api/v1
      const API_BASE_URL = '/api/v1';
      
      try {
        // Essayer d'abord l'API FastAPI
        const response = await fetch(`${API_BASE_URL}/media/latest?limit=${PAGE_SIZE}&auto_scrape=false`);
        if (response.ok) {
          const result = await response.json();
          const apiArticles = (result.data || []).map((article: any) => ({
            id: article.id?.toString() || article.url,
            title: article.title || 'Titre non disponible',
            description: article.summary || null,
            content: article.content || null,
            source: article.source || 'Source inconnue',
            source_url: article.url || '#',
            image_url: article.image_url || null,
            published_at: article.published_at || null,
            category: null,
            tags: null,
          }));
          
          console.log(`✅ ${apiArticles.length} articles récupérés depuis l'API FastAPI`);
          
          setArticles(apiArticles);
          setFilteredArticles(apiArticles);
          setPage(0);
          setHasMore((apiArticles.length || 0) >= PAGE_SIZE);
          setInitialLoad(false);
          
          // Ne pas continuer avec Supabase si l'API fonctionne
          return;
        } else {
          console.warn(`⚠️  API FastAPI retourne ${response.status}: ${response.statusText}`);
        }
      } catch (apiError) {
        console.warn('API FastAPI non disponible, fallback vers Supabase:', apiError);
      }
      
      // Fallback vers Supabase si l'API FastAPI n'est pas disponible
      const { data, error } = await supabase
        .from('articles')
        .select('*')
        .order('published_at', { ascending: false })
        .range(0, PAGE_SIZE - 1);

      if (error) throw error;

      const initial = data || [];
      setArticles(initial);
      setFilteredArticles(initial);
      setPage(0);
      setHasMore((initial.length || 0) === PAGE_SIZE);
      setInitialLoad(false); // Marquer le chargement initial comme terminé

      // Fetch auto-update stats (latest update time)
      setStatsLoading(true);
      try {
        const { data: statsData, error: statsError } = await supabase.rpc('get_auto_update_stats');
        if (!statsError && statsData) {
          const row = Array.isArray(statsData) ? statsData[0] as AutoUpdateStats | undefined : (statsData as AutoUpdateStats | undefined);
          setLastUpdated(row?.latest_article_date ?? null);
        }
      } catch (error) {
        console.warn('Could not fetch auto-update stats:', error);
      }
    } catch (error) {
      console.error('Error fetching articles:', error);
      if (showLoading) {
        toast({
          title: "Erreur",
          description: "Impossible de charger les articles",
          variant: "destructive",
        });
      }
    } finally {
      if (showLoading) {
        setLoading(false);
      }
      setStatsLoading(false);
    }
  }, [toast]);


  const loadMore = async () => {
    if (loadingMore || !hasMore) return;
    
    // Utiliser l'API FastAPI si disponible
    // Utiliser le proxy Vite qui redirige /api/v1 vers http://localhost:8001/api/v1
    const API_BASE_URL = '/api/v1';
    
    try {
      const response = await fetch(`${API_BASE_URL}/media/latest?limit=${PAGE_SIZE}&offset=${(page + 1) * PAGE_SIZE}&auto_scrape=false`);
      if (response.ok) {
        const result = await response.json();
        const newArticles = (result.data || []).map((article: any) => ({
          id: article.id?.toString() || article.url,
          title: article.title || 'Titre non disponible',
          description: article.summary || null,
          content: article.content || null,
          source: article.source || 'Source inconnue',
          source_url: article.url || '#',
          image_url: article.image_url || null,
          published_at: article.published_at || null,
          category: null,
          tags: null,
        }));
        
        if (newArticles.length > 0) {
          setArticles(prev => [...prev, ...newArticles]);
          setFilteredArticles(prev => [...prev, ...newArticles]);
          setPage(prev => prev + 1);
          setHasMore(newArticles.length >= PAGE_SIZE);
        } else {
          setHasMore(false);
        }
        return;
      }
    } catch (apiError) {
      console.warn('API FastAPI non disponible pour loadMore, fallback vers Supabase:', apiError);
    }
    setLoadingMore(true);
    try {
      const nextPage = page + 1;
      const from = nextPage * PAGE_SIZE;
      const to = from + PAGE_SIZE - 1;
      const { data, error } = await supabase
        .from('articles')
        .select('*')
        .order('published_at', { ascending: false })
        .range(from, to);
      if (error) throw error;
      const newItems = data || [];
      const mergedMap = new Map<string, Article>();
      [...articles, ...newItems].forEach((a) => mergedMap.set(a.id, a));
      setArticles(Array.from(mergedMap.values()));
      setPage(nextPage);
      setHasMore(newItems.length === PAGE_SIZE);
    } catch (error) {
      console.error('Error loading more:', error);
      toast({ title: 'Erreur', description: "Impossible de charger plus d'articles", variant: 'destructive' });
    } finally {
      setLoadingMore(false);
    }
  };

  const refreshArticles = async () => {
    // Éviter les appels multiples simultanés
    if (refreshing) {
      console.log('⏳ Actualisation déjà en cours, ignorée');
      return;
    }
    
    console.log('🔄 Démarrage de l\'actualisation manuelle...');
    setRefreshing(true);
    
    try {
      console.log('🔄 Déclenchement de l\'auto-update des articles...')
      
      // Utiliser la fonction d'auto-update
      const { data, error } = await supabase.functions.invoke('auto-update-news');
      if (error) throw error;
      
      const resp = data as { 
        success: boolean; 
        articles_added: number; 
        articles_cleaned: number;
        sources_processed: string[]; 
        timestamp: string;
        error?: string;
      };
      
      if (!resp.success) {
        throw new Error(resp.error || 'Erreur lors de l\'auto-update');
      }

      // Afficher le toast avec les résultats
      if (resp.articles_added > 0) {
        toast({
          title: "✅ Articles mis à jour",
          description: `${resp.articles_added} nouveaux articles ajoutés, ${resp.articles_cleaned} anciens articles nettoyés`,
          duration: 4000,
        });
        
        // Recharger les articles seulement s'il y a des nouveaux articles
        console.log(`📰 ${resp.articles_added} nouveaux articles trouvés, rechargement...`);
        await fetchArticles(false); // Recharger sans affecter l'état loading
      } else {
        toast({
          title: "ℹ️ Aucun nouvel article",
          description: "Aucun nouvel article trouvé lors de l'actualisation",
          duration: 3000,
        });
      }

    } catch (error) {
      console.error('Error refreshing articles:', error);
      toast({
        title: "Erreur",
        description: error instanceof Error ? error.message : "Impossible d'actualiser les articles",
        variant: "destructive",
      });
    } finally {
      setRefreshing(false);
    }
  };


  useEffect(() => {
    // Charger les articles une seule fois au montage du composant
    fetchArticles();
    
    // AUCUNE actualisation automatique - les articles restent affichés en permanence
    console.log('📰 Articles chargés - aucun auto-update pour garantir l\'affichage stable');
  }, [fetchArticles]);

  useEffect(() => {
    let filtered = articles;

    // Période
    if (dateRange !== "all") {
      const now = Date.now();
      const ranges = {
        "24h": 24 * 60 * 60 * 1000,
        "7d": 7 * 24 * 60 * 60 * 1000,
        "30d": 30 * 24 * 60 * 60 * 1000,
      } as const;
      const threshold = now - ranges[dateRange as Exclude<DateRange, "all">];
      filtered = filtered.filter((a) => {
        if (!a.published_at) return false;
        const ts = new Date(a.published_at).getTime();
        return !Number.isNaN(ts) && ts >= threshold;
      });
    }

    // Catégorie
    if (selectedCategory !== "all") {
      filtered = filtered.filter((article) => article.category === selectedCategory);
    }

    // Source
    if (selectedSource !== "all") {
      filtered = filtered.filter((article) => article.source === selectedSource);
    }

    // Tags (ET logique: l'article doit contenir tous les tags sélectionnés)
    if (selectedTags.length > 0) {
      filtered = filtered.filter((article) => {
        const tags = article.tags || [];
        return selectedTags.every((t) => tags.includes(t));
      });
    }

    // Recherche
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter((article) =>
        article.title.toLowerCase().includes(q) ||
        (article.description ?? "").toLowerCase().includes(q)
      );
    }

    setFilteredArticles(filtered);
  }, [articles, dateRange, selectedCategory, selectedSource, selectedTags, searchQuery]);

  const categories = useMemo(
    () => Array.from(new Set(articles.map((a) => a.category).filter(Boolean))),
    [articles]
  );
  const sources = useMemo(
    () => Array.from(new Set(articles.map((a) => a.source).filter(Boolean))),
    [articles]
  );
  const tags = useMemo(
    () => Array.from(new Set(articles.flatMap((a) => a.tags || []))).slice(0, 24),
    [articles]
  );

  const IMAGE_PROXY = import.meta.env.VITE_IMAGE_PROXY_URL || 'https://zhyzjahvhctonjtebsff.functions.supabase.co/image-proxy';

  const proxiedSrc = (url: string | null) => {
    if (!url) return null;
    try {
      return `${IMAGE_PROXY}?url=${encodeURIComponent(url)}`;
    } catch {
      return url;
    }
  };

  if (selectedArticle) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
        <Navigation />
        <main className="max-w-4xl mx-auto px-4 py-8">
          <Button 
            variant="outline" 
            onClick={() => setSelectedArticle(null)}
            className="mb-6"
          >
            ← Retour aux actualités
          </Button>

          <article className="bg-card rounded-xl shadow-lg overflow-hidden">
            {selectedArticle.image_url && (
              <img 
                src={proxiedSrc(selectedArticle.image_url) || selectedArticle.image_url}
                alt={selectedArticle.title}
                className="w-full h-96 object-cover"
                onError={(e) => {
                  const el = e.currentTarget as HTMLImageElement;
                  if (el.src.includes('source.unsplash.com')) return;
                  const fallback = `https://source.unsplash.com/1200x600/?${encodeURIComponent(selectedArticle.source || 'economy')}`;
                  el.src = fallback;
                }}
              />
            )}
            
            <div className="p-8">
              <div className="flex items-center gap-4 mb-4 text-sm text-muted-foreground">
                <Badge variant="secondary">{selectedArticle.source}</Badge>
                {selectedArticle.category && (
                  <Badge>{selectedArticle.category}</Badge>
                )}
                {selectedArticle.published_at && (
                  <div className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {format(new Date(selectedArticle.published_at), "d MMMM yyyy 'à' HH:mm", { locale: fr })}
                  </div>
                )}
              </div>

              <h1 className="text-4xl font-bold mb-6">{selectedArticle.title}</h1>
              
              {selectedArticle.description && (
                <p className="text-xl text-muted-foreground mb-6 font-medium">
                  {selectedArticle.description}
                </p>
              )}

              <div className="prose prose-lg max-w-none prose-headings:scroll-mt-24 prose-p:leading-relaxed prose-a:text-primary hover:prose-a:underline">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {selectedArticle.content || ""}
                </ReactMarkdown>
              </div>

              {selectedArticle.tags && selectedArticle.tags.length > 0 && (
                <div className="mt-8 pt-6 border-t">
                  <div className="flex items-center gap-2 flex-wrap">
                    <Tag className="w-4 h-4 text-muted-foreground" />
                    {selectedArticle.tags.map((tag) => (
                      <Badge
                        key={tag}
                        variant="outline"
                        className="cursor-pointer hover:bg-accent/50"
                        onClick={() => {
                          setSelectedArticle(null);
                          setSearchQuery(tag);
                        }}
                      >
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-8">
                <a 
                  href={selectedArticle.source_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-primary hover:underline"
                >
                  Lire l'article original sur {selectedArticle.source} →
                </a>
              </div>
            </div>
          </article>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Actualités Économiques & Politiques</h1>
          <p className="text-muted-foreground">
            Suivez les dernières nouvelles économiques, financières et politiques du Maroc
          </p>
          <div className="flex flex-wrap gap-2 mt-4">
            <Badge variant="secondary" className="bg-blue-100 text-blue-800">
              <RefreshCw className={`w-3 h-3 mr-1 ${refreshing ? 'animate-spin' : ''}`} />
              {refreshing ? 'Actualisation en cours...' : 'Actualisation automatique'}
            </Badge>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Hespress • Boursenews • Medias24
            </Badge>
            <Badge variant="secondary" className="bg-purple-100 text-purple-800">
              Économie • Politique • Finance
            </Badge>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Affichage stable - Actualisation manuelle
            </Badge>
          </div>
        </div>

        <div className="bg-card rounded-xl shadow-sm p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher des articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Catégorie" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes catégories</SelectItem>
                {categories.map(cat => (
                  <SelectItem key={cat} value={cat!}>{cat}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedSource} onValueChange={setSelectedSource}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Source" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes sources</SelectItem>
                {sources.map(src => (
                  <SelectItem key={src} value={src!}>{src}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={dateRange} onValueChange={(v) => setDateRange(v as DateRange)}>
              <SelectTrigger className="w-full md:w-40">
                <SelectValue placeholder="Période" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes périodes</SelectItem>
                <SelectItem value="24h">Dernières 24h</SelectItem>
                <SelectItem value="7d">7 jours</SelectItem>
                <SelectItem value="30d">30 jours</SelectItem>
              </SelectContent>
            </Select>

            <Button 
              onClick={refreshArticles}
              disabled={refreshing}
              className="bg-gradient-primary"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
              Actualiser maintenant
            </Button>
          </div>
          {/* Tags chips */}
          {tags.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {tags.map((tag) => {
                const isActive = selectedTags.includes(tag);
                return (
                  <Badge
                    key={tag}
                    variant={isActive ? 'default' : 'outline'}
                    className="cursor-pointer select-none"
                    onClick={() => {
                      setSelectedTags((prev) =>
                        prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
                      );
                    }}
                  >
                    {tag}
                  </Badge>
                );
              })}
              {(selectedCategory !== 'all' || selectedSource !== 'all' || dateRange !== 'all' || searchQuery || selectedTags.length > 0) && (
                <Button
                  variant="ghost"
                  className="ml-auto"
                  onClick={() => {
                    setSelectedCategory('all');
                    setSelectedSource('all');
                    setDateRange('all');
                    setSearchQuery('');
                    setSelectedTags([]);
                  }}
                >
                  Effacer filtres
                </Button>
              )}
            </div>
          )}
        </div>

        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <Card key={i}>
                <Skeleton className="h-48 w-full" />
                <CardHeader>
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-full" />
                </CardHeader>
              </Card>
            ))}
          </div>
        ) : filteredArticles.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">Aucun article trouvé</p>
            <p className="text-muted-foreground text-sm mt-2">
              L'auto-update va récupérer des articles automatiquement...
            </p>
          </div>
        ) : (
          <>
          {/* Statistiques rapides */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-500 rounded-lg">
                    <Calendar className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-blue-700 font-medium">Articles trouvés</p>
                    <p className="text-2xl font-bold text-blue-900">{filteredArticles.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-500 rounded-lg">
                    <Tag className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-green-700 font-medium">Sources actives</p>
                    <p className="text-2xl font-bold text-green-900">{sources.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-500 rounded-lg">
                    <Search className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-purple-700 font-medium">Catégories</p>
                    <p className="text-2xl font-bold text-purple-900">{categories.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-gradient-to-r from-orange-50 to-orange-100 border-orange-200">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-500 rounded-lg">
                    <RefreshCw className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-sm text-orange-700 font-medium">Dernière MAJ</p>
                    <p className="text-sm font-bold text-orange-900">
                      {statsLoading ? '...' : (lastUpdated ? format(new Date(lastUpdated), "d MMMM yyyy 'à' HH:mm", { locale: fr }) : '-')}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredArticles.map(article => (
              <Card 
                key={article.id} 
                className="hover:shadow-lg transition-all cursor-pointer group border-l-4 border-l-primary/20"
                onClick={() => setSelectedArticle(article)}
              >
                <div className="overflow-hidden">
                  <img 
                    src={proxiedSrc(article.image_url) || `https://source.unsplash.com/800x450/?economy,market`}
                    alt={article.title}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform"
                    onError={(e) => {
                      const el = e.currentTarget as HTMLImageElement;
                      if (el.src.includes('source.unsplash.com')) return; // avoid loop
                      el.src = `https://source.unsplash.com/800x450/?economy,maroc`;
                    }}
                  />
                </div>
                <CardHeader>
                  <div className="flex items-center gap-2 mb-2">
                    <Badge 
                      variant="secondary" 
                      className={`text-xs ${
                        article.source === 'Hespress' ? 'bg-red-100 text-red-800' :
                        article.source === 'Boursenews' ? 'bg-blue-100 text-blue-800' :
                        article.source === 'Medias24' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {article.source}
                    </Badge>
                    {article.category && (
                      <Badge 
                        className={`text-xs ${
                          article.category === 'Économie' ? 'bg-green-500' :
                          article.category === 'Politique' ? 'bg-blue-500' :
                          article.category === 'Finance' ? 'bg-purple-500' :
                          'bg-gray-500'
                        }`}
                      >
                        {article.category}
                      </Badge>
                    )}
                  </div>
                  <CardTitle className="group-hover:text-primary transition-colors line-clamp-2">
                    {article.title}
                  </CardTitle>
                  <CardDescription className="line-clamp-2">
                    {article.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {article.published_at && (
                    <p className="text-xs text-muted-foreground flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {format(new Date(article.published_at), "d MMMM yyyy", { locale: fr })}
                    </p>
                  )}
                  {article.tags && article.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {article.tags.slice(0, 3).map(tag => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {article.tags.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{article.tags.length - 3}
                        </Badge>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
          {hasMore && (
            <div className="flex justify-center mt-8">
              <Button variant="outline" onClick={loadMore} disabled={loadingMore}>
                {loadingMore ? 'Chargement…' : 'Charger plus'}
              </Button>
            </div>
          )}
          </>
        )}
      </main>
    </div>
  );
}
