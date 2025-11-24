import { Navigation } from "@/components/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Support() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
      <Navigation />
      <main className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">Support & Aide</h1>
        <p className="text-muted-foreground mb-8">FAQ, contact et assistance</p>

        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle>FAQ rapide</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p><strong>Comment créer un compte ?</strong> Via la page Connexion puis S'inscrire.</p>
              <p><strong>Accès aux fonctionnalités ?</strong> Connectez-vous pour accéder au Marché, Actualités, Alertes…</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Nous contacter</CardTitle>
            </CardHeader>
            <CardContent className="flex gap-2">
              <Input placeholder="Votre email" />
              <Button>Envoyer</Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}

