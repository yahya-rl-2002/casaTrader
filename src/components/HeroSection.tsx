import { Button } from "@/components/ui/button";
import { FinancialCard } from "@/components/ui/financial-card";
import { TrendingUp, BarChart3, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
export function HeroSection() {
  return <section className="relative bg-gradient-to-br from-primary to-primary/80 text-primary-foreground py-24 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-32 h-32 bg-white rounded-full"></div>
        <div className="absolute top-40 right-20 w-24 h-24 bg-white rounded-full"></div>
        <div className="absolute bottom-20 left-1/4 w-16 h-16 bg-white rounded-full"></div>
        <div className="absolute bottom-40 right-1/3 w-20 h-20 bg-white rounded-full"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                Investissez plus intelligemment avec
                <span className="block text-white/90">CasaTrader</span>
              </h1>
              <p className="text-xl text-primary-foreground/80 leading-relaxed max-w-lg">
                La plateforme de trading nouvelle génération pour la Bourse de Casablanca. 
                Données temps réel, analyses avancées et interface intuitive.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <Link to="/auth">
                <Button size="lg" className="bg-white text-primary hover:bg-white/90 text-lg px-8">
                  Commencer gratuitement
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Button variant="outline-primary" size="lg" className="text-lg px-8 text-neutral-950">
                <BarChart3 className="w-5 h-5" />
                Voir la Démo
              </Button>
            </div>

            <div className="flex items-center gap-8 text-sm text-primary-foreground/70">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-white rounded-full"></div>
                <span>Données temps réel</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-white rounded-full"></div>
                <span>Analyses techniques</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-white rounded-full"></div>
                <span>Alertes intelligentes</span>
              </div>
            </div>
          </div>

          {/* Right Content - Dashboard Preview */}
          <div className="relative">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 shadow-elevation">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-white">Dashboard</h3>
                  <div className="flex gap-2">
                    <div className="w-3 h-3 bg-white/30 rounded-full"></div>
                    <div className="w-3 h-3 bg-white/30 rounded-full"></div>
                    <div className="w-3 h-3 bg-white/30 rounded-full"></div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-white/20 rounded-lg p-4">
                    <div className="flex justify-between items-center">
                      <span className="text-white/80">MASI Index</span>
                      <TrendingUp className="w-4 h-4 text-white" />
                    </div>
                    <div className="mt-2">
                      <span className="text-2xl font-bold text-white">12,847.65</span>
                      <span className="ml-2 text-white/80">+0.35%</span>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white/20 rounded-lg p-4">
                      <span className="text-white/80 text-sm">ATW</span>
                      <div className="mt-1">
                        <span className="text-lg font-bold text-white">445.50</span>
                        <div className="text-success text-sm">+1.90%</div>
                      </div>
                    </div>
                    <div className="bg-white/20 rounded-lg p-4">
                      <span className="text-white/80 text-sm">OCP</span>
                      <div className="mt-1">
                        <span className="text-lg font-bold text-white">5,240</span>
                        <div className="text-bear text-sm">-0.85%</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Floating elements */}
            <div className="absolute -top-4 -right-4 w-8 h-8 bg-success rounded-full opacity-80"></div>
            <div className="absolute -bottom-4 -left-4 w-6 h-6 bg-warning rounded-full opacity-80"></div>
          </div>
        </div>
      </div>
    </section>;
}
