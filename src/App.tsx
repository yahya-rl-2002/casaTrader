import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ErrorBoundary } from "@/components/ui/error-boundary";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Market from "./pages/Market";
import News from "./pages/News";
import Auth from "./pages/Auth";
import Portfolio from "./pages/Portfolio";
import Alerts from "./pages/Alerts";
import Pricing from "./pages/Pricing";
import Reports from "./pages/Reports";
import Profile from "./pages/Profile";
import Activity from "./pages/Activity";
import Support from "./pages/Support";
import About from "./pages/About";
import FearGreedDashboard from "./pages/FearGreedDashboard";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { PublicOnly } from "@/components/PublicOnly";
import { FloatingAssistantButton } from "@/components/FloatingAssistantButton";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <ErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <BrowserRouter future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}>
          <Toaster />
          <Sonner />
          <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/pricing" element={<PublicOnly><Pricing /></PublicOnly>} />
          <Route path="/support" element={<PublicOnly><Support /></PublicOnly>} />
          <Route path="/about" element={<PublicOnly><About /></PublicOnly>} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/market" element={<ProtectedRoute><Market /></ProtectedRoute>} />
          <Route path="/news" element={<ProtectedRoute><News /></ProtectedRoute>} />
          <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
          <Route path="/portfolio" element={<ProtectedRoute><Portfolio /></ProtectedRoute>} />
          <Route path="/alerts" element={<ProtectedRoute><Alerts /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/activity" element={<ProtectedRoute><Activity /></ProtectedRoute>} />
          <Route path="/fear-greed" element={<ProtectedRoute><FearGreedDashboard /></ProtectedRoute>} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
        <FloatingAssistantButton />
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
  </ErrorBoundary>
);

export default App;
