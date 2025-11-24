import { Navigation } from "@/components/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
      <Navigation />
      <main className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">À propos</h1>
        <p className="text-muted-foreground mb-8">CasaTrader — Bourse de Casablanca</p>

        <Card>
          <CardHeader>
            <CardTitle>Notre mission</CardTitle>
          </CardHeader>
          <CardContent className="text-sm">
            Offrir une plateforme claire et efficace pour suivre le marché marocain, les actualités financières et gérer vos alertes.
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

