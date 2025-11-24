import React from 'react';
import { Tables } from '@/integrations/supabase/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { 
  Building2, 
  FileText, 
  Download, 
  ExternalLink, 
  Calendar,
  Tag,
  Star,
  TrendingUp
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface CompanyReportsProps {
  reports: Tables<'financial_reports'>[];
  companyName: string;
  companySymbol: string;
  onOpen: (url: string) => void;
  onDownload: (url: string, fileName: string) => void;
  onBack: () => void;
}

export const CompanyReports: React.FC<CompanyReportsProps> = ({
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

  const formatFileSize = (bytes: number | null) => {
    if (!bytes) return 'Taille inconnue';
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const getReportTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'rapport-annuel': 'bg-blue-100 text-blue-800',
      'rapport-trimestriel': 'bg-green-100 text-green-800',
      'rapport-semestriel': 'bg-yellow-100 text-yellow-800',
      'communique': 'bg-purple-100 text-purple-800',
      'presentation': 'bg-pink-100 text-pink-800',
      'autre': 'bg-gray-100 text-gray-800'
    };
    return colors[type] || colors['autre'];
  };

  const getReportTypeIcon = (type: string) => {
    switch (type) {
      case 'rapport-annuel': return TrendingUp;
      case 'rapport-trimestriel': return Calendar;
      case 'rapport-semestriel': return Calendar;
      case 'communique': return FileText;
      case 'presentation': return FileText;
      default: return FileText;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header avec bouton retour */}
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={onBack} className="flex items-center gap-2">
          ← Retour
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

      {/* Statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-600" />
              <div>
                <p className="text-sm text-muted-foreground">Total Rapports</p>
                <p className="text-2xl font-bold">{reports.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Star className="w-5 h-5 text-yellow-600" />
              <div>
                <p className="text-sm text-muted-foreground">À la une</p>
                <p className="text-2xl font-bold">
                  {reports.filter(r => r.featured).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-green-600" />
              <div>
                <p className="text-sm text-muted-foreground">Téléchargements</p>
                <p className="text-2xl font-bold">
                  {reports.reduce((sum, r) => sum + (r.download_count || 0), 0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Liste des rapports */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Rapports Financiers</h2>
        
        {reports.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <FileText className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-muted-foreground">Aucun rapport disponible pour {companyName}</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {reports.map((report) => {
              const IconComponent = getReportTypeIcon(report.report_type);
              
              return (
                <Card key={report.id} className="hover:shadow-lg transition-all cursor-pointer group">
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-primary/10">
                          <IconComponent className="w-5 h-5 text-primary" />
                        </div>
                        <div className="flex-1">
                          <CardTitle className="text-base leading-tight line-clamp-2">
                            {report.title}
                          </CardTitle>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge 
                              variant="secondary" 
                              className={cn("text-xs", getReportTypeColor(report.report_type))}
                            >
                              {report.report_type.replace('-', ' ')}
                            </Badge>
                            {report.featured && (
                              <Badge variant="outline" className="text-xs">
                                <Star className="w-3 h-3 mr-1" />
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
                      <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                        {report.description}
                      </p>
                    )}
                    
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <Calendar className="w-3 h-3" />
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
                      
                      {report.file_size && (
                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <FileText className="w-3 h-3" />
                          <span>{formatFileSize(report.file_size)}</span>
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
                        className="flex-1"
                      >
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Ouvrir
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => onDownload(report.file_url || '', report.file_name || '')}
                        className="flex-1"
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
        )}
      </div>
    </div>
  );
};




















