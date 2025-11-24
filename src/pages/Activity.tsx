import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Activity() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h1 className="text-3xl font-bold mb-6">Historique des activités</h1>
        <Card>
          <CardHeader>
            <CardTitle>À venir</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Cette page affichera vos actions récentes (connexions, mises à jour de profil, etc.).
            </p>
          </CardContent>
        </Card>
      </main>
      <Footer />
    </div>
  );
}

