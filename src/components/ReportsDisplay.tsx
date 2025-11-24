import { useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { 
  Calendar, 
  Download, 
  ExternalLink, 
  Star, 
  Building2, 
  Tag, 
  TrendingUp,
  FileText,
  Globe,
  AlertTriangle,
  Clock
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { Tables } from "@/integrations/supabase/types";

interface ReportsDisplayProps {
  reports: Tables<'financial_reports'>[];
  viewMode: 'grid' | 'list';
  onOpen: (report: Tables<'financial_reports'>) => void;
  onDownload: (report: Tables<'financial_reports'>) => void;
}

export function ReportsDisplay({ reports, viewMode, onOpen, onDownload }: ReportsDisplayProps) {
  
  const getReportTypeIcon = (type: string) => {
    const icons: { [key: string]: any } = {
      'rapport-annuel': { icon: FileText, color: 'bg-blue-100 text-blue-800 border-blue-200' },
      'resultats': { icon: TrendingUp, color: 'bg-green-100 text-green-800 border-green-200' },
      'communique': { icon: Globe, color: 'bg-purple-100 text-purple-800 border-purple-200' },
      'profit-warning': { icon: AlertTriangle, color: 'bg-red-100 text-red-800 border-red-200' },
      'autre': { icon: FileText, color: 'bg-gray-100 text-gray-800 border-gray-200' }
    };
    return icons[type] || icons['autre'];
  };

  const getReportTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      'rapport-annuel': 'Rapport Annuel',
      'resultats': 'Résultats',
      'communique': 'Communiqué',
      'profit-warning': 'Profit Warning',
      'autre': 'Autre'
    };
    return labels[type] || 'Autre';
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
  };

  const getTimeAgo = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffInDays === 0) return 'Aujourd\'hui';
    if (diffInDays === 1) return 'Hier';
    if (diffInDays < 7) return `Il y a ${diffInDays} jours`;
    if (diffInDays < 30) return `Il y a ${Math.floor(diffInDays / 7)} semaine${Math.floor(diffInDays / 7) > 1 ? 's' : ''}`;
    if (diffInDays < 365) return `Il y a ${Math.floor(diffInDays / 30)} mois`;
    return `Il y a ${Math.floor(diffInDays / 365)} an${Math.floor(diffInDays / 365) > 1 ? 's' : ''}`;
  };

  const initialsFromName = (name: string) => {
    // Utiliser le nom tel quel (plus de remplacement nécessaire)
    const displayName = name;
    const parts = displayName.replace(/[^A-Za-zÀ-ÿ0-9 ]/g, "").trim().split(/\s+/);
    const first = parts[0]?.[0] || "A";
    const last = parts[1]?.[0] || parts[0]?.[1] || "K";
    return (first + last).toUpperCase();
  };

  if (reports.length === 0) {
    return (
      <Card>
        <CardContent className="p-8 text-center text-muted-foreground">
          <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <div className="text-lg font-medium mb-2">Aucun rapport trouvé</div>
          <div className="text-sm">Essayez de modifier vos filtres de recherche</div>
        </CardContent>
      </Card>
    );
  }

  if (viewMode === 'grid') {
    return (
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map((report) => {
          const typeInfo = getReportTypeIcon(report.report_type || 'autre');
          const TypeIcon = typeInfo.icon;
          
          return (
            <Card key={report.id} className="hover:shadow-lg transition-all duration-200 group">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                        {initialsFromName(report.company_name || '')}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium leading-tight truncate">
                        {report.company_name}
                      </div>
                      <div className="text-xs text-muted-foreground flex items-center gap-1">
                        <Building2 className="w-3 h-3" />
                        {report.company_symbol}
                      </div>
                    </div>
                  </div>
                  <Badge className={cn("flex items-center gap-1", typeInfo.color)}>
                    <TypeIcon className="w-3 h-3" />
                    {getReportTypeLabel(report.report_type || 'autre')}
                  </Badge>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div>
                  <div className="text-base font-semibold leading-snug line-clamp-2 mb-2">
                    {report.title}
                  </div>
                  {report.file_name && report.file_name !== report.title && (
                    <div className="text-xs text-muted-foreground mb-1 line-clamp-1" title={report.file_name}>
                      📄 {report.file_name}
                    </div>
                  )}
                  {report.description && (
                    <div className="text-sm text-muted-foreground line-clamp-2">
                      {report.description}
                    </div>
                  )}
                </div>

                <div className="space-y-2">
                  {report.published_at && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <Calendar className="w-3.5 h-3.5" />
                      <span>{new Date(report.published_at).toLocaleDateString()}</span>
                      <span>•</span>
                      <span>{getTimeAgo(report.published_at)}</span>
                    </div>
                  )}
                  
                  {report.file_size && (
                    <div className="text-xs text-muted-foreground">
                      {formatFileSize(report.file_size)}
                    </div>
                  )}
                  
                  {report.download_count > 0 && (
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Download className="w-3 h-3" />
                      {report.download_count} téléchargement{report.download_count > 1 ? 's' : ''}
                    </div>
                  )}
                </div>

                {report.tags && report.tags.length > 0 && (
                  <div className="flex items-center gap-2 flex-wrap">
                    <Tag className="w-3.5 h-3.5 text-muted-foreground" />
                    {report.tags.slice(0, 3).map((tag) => (
                      <Badge key={tag} variant="outline" className="text-[11px]">
                        {tag}
                      </Badge>
                    ))}
                    {report.tags.length > 3 && (
                      <Badge variant="outline" className="text-[11px]">
                        +{report.tags.length - 3}
                      </Badge>
                    )}
                  </div>
                )}

                <Separator />

                <div className="flex items-center justify-between">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={() => onOpen(report)}
                    className="flex-1 mr-2"
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Voir
                  </Button>
                  <Button 
                    size="sm" 
                    onClick={() => onDownload(report)}
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
    );
  }

  // Vue liste
  return (
    <div className="space-y-4">
      {reports.map((report) => {
        const typeInfo = getReportTypeIcon(report.report_type || 'autre');
        const TypeIcon = typeInfo.icon;
        
        return (
          <Card key={report.id} className="hover:shadow-md transition-all duration-200 group">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1 min-w-0">
                  <Avatar className="h-12 w-12">
                    <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                      {initialsFromName(report.company_name || '')}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1">
                      <div className="font-medium truncate">{report.title}</div>
                      {report.featured && (
                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                      )}
                    </div>
                    
                    <div className="text-sm text-muted-foreground mb-2">
                      {report.company_name} • {report.company_symbol}
                    </div>
                    
                    {report.description && (
                      <div className="text-sm text-muted-foreground line-clamp-1 mb-2">
                        {report.description}
                      </div>
                    )}
                    
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      {report.published_at && (
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {new Date(report.published_at).toLocaleDateString()}
                        </div>
                      )}
                      
                      {report.download_count > 0 && (
                        <div className="flex items-center gap-1">
                          <Download className="w-3 h-3" />
                          {report.download_count} téléchargement{report.download_count > 1 ? 's' : ''}
                        </div>
                      )}
                      
                      {report.file_size && (
                        <div>{formatFileSize(report.file_size)}</div>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <Badge className={cn("flex items-center gap-1", typeInfo.color)}>
                    <TypeIcon className="w-3 h-3" />
                    {getReportTypeLabel(report.report_type || 'autre')}
                  </Badge>
                  
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" onClick={() => onOpen(report)}>
                      <ExternalLink className="w-4 h-4 mr-2" />
                      Voir
                    </Button>
                    <Button size="sm" onClick={() => onDownload(report)}>
                      <Download className="w-4 h-4 mr-2" />
                      Télécharger
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
