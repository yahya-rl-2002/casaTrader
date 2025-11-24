import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { TradingViewTicker } from "@/components/TradingViewTicker";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Bell } from "lucide-react";
import { useSession } from "@/hooks/use-session";
import { Link } from "react-router-dom";

export default function Alerts() {
  const { user } = useSession();

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="border-b">
        <TradingViewTicker showAttribution={false} />
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-10 space-y-3">
          <h1 className="text-3xl lg:text-4xl font-bold text-foreground">Alertes</h1>
          <p className="text-muted-foreground">Recevez des notifications quand un prix seuil est atteint</p>
        </div>

        <Card className="max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="w-5 h-5" />
              Fonctionnalité en préparation
            </CardTitle>
            <CardDescription>
              Créez des alertes sur prix, variation, volume, ou indicateurs techniques.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {!user ? (
              <div className="flex items-center justify-between gap-4">
                <p className="text-sm text-muted-foreground">Connectez-vous pour créer vos alertes personnalisées.</p>
                <Link to="/auth">
                  <Button className="bg-gradient-primary">Se connecter</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">La création d’alertes arrive bientôt.</p>
                <div>
                  <Button variant="outline" disabled>Nouvelle alerte (bientôt)</Button>
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

