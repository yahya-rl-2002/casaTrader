import { Button } from "@/components/ui/button";
import { FinancialCard } from "@/components/ui/financial-card";
import { Check, ArrowRight } from "lucide-react";

const plans = [
  {
    name: "Essentiel",
    price: "Gratuit",
    description: "Parfait pour commencer",
    features: [
      "Données de marché en différé",
      "Graphiques de base", 
      "5 alertes par mois",
      "Support communautaire"
    ],
    popular: false,
    cta: "Commencer gratuitement"
  },
  {
    name: "Professionnel", 
    price: "299 MAD",
    period: "/mois",
    description: "Pour les investisseurs actifs",
    features: [
      "Données temps réel",
      "Analyses techniques avancées",
      "Alertes illimitées",
      "Support prioritaire",
      "API d'intégration",
      "Rapports personnalisés"
    ],
    popular: true,
    cta: "Essai gratuit 14 jours"
  },
  {
    name: "Entreprise",
    price: "Sur mesure", 
    description: "Pour les institutions",
    features: [
      "Tout du plan Pro",
      "Données historiques complètes",
      "Intégration personnalisée",
      "Support dédié 24/7",
      "Formation équipe",
      "SLA garanti"
    ],
    popular: false,
    cta: "Nous contacter"
  }
];

export function PricingSection() {
  return (
    <section className="py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-foreground">
            Choisissez votre
            <span className="text-transparent bg-clip-text bg-gradient-primary"> plan</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Des tarifs transparents adaptés à tous les profils d'investisseurs, 
            du débutant à l'institution financière
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <div key={index} className="relative">
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                  <span className="bg-gradient-primary text-primary-foreground px-4 py-2 rounded-full text-sm font-medium">
                    Plus populaire
                  </span>
                </div>
              )}
              
              <FinancialCard 
                title="" 
                className={`h-full ${plan.popular ? 'ring-2 ring-primary shadow-elevation' : ''}`}
              >
                <div className="space-y-6">
                  {/* Plan Header */}
                  <div className="text-center space-y-2">
                    <h3 className="text-2xl font-bold text-foreground">{plan.name}</h3>
                    <p className="text-muted-foreground">{plan.description}</p>
                    <div className="space-y-1">
                      <div className="text-4xl font-bold text-foreground">
                        {plan.price}
                        {plan.period && <span className="text-lg text-muted-foreground">{plan.period}</span>}
                      </div>
                    </div>
                  </div>

                  {/* Features */}
                  <div className="space-y-3">
                    {plan.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center gap-3">
                        <Check className="w-5 h-5 text-success flex-shrink-0" />
                        <span className="text-foreground">{feature}</span>
                      </div>
                    ))}
                  </div>

                  {/* CTA */}
                  <Button 
                    className={`w-full ${plan.popular ? 'bg-gradient-primary' : ''}`}
                    variant={plan.popular ? 'default' : 'outline'}
                  >
                    {plan.cta}
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              </FinancialCard>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16 space-y-4">
          <p className="text-muted-foreground">
            Besoin d'aide pour choisir ? Notre équipe est là pour vous conseiller.
          </p>
          <Button variant="outline">
            Parler à un expert
          </Button>
        </div>
      </div>
    </section>
  );
}