import { FinancialCard } from "@/components/ui/financial-card";
import { StockTicker } from "@/components/ui/stock-ticker";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";

const allStocksData = [
  // Banques
  { symbol: "ATW", name: "Attijariwafa Bank", price: 445.50, change: 8.30, changePercent: 1.90, sector: "Banques" },
  { symbol: "BCP", name: "Banque Populaire", price: 285.75, change: -3.25, changePercent: -1.12, sector: "Banques" },
  { symbol: "BMCE", name: "BMCE Bank", price: 825.00, change: 12.50, changePercent: 1.54, sector: "Banques" },
  { symbol: "CIH", name: "CIH Bank", price: 315.40, change: 4.80, changePercent: 1.55, sector: "Banques" },
  { symbol: "CDM", name: "Crédit du Maroc", price: 685.50, change: -2.10, changePercent: -0.31, sector: "Banques" },
  
  // Télécommunications
  { symbol: "IAM", name: "Maroc Telecom", price: 145.20, change: 2.15, changePercent: 1.50, sector: "Télécoms" },
  
  // Mines et Chimie
  { symbol: "OCP", name: "OCP Group", price: 5240.00, change: -45.00, changePercent: -0.85, sector: "Mines" },
  { symbol: "CMT", name: "Ciments du Maroc", price: 1850.00, change: 15.75, changePercent: 0.86, sector: "Matériaux" },
  { symbol: "HOL", name: "Holcim Maroc", price: 1240.50, change: -8.25, changePercent: -0.66, sector: "Matériaux" },
  { symbol: "LHM", name: "LafargeHolcim Maroc", price: 1680.75, change: 22.40, changePercent: 1.35, sector: "Matériaux" },
  
  // Énergie et Utilities
  { symbol: "SID", name: "Lydec", price: 425.80, change: 3.90, changePercent: 0.93, sector: "Utilities" },
  { symbol: "RED", name: "Redal", price: 285.40, change: -1.60, changePercent: -0.56, sector: "Utilities" },
  { symbol: "TQM", name: "Taqa Morocco", price: 865.25, change: 7.85, changePercent: 0.92, sector: "Énergie" },
  
  // Assurances
  { symbol: "WAA", name: "Wafa Assurance", price: 4250.00, change: 35.50, changePercent: 0.84, sector: "Assurances" },
  { symbol: "SAH", name: "Saham Assurance", price: 1450.75, change: -12.25, changePercent: -0.84, sector: "Assurances" },
  
  // Agroalimentaire
  { symbol: "LES", name: "Lesieur Cristal", price: 125.60, change: 1.85, changePercent: 1.49, sector: "Agroalimentaire" },
  { symbol: "COB", name: "Cosumar", price: 185.90, change: -2.40, changePercent: -1.27, sector: "Agroalimentaire" },
  { symbol: "CSR", name: "Centrale Laitière", price: 2150.40, change: 18.60, changePercent: 0.87, sector: "Agroalimentaire" },
  
  // Immobilier
  { symbol: "CGI", name: "CGI", price: 315.25, change: 4.15, changePercent: 1.33, sector: "Immobilier" },
  { symbol: "ADI", name: "Addoha", price: 8.45, change: -0.15, changePercent: -1.74, sector: "Immobilier" },
  { symbol: "ALM", name: "Alliances", price: 285.70, change: 6.30, changePercent: 2.25, sector: "Immobilier" },
  
  // Distribution
  { symbol: "LBV", name: "Label Vie", price: 2850.50, change: 22.75, changePercent: 0.81, sector: "Distribution" },
  { symbol: "MAR", name: "Marjane", price: 1150.80, change: -8.40, changePercent: -0.72, sector: "Distribution" },
  
  // Transport et Logistique
  { symbol: "RAM", name: "Royal Air Maroc", price: 42.85, change: 0.95, changePercent: 2.27, sector: "Transport" },
  { symbol: "CTM", name: "CTM", price: 685.40, change: -3.60, changePercent: -0.52, sector: "Transport" },
  
  // Textile
  { symbol: "SOT", name: "Sotherma", price: 1240.60, change: 15.40, changePercent: 1.26, sector: "Textile" },
  
  // Technologie
  { symbol: "HPS", name: "HPS", price: 4850.25, change: 48.75, changePercent: 1.02, sector: "Technologie" },
  { symbol: "IB", name: "Involys", price: 125.80, change: 2.30, changePercent: 1.86, sector: "Technologie" },
  
  // Pharmacie
  { symbol: "PRO", name: "Promopharm", price: 850.40, change: 12.60, changePercent: 1.50, sector: "Pharmacie" },
  { symbol: "SOT", name: "Sothema", price: 1685.75, change: -15.25, changePercent: -0.90, sector: "Pharmacie" },
];

