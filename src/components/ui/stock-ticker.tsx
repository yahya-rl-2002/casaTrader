import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface StockTickerProps {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  className?: string;
}

export function StockTicker({ symbol, name, price, change, changePercent, className }: StockTickerProps) {
  const isPositive = change > 0;
  const isNegative = change < 0;
  
  return (
    <div className={cn("flex items-center justify-between p-4 bg-gradient-card rounded-lg shadow-card hover:shadow-elevation transition-all duration-300", className)}>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <h3 className="font-semibold text-foreground">{symbol}</h3>
          <span className="text-sm text-muted-foreground">{name}</span>
        </div>
        <div className="mt-1">
          <span className="text-2xl font-bold text-foreground">{price.toFixed(2)} MAD</span>
        </div>
      </div>
      
      <div className="text-right">
        <div className={cn(
          "flex items-center gap-1 text-sm font-medium",
          isPositive && "text-bull",
          isNegative && "text-bear",
          !isPositive && !isNegative && "text-muted-foreground"
        )}>
          {isPositive && <TrendingUp className="w-4 h-4" />}
          {isNegative && <TrendingDown className="w-4 h-4" />}
          {!isPositive && !isNegative && <Minus className="w-4 h-4" />}
          <span>{change > 0 ? '+' : ''}{change.toFixed(2)}</span>
        </div>
        <div className={cn(
          "text-sm font-medium",
          isPositive && "text-bull",
          isNegative && "text-bear",
          !isPositive && !isNegative && "text-muted-foreground"
        )}>
          {changePercent > 0 ? '+' : ''}{changePercent.toFixed(2)}%
        </div>
      </div>
    </div>
  );
}