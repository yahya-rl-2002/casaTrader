import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  FileText, 
  Download, 
  ExternalLink, 
  Building2, 
  Calendar,
  HardDrive,
  TrendingUp,
  Star,
  Tag
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface StoredPdf {
  id: string;
  company: string;
  symbol: string;
  title: string;
  type: string;
  fileUrl: string;
  fileName: string;
  fileSize: number;
  fileType: string;
  publishedAt: string;
  downloadCount: number;
  featured: boolean;
  tags: string[];
}

interface StoredPdfsViewProps {
  stats: {
    totalReports: number;
    reportsWithFiles: number;
    reportsWithoutFiles: number;
    companiesWithFiles: number;
    fileTypes: number;
    totalFileSize: number;
    averageFileSize: number;
  };
  byCompany: { [key: string]: StoredPdf[] };
  byFileType: { [key: string]: StoredPdf[] };
  fileDetails: StoredPdf[];
  onOpen: (url: string) => void;
  onDownload: (url: string, fileName: string) => void;
  onClose: () => void;
}

export const StoredPdfsView: React.FC<StoredPdfsViewProps> = ({
  stats,
  byCompany,
  byFileType,
  fileDetails,
  onOpen,
  onDownload,
  onClose
}) => {
  const formatFileSize = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getFileTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'application/pdf': 'bg-red-100 text-red-800',
      'application/msword': 'bg-blue-100 text-blue-800',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'bg-blue-100 text-blue-800',
      'application/vnd.ms-excel': 'bg-green-100 text-green-800',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'bg-green-100 text-green-800',
      'inconnu': 'bg-gray-100 text-gray-800'
    };
    return colors[type] || colors['inconnu'];
  };

  return (
    <div className="space-y-6">
      {/* Header avec bouton fermer */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-lg bg-primary/10">
            <HardDrive className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">PDF Stockés - Akdital</h1>
            <p className="text-muted-foreground">Analyse des fichiers téléchargés et stockés pour l'entreprise Akdital</p>
          </div>
        </div>
        <Button variant="outline" onClick={onClose}>
          ✕ Fermer
        </Button>
      </div>

      {/* Statistiques globales */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-600" />
              <div>
                <p className="text-sm text-muted-foreground">Rapports Akdital</p>
                <p className="text-2xl font-bold">{stats.akditalReports || stats.totalReports}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Download className="w-5 h-5 text-green-600" />
              <div>
                <p className="text-sm text-muted-foreground">Avec PDF</p>
                <p className="text-2xl font-bold">{stats.reportsWithFiles}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Building2 className="w-5 h-5 text-purple-600" />
              <div>
                <p className="text-sm text-muted-foreground">Akdital</p>
                <p className="text-2xl font-bold">{stats.isAllAkdital ? '100%' : 'Mix'}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <HardDrive className="w-5 h-5 text-orange-600" />
              <div>
                <p className="text-sm text-muted-foreground">Taille Totale</p>
                <p className="text-2xl font-bold">{formatFileSize(stats.totalFileSize)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* PDF par entreprise */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Building2 className="w-5 h-5" />
            PDF Akdital
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[300px]">
            <div className="space-y-3">
              {Object.entries(byCompany).map(([company, pdfs]) => (
                <div key={company} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                        {company.substring(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <div className="font-medium">{company}</div>
                      <div className="text-sm text-muted-foreground">
                        {pdfs.length} PDF • {formatFileSize(pdfs.reduce((sum, pdf) => sum + pdf.fileSize, 0))}
                      </div>
                    </div>
                  </div>
                  <Badge variant="secondary">{pdfs.length}</Badge>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* PDF par type de fichier */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Tag className="w-5 h-5" />
            PDF par Type de Fichier
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(byFileType).map(([fileType, pdfs]) => (
              <div key={fileType} className="p-4 border rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <Badge className={getFileTypeColor(fileType)}>
                    {fileType === 'application/pdf' ? 'PDF' : 
                     fileType.includes('word') ? 'Word' :
                     fileType.includes('excel') ? 'Excel' : 'Autre'}
                  </Badge>
                  <span className="text-sm font-medium">{pdfs.length} fichiers</span>
                </div>
                <div className="text-sm text-muted-foreground">
                  Taille: {formatFileSize(pdfs.reduce((sum, pdf) => sum + pdf.fileSize, 0))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Liste détaillée des PDF */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Détails des PDF Akdital Stockés
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[400px]">
            <div className="space-y-3">
              {fileDetails.map((pdf) => (
                <div key={pdf.id} className="p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h4 className="font-medium line-clamp-1">{pdf.title}</h4>
                        {pdf.featured && (
                          <Badge variant="outline" className="text-xs">
                            <Star className="w-3 h-3 mr-1" />
                            À la une
                          </Badge>
                        )}
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm text-muted-foreground mb-2">
                        <span className="flex items-center gap-1">
                          <Building2 className="w-3 h-3" />
                          {pdf.company}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {formatDate(pdf.publishedAt)}
                        </span>
                        <span className="flex items-center gap-1">
                          <Download className="w-3 h-3" />
                          {pdf.downloadCount} téléchargements
                        </span>
                      </div>
                      
                      <div className="flex items-center gap-2 text-xs">
                        <Badge variant="outline">{pdf.type}</Badge>
                        <span className="text-muted-foreground">
                          {pdf.fileName} • {formatFileSize(pdf.fileSize)}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex gap-2 ml-4">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => onOpen(pdf.fileUrl)}
                      >
                        <ExternalLink className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => onDownload(pdf.fileUrl, pdf.fileName)}
                      >
                        <Download className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
};
