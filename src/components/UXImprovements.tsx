/**
 * Composant central pour les améliorations UX
 * Inclut ErrorBoundary, Toaster, etc.
 */
import { ErrorBoundary, ErrorDisplay } from "@/components/ui/error-boundary";
import { Toaster } from "@/components/ui/sonner";
import { Toaster as ShadcnToaster } from "@/components/ui/toaster";

export function UXImprovements() {
  return (
    <>
      {/* Sonner toaster (recommandé) */}
      <Toaster position="top-right" richColors closeButton />

      {/* Shadcn toaster (alternative) */}
      <ShadcnToaster />
    </>
  );
}

/**
 * Wrapper pour les pages avec ErrorBoundary
 */
export function PageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary
      fallback={
        <ErrorDisplay
          error={null}
          title="Erreur de chargement"
          description="Une erreur est survenue lors du chargement de la page."
        />
      }
    >
      {children}
    </ErrorBoundary>
  );
}



