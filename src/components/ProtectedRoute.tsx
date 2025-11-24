import { Navigate, useLocation } from "react-router-dom";
import { useSession } from "@/hooks/use-session";

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { user, loading } = useSession();
  const location = useLocation();

  if (loading) return null;
  if (!user) return <Navigate to="/auth" replace state={{ from: location.pathname }} />;
  return children;
}

