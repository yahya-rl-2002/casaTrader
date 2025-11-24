/**
 * Hook pour gérer les notifications utilisateur de manière centralisée
 */
import { toast } from "sonner";
import { useToast } from "@/hooks/use-toast";

export type NotificationType = "success" | "error" | "warning" | "info";

export interface NotificationOptions {
  title?: string;
  description?: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

/**
 * Hook pour les notifications avec Sonner (recommandé)
 */
export function useNotification() {
  const showNotification = (
    type: NotificationType,
    message: string,
    options?: NotificationOptions
  ) => {
    const { title, description, duration = 4000, action } = options || {};

    const config = {
      duration,
      ...(action && {
        action: {
          label: action.label,
          onClick: action.onClick,
        },
      }),
    };

    switch (type) {
      case "success":
        toast.success(title || message, {
          description,
          ...config,
        });
        break;
      case "error":
        toast.error(title || message, {
          description,
          ...config,
        });
        break;
      case "warning":
        toast.warning(title || message, {
          description,
          ...config,
        });
        break;
      case "info":
        toast.info(title || message, {
          description,
          ...config,
        });
        break;
    }
  };

  return {
    success: (message: string, options?: NotificationOptions) =>
      showNotification("success", message, options),
    error: (message: string, options?: NotificationOptions) =>
      showNotification("error", message, options),
    warning: (message: string, options?: NotificationOptions) =>
      showNotification("warning", message, options),
    info: (message: string, options?: NotificationOptions) =>
      showNotification("info", message, options),
    promise: toast.promise,
  };
}

/**
 * Hook pour les notifications avec le système de toast shadcn (alternative)
 */
export function useNotificationToast() {
  const { toast: toastFn } = useToast();

  return {
    success: (title: string, description?: string) =>
      toastFn({
        title,
        description,
        variant: "default",
      }),
    error: (title: string, description?: string) =>
      toastFn({
        title,
        description,
        variant: "destructive",
      }),
    info: (title: string, description?: string) =>
      toastFn({
        title,
        description,
      }),
  };
}



