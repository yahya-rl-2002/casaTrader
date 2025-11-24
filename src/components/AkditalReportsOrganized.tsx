import React from 'react';
import { Tables } from '@/integrations/supabase/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { 
  Building2, 
  FileText, 
  Download, 
  ExternalLink, 
  Calendar,
  Tag,
  Star,
  TrendingUp,
  Clock,
  Award,
  BarChart3,
  PieChart,
  ArrowLeft,
  ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface AkditalReportsOrganizedProps {
  reports: Tables<'financial_reports'>[];
  companyName: string;
  companySymbol: string;
  onOpen: (url: string) => void;
  onDownload: (url: string, fileName: string) => void;
  onBack: () => void;
}

export const AkditalReportsOrganized: React.FC<AkditalReportsOrganizedProps> = ({
  reports,
  companyName,
  companySymbol,
  onOpen,
  onDownload,
  onBack
}) => {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Date inconnue';
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getReportTypeInfo = (type: string) => {
    const types: { [key: string]: { label: string; icon: any; color: string; bgColor: string } } = {
      'rapport-annuel': { 
        label: 'Rapport Annuel', 
        icon: Award, 
        color: 'text-blue-600', 
        bgColor: 'bg-blue-50 border-blue-200' 
      },
      'rapport-semestriel': { 
        label: 'Rapport Semestriel', 
        icon: BarChart3, 
        color: 'text-green-600', 
        bgColor: 'bg-green-50 border-green-200' 
      },
      'rapport-trimestriel': { 
        label: 'Rapport Trimestriel', 
        icon: PieChart, 
        color: 'text-orange-600', 
        bgColor: 'bg-orange-50 border-orange-200' 
      },
      'resultats': { 
        label: 'Résultats', 
        icon: TrendingUp, 
        color: 'text-purple-600', 
        bgColor: 'bg-purple-50 border-purple-200' 
      },
      'communique': { 
        label: 'Communiqué', 
        icon: FileText, 
        color: 'text-gray-600', 
        bgColor: 'bg-gray-50 border-gray-200' 
      },
      'autre': { 
        label: 'Autre', 
        icon: FileText, 
        color: 'text-gray-600', 
        bgColor: 'bg-gray-50 border-gray-200' 
      }
    };
    return types[type] || types['autre'];
  };

  // Organiser les rapports par année
  const reportsByYear = reports.reduce((acc, report) => {
    const year = report.published_at ? new Date(report.published_at).getFullYear() : 'Inconnue';
    if (!acc[year]) {
      acc[year] = [];
    }
    acc[year].push(report);
    return acc;
  }, {} as Record<string, Tables<'financial_reports'>[]>);

  // Trier les années par ordre décroissant
  const sortedYears = Object.keys(reportsByYear).sort((a, b) => {
    if (a === 'Inconnue') return 1;
    if (b === 'Inconnue') return -1;
    return parseInt(b) - parseInt(a);
  });

  // Statistiques par année
  const getYearStats = (yearReports: Tables<'financial_reports'>[]) => {
    const annualReports = yearReports.filter(r => r.report_type === 'rapport-annuel').length;
    const semestrialReports = yearReports.filter(r => r.report_type === 'rapport-semestriel').length;
    const quarterlyReports = yearReports.filter(r => r.report_type === 'rapport-trimestriel').length;
    const otherReports = yearReports.filter(r => !['rapport-annuel', 'rapport-semestriel', 'rapport-trimestriel'].includes(r.report_type)).length;
    
    return { annualReports, semestrialReports, quarterlyReports, otherReports };
  };

  return (
    <div className="space-y-8">
      {/* Header avec bouton retour */}
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={onBack} className="flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" />
          Retour
        </Button>
        <div className="flex items-center gap-3">
          <Avatar className="h-12 w-12">
            <AvatarFallback className="bg-primary/10 text-primary font-semibold text-lg">
              {companySymbol.split(':')[1]?.substring(0, 2) || 'CO'}
            </AvatarFallback>
          </Avatar>
          <div>
            <h1 className="text-2xl font-bold">{companyName}</h1>
            <p className="text-muted-foreground">{companySymbol}</p>
          </div>
        </div>
      </div>

      {/* Statistiques globales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-500 rounded-lg">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-blue-700 font-medium">Total Rapports</p>
                <p className="text-2xl font-bold text-blue-900">{reports.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-500 rounded-lg">
                <Award className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-green-700 font-medium">Rapports Annuels</p>
                <p className="text-2xl font-bold text-green-900">
                  {reports.filter(r => r.report_type === 'rapport-annuel').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-r from-orange-50 to-orange-100 border-orange-200">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-500 rounded-lg">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-orange-700 font-medium">Rapports Semestriels</p>
                <p className="text-2xl font-bold text-orange-900">
                  {reports.filter(r => r.report_type === 'rapport-semestriel').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-500 rounded-lg">
                <TrendingUp className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-purple-700 font-medium">Téléchargements</p>
                <p className="text-2xl font-bold text-purple-900">
                  {reports.reduce((sum, r) => sum + (r.download_count || 0), 0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Rapports organisés par année */}
      <div className="space-y-8">
        <h2 className="text-2xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Rapports Financiers par Année
        </h2>
        
        {reports.length === 0 ? (
          <Card className="border-dashed">
            <CardContent className="p-12 text-center">
              <FileText className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">Aucun rapport disponible</h3>
              <p className="text-muted-foreground">Aucun rapport financier trouvé pour {companyName}</p>
            </CardContent>
          </Card>
        ) : (
          sortedYears.map((year) => {
            const yearReports = reportsByYear[year];
            const stats = getYearStats(yearReports);
            
            return (
              <div key={year} className="space-y-4">
                {/* En-tête de l'année */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl text-white">
                      <Calendar className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold">{year}</h3>
                      <p className="text-muted-foreground">{yearReports.length} rapport{yearReports.length > 1 ? 's' : ''}</p>
                    </div>
                  </div>
                  
                  {/* Statistiques de l'année */}
                  <div className="flex gap-2">
                    {stats.annualReports > 0 && (
                      <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                        {stats.annualReports} Annuel{stats.annualReports > 1 ? 's' : ''}
                      </Badge>
                    )}
                    {stats.semestrialReports > 0 && (
                      <Badge variant="secondary" className="bg-green-100 text-green-800">
                        {stats.semestrialReports} Semestriel{stats.semestrialReports > 1 ? 's' : ''}
                      </Badge>
                    )}
                    {stats.quarterlyReports > 0 && (
                      <Badge variant="secondary" className="bg-orange-100 text-orange-800">
                        {stats.quarterlyReports} Trimestriel{stats.quarterlyReports > 1 ? 's' : ''}
                      </Badge>
                    )}
                    {stats.otherReports > 0 && (
                      <Badge variant="secondary" className="bg-gray-100 text-gray-800">
                        {stats.otherReports} Autre{stats.otherReports > 1 ? 's' : ''}
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Rapports de l'année */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {yearReports.map((report) => {
                    const typeInfo = getReportTypeInfo(report.report_type);
                    const IconComponent = typeInfo.icon;
                    
                    return (
                      <Card key={report.id} className="hover:shadow-xl transition-all duration-300 cursor-pointer group border-2 hover:border-primary/20">
                        <CardHeader className="pb-3">
                          <div className="flex items-start justify-between">
                            <div className="flex items-center gap-3">
                              <div className={cn("p-3 rounded-xl border-2", typeInfo.bgColor)}>
                                <IconComponent className={cn("w-6 h-6", typeInfo.color)} />
                              </div>
                              <div className="flex-1">
                                <CardTitle className="text-base leading-tight line-clamp-2 group-hover:text-primary transition-colors">
                                  {report.title}
                                </CardTitle>
                                <div className="flex items-center gap-2 mt-2">
                                  <Badge 
                                    variant="secondary" 
                                    className={cn("text-xs font-medium", typeInfo.bgColor, typeInfo.color)}
                                  >
                                    {typeInfo.label}
                                  </Badge>
                                  {report.featured && (
                                    <Badge variant="outline" className="text-xs border-yellow-300 text-yellow-700">
                                      <Star className="w-3 h-3 mr-1 fill-current" />
                                      À la une
                                    </Badge>
                                  )}
                                </div>
                              </div>
                            </div>
                          </div>
                        </CardHeader>
                        
                        <CardContent className="pt-0">
                          {report.description && (
                            <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
                              {report.description}
                            </p>
                          )}
                          
                          <div className="space-y-2 mb-4">
                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                              <Clock className="w-3 h-3" />
                              <span>Publié: {formatDate(report.published_at)}</span>
                            </div>
                            
                            {report.period_start && report.period_end && (
                              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                <Calendar className="w-3 h-3" />
                                <span>
                                  Période: {formatDate(report.period_start)} - {formatDate(report.period_end)}
                                </span>
                              </div>
                            )}
                          </div>
                          
                          {report.tags && report.tags.length > 0 && (
                            <div className="flex flex-wrap gap-1 mb-4">
                              {report.tags.slice(0, 3).map((tag, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  <Tag className="w-2 h-2 mr-1" />
                                  {tag}
                                </Badge>
                              ))}
                              {report.tags.length > 3 && (
                                <Badge variant="outline" className="text-xs">
                                  +{report.tags.length - 3}
                                </Badge>
                              )}
                            </div>
                          )}
                          
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              onClick={() => onOpen(report.file_url || '')}
                              className="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
                            >
                              <ExternalLink className="w-4 h-4 mr-2" />
                              Ouvrir
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => onDownload(report.file_url || '', report.file_name || '')}
                              className="flex-1 border-primary/20 hover:bg-primary/5"
                            >
                              <Download className="w-4 h-4 mr-2" />
                              Télécharger
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
                
                {year !== sortedYears[sortedYears.length - 1] && (
                  <Separator className="my-8" />
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};




















