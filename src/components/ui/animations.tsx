/**
 * Composants d'animation et transitions pour une meilleure UX
 * Note: Nécessite framer-motion (npm install framer-motion)
 */
import { ReactNode } from "react";
import { cn } from "@/lib/utils";

// Types pour les variants (sera remplacé par framer-motion une fois installé)
type Variants = {
  hidden: { opacity?: number; y?: number; scale?: number };
  visible: { opacity?: number; y?: number; scale?: number };
};

// Wrapper temporaire jusqu'à l'installation de framer-motion
const MotionDiv = ({ children, ...props }: any) => <div {...props}>{children}</div>;
const AnimatePresence = ({ children }: { children: ReactNode }) => <>{children}</>;
const motion = { div: MotionDiv };

// Variants d'animation réutilisables
export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
};

export const slideUp: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export const slideDown: Variants = {
  hidden: { opacity: 0, y: -20 },
  visible: { opacity: 1, y: 0 },
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: { opacity: 1, scale: 1 },
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

/**
 * Wrapper avec animation fade in
 */
export function FadeIn({
  children,
  delay = 0,
  duration = 0.3,
  className,
}: {
  children: ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}) {
  // Version simple sans framer-motion (sera améliorée après installation)
  return (
    <div
      className={cn("animate-in fade-in duration-300", className)}
      style={{ animationDelay: `${delay}s`, animationDuration: `${duration}s` }}
    >
      {children}
    </div>
  );
}

/**
 * Wrapper avec animation slide up
 */
export function SlideUp({
  children,
  delay = 0,
  duration = 0.3,
  className,
}: {
  children: ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}) {
  return (
    <div
      className={cn("animate-in slide-in-from-bottom-4 duration-300", className)}
      style={{ animationDelay: `${delay}s`, animationDuration: `${duration}s` }}
    >
      {children}
    </div>
  );
}

/**
 * Wrapper avec animation scale in
 */
export function ScaleIn({
  children,
  delay = 0,
  duration = 0.3,
  className,
}: {
  children: ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}) {
  return (
    <div
      className={cn("animate-in zoom-in-95 duration-300", className)}
      style={{ animationDelay: `${delay}s`, animationDuration: `${duration}s` }}
    >
      {children}
    </div>
  );
}

/**
 * Container avec stagger animation pour les listes
 */
export function StaggerContainer({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={className}>{children}</div>;
}

/**
 * Item avec animation pour les listes staggerées
 */
export function StaggerItem({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("animate-in slide-in-from-bottom-4 duration-300", className)}>
      {children}
    </div>
  );
}

/**
 * Animation de pulse pour les indicateurs
 */
export function Pulse({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("animate-pulse", className)}>
      {children}
    </div>
  );
}

/**
 * Hover animation pour les cartes
 */
export function HoverCard({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("transition-all duration-200 hover:scale-[1.02] hover:-translate-y-1", className)}>
      {children}
    </div>
  );
}

/**
 * AnimatedList wrapper pour les transitions d'entrée/sortie
 */
export function AnimatedList({
  items,
  renderItem,
  className,
}: {
  items: any[];
  renderItem: (item: any, index: number) => ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
      {items.map((item, index) => (
        <div
          key={item.id || index}
          className="animate-in fade-in slide-in-from-bottom-4 duration-200"
        >
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  );
}

