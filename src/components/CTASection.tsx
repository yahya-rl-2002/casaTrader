import { Button } from "@/components/ui/button";
import { TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";

const partners = [
  { name: "Attijariwafa Bank", logo: "ATW" },
  { name: "Bank of Africa", logo: "BOA" }, 
  { name: "BMCE Bank", logo: "BMCE" },
  { name: "CIH Bank", logo: "CIH" },
  { name: "Société Générale", logo: "SG" },
  { name: "Crédit du Maroc", logo: "CDM" }
];

export function PartnersSection() {
  return (
    <section className="py-16 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-8">
          <h3 className="text-lg font-medium text-muted-foreground">
            Partenaires de confiance
          </h3>
          
          <div className="grid grid-cols-3 md:grid-cols-6 gap-8 items-center">
            {partners.map((partner, index) => (
              <div key={index} className="flex items-center justify-center">
                <div className="w-16 h-16 bg-gradient-card rounded-lg flex items-center justify-center shadow-card">
                  <span className="text-sm font-bold text-foreground">{partner.logo}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export function CTASection() {
  return (
    <section className="py-24 bg-gradient-to-br from-primary to-primary/80 text-primary-foreground relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-20 w-32 h-32 bg-white rounded-full"></div>
        <div className="absolute bottom-20 right-10 w-24 h-24 bg-white rounded-full"></div>
        <div className="absolute top-1/2 left-10 w-16 h-16 bg-white rounded-full"></div>
        <div className="absolute bottom-1/3 right-1/4 w-20 h-20 bg-white rounded-full"></div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <div className="space-y-8">
          <h2 className="text-4xl lg:text-6xl font-bold leading-tight">
            Prêt à transformer votre
            <span className="block text-white/90">façon d'investir ?</span>
          </h2>
          
          <p className="text-xl text-primary-foreground/80 max-w-2xl mx-auto leading-relaxed">
            Rejoignez des milliers d'investisseurs qui utilisent déjà CasaTrader 
            pour optimiser leurs performances sur la Bourse de Casablanca.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/auth">
              <Button size="lg" className="bg-white text-primary hover:bg-white/90 text-lg px-8">
                <TrendingUp className="w-5 h-5 mr-2" />
                Commencer maintenant
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="border-white text-white hover:bg-white/10 text-lg px-8">
              Planifier une démo
            </Button>
          </div>

          <div className="text-sm text-primary-foreground/70">
            Essai gratuit • Sans engagement • Support 7j/7
          </div>
        </div>
      </div>
    </section>
  );
}
