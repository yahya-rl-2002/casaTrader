import { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { 
  Search, 
  Building2, 
  TrendingUp, 
  Calendar, 
  Filter,
  Grid3X3,
  List,
  Star,
  Globe,
  FileText,
  Download,
  ExternalLink,
  ChevronRight,
  Building,
  Banknote,
  Smartphone,
  Shield,
  Home,
  Factory,
  Zap,
  Car,
  ShoppingCart,
  Heart,
  Utensils
} from "lucide-react";
import { cn } from "@/lib/utils";
import { CASABLANCA_COMPANIES } from "@/data/casablanca-companies";
import { SectorReports } from "@/components/SectorReports";
import { CompanyReports } from "@/components/CompanyReports";
import { AkditalReportsOrganized } from "@/components/AkditalReportsOrganized";
import { OrganizedCompanyReports } from "@/components/OrganizedCompanyReports";
import type { Tables } from "@/integrations/supabase/types";

interface ReportsNavigationProps {
  reports: Tables<'financial_reports'>[];
  onCompanySelect: (company: string) => void;
  onSectorSelect: (sector: string) => void;
  onReportTypeSelect: (type: string) => void;
  onViewModeChange: (mode: 'grid' | 'list') => void;
  onOpen: (report: Tables<'financial_reports'>) => void;
  onDownload: (report: Tables<'financial_reports'>) => void;
  selectedCompany: string;
  selectedSector: string;
  selectedReportType: string;
  viewMode: 'grid' | 'list';
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

// Secteurs avec icônes et couleurs (basés sur la liste officielle de la Bourse de Casablanca)
const SECTORS = [
  { id: 'all', name: 'Tous les secteurs', icon: Building2, color: 'bg-gray-100 text-gray-800', count: 0 },
  { id: 'Financials', name: 'Financials', icon: Banknote, color: 'bg-blue-100 text-blue-800', count: 0 },
  { id: 'Industrials', name: 'Industrials', icon: Factory, color: 'bg-red-100 text-red-800', count: 0 },
  { id: 'Oil & Gas', name: 'Oil & Gas', icon: Zap, color: 'bg-yellow-100 text-yellow-800', count: 0 },
  { id: 'Telecom', name: 'Telecom', icon: Smartphone, color: 'bg-green-100 text-green-800', count: 0 },
  { id: 'Health Care', name: 'Health Care', icon: Heart, color: 'bg-teal-100 text-teal-800', count: 0 },
  { id: 'Consumer Services', name: 'Consumer Services', icon: ShoppingCart, color: 'bg-pink-100 text-pink-800', count: 0 },
  { id: 'Consumer Goods', name: 'Consumer Goods', icon: Utensils, color: 'bg-indigo-100 text-indigo-800', count: 0 },
  { id: 'Basic Materials', name: 'Basic Materials', icon: Building, color: 'bg-orange-100 text-orange-800', count: 0 },
  { id: 'Technology', name: 'Technology', icon: Globe, color: 'bg-purple-100 text-purple-800', count: 0 },
  { id: 'Utilities', name: 'Utilities', icon: Zap, color: 'bg-cyan-100 text-cyan-800', count: 0 }
];

// Types de rapports
const REPORT_TYPES = [
  { id: 'all', name: 'Tous les types', icon: FileText },
  { id: 'rapport-annuel', name: 'Rapport Annuel', icon: Calendar },
  { id: 'resultats', name: 'Résultats', icon: TrendingUp },
  { id: 'communique', name: 'Communiqué', icon: Globe },
  { id: 'profit-warning', name: 'Profit Warning', icon: Star }
];

export function ReportsNavigation({
  reports,
  onCompanySelect,
  onSectorSelect,
  onReportTypeSelect,
  onViewModeChange,
  onOpen,
  onDownload,
  selectedCompany,
  selectedSector,
  selectedReportType,
  viewMode,
  searchQuery,
  onSearchChange
}: ReportsNavigationProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'companies' | 'sectors'>('overview');
  const [showCompanyReports, setShowCompanyReports] = useState(false);
  const [selectedCompanyForReports, setSelectedCompanyForReports] = useState<{name: string, symbol: string} | null>(null);

  const handleCompanyClick = (companySymbol: string) => {
    const company = CASABLANCA_COMPANIES.find(c => c.symbol === companySymbol);
    if (company) {
      // Filtrer les rapports pour cette entreprise
      const companyReports = reports.filter(report => 
        report.company_symbol === companySymbol || 
        report.company_name === company.name ||
        (company.name === 'Akdital' && (
          report.company_name === 'Akdital' || 
          report.company_symbol === 'CSEMA:AKT' ||
          report.company_symbol === 'CSEMA:UNKNOWN'
        ))
      );
      
      if (companyReports.length > 0) {
        setSelectedCompanyForReports({ name: company.name, symbol: company.symbol });
        setShowCompanyReports(true);
      } else {
        // Si aucun rapport, afficher quand même la page mais vide
        setSelectedCompanyForReports({ name: company.name, symbol: company.symbol });
        setShowCompanyReports(true);
      }
    }
  };

  const handleBackToCompanies = () => {
    setShowCompanyReports(false);
    setSelectedCompanyForReports(null);
  };

  // Statistiques globales
  const stats = useMemo(() => {
    const totalReports = reports.length;
    const uniqueCompanies = new Set(reports.map(r => r.company_symbol)).size;
    const featuredReports = reports.filter(r => r.featured).length;
    const recentReports = reports.filter(r => {
      if (!r.published_at) return false;
      const reportDate = new Date(r.published_at);
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return reportDate > thirtyDaysAgo;
    }).length;

    return { totalReports, uniqueCompanies, featuredReports, recentReports };
  }, [reports]);

  // Grouper les rapports par entreprise
  const reportsByCompany = useMemo(() => {
    const grouped: { [key: string]: Tables<'financial_reports'>[] } = {};
    console.log('🔍 Groupement - Total rapports:', reports.length);
    
    reports.forEach(report => {
      // Pour Akdital, grouper tous les rapports sous CSEMA:AKT
      let companyKey = report.company_symbol;
      if (report.company_name === 'Akdital' || 
          report.company_symbol === 'CSEMA:AKT' ||
          report.tags?.includes('akdital')) {
        companyKey = 'CSEMA:AKT';
        console.log('🏥 Rapport Akdital trouvé:', report.title, '→', companyKey);
      }
      
      if (!grouped[companyKey]) {
        grouped[companyKey] = [];
      }
      grouped[companyKey].push(report);
    });
    
    console.log('🔍 Groupement - Résultat:', Object.keys(grouped).map(key => `${key}: ${grouped[key].length}`));
    console.log('🔍 Groupement - Akdital:', grouped['CSEMA:AKT']?.length || 0);
    
    return grouped;
  }, [reports]);

  // Créer une liste complète des entreprises avec leurs rapports
  const allCompaniesWithReports = useMemo(() => {
    return CASABLANCA_COMPANIES.map(company => {
      const companyReports = reportsByCompany[company.symbol] || [];
      return {
        ...company,
        reportCount: companyReports.length,
        reports: companyReports
      };
    }).sort((a, b) => a.name.localeCompare(b.name, 'fr')); // Trier par ordre alphabétique
  }, [reportsByCompany]);

  // Grouper les rapports par secteur (basé sur les vrais secteurs de la Bourse)
  const reportsBySector = useMemo(() => {
    const sectorMap: { [key: string]: Tables<'financial_reports'>[] } = {};
    
    reports.forEach(report => {
      let sector = 'autre';
      
      // Akdital est dans le secteur Health Care
      if (report.company_name === 'Akdital' || 
          report.company_symbol === 'CSEMA:AKT' || 
          report.tags?.includes('akdital')) {
        sector = 'Health Care';
      } else {
        // Pour les autres entreprises, utiliser la liste officielle
        const company = CASABLANCA_COMPANIES.find(c => c.symbol === report.company_symbol);
        sector = company?.sector || 'autre';
      }
      
      if (!sectorMap[sector]) {
        sectorMap[sector] = [];
      }
      sectorMap[sector].push(report);
    });
    
    return sectorMap;
  }, [reports]);

  // Mettre à jour les compteurs de secteurs
  const sectorsWithCounts = SECTORS.map(sector => ({
    ...sector,
    count: sector.id === 'all' ? stats.totalReports : reportsBySector[sector.id]?.length || 0
  }));

  // Si on affiche les rapports d'une entreprise spécifique
  if (showCompanyReports && selectedCompanyForReports) {
    const companyReports = reportsByCompany[selectedCompanyForReports.symbol] || [];
    
    // Utiliser le composant organisé pour TOUTES les entreprises
    // Cela permet une organisation cohérente par année et par type
    return (
      <OrganizedCompanyReports
        reports={companyReports}
        companyName={selectedCompanyForReports.name}
        companySymbol={selectedCompanyForReports.symbol}
        onOpen={(url) => onOpen({ file_url: url } as Tables<'financial_reports'>)}
        onDownload={(url, fileName) => onDownload({ file_url: url, file_name: fileName } as Tables<'financial_reports'>)}
        onBack={handleBackToCompanies}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête avec statistiques */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Building2 className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.uniqueCompanies}</div>
                <div className="text-sm text-muted-foreground">Entreprises</div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <FileText className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.totalReports}</div>
                <div className="text-sm text-muted-foreground">Rapports</div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Star className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.featuredReports}</div>
                <div className="text-sm text-muted-foreground">À la une</div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.recentReports}</div>
                <div className="text-sm text-muted-foreground">30 derniers jours</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Barre de recherche et filtres */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input 
                placeholder="Rechercher par entreprise, rapport, secteur..." 
                value={searchQuery} 
                onChange={(e) => onSearchChange(e.target.value)} 
                className="pl-9" 
              />
            </div>
            
            <div className="flex gap-2">
              <Button
                variant={viewMode === "grid" ? "default" : "outline"}
                size="sm"
                onClick={() => onViewModeChange("grid")}
              >
                <Grid3X3 className="w-4 h-4 mr-2" />
                Grille
              </Button>
              <Button
                variant={viewMode === "list" ? "default" : "outline"}
                size="sm"
                onClick={() => onViewModeChange("list")}
              >
                <List className="w-4 h-4 mr-2" />
                Liste
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Navigation par onglets */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as typeof activeTab)}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="companies">Par Entreprise</TabsTrigger>
          <TabsTrigger value="sectors">Par Secteur</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Secteurs populaires */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Building className="w-5 h-5" />
                  Secteurs d'Activité
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {sectorsWithCounts.slice(1, 6).map((sector) => (
                    <div 
                      key={sector.id}
                      className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                      onClick={() => onSectorSelect(sector.id)}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`p-2 rounded-lg ${sector.color}`}>
                          <sector.icon className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="font-medium">{sector.name}</div>
                          <div className="text-sm text-muted-foreground">{sector.count} rapport{sector.count > 1 ? 's' : ''}</div>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-muted-foreground" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Types de rapports */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Types de Rapports
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {REPORT_TYPES.map((type) => (
                    <div 
                      key={type.id}
                      className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                      onClick={() => onReportTypeSelect(type.id)}
                    >
                      <div className="flex items-center gap-3">
                        <type.icon className="w-4 h-4 text-muted-foreground" />
                        <div className="font-medium">{type.name}</div>
                      </div>
                      <Badge variant="secondary">
                        {reports.filter(r => type.id === 'all' || r.report_type === type.id).length}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="companies" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Entreprises Cotées ({CASABLANCA_COMPANIES.length} entreprises)</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <ScrollArea className="h-[500px]">
                <div className="divide-y">
                  {allCompaniesWithReports.map((company) => (
                    <div 
                      key={company.symbol} 
                      className="flex items-center justify-between gap-3 px-4 py-3 hover:bg-muted/50 cursor-pointer transition-colors"
                      onClick={() => handleCompanyClick(company.symbol)}
                    >
                      <div className="flex items-center gap-3">
                        <Avatar className="h-10 w-10">
                          {company.logo ? (
                            <img 
                              src={company.logo} 
                              alt={`Logo ${company.name}`}
                              className="w-full h-full object-contain"
                            />
                          ) : (
                            <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                              {company.symbol.split(':')[1]?.substring(0, 2) || 'CO'}
                            </AvatarFallback>
                          )}
                        </Avatar>
                        <div className="flex-1">
                          <div className="font-medium">{company.name}</div>
                          <div className="text-sm text-muted-foreground">{company.symbol}</div>
                          <div className="text-xs text-muted-foreground">{company.sector}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant="secondary">{company.reportCount} rapport{company.reportCount > 1 ? 's' : ''}</Badge>
                        <Badge variant="outline" className="text-xs">
                          {company.marketCap}
                        </Badge>
                        <ChevronRight className="w-4 h-4 text-muted-foreground" />
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sectors" className="mt-6">
          {selectedSector && selectedSector !== 'all' ? (
            <SectorReports 
              reports={reportsBySector[selectedSector] || []}
              sector={selectedSector}
              onOpen={onOpen}
              onDownload={onDownload}
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {sectorsWithCounts.map((sector) => (
                <Card 
                  key={sector.id}
                  className="cursor-pointer hover:shadow-lg transition-all"
                  onClick={() => onSectorSelect(sector.id)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`p-3 rounded-lg ${sector.color}`}>
                          <sector.icon className="w-6 h-6" />
                        </div>
                        <div>
                          <CardTitle className="text-lg">{sector.name}</CardTitle>
                          <div className="text-sm text-muted-foreground">{sector.count} rapport{sector.count > 1 ? 's' : ''}</div>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-muted-foreground" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-sm text-muted-foreground">
                      Cliquez pour voir les rapports de ce secteur
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
