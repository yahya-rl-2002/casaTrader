import { FinancialCard } from "@/components/ui/financial-card";
import { Star } from "lucide-react";

const testimonials = [
  {
    name: "Ahmed Benali",
    role: "Investisseur particulier",
    company: "Casablanca",
    content: "CasaTrader a révolutionné ma façon d'investir. Les analyses en temps réel m'ont permis d'optimiser mes performances de 30%.",
    rating: 5,
    avatar: "AB"
  },
  {
    name: "Fatima El Alami", 
    role: "Gestionnaire de portefeuille",
    company: "Rabat Capital",
    content: "Interface intuitive et données fiables. Mes clients apprécient la transparence et la rapidité des informations fournies.",
    rating: 5,
    avatar: "FE"
  },
  {
    name: "Youssef Radi",
    role: "Analyste financier", 
    company: "Maroc Invest",
    content: "Les outils d'analyse technique sont exceptionnels. Je recommande CasaTrader à tous mes collègues du secteur financier.",
    rating: 5,
    avatar: "YR"
  }
];

export function TestimonialsSection() {
  return (
    <section className="py-24 bg-gradient-to-br from-primary/5 to-accent/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-foreground">
            Ce que disent nos
            <span className="text-transparent bg-clip-text bg-gradient-primary"> clients</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Rejoignez des milliers d'investisseurs qui font confiance à CasaTrader 
            pour leurs décisions financières
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <FinancialCard key={index} title="">
              <div className="space-y-6">
                {/* Rating */}
                <div className="flex items-center gap-1">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-warning text-warning" />
                  ))}
                </div>

                {/* Content */}
                <blockquote className="text-foreground leading-relaxed">
                  "{testimonial.content}"
                </blockquote>

                {/* Author */}
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gradient-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="font-semibold text-foreground">{testimonial.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {testimonial.role} • {testimonial.company}
                    </div>
                  </div>
                </div>
              </div>
            </FinancialCard>
          ))}
        </div>
      </div>
    </section>
  );
}