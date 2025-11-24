import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';

// Utilise le même port que le frontend grâce au proxy Vite
const API_BASE_URL = '/api/v1';

interface IndexData {
  score: number;
  label: string;
  as_of: string;
}

export default function FearGreedIndex() {
  const [index, setIndex] = useState<IndexData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchScore() {
      try {
        const response = await fetch(`${API_BASE_URL}/index/latest`);
        if (!response.ok) throw new Error('API non disponible');
        const data = await response.json();
        setIndex(data);
        setError(null);
      } catch (err) {
        setError('Impossible de récupérer les données');
        console.error('Failed to fetch score:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchScore();
    const interval = setInterval(fetchScore, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const getColor = (score: number) => {
    if (score >= 70) return 'from-green-500 to-green-600';
    if (score >= 55) return 'from-lime-500 to-lime-600';
    if (score >= 45) return 'from-amber-400 to-amber-500';
    if (score >= 30) return 'from-orange-500 to-orange-600';
    return 'from-red-500 to-red-600';
  };

  const getLabel = (score: number) => {
    if (score >= 70) return 'EXTREME GREED';
    if (score >= 55) return 'GREED';
    if (score >= 45) return 'NEUTRAL';
    if (score >= 30) return 'FEAR';
    return 'EXTREME FEAR';
  };

  const getIcon = (score: number) => {
    if (score >= 55) return <TrendingUp className="w-16 h-16" />;
    if (score >= 45) return <Activity className="w-16 h-16" />;
    return <TrendingDown className="w-16 h-16" />;
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error || !index) {
    return (
      <div className="container mx-auto p-6">
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-6 text-center">
            <p className="text-red-600">⚠️ {error || 'Données indisponibles'}</p>
            <p className="text-sm text-gray-600 mt-2">
              Assurez-vous que le backend est démarré sur le port 8001
            </p>
            <Button 
              onClick={() => window.location.reload()} 
              className="mt-4"
              variant="outline"
            >
              Réessayer
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-4xl font-bold">Fear & Greed Index</h1>
        <p className="text-gray-600 mt-2">Indice de sentiment du marché - Bourse de Casablanca</p>
      </div>

      {/* Carte cliquable principale */}
      <Card 
        className="cursor-pointer transition-all duration-300 hover:shadow-2xl hover:scale-[1.02] border-2"
        onClick={() => navigate('/fear-greed-dashboard')}
      >
        <CardHeader>
          <CardTitle className="text-2xl">Sentiment du Marché</CardTitle>
          <CardDescription>Cliquez pour voir le dashboard complet</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            {/* Score principal */}
            <div className="flex-1">
              <div className={`text-8xl font-bold bg-gradient-to-r ${getColor(index.score)} bg-clip-text text-transparent`}>
                {index.score.toFixed(2)}
              </div>
              <div className="text-3xl font-semibold mt-4 text-gray-700">
                {getLabel(index.score)}
              </div>
              <div className="text-sm text-gray-500 mt-2">
                Mis à jour : {new Date(index.as_of).toLocaleString('fr-FR')}
              </div>
            </div>

            {/* Icône */}
            <div className={`bg-gradient-to-r ${getColor(index.score)} p-6 rounded-full text-white`}>
              {getIcon(index.score)}
            </div>
          </div>

          {/* Barre gradient */}
          <div className="mt-8 relative w-full h-20 rounded-xl overflow-hidden shadow-lg"
               style={{
                 background: 'linear-gradient(to right, #ef4444 0%, #f97316 25%, #fbbf24 50%, #84cc16 75%, #10b981 100%)'
               }}>
            <div className="absolute inset-0 flex justify-between items-center px-6 text-sm font-bold text-white drop-shadow-lg">
              <span>FEAR</span>
              <span>NEUTRAL</span>
              <span>GREED</span>
            </div>
            {/* Indicateur de position */}
            <div 
              className="absolute top-0 bottom-0 w-1 bg-white shadow-2xl transition-all duration-500"
              style={{ left: `${index.score}%` }}
            >
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-6 h-6 bg-white rounded-full shadow-xl border-4 border-gray-900"></div>
              <div className="absolute -bottom-3 left-1/2 -translate-x-1/2 w-6 h-6 bg-white rounded-full shadow-xl border-4 border-gray-900"></div>
            </div>
          </div>

          {/* Valeurs de référence */}
          <div className="flex justify-between mt-3 text-xs text-gray-500 px-2">
            <span>0</span>
            <span>25</span>
            <span>50</span>
            <span>75</span>
            <span>100</span>
          </div>

          {/* Call to action */}
          <div className="mt-6 text-center">
            <Button 
              size="lg" 
              className="w-full"
              onClick={(e) => {
                e.stopPropagation();
                navigate('/fear-greed-dashboard');
              }}
            >
              📊 Voir le Dashboard Complet →
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Informations supplémentaires */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Qu'est-ce que c'est ?</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-700">
              L'indice Fear & Greed mesure le sentiment des investisseurs sur la Bourse de Casablanca.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Comment l'utiliser ?</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-700">
              Un score élevé indique de la cupidité (moment de vendre), un score bas indique de la peur (moment d'acheter).
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Fréquence de mise à jour</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-700">
              Actualisé automatiquement toutes les 10 minutes avec les dernières données du marché.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

