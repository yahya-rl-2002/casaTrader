import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import { CASEMA_SYMBOLS } from "@/data/casema-symbols";
import { Upload, FileText, Calendar, Building2, Tag, X } from "lucide-react";
import { cn } from "@/lib/utils";

type ReportType = "rapport-annuel" | "resultats" | "communique" | "profit-warning" | "autre";

interface FinancialReportUploadProps {
  onUploadSuccess?: () => void;
}

export function FinancialReportUpload({ onUploadSuccess }: FinancialReportUploadProps) {
  const { toast } = useToast();
  const [isOpen, setIsOpen] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [tags, setTags] = useState<string[]>([]);
  const [newTag, setNewTag] = useState("");

  const [formData, setFormData] = useState({
    companySymbol: "",
    companyName: "",
    reportType: "" as ReportType | "",
    title: "",
    description: "",
    publishedAt: "",
    periodStart: "",
    periodEnd: "",
    featured: false,
  });

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Vérifier la taille du fichier (max 50MB)
      if (file.size > 50 * 1024 * 1024) {
        toast({
          title: "Fichier trop volumineux",
          description: "La taille maximale autorisée est de 50MB.",
          variant: "destructive",
        });
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleCompanyChange = (symbol: string) => {
    const company = CASEMA_SYMBOLS.find(c => c.value === symbol);
    setFormData(prev => ({
      ...prev,
      companySymbol: symbol,
      companyName: company?.label || "",
    }));
  };

  const addTag = () => {
    if (newTag.trim() && !tags.includes(newTag.trim())) {
      setTags(prev => [...prev, newTag.trim()]);
      setNewTag("");
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(prev => prev.filter(tag => tag !== tagToRemove));
  };

  const uploadFile = async (file: File): Promise<string> => {
    const fileExt = file.name.split('.').pop();
    const fileName = `${Date.now()}-${Math.random().toString(36).substring(2)}.${fileExt}`;
    const filePath = `financial-reports/${fileName}`;

    const { error: uploadError } = await supabase.storage
      .from('documents')
      .upload(filePath, file);

    if (uploadError) {
      throw new Error(`Erreur d'upload: ${uploadError.message}`);
    }

    const { data } = supabase.storage
      .from('documents')
      .getPublicUrl(filePath);

    return data.publicUrl;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFile) {
      toast({
        title: "Fichier requis",
        description: "Veuillez sélectionner un fichier à uploader.",
        variant: "destructive",
      });
      return;
    }

    if (!formData.companySymbol || !formData.reportType || !formData.title) {
      toast({
        title: "Champs requis",
        description: "Veuillez remplir tous les champs obligatoires.",
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);

    try {
      // Upload du fichier
      const fileUrl = await uploadFile(selectedFile);

      // Insertion en base de données
      const { error } = await supabase
        .from('financial_reports')
        .insert({
          company_symbol: formData.companySymbol,
          company_name: formData.companyName,
          report_type: formData.reportType,
          title: formData.title,
          description: formData.description || null,
          file_url: fileUrl,
          file_name: selectedFile.name,
          file_size: selectedFile.size,
          file_type: selectedFile.type,
          published_at: formData.publishedAt || null,
          period_start: formData.periodStart || null,
          period_end: formData.periodEnd || null,
          tags: tags.length > 0 ? tags : null,
          featured: formData.featured,
        });

      if (error) {
        throw new Error(`Erreur de sauvegarde: ${error.message}`);
      }

      toast({
        title: "Rapport ajouté avec succès",
        description: "Le rapport financier a été uploadé et enregistré.",
      });

      // Reset form
      setFormData({
        companySymbol: "",
        companyName: "",
        reportType: "",
        title: "",
        description: "",
        publishedAt: "",
        periodStart: "",
        periodEnd: "",
        featured: false,
      });
      setSelectedFile(null);
      setTags([]);
      setIsOpen(false);
      onUploadSuccess?.();

    } catch (error) {
      console.error('Erreur upload:', error);
      toast({
        title: "Erreur d'upload",
        description: error instanceof Error ? error.message : "Une erreur inattendue s'est produite.",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button>
          <Upload className="w-4 h-4 mr-2" />
          Ajouter un rapport
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Ajouter un rapport financier
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Upload de fichier */}
          <div className="space-y-2">
            <Label htmlFor="file">Fichier du rapport *</Label>
            <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
              <input
                id="file"
                type="file"
                accept=".pdf,.doc,.docx,.xls,.xlsx"
                onChange={handleFileSelect}
                className="hidden"
              />
              <label htmlFor="file" className="cursor-pointer">
                {selectedFile ? (
                  <div className="space-y-2">
                    <FileText className="w-8 h-8 mx-auto text-primary" />
                    <p className="font-medium">{selectedFile.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Upload className="w-8 h-8 mx-auto text-muted-foreground" />
                    <p className="font-medium">Cliquez pour sélectionner un fichier</p>
                    <p className="text-sm text-muted-foreground">
                      PDF, DOC, DOCX, XLS, XLSX (max 50MB)
                    </p>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* Informations de base */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="company">Société *</Label>
              <Select value={formData.companySymbol} onValueChange={handleCompanyChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner une société" />
                </SelectTrigger>
                <SelectContent>
                  {CASEMA_SYMBOLS.map((company) => (
                    <SelectItem key={company.value} value={company.value}>
                      <div className="flex items-center gap-2">
                        <Building2 className="w-4 h-4" />
                        {company.label}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="reportType">Type de rapport *</Label>
              <Select value={formData.reportType} onValueChange={(value) => setFormData(prev => ({ ...prev, reportType: value as ReportType }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner le type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rapport-annuel">Rapport annuel</SelectItem>
                  <SelectItem value="resultats">Résultats</SelectItem>
                  <SelectItem value="communique">Communiqué</SelectItem>
                  <SelectItem value="profit-warning">Profit warning</SelectItem>
                  <SelectItem value="autre">Autre</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="title">Titre du rapport *</Label>
            <Input
              id="title"
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              placeholder="Ex: Résultats semestriels 2025"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="Description optionnelle du rapport..."
              rows={3}
            />
          </div>

          {/* Période */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="publishedAt">Date de publication</Label>
              <Input
                id="publishedAt"
                type="date"
                value={formData.publishedAt}
                onChange={(e) => setFormData(prev => ({ ...prev, publishedAt: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="periodStart">Début de période</Label>
              <Input
                id="periodStart"
                type="date"
                value={formData.periodStart}
                onChange={(e) => setFormData(prev => ({ ...prev, periodStart: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="periodEnd">Fin de période</Label>
              <Input
                id="periodEnd"
                type="date"
                value={formData.periodEnd}
                onChange={(e) => setFormData(prev => ({ ...prev, periodEnd: e.target.value }))}
              />
            </div>
          </div>

          {/* Tags */}
          <div className="space-y-2">
            <Label>Tags</Label>
            <div className="flex gap-2">
              <Input
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                placeholder="Ajouter un tag..."
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
              />
              <Button type="button" variant="outline" onClick={addTag}>
                <Tag className="w-4 h-4" />
              </Button>
            </div>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {tags.map((tag) => (
                  <Badge key={tag} variant="secondary" className="flex items-center gap-1">
                    {tag}
                    <X
                      className="w-3 h-3 cursor-pointer hover:text-destructive"
                      onClick={() => removeTag(tag)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Options */}
          <div className="flex items-center space-x-2">
            <input
              id="featured"
              type="checkbox"
              checked={formData.featured}
              onChange={(e) => setFormData(prev => ({ ...prev, featured: e.target.checked }))}
              className="rounded"
            />
            <Label htmlFor="featured">Mettre en avant (à la une)</Label>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>
              Annuler
            </Button>
            <Button type="submit" disabled={isUploading}>
              {isUploading ? "Upload en cours..." : "Ajouter le rapport"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}



