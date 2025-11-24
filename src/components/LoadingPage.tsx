/**
 * Page de chargement améliorée - Version moderne sans emojis
 * Design professionnel avec animations CSS pures
 */
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

interface LoadingPageProps {
  message?: string;
  onComplete?: () => void;
  minDisplayTime?: number; // Temps minimum d'affichage en ms
}

export function LoadingPage({ 
  message = "Chargement...", 
  onComplete,
  minDisplayTime = 1500 
}: LoadingPageProps) {
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    // Animation de progression
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 100);

    // Timer minimum d'affichage
    const minTimer = setTimeout(() => {
      setIsComplete(true);
      if (onComplete) {
        setTimeout(onComplete, 300); // Délai pour l'animation de sortie
      }
    }, minDisplayTime);

    return () => {
      clearInterval(progressInterval);
      clearTimeout(minTimer);
    };
  }, [onComplete, minDisplayTime]);

  return (
    <div 
      className={cn(
        "fixed inset-0 z-50 flex items-center justify-center",
        "bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900",
        "transition-opacity duration-300",
        isComplete && "opacity-0 pointer-events-none"
      )}
    >
      <div className="flex flex-col items-center gap-8 px-4">
        {/* Logo/Icon animé */}
        <div className="relative">
          {/* Cercle externe rotatif */}
          <div className="absolute inset-0 border-4 border-slate-700 rounded-full animate-spin-slow" 
               style={{ animationDuration: '3s' }} />
          
          {/* Cercle moyen */}
          <div className="absolute inset-2 border-4 border-blue-500/30 rounded-full animate-spin" 
               style={{ animationDuration: '2s', animationDirection: 'reverse' }} />
          
          {/* Cercle intérieur avec logo */}
          <div className="relative w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-2xl">
            <div className="w-12 h-12 bg-white rounded-lg transform rotate-45 flex items-center justify-center">
              <div className="w-6 h-6 bg-blue-600 rounded-sm transform -rotate-45"></div>
            </div>
          </div>
        </div>

        {/* Titre */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-white tracking-tight">
            CasaTrader
          </h1>
          <p className="text-slate-400 text-sm font-medium">
            Bourse de Casablanca
          </p>
        </div>

        {/* Barre de progression */}
        <div className="w-64 space-y-2">
          <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 via-blue-400 to-blue-500 rounded-full transition-all duration-300 ease-out relative"
              style={{ width: `${Math.min(progress, 100)}%` }}
            >
              {/* Effet de brillance animé */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
            </div>
          </div>
          
          {/* Pourcentage */}
          <div className="text-center">
            <span className="text-xs text-slate-500 font-mono">
              {Math.round(Math.min(progress, 100))}%
            </span>
          </div>
        </div>

        {/* Message */}
        <p className="text-sm text-slate-400 animate-pulse">
          {message}
        </p>

        {/* Points de chargement animés */}
        <div className="flex gap-2">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
              style={{
                animationDelay: `${i * 0.2}s`,
                animationDuration: '1s'
              }}
            />
          ))}
        </div>
      </div>

      <style>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        
        .animate-spin-slow {
          animation: spin-slow 3s linear infinite;
        }
        
        .animate-shimmer {
          animation: shimmer 2s infinite;
        }
      `}</style>
    </div>
  );
}

/**
 * Version simplifiée pour les chargements rapides
 */
export function LoadingPageSimple({ message = "Chargement..." }: { message?: string }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/95 backdrop-blur-sm">
      <div className="flex flex-col items-center gap-4">
        {/* Spinner moderne */}
        <div className="relative w-16 h-16">
          <div className="absolute inset-0 border-4 border-slate-700 rounded-full" />
          <div className="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
        
        {/* Message */}
        <p className="text-sm text-slate-300 font-medium">{message}</p>
      </div>
    </div>
  );
}



