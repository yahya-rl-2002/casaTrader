import { Navigation } from "@/components/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { Link } from "react-router-dom";

export default function Pricing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
      <Navigation />
      <main className="max-w-6xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">Tarifs</h1>
        <p className="text-muted-foreground mb-8">Choisissez le plan qui vous convient</p>
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Gratuit</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-3xl font-bold">0 DH<span className="text-sm text-muted-foreground">/mois</span></p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Accès landing + support</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Inscription / Connexion</li>
              </ul>
              <Link to="/auth"><Button className="w-full bg-gradient-primary">Commencer</Button></Link>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Essentiel</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-3xl font-bold">99 DH<span className="text-sm text-muted-foreground">/mois</span></p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Marché + Actualités</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Alertes basiques</li>
              </ul>
              <Link to="/auth"><Button className="w-full">S'abonner</Button></Link>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Pro</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-3xl font-bold">199 DH<span className="text-sm text-muted-foreground">/mois</span></p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Toutes fonctionnalités</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-500" /> Priorité support</li>
              </ul>
              <Link to="/auth"><Button className="w-full">S'abonner</Button></Link>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}

