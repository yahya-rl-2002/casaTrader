/**
 * Exemple d'amélioration UX pour la page News
 * Montre comment utiliser tous les nouveaux composants UX
 */
import { useState, useEffect } from "react";
import { ArticleSkeleton, LoadingSpinner } from "@/components/ui/loading-states";
import { InlineError, EmptyState } from "@/components/ui/error-boundary";
import { useNotification } from "@/hooks/use-notification";
import { FadeIn, StaggerContainer, StaggerItem, HoverCard } from "@/components/ui/animations";
import { useDebounce } from "@/components/ui/performance";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { RefreshCw, Search } from "lucide-react";

// Exemple d'utilisation des composants UX
export function NewsPageImproved() {
  const [articles, setArticles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const notification = useNotification();

  // Debounce de la recherche
  const debouncedSearch = useDebounce(searchQuery, 300);

  useEffect(() => {
    fetchArticles();
  }, [debouncedSearch]);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`/api/v1/media/latest?limit=20`);
      if (!response.ok) throw new Error("Erreur de chargement");

      const data = await response.json();
      setArticles(data.articles || []);

      notification.success("Articles chargés avec succès");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Erreur inconnue";
      setError(errorMessage);
      notification.error("Erreur", {
        description: errorMessage,
        action: {
          label: "Réessayer",
          onClick: fetchArticles,
        },
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    notification.info("Actualisation en cours...");
    await fetchArticles();
  };

  // État de chargement
  if (loading && articles.length === 0) {
    return (
      <FadeIn>
        <div className="container mx-auto p-6">
          <ArticleSkeleton count={5} />
        </div>
      </FadeIn>
    );
  }

  // État d'erreur
  if (error && articles.length === 0) {
    return (
      <div className="container mx-auto p-6">
        <InlineError message={error} onRetry={fetchArticles} />
      </div>
    );
  }

  // État vide
  if (articles.length === 0) {
    return (
      <div className="container mx-auto p-6">
        <EmptyState
          title="Aucun article trouvé"
          description="Essayez de modifier vos critères de recherche"
          action={
            <Button onClick={handleRefresh}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Actualiser
            </Button>
          }
        />
      </div>
    );
  }

  // Contenu avec animations
  return (
    <FadeIn>
      <div className="container mx-auto p-6 space-y-6">
        {/* Barre de recherche avec debounce */}
        <Card>
          <CardHeader>
            <CardTitle>Rechercher des articles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Rechercher..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button onClick={handleRefresh} disabled={loading}>
                <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Liste d'articles avec animations staggerées */}
        <StaggerContainer>
          <div className="grid gap-4">
            {articles.map((article) => (
              <StaggerItem key={article.id}>
                <HoverCard>
                  <Card className="transition-shadow hover:shadow-lg">
                    <CardHeader>
                      <CardTitle>{article.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground">{article.summary}</p>
                    </CardContent>
                  </Card>
                </HoverCard>
              </StaggerItem>
            ))}
          </div>
        </StaggerContainer>

        {/* Indicateur de chargement pour le refresh */}
        {loading && articles.length > 0 && (
          <div className="flex justify-center">
            <LoadingSpinner />
          </div>
        )}
      </div>
    </FadeIn>
  );
}