const indexData = [
  { name: "MASI", value: 12847.65, change: 45.23, changePercent: 0.35 },
  { name: "MADEX", value: 10421.88, change: -12.45, changePercent: -0.12 },
  { name: "MSI20", value: 1045.32, change: 8.97, changePercent: 0.87 },
];

export function MarketOverview() {
  const sectors = [...new Set(allStocksData.map(stock => stock.sector))];
  const topPerformers = allStocksData.filter(stock => stock.changePercent > 1).slice(0, 6);
  const topLosers = allStocksData.filter(stock => stock.changePercent < -0.5).slice(0, 6);

  return (
    <div className="space-y-8">
      {/* Market Indices */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {indexData.map((index) => (
          <FinancialCard 
            key={index.name}
            title={index.name}
            trend={index.change > 0 ? "up" : index.change < 0 ? "down" : "neutral"}
            className="bg-gradient-card hover:shadow-elevation transition-all duration-500"
          >
            <div className="space-y-3">
              <div className="text-3xl font-bold text-foreground">
                {index.value.toLocaleString('fr-FR', { minimumFractionDigits: 2 })}
              </div>
              <div className={`flex items-center gap-2 text-sm font-medium ${
                index.change > 0 ? "text-bull" : index.change < 0 ? "text-bear" : "text-muted-foreground"
              }`}>
                {index.change > 0 ? (
                  <TrendingUp className="w-5 h-5" />
                ) : index.change < 0 ? (
                  <TrendingDown className="w-5 h-5" />
                ) : (
                  <Activity className="w-5 h-5" />
                )}
                <span className="text-base">
                  {index.change > 0 ? '+' : ''}{index.change.toFixed(2)} 
                  ({index.changePercent > 0 ? '+' : ''}{index.changePercent.toFixed(2)}%)
                </span>
              </div>
            </div>
          </FinancialCard>
        ))}
      </div>

      {/* Top Performers & Losers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FinancialCard 
          title="🚀 Top Performers" 
          className="bg-gradient-to-br from-success/5 to-bull/5 border-success/20"
        >
          <div className="space-y-3">
            {topPerformers.map((stock) => (
              <StockTicker
                key={stock.symbol}
                symbol={stock.symbol}
                name={stock.name}
                price={stock.price}
                change={stock.change}
                changePercent={stock.changePercent}
                className="bg-background/60 backdrop-blur-sm"
              />
            ))}
          </div>
        </FinancialCard>

        <FinancialCard 
          title="📉 Plus grandes baisses" 
          className="bg-gradient-to-br from-destructive/5 to-bear/5 border-destructive/20"
        >
          <div className="space-y-3">
            {topLosers.map((stock) => (
              <StockTicker
                key={stock.symbol}
                symbol={stock.symbol}
                name={stock.name}
                price={stock.price}
                change={stock.change}
                changePercent={stock.changePercent}
                className="bg-background/60 backdrop-blur-sm"
              />
            ))}
          </div>
        </FinancialCard>
      </div>

      {/* All Stocks by Sector */}
      <div className="space-y-8">
        <h3 className="text-2xl font-bold text-foreground text-center">
          Toutes les actions par 
          <span className="text-transparent bg-clip-text bg-gradient-primary"> secteur</span>
        </h3>
        
        {sectors.map((sector) => {
          const sectorStocks = allStocksData.filter(stock => stock.sector === sector);
          return (
            <FinancialCard 
              key={sector}
              title={`📊 ${sector}`}
              className="bg-gradient-subtle"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {sectorStocks.map((stock) => (
                  <div 
                    key={stock.symbol}
                    className="p-4 rounded-lg bg-background/50 backdrop-blur-sm border border-border/50 hover:shadow-card transition-all duration-300"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-semibold text-foreground">{stock.symbol}</div>
                        <div className="text-sm text-muted-foreground truncate">{stock.name}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-foreground">
                          {stock.price.toLocaleString('fr-FR', { minimumFractionDigits: 2 })} MAD
                        </div>
                        <div className={`text-sm font-medium ${
                          stock.changePercent > 0 ? "text-bull" : stock.changePercent < 0 ? "text-bear" : "text-muted-foreground"
                        }`}>
                          {stock.changePercent > 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </FinancialCard>
          );
        })}
      </div>
    </div>
  );
}