import { FinancialCard } from "@/components/ui/financial-card";
import { StockTicker } from "@/components/ui/stock-ticker";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const topStocks = [
  { symbol: "ATW", name: "Attijariwafa Bank", price: 445.50, change: 8.30, changePercent: 1.90 },
  { symbol: "OCP", name: "OCP Group", price: 5240.00, change: -45.00, changePercent: -0.85 },
  { symbol: "IAM", name: "Maroc Telecom", price: 145.20, change: 2.15, changePercent: 1.50 },
  { symbol: "BCP", name: "Banque Populaire", price: 285.75, change: -3.25, changePercent: -1.12 },
  { symbol: "BMCE", name: "BMCE Bank", price: 825.00, change: 12.50, changePercent: 1.54 },
  { symbol: "CIH", name: "CIH Bank", price: 315.40, change: 4.80, changePercent: 1.55 },
];

const indexData = [
  { name: "MASI", value: 12847.65, change: 45.23, changePercent: 0.35 },
  { name: "MADEX", value: 10421.88, change: -12.45, changePercent: -0.12 },
  { name: "MSI20", value: 1045.32, change: 8.97, changePercent: 0.87 },
];

export function MarketOverviewSimple() {
  return (
    <div className="space-y-6">
      {/* Market Indices */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {indexData.map((index) => (
          <FinancialCard 
            key={index.name}
            title={index.name}
            trend={index.change > 0 ? "up" : index.change < 0 ? "down" : "neutral"}
          >
            <div className="space-y-2">
              <div className="text-2xl font-bold text-foreground">
                {index.value.toLocaleString('fr-FR', { minimumFractionDigits: 2 })}
              </div>
              <div className={`flex items-center gap-1 text-sm font-medium ${
                index.change > 0 ? "text-bull" : index.change < 0 ? "text-bear" : "text-muted-foreground"
              }`}>
                {index.change > 0 ? (
                  <TrendingUp className="w-4 h-4" />
                ) : index.change < 0 ? (
                  <TrendingDown className="w-4 h-4" />
                ) : (
                  <Activity className="w-4 h-4" />
                )}
                <span>{index.change > 0 ? '+' : ''}{index.change.toFixed(2)} ({index.changePercent > 0 ? '+' : ''}{index.changePercent.toFixed(2)}%)</span>
              </div>
            </div>
          </FinancialCard>
        ))}
      </div>

      {/* Top Stocks */}
      <FinancialCard title="Actions les plus actives" className="col-span-full">
        <div className="space-y-3">
          {topStocks.map((stock) => (
            <StockTicker
              key={stock.symbol}
              symbol={stock.symbol}
              name={stock.name}
              price={stock.price}
              change={stock.change}
              changePercent={stock.changePercent}
            />
          ))}
        </div>
        
        <div className="mt-6 text-center">
          <Link to="/market">
            <Button className="bg-gradient-primary">
              Voir tous les marchés
            </Button>
          </Link>
        </div>
      </FinancialCard>
    </div>
  );
}