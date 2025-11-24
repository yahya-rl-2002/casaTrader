/**
 * Helpers pour les mises à jour optimistes (optimistic updates)
 */
import { useState, useCallback } from "react";
import { useNotification } from "@/hooks/use-notification";

/**
 * Hook pour les mises à jour optimistes
 */
export function useOptimisticUpdate<T>(
  initialData: T,
  updateFn: (data: T) => Promise<T>,
  options?: {
    onSuccess?: (data: T) => void;
    onError?: (error: Error, rollbackData: T) => void;
    successMessage?: string;
    errorMessage?: string;
  }
) {
  const [data, setData] = useState<T>(initialData);
  const [isUpdating, setIsUpdating] = useState(false);
  const notification = useNotification();

  const update = useCallback(async (optimisticData: T) => {
    // Sauvegarder l'état actuel pour rollback
    const previousData = data;

    // Mise à jour optimiste immédiate
    setData(optimisticData);
    setIsUpdating(true);

    try {
      // Mise à jour réelle
      const updatedData = await updateFn(optimisticData);
      setData(updatedData);

      if (options?.onSuccess) {
        options.onSuccess(updatedData);
      }

      if (options?.successMessage) {
        notification.success(options.successMessage);
      }
    } catch (error) {
      // Rollback en cas d'erreur
      setData(previousData);

      if (options?.onError) {
        options.onError(error as Error, previousData);
      }

      if (options?.errorMessage) {
        notification.error(
          options.errorMessage,
          {
            description: error instanceof Error ? error.message : "Erreur inconnue",
          }
        );
      }
    } finally {
      setIsUpdating(false);
    }
  }, [data, updateFn, options, notification]);

  return {
    data,
    update,
    isUpdating,
    setData, // Pour les mises à jour manuelles
  };
}



