import { Button } from "@/components/ui/button";
import { TrendingUp, BarChart3, Bell, User, Menu, Newspaper, LogOut, HelpCircle, Info, BadgeDollarSign, Settings, ChevronDown, Sun, Moon, FileText, Activity } from "lucide-react";
import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useSession } from "@/hooks/use-session";
import { supabase } from "@/integrations/supabase/client";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger, DropdownMenuLabel } from "@/components/ui/dropdown-menu";
import { useTheme } from "next-themes";

export function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const { user } = useSession();
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  React.useEffect(() => setMounted(true), []);
  const initials = (() => {
    const email = user?.email ?? "";
    const local = (email.split("@")[0] ?? "").replace(/[^A-Za-z0-9]/g, "");
    const up = local.toUpperCase();
    if (up.length >= 2) return up.slice(0, 2);
    if (up.length === 1) return up + "_";
    return "US";
  })();
  const handleLogout = async () => { await supabase.auth.signOut(); };

  return (
    <nav className="bg-background border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-bold text-foreground">CasaTrader</h1>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {/* Public links */}
            {!user && (
              <Link to="/pricing">
                <Button variant={location.pathname === "/pricing" ? "default" : "ghost"} className="flex items-center gap-2">
                  <BadgeDollarSign className="w-4 h-4" /> Tarifs
                </Button>
              </Link>
            )}
            {!user && (
              <>
                <Link to="/support">
                  <Button variant={location.pathname === "/support" ? "default" : "ghost"} className="flex items-center gap-2">
                    <HelpCircle className="w-4 h-4" /> Support
                  </Button>
                </Link>
                <Link to="/about">
                  <Button variant={location.pathname === "/about" ? "default" : "ghost"} className="flex items-center gap-2">
                    <Info className="w-4 h-4" /> À propos
                  </Button>
                </Link>
              </>
            )}

            {/* SaaS features (affichées uniquement si connecté) */}
            {user && (
              <>
                <Link to="/market">
                  <Button variant={location.pathname === "/market" ? "default" : "ghost"} className="flex items-center gap-2">
                    <BarChart3 className="w-4 h-4" /> Marché
                  </Button>
                </Link>
                <Link to="/fear-greed">
                  <Button variant={location.pathname === "/fear-greed" ? "default" : "ghost"} className="flex items-center gap-2">
                    <Activity className="w-4 h-4" /> Fear & Greed
                  </Button>
                </Link>
                <Link to="/news">
                  <Button variant={location.pathname === "/news" ? "default" : "ghost"} className="flex items-center gap-2">
                    <Newspaper className="w-4 h-4" /> Actualités
                  </Button>
                </Link>
                <Link to="/reports">
                  <Button variant={location.pathname === "/reports" ? "default" : "ghost"} className="flex items-center gap-2">
                    <FileText className="w-4 h-4" /> Rapports
                  </Button>
                </Link>
                <Link to="/portfolio">
                  <Button variant={location.pathname === "/portfolio" ? "default" : "ghost"} className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" /> Portfolio
                  </Button>
                </Link>
                <Link to="/alerts">
                  <Button variant={location.pathname === "/alerts" ? "default" : "ghost"} className="flex items-center gap-2">
                    <Bell className="w-4 h-4" /> Alertes
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Right Side */}
          <div className="flex items-center gap-4">
            {/* Theme toggle */}
            <button
              aria-label="Basculer le thème"
              className="hidden md:flex h-9 w-9 items-center justify-center rounded-md hover:bg-muted transition"
              onClick={() => setTheme((resolvedTheme ?? theme) === "dark" ? "light" : "dark")}
            >
              {mounted && (resolvedTheme ?? theme) === "dark" ? (
                <Sun className="w-4 h-4" />
              ) : (
                <Moon className="w-4 h-4" />
              )}
            </button>
            {!user ? (
              <>
                <Link to="/auth">
                  <Button variant="outline" size="sm" className="hidden md:flex">
                    <User className="w-4 h-4 mr-2" />
                    Connexion
                  </Button>
                </Link>
                <Link to="/auth">
                  <Button className="hidden md:flex bg-gradient-primary">
                    S'inscrire
                  </Button>
                </Link>
              </>
            ) : (
              <>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <button className="hidden md:flex items-center gap-2 text-sm text-foreground hover:bg-muted/50 px-2 py-1 rounded-md transition">
                      <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center font-semibold text-primary">
                        {initials}
                      </div>
                      <span className="text-muted-foreground">{user.email}</span>
                      <ChevronDown className="w-4 h-4 text-muted-foreground" />
                    </button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-56">
                    <DropdownMenuLabel className="text-xs text-muted-foreground">
                      Connecté en tant que
                      <div className="truncate text-foreground text-xs font-medium">{user.email}</div>
                    </DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <Link to="/profile">
                      <DropdownMenuItem>
                        <User className="w-4 h-4 mr-2" /> Profil
                      </DropdownMenuItem>
                    </Link>
                    <Link to="/profile#settings">
                      <DropdownMenuItem>
                        <Settings className="w-4 h-4 mr-2" /> Paramètres
                      </DropdownMenuItem>
                    </Link>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onSelect={(e) => { e.preventDefault(); void handleLogout(); }}>
                      <LogOut className="w-4 h-4 mr-2" /> Déconnexion
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            )}
            
            {/* Mobile menu button */}
            <Button 
              variant="ghost" 
              size="sm" 
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <Menu className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border py-4">
            <div className="flex flex-col gap-2">
              {/* Public links */}
              {!user && (
                <>
                  <Link to="/pricing">
                    <Button variant={location.pathname === "/pricing" ? "default" : "ghost"} className="justify-start w-full">
                      <BadgeDollarSign className="w-4 h-4 mr-2" /> Tarifs
                    </Button>
                  </Link>
                  <Link to="/support">
                    <Button variant={location.pathname === "/support" ? "default" : "ghost"} className="justify-start w-full">
                      <HelpCircle className="w-4 h-4 mr-2" /> Support
                    </Button>
                  </Link>
                  <Link to="/about">
                    <Button variant={location.pathname === "/about" ? "default" : "ghost"} className="justify-start w-full">
                      <Info className="w-4 h-4 mr-2" /> À propos
                    </Button>
                  </Link>
                </>
              )}
              <Link to="/support">
                <Button variant={location.pathname === "/support" ? "default" : "ghost"} className="justify-start w-full">
                  <HelpCircle className="w-4 h-4 mr-2" /> Support
                </Button>
              </Link>
              <Link to="/about">
                <Button variant={location.pathname === "/about" ? "default" : "ghost"} className="justify-start w-full">
                  <Info className="w-4 h-4 mr-2" /> À propos
                </Button>
              </Link>
              {user && (
                <>
                  <Link to="/market">
                    <Button variant={location.pathname === "/market" ? "default" : "ghost"} className="justify-start w-full">
                      <BarChart3 className="w-4 h-4 mr-2" /> Marché
                    </Button>
                  </Link>
                  <Link to="/fear-greed">
                    <Button variant={location.pathname === "/fear-greed" ? "default" : "ghost"} className="justify-start w-full">
                      <Activity className="w-4 h-4 mr-2" /> Fear & Greed
                    </Button>
                  </Link>
                  <Link to="/news">
                    <Button variant={location.pathname === "/news" ? "default" : "ghost"} className="justify-start w-full">
                      <Newspaper className="w-4 h-4 mr-2" /> Actualités
                    </Button>
                  </Link>
                  <Link to="/reports">
                    <Button variant={location.pathname === "/reports" ? "default" : "ghost"} className="justify-start w-full">
                      <FileText className="w-4 h-4 mr-2" /> Rapports
                    </Button>
                  </Link>
                  <Link to="/portfolio">
                    <Button variant={location.pathname === "/portfolio" ? "default" : "ghost"} className="justify-start w-full">
                      <TrendingUp className="w-4 h-4 mr-2" /> Portfolio
                    </Button>
                  </Link>
                  <Link to="/alerts">
                    <Button variant={location.pathname === "/alerts" ? "default" : "ghost"} className="justify-start w-full">
                      <Bell className="w-4 h-4 mr-2" /> Alertes
                    </Button>
                  </Link>
                </>
              )}
              <div className="flex gap-2 mt-4">
                {!user ? (
                  <>
                    <Link to="/auth" className="flex-1">
                      <Button variant="outline" className="w-full">
                        Connexion
                      </Button>
                    </Link>
                    <Link to="/auth" className="flex-1">
                      <Button className="w-full bg-gradient-primary">
                        S'inscrire
                      </Button>
                    </Link>
                  </>
                ) : (
                  <Button variant="outline" className="w-full" onClick={handleLogout}>
                    <LogOut className="w-4 h-4 mr-2" />
                    Déconnexion
                  </Button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
