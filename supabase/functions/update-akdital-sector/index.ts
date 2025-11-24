import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
      {
        auth: {
          autoRefreshToken: false,
          persistSession: false
        }
      }
    )

    console.log('🏥 Mise à jour des rapports Akdital vers le secteur Health Care...')
    
    // Récupérer tous les rapports d'Akdital
    const { data: akditalReports, error: fetchError } = await supabaseClient
      .from('financial_reports')
      .select('*')
      .or('company_name.ilike.%Akdital%,company_name.ilike.%Société Inconnue%,company_symbol.eq.CSEMA:AKDITAL,company_symbol.eq.CSEMA:UNKNOWN,tags.cs.{akdital}');

    if (fetchError) {
      throw fetchError;
    }

    console.log(`📊 ${akditalReports?.length || 0} rapports Akdital trouvés`);

    let totalUpdated = 0;

    // Mettre à jour chaque rapport Akdital
    for (const report of akditalReports || []) {
      try {
        // Mettre à jour le rapport avec les informations Akdital et secteur Health Care
        const updatedReport = {
          company_name: 'Akdital',
          company_symbol: 'CSEMA:AKDITAL',
          description: report.description?.replace('Société Inconnue', 'Akdital') || `Rapport financier officiel d'Akdital - Secteur Santé`,
          tags: [...(report.tags || []), 'akdital', 'officiel', 'health-care', 'sante'].filter((tag, index, arr) => arr.indexOf(tag) === index), // Supprimer les doublons
          updated_at: new Date().toISOString()
        };

        const { error: updateError } = await supabaseClient
          .from('financial_reports')
          .update(updatedReport)
          .eq('id', report.id);

        if (!updateError) {
          totalUpdated++;
          console.log(`✅ Rapport Akdital mis à jour: ${report.title} → Secteur Health Care`);
        } else {
          console.error(`❌ Erreur mise à jour ${report.title}:`, updateError);
        }

      } catch (err) {
        console.error(`❌ Erreur traitement rapport ${report.title}:`, err);
      }
    }

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Mise à jour des rapports Akdital vers le secteur Health Care terminée',
        totalFound: akditalReports?.length || 0,
        totalUpdated: totalUpdated,
        sector: 'Health Care',
        details: {
          companyName: 'Akdital',
          companySymbol: 'CSEMA:AKDITAL',
          sector: 'Health Care',
          description: 'Rapport financier officiel d\'Akdital - Secteur Santé'
        }
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )

  } catch (error) {
    console.error('Erreur mise à jour secteur Akdital:', error)
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: 'Erreur lors de la mise à jour du secteur Akdital' 
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )
  }
})




















