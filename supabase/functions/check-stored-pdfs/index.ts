import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Create Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    console.log('🔍 Vérification des PDF stockés pour Akdital...');

    // Utiliser les fonctions RPC spécialisées pour Akdital
    const { data: stats, error: statsError } = await supabase.rpc('get_akdital_stats');
    const { data: byCompany, error: byCompanyError } = await supabase.rpc('get_akdital_by_company');
    const { data: byFileType, error: byFileTypeError } = await supabase.rpc('get_akdital_by_file_type');

    if (statsError || byCompanyError || byFileTypeError) {
      console.error('❌ Erreur lors de la récupération des statistiques Akdital:', { statsError, byCompanyError, byFileTypeError });
      return new Response(
        JSON.stringify({ 
          success: false, 
          error: `Erreur statistiques: ${statsError?.message || byCompanyError?.message || byFileTypeError?.message}` 
        }),
        { 
          status: 500, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }

    console.log(`📊 Statistiques Akdital récupérées:`, stats);

    // Récupérer les détails des rapports pour l'affichage
    const { data: reports, error: reportsError } = await supabase
      .from('financial_reports')
      .select('*')
      .or('company_name.eq.Akdital,company_name.eq.Société Inconnue,company_symbol.eq.CSEMA:AKDITAL,company_symbol.eq.CSEMA:UNKNOWN')
      .order('created_at', { ascending: false });

    if (reportsError) {
      console.error('❌ Erreur lors de la récupération des rapports:', reportsError);
      return new Response(
        JSON.stringify({ 
          success: false, 
          error: reportsError.message 
        }),
        { 
          status: 500, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }

    console.log(`📊 Total des rapports Akdital trouvés: ${reports?.length || 0}`);

    // Analyser les rapports avec fichiers (tous d'Akdital)
    const reportsWithFiles = reports?.filter(report => report.file_url) || [];
    const reportsWithoutFiles = reports?.filter(report => !report.file_url) || [];

    // Utiliser les données des fonctions RPC
    const statsData = stats?.[0] || {};
    const companyData = byCompany || [];
    const fileTypeData = byFileType || [];

    // Convertir les données RPC en format attendu par le frontend
    const byCompanyFormatted: { [key: string]: any[] } = {};
    companyData.forEach((company: any) => {
      byCompanyFormatted[company.company_name] = reports?.filter(r => r.company_name === company.company_name) || [];
    });

    const byFileTypeFormatted: { [key: string]: any[] } = {};
    fileTypeData.forEach((fileType: any) => {
      byFileTypeFormatted[fileType.file_type] = reports?.filter(r => r.file_type === fileType.file_type) || [];
    });

    // Statistiques détaillées (depuis les fonctions RPC)
    const stats = {
      totalReports: Number(statsData.total_reports || 0),
      akditalReports: Number(statsData.akdital_reports || 0),
      reportsWithFiles: Number(statsData.reports_with_files || 0),
      reportsWithoutFiles: Number(statsData.reports_without_files || 0),
      companiesWithFiles: Number(statsData.companies_count || 0),
      fileTypes: Number(statsData.file_types_count || 0),
      totalFileSize: Number(statsData.total_file_size || 0),
      averageFileSize: Number(statsData.average_file_size || 0),
      isAllAkdital: Boolean(statsData.is_all_akdital)
    };

    // Détails des rapports avec fichiers
    const fileDetails = reportsWithFiles.map(report => ({
      id: report.id,
      company: report.company_name,
      symbol: report.company_symbol,
      title: report.title,
      type: report.report_type,
      fileUrl: report.file_url,
      fileName: report.file_name,
      fileSize: report.file_size,
      fileType: report.file_type,
      publishedAt: report.published_at,
      downloadCount: report.download_count,
      featured: report.featured,
      tags: report.tags
    }));

    console.log('✅ Analyse des PDF Akdital terminée avec succès');

    return new Response(
      JSON.stringify({
        success: true,
        stats,
        byCompany: byCompanyFormatted,
        byFileType: byFileTypeFormatted,
        fileDetails,
        message: `Analyse complète Akdital: ${stats.totalReports} rapports, ${stats.reportsWithFiles} avec fichiers, ${stats.isAllAkdital ? 'Tous d\'Akdital' : 'Mix d\'entreprises'}`
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );

  } catch (error) {
    console.error('❌ Erreur dans la fonction:', error);
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: error.message 
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );
  }
});
