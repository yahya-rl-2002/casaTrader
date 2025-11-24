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

    console.log('🔍 Debug - Vérification des rapports Akdital...');

    // 1. Compter tous les rapports
    const { count: totalCount, error: totalError } = await supabase
      .from('financial_reports')
      .select('*', { count: 'exact', head: true });

    console.log('📊 Total rapports dans la base:', totalCount);

    // 2. Chercher tous les rapports Akdital possibles
    const { data: allReports, error: allError } = await supabase
      .from('financial_reports')
      .select('*')
      .order('created_at', { ascending: false });

    if (allError) {
      console.error('❌ Erreur récupération tous rapports:', allError);
    }

    console.log('📊 Tous les rapports récupérés:', allReports?.length || 0);

    // 3. Filtrer les rapports Akdital
    const akditalReports = allReports?.filter(report => 
      report.company_name === 'Akdital' || 
      report.company_name === 'Société Inconnue' ||
      report.company_symbol === 'CSEMA:AKDITAL' ||
      report.company_symbol === 'CSEMA:UNKNOWN' ||
      report.tags?.includes('akdital')
    ) || [];

    console.log('🏥 Rapports Akdital filtrés:', akditalReports.length);
    console.log('🏥 Détails rapports Akdital:', akditalReports.map(r => ({
      id: r.id,
      title: r.title,
      company_name: r.company_name,
      company_symbol: r.company_symbol,
      tags: r.tags
    })));

    // 4. Vérifier les différents critères
    const byCompanyName = allReports?.filter(r => r.company_name === 'Akdital') || [];
    const byCompanyNameUnknown = allReports?.filter(r => r.company_name === 'Société Inconnue') || [];
    const bySymbolAkdital = allReports?.filter(r => r.company_symbol === 'CSEMA:AKDITAL') || [];
    const bySymbolUnknown = allReports?.filter(r => r.company_symbol === 'CSEMA:UNKNOWN') || [];
    const byTags = allReports?.filter(r => r.tags?.includes('akdital')) || [];

    console.log('🔍 Par company_name = Akdital:', byCompanyName.length);
    console.log('🔍 Par company_name = Société Inconnue:', byCompanyNameUnknown.length);
    console.log('🔍 Par company_symbol = CSEMA:AKDITAL:', bySymbolAkdital.length);
    console.log('🔍 Par company_symbol = CSEMA:UNKNOWN:', bySymbolUnknown.length);
    console.log('🔍 Par tags incluant akdital:', byTags.length);

    return new Response(
      JSON.stringify({
        success: true,
        totalReports: totalCount || 0,
        allReportsCount: allReports?.length || 0,
        akditalReportsCount: akditalReports.length,
        akditalReports: akditalReports,
        breakdown: {
          byCompanyName: byCompanyName.length,
          byCompanyNameUnknown: byCompanyNameUnknown.length,
          bySymbolAkdital: bySymbolAkdital.length,
          bySymbolUnknown: bySymbolUnknown.length,
          byTags: byTags.length
        },
        message: `Debug complet: ${totalCount} total, ${akditalReports.length} Akdital`
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );

  } catch (error) {
    console.error('❌ Erreur dans debug-akdital-reports:', error);
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




















