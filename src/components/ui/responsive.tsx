/**
 * Composants et hooks pour le responsive design
 */
import { useMediaQuery } from "@/hooks/use-mobile";
import { cn } from "@/lib/utils";

/**
 * Hook pour les breakpoints Tailwind
 */
export function useBreakpoint() {
  const isMobile = useMediaQuery("(max-width: 768px)");
  const isTablet = useMediaQuery("(min-width: 769px) and (max-width: 1024px)");
  const isDesktop = useMediaQuery("(min-width: 1025px)");

  return {
    isMobile,
    isTablet,
    isDesktop,
    isMobileOrTablet: isMobile || isTablet,
  };
}

/**
 * Composant conditionnel selon le breakpoint
 */
export function Responsive({
  mobile,
  tablet,
  desktop,
  className,
}: {
  mobile?: React.ReactNode;
  tablet?: React.ReactNode;
  desktop?: React.ReactNode;
  className?: string;
}) {
  const { isMobile, isTablet, isDesktop } = useBreakpoint();

  return (
    <div className={className}>
      {isMobile && mobile}
      {isTablet && (tablet || mobile)}
      {isDesktop && (desktop || tablet || mobile)}
    </div>
  );
}

/**
 * Grid responsive avec colonnes adaptatives
 */
export function ResponsiveGrid({
  children,
  className,
  mobileCols = 1,
  tabletCols = 2,
  desktopCols = 3,
}: {
  children: React.ReactNode;
  className?: string;
  mobileCols?: number;
  tabletCols?: number;
  desktopCols?: number;
}) {
  return (
    <div
      className={cn(
        "grid gap-4",
        `grid-cols-${mobileCols}`,
        `md:grid-cols-${tabletCols}`,
        `lg:grid-cols-${desktopCols}`,
        className
      )}
    >
      {children}
    </div>
  );
}



