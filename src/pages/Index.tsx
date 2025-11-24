import { Navigation } from "@/components/Navigation";
import { HeroSection } from "@/components/HeroSection";
import { TradingViewTicker } from "@/components/TradingViewTicker";
import { MarketOverviewSimple } from "@/components/MarketOverviewSimple";
import { FeaturesSection } from "@/components/FeaturesSection";
import { TestimonialsSection } from "@/components/TestimonialsSection";
import { PricingSection } from "@/components/PricingSection";
import { PartnersSection, CTASection } from "@/components/CTASection";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="border-b">
        <TradingViewTicker showAttribution={false} />
      </div>
      <HeroSection />
      
      <main className="relative">
        {/* Market Overview Section */}
        <section className="py-16 bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center space-y-4 mb-12">
              <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
                Vue d'ensemble du
                <span className="text-transparent bg-clip-text bg-gradient-primary"> marché</span>
              </h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                Suivez les principales valeurs et indices de la Bourse de Casablanca en temps réel
              </p>
            </div>
            <MarketOverviewSimple />
          </div>
        </section>

        <FeaturesSection />
        <TestimonialsSection />
        <PricingSection />
        <PartnersSection />
        <CTASection />
      </main>
      
      <Footer />
    </div>
  );
};

export default Index;
