import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { TradingViewTicker } from "@/components/TradingViewTicker";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useSession } from "@/hooks/use-session";
import { Link } from "react-router-dom";
import { TrendingUp } from "lucide-react";

export default function Portfolio() {
  const { user } = useSession();

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="border-b">
        <TradingViewTicker showAttribution={false} />
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-10 space-y-3">
          <h1 className="text-3xl lg:text-4xl font-bold text-foreground">Votre portefeuille</h1>
          <p className="text-muted-foreground">Suivez la valeur de vos positions et vos performances</p>
        </div>

        <Card className="max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Bientôt disponible
            </CardTitle>
            <CardDescription>
              La gestion de portefeuille arrive très vite: positions, PRU, plus/moins-values, allocation et rapports.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {!user ? (
              <div className="flex items-center justify-between gap-4">
                <p className="text-sm text-muted-foreground">Connectez-vous pour préparer votre portefeuille.</p>
                <Link to="/auth">
                  <Button className="bg-gradient-primary">Se connecter</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">
                  Vous serez bientôt en mesure d’ajouter vos titres, quantités et prix de revient.
                </p>
                <div>
                  <Button variant="outline" disabled>Ajouter une position (bientôt)</Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </main>

      <Footer />
    </div>
  );
}

