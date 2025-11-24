import { TrendingUp, Mail, Phone, MapPin } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

export function Footer() {
  return (
    <footer className="bg-background border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-primary-foreground" />
              </div>
              <h3 className="text-xl font-bold text-foreground">CasaTrader</h3>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              La plateforme de trading nouvelle génération pour la Bourse de Casablanca.
            </p>
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Mail className="w-4 h-4" />
                <span>contact@casatrader.ma</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Phone className="w-4 h-4" />
                <span>+212 5 22 00 00 00</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <MapPin className="w-4 h-4" />
                <span>Casablanca, Maroc</span>
              </div>
            </div>
          </div>

          {/* Product */}
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Produit</h4>
            <div className="space-y-2">
              {["Fonctionnalités", "Tarifs", "API", "Sécurité", "Mises à jour"].map((item) => (
                <div key={item}>
                  <Button variant="ghost" className="p-0 h-auto text-muted-foreground hover:text-foreground">
                    {item}
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* Ressources */}
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Ressources</h4>
            <div className="space-y-2">
              {["Documentation", "Guides", "Blog", "Support", "Communauté"].map((item) => (
                <div key={item}>
                  <Button variant="ghost" className="p-0 h-auto text-muted-foreground hover:text-foreground">
                    {item}
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* Entreprise */}
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Entreprise</h4>
            <div className="space-y-2">
              {["À propos", "Carrières", "Presse", "Partenaires", "Contact"].map((item) => (
                <div key={item}>
                  <Button variant="ghost" className="p-0 h-auto text-muted-foreground hover:text-foreground">
                    {item}
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>

        <Separator className="my-8" />

        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="text-sm text-muted-foreground">
            © 2024 CasaTrader. Tous droits réservés.
          </div>
          <div className="flex gap-6 text-sm">
            <Button variant="ghost" className="p-0 h-auto text-muted-foreground hover:text-foreground">
              Mentions légales
            </Button>
            <Button variant="ghost" className="p-0 h-auto text-muted-foreground hover:text-foreground">
              Confidentialité
            </Button>
            <Button variant="ghost" className="p-0 h-auto text-muted-foreground hover:text-foreground">
              Cookies
            </Button>
          </div>
        </div>
      </div>
    </footer>
  );
}