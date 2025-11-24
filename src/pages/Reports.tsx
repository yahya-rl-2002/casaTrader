import { useMemo, useState, useEffect } from "react";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";
import { CASEMA_SYMBOLS } from "@/data/casema-symbols";
import { CASABLANCA_COMPANIES } from "@/data/casablanca-companies";
import { ReportsNavigation } from "@/components/ReportsNavigation";
import { ReportsDisplay } from "@/components/ReportsDisplay";
import { Calendar, Download, ExternalLink, Search, Star, Building2, Tag, RefreshCw, Globe } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { FinancialReportUpload } from "@/components/FinancialReportUpload";
import type { Tables } from "@/integrations/supabase/types";

type DocType = "rapport-annuel" | "resultats" | "communique" | "profit-warning" | "autre";

type FinancialDoc = Tables<'financial_reports'>;

export default function Reports() {
  const companies = useMemo(() => CASEMA_SYMBOLS, []);
  const { toast } = useToast();

  const [tab, setTab] = useState<"docs" | "companies">("companies");
  const [search, setSearch] = useState("");
  const [company, setCompany] = useState<string>("all");
  const [docType, setDocType] = useState<DocType | "all">("all");
  const [range, setRange] = useState<"all" | "30d" | "90d" | "1y">("all");
  const [onlyFeatured, setOnlyFeatured] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [reports, setReports] = useState<FinancialDoc[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedSector, setSelectedSector] = useState<string>("all");

  // Charger les rapports depuis Supabase
  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      console.log('Chargement de tous les rapports financiers...');
      
      // Récupération de TOUS les rapports depuis la base de données
      const { data, error } = await supabase
        .from('financial_reports')
        .select('*')
        .order('created_at', { ascending: false });

      console.log('Résultat:', { data, error });

      if (error) {
        console.error('Erreur récupération:', error);
        throw error;
      }

      console.log('Tous les rapports récupérés:', data?.length || 0);
      
      // Charger TOUS les rapports (pas seulement Akdital)
      setReports(data || []);
      
      // Afficher un toast avec les statistiques
      const uniqueCompanies = new Set(data?.map(r => r.company_symbol) || []).size;
      toast({
        title: "Rapports chargés",
        description: `${data?.length || 0} rapports trouvés pour ${uniqueCompanies} entreprises`,
        variant: "default",
      });
      
    } catch (error: any) {
      console.error('Erreur chargement:', error);
      toast({
        title: "Erreur de chargement",
        description: `Impossible de charger les rapports: ${error.message}`,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const stats = useMemo(() => {
    const uniqueCompanies = new Set(reports.map((d) => d.company_symbol));
    return { companies: uniqueCompanies.size, docs: reports.length };
  }, [reports]);

  const filtered = useMemo(() => {
    const now = Date.now();
    const threshold = range === "30d" ? now - 30 * 86400000 : range === "90d" ? now - 90 * 86400000 : range === "1y" ? now - 365 * 86400000 : 0;
    
    console.log('🔍 Filtrage - selectedCompany:', selectedCompany);
    console.log('🔍 Filtrage - total rapports:', reports.length);
    
    const result = reports.filter((d) => {
      if (onlyFeatured && !d.featured) return false;
      
      // Filtre par entreprise sélectionnée (priorité)
      if (selectedCompany) {
        // Filtre normal pour toutes les entreprises
        if (d.company_symbol !== selectedCompany && d.company_name !== selectedCompany) {
          return false;
        }
      } else if (company !== "all" && d.company_symbol !== company) {
        return false;
      }
      
      // Filtre par secteur si sélectionné
      if (selectedSector && selectedSector !== "all") {
        const companyData = CASABLANCA_COMPANIES.find(c => c.symbol === d.company_symbol);
        if (companyData?.sector !== selectedSector) {
          return false;
        }
      }
      
      if (docType !== "all" && d.report_type !== docType) return false;
      if (threshold && d.published_at && new Date(d.published_at).getTime() < threshold) return false;
      if (search) {
        const q = search.toLowerCase();
        const text = `${d.title} ${d.company_name} ${(d.tags || []).join(" ")}`.toLowerCase();
        if (!text.includes(q)) return false;
      }
      return true;
    }).sort((a, b) => {
      const dateA = a.published_at ? new Date(a.published_at).getTime() : 0;
      const dateB = b.published_at ? new Date(b.published_at).getTime() : 0;
      return dateB - dateA;
    });
    
    console.log('🔍 Filtrage - résultat:', result.length, 'rapports filtrés');
    if (selectedCompany) {
      console.log('🔍 Filtrage - rapports pour', selectedCompany, ':', result);
    }
    
    return result;
  }, [reports, search, company, docType, range, onlyFeatured, selectedCompany, selectedSector]);

  // Handlers pour la navigation
  const handleCompanySelect = (companySymbol: string) => {
    setCompany(companySymbol);
    setSelectedCompany(companySymbol);
    setTab("docs");
  };

  const handleSectorSelect = (sector: string) => {
    setSelectedSector(sector);
    setTab("docs");
  };

  const handleReportTypeSelect = (type: string) => {
    setDocType(type as DocType | "all");
    setTab("docs");
  };

  const handleViewModeChange = (mode: 'grid' | 'list') => {
    setViewMode(mode);
  };

  const handleSearchChange = (query: string) => {
    setSearch(query);
  };

  function initialsFromName(name: string) {
    const parts = name.replace(/[^A-Za-zÀ-ÿ0-9 ]/g, "").trim().split(/\s+/);
    const first = parts[0]?.[0] || "C";
    const last = parts[1]?.[0] || parts[0]?.[1] || "T";
    return (first + last).toUpperCase();
  }

  const onOpen = async (report: FinancialDoc) => {
    if (!report.file_url) {
      toast({ title: "Fichier indisponible", description: "Le fichier n'est pas disponible.", variant: "destructive" });
      return;
    }
    window.open(report.file_url, "_blank");
  };

  const onDownload = async (report: FinancialDoc) => {
    if (!report.file_url) {
      toast({ title: "Fichier indisponible", description: "Le fichier n'est pas disponible.", variant: "destructive" });
      return;
    }

    try {
      // Incrémenter le compteur de téléchargements
      await supabase.rpc('increment_download_count', { report_id: report.id });
      
      // Télécharger avec le nom de fichier complet
      const fileName = report.file_name || report.title || 'document.pdf';
      
      // Créer un lien de téléchargement avec le nom de fichier
      const link = document.createElement('a');
      link.href = report.file_url;
      link.download = fileName;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      toast({ 
        title: "Téléchargement", 
        description: `Téléchargement de ${fileName}...` 
      });
    } catch (error) {
      console.error('Erreur téléchargement:', error);
      // Fallback : ouvrir dans un nouvel onglet
      window.open(report.file_url, "_blank");
    }
  };


  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <section className="mb-8">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold">Rapports Financiers Officiels</h1>
              <p className="text-muted-foreground mt-2">
                Documents financiers officiels des entreprises cotées à la Bourse de Casablanca.
                {selectedCompany && (
                  <span className="ml-2 text-primary font-medium">
                    • Filtrage par: {selectedCompany === 'CSEMA:AKT' ? 'Akdital' : selectedCompany}
                  </span>
                )}
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Card><CardContent className="p-3"><div className="text-xs text-muted-foreground">Sociétés</div><div className="text-xl font-semibold">{stats.companies}</div></CardContent></Card>
              <Card><CardContent className="p-3"><div className="text-xs text-muted-foreground">Documents</div><div className="text-xl font-semibold">{stats.docs}</div></CardContent></Card>
            </div>
          </div>
        </section>

        <section className="bg-card border rounded-xl p-4 shadow-sm">
          <div className="flex flex-col lg:flex-row lg:items-center gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input placeholder="Rechercher un document, une société, un tag…" value={search} onChange={(e) => setSearch(e.target.value)} className="pl-9" />
            </div>
            <Select value={company} onValueChange={setCompany}>
              <SelectTrigger className="w-full lg:w-56"><SelectValue placeholder="Société" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes sociétés</SelectItem>
                {companies.map((c) => (
                  <SelectItem key={c.value} value={c.value}>{c.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={docType} onValueChange={(v) => setDocType(v as DocType | "all") }>
              <SelectTrigger className="w-full lg:w-44"><SelectValue placeholder="Type" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous types</SelectItem>
                <SelectItem value="rapport-annuel">Rapport annuel</SelectItem>
                <SelectItem value="resultats">Résultats</SelectItem>
                <SelectItem value="communique">Communiqué</SelectItem>
                <SelectItem value="profit-warning">Profit warning</SelectItem>
                <SelectItem value="autre">Autre</SelectItem>
              </SelectContent>
            </Select>
            <Select value={range} onValueChange={(v) => setRange(v as typeof range)}>
              <SelectTrigger className="w-full lg:w-40"><SelectValue placeholder="Période" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes périodes</SelectItem>
                <SelectItem value="30d">30 jours</SelectItem>
                <SelectItem value="90d">90 jours</SelectItem>
                <SelectItem value="1y">1 an</SelectItem>
              </SelectContent>
            </Select>
            <Button variant={onlyFeatured ? "default" : "outline"} onClick={() => setOnlyFeatured((v) => !v)} className="whitespace-nowrap">
              <Star className={cn("w-4 h-4 mr-2", onlyFeatured ? "fill-current" : "")} /> À la une
            </Button>
            <FinancialReportUpload onUploadSuccess={loadReports} />
            <Button
              variant="outline"
              onClick={loadReports}
              disabled={loading}
            >
              <RefreshCw className={cn("w-4 h-4 mr-2", loading && "animate-spin")} />
              Actualiser
            </Button>
            {selectedCompany && (
              <Button
                variant="outline"
                onClick={() => {
                  setSelectedCompany(null);
                  setCompany("all");
                }}
              >
                ✕ Effacer filtre
              </Button>
            )}
          </div>
        </section>

        <section className="mt-6">
          <Tabs value={tab} onValueChange={(v) => setTab(v as typeof tab)}>
            <TabsList>
              <TabsTrigger value="companies">Navigation</TabsTrigger>
              <TabsTrigger value="docs">Documents</TabsTrigger>
            </TabsList>

            <TabsContent value="docs" className="mt-4">
              {loading ? (
                <Card><CardContent className="p-8 text-center text-muted-foreground">Chargement des rapports...</CardContent></Card>
              ) : (
                <ReportsDisplay 
                  reports={filtered}
                  viewMode={viewMode}
                  onOpen={onOpen}
                  onDownload={onDownload}
                />
              )}
            </TabsContent>

            <TabsContent value="companies" className="mt-4">
              <ReportsNavigation 
                reports={reports}
                onCompanySelect={handleCompanySelect}
                onSectorSelect={handleSectorSelect}
                onReportTypeSelect={handleReportTypeSelect}
                onViewModeChange={handleViewModeChange}
                onOpen={onOpen}
                onDownload={onDownload}
                selectedCompany={company}
                selectedSector={selectedSector}
                selectedReportType={docType}
                viewMode={viewMode}
                searchQuery={search}
                onSearchChange={handleSearchChange}
              />
            </TabsContent>
          </Tabs>
        </section>
      </main>
      <Footer />
    </div>
  );
}