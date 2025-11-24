import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ReactNode } from "react";

interface FinancialCardProps {
  title: string;
  children: ReactNode;
  className?: string;
  trend?: "up" | "down" | "neutral";
}

export function FinancialCard({ title, children, className, trend }: FinancialCardProps) {
  return (
    <Card className={cn("bg-gradient-card shadow-card hover:shadow-elevation transition-all duration-300", className)}>
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
          {title}
          {trend && (
            <div className={cn(
              "w-2 h-2 rounded-full",
              trend === "up" && "bg-bull",
              trend === "down" && "bg-bear",
              trend === "neutral" && "bg-muted-foreground"
            )} />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
    </Card>
  );
}