import { Navigation } from "@/components/Navigation";
import { MarketOverview } from "@/components/MarketOverview";
import { Footer } from "@/components/Footer";
import { TradingViewTicker } from "@/components/TradingViewTicker";
import { SymbolOverview } from "@/components/tradingview/SymbolOverview";
import { Hotlists } from "@/components/tradingview/Hotlists";
import { StockHeatmap } from "@/components/tradingview/StockHeatmap";
import { Screener } from "@/components/tradingview/Screener";
import { SymbolProfile } from "@/components/tradingview/SymbolProfile";
import { AdvancedChart } from "@/components/tradingview/AdvancedChart";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useMemo, useState } from "react";
import { CASEMA_SYMBOLS } from "@/data/casema-symbols";

const Market = () => {
  const symbols = useMemo(() => CASEMA_SYMBOLS, []);

  const [symbol, setSymbol] = useState<string>(symbols[0].value);

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="border-b">
        <TradingViewTicker showAttribution={false} />
      </div>
      
      <main className="relative pt-20">
        {/* Header */}
        <section className="py-16 bg-gradient-subtle">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center space-y-6">
              <h1 className="text-4xl lg:text-6xl font-bold text-foreground">
                Marché 
                <span className="text-transparent bg-clip-text bg-gradient-primary"> Boursier</span>
              </h1>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Suivez en temps réel toutes les actions, indices et performances de la Bourse de Casablanca
              </p>
            </div>
          </div>
        </section>

        {/* Sélecteur & blocs TradingView */}
        <section className="py-6 bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-end mb-4">
              <div className="w-72">
                <Select value={symbol} onValueChange={setSymbol}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choisir un symbole" />
                  </SelectTrigger>
                  <SelectContent>
                    {symbols.map((s) => (
                      <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle className="text-lg">Graphique avancé – {symbol}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-[520px]">
                    <AdvancedChart symbol={symbol} />
                  </div>
                </CardContent>
              </Card>
              <Card className="lg:col-span-1">
                <CardHeader>
                  <CardTitle className="text-lg">Hotlists Casablanca</CardTitle>
                </CardHeader>
                <CardContent>
                  <Hotlists />
                </CardContent>
              </Card>
            </div>

            <div className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Heatmap</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-[520px]">
                    <StockHeatmap theme="light" />
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="mt-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Screener</CardTitle>
                </CardHeader>
                <CardContent>
                  <Screener />
                  {/* Profil Entreprise avec sélecteur local */}
                  <div className="mt-8">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-sm font-medium text-muted-foreground">Profil entreprise</h3>
                      <div className="w-64">
                        <Select value={symbol} onValueChange={setSymbol}>
                          <SelectTrigger>
                            <SelectValue placeholder="Choisir une entreprise" />
                          </SelectTrigger>
                          <SelectContent>
                            {symbols.map((s) => (
                              <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    <div className="h-[360px]">
                      <SymbolProfile symbol={symbol} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="mt-10">
              <MarketOverview />
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Market;
