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

    console.log('🏥 Récupération des rapports Akdital...');

    // Récupérer directement les rapports Akdital depuis la table
    const { data: reports, error: reportsError } = await supabase
      .from('financial_reports')
      .select('*')
      .or('company_name.eq.Akdital,company_name.eq.Société Inconnue,company_symbol.eq.CSEMA:AKDITAL,company_symbol.eq.CSEMA:UNKNOWN')
      .order('published_at', { ascending: false });

    if (reportsError) {
      console.error('❌ Erreur lors de la récupération des rapports Akdital:', reportsError);
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

    console.log(`📊 Rapports Akdital trouvés: ${reports?.length || 0}`);

    // Obtenir les statistiques Akdital
    const { data: stats, error: statsError } = await supabase.rpc('get_akdital_summary');

    if (statsError) {
      console.error('❌ Erreur lors de la récupération des statistiques:', statsError);
    }

    // Grouper par type de rapport
    const byReportType: { [key: string]: any[] } = {};
    reports?.forEach(report => {
      const type = report.report_type || 'autre';
      if (!byReportType[type]) {
        byReportType[type] = [];
      }
      byReportType[type].push(report);
    });

    // Grouper par année
    const byYear: { [key: string]: any[] } = {};
    reports?.forEach(report => {
      if (report.published_at) {
        const year = new Date(report.published_at).getFullYear().toString();
        if (!byYear[year]) {
          byYear[year] = [];
        }
        byYear[year].push(report);
      }
    });

    // Statistiques détaillées
    const reportStats = {
      totalReports: reports?.length || 0,
      reportsWithFiles: reports?.filter(r => r.file_url).length || 0,
      reportsWithoutFiles: reports?.filter(r => !r.file_url).length || 0,
      totalFileSize: reports?.reduce((sum, r) => sum + (r.file_size || 0), 0) || 0,
      averageFileSize: reports?.length > 0 
        ? Math.round(reports.reduce((sum, r) => sum + (r.file_size || 0), 0) / reports.length)
        : 0,
      featuredReports: reports?.filter(r => r.featured).length || 0,
      totalDownloads: reports?.reduce((sum, r) => sum + (r.download_count || 0), 0) || 0,
      reportTypes: Object.keys(byReportType).length,
      years: Object.keys(byYear).length,
      isAllAkdital: true, // Toujours true car on utilise la vue Akdital
      sector: 'Health Care'
    };

    console.log('✅ Rapports Akdital récupérés avec succès');

    return new Response(
      JSON.stringify({
        success: true,
        reports: reports || [],
        stats: reportStats,
        summary: stats?.[0] || null,
        byReportType,
        byYear,
        message: `Rapports Akdital: ${reportStats.totalReports} total, ${reportStats.reportsWithFiles} avec fichiers`
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );

  } catch (error) {
    console.error('❌ Erreur dans la fonction get-akdital-reports:', error);
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
