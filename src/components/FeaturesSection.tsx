import { FinancialCard } from "@/components/ui/financial-card";
import { Button } from "@/components/ui/button";
import { TrendingUp, Shield, Zap, BarChart3, Bell, Users } from "lucide-react";

const features = [
  {
    icon: TrendingUp,
    title: "Analyses en temps réel",
    description: "Suivez les mouvements du marché avec des données actualisées à la seconde",
    color: "text-bull"
  },
  {
    icon: Shield,
    title: "Sécurité maximale", 
    description: "Vos données et investissements protégés par une sécurité de niveau bancaire",
    color: "text-primary"
  },
  {
    icon: Zap,
    title: "Exécution rapide",
    description: "Passez vos ordres instantanément avec notre technologie ultra-rapide",
    color: "text-warning"
  },
  {
    icon: BarChart3,
    title: "Outils d'analyse",
    description: "Graphiques avancés et indicateurs techniques pour optimiser vos décisions",
    color: "text-success"
  },
  {
    icon: Bell,
    title: "Alertes intelligentes",
    description: "Notifications personnalisées basées sur vos critères d'investissement",
    color: "text-destructive"
  },
  {
    icon: Users,
    title: "Communauté active",
    description: "Échangez avec d'autres investisseurs et apprenez des experts",
    color: "text-accent-foreground"
  }
];

export function FeaturesSection() {
  return (
    <section className="py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-foreground">
            Fonctionnalités
            <span className="text-transparent bg-clip-text bg-gradient-primary"> puissantes</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Découvrez les outils qui font de CasaTrader la plateforme de choix 
            des investisseurs marocains modernes
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <FinancialCard key={index} title="">
              <div className="space-y-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-card flex items-center justify-center ${feature.color}`}>
                  <feature.icon className="w-6 h-6" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-foreground">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                </div>
              </div>
            </FinancialCard>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center">
          <Button size="lg" className="bg-gradient-primary text-lg px-8">
            Découvrir toutes les fonctionnalités
          </Button>
        </div>
      </div>

      {/* Decorative elements */}
      <div className="absolute left-10 top-1/2 w-4 h-4 bg-bull rounded-full opacity-30"></div>
      <div className="absolute right-20 top-1/4 w-6 h-6 bg-warning rounded-full opacity-30"></div>
      <div className="absolute left-1/3 bottom-20 w-3 h-3 bg-primary rounded-full opacity-30"></div>
    </section>
  );
}