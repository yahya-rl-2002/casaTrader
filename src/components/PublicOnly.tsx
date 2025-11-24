import { Navigate } from "react-router-dom";
import { useSession } from "@/hooks/use-session";

export function PublicOnly({ children }: { children: JSX.Element }) {
  const { user, loading } = useSession();
  if (loading) return null;
  if (user) return <Navigate to="/market" replace />;
  return children;
}

