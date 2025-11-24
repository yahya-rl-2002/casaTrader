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

    console.log('🔄 Mise à jour des rapports "Société Inconnue" vers "Akdital"...')
    
    // Récupérer tous les rapports avec "Société Inconnue"
    const { data: reportsToUpdate, error: fetchError } = await supabaseClient
      .from('financial_reports')
      .select('*')
      .or('company_name.ilike.%Société Inconnue%,company_name.ilike.%société inconnue%,company_name.ilike.%Societe Inconnue%');

    if (fetchError) {
      throw fetchError;
    }

    console.log(`📊 ${reportsToUpdate?.length || 0} rapports "Société Inconnue" trouvés`);

    let totalUpdated = 0;

    // Mettre à jour chaque rapport
    for (const report of reportsToUpdate || []) {
      try {
        // Mettre à jour le rapport avec les informations Akdital
        const updatedReport = {
          company_name: 'Akdital',
          company_symbol: 'CSEMA:AKDITAL',
          description: report.description?.replace('Société Inconnue', 'Akdital') || `Rapport financier officiel d'Akdital`,
          tags: [...(report.tags || []), 'akdital', 'officiel'].filter((tag, index, arr) => arr.indexOf(tag) === index), // Supprimer les doublons
          updated_at: new Date().toISOString()
        };

        const { error: updateError } = await supabaseClient
          .from('financial_reports')
          .update(updatedReport)
          .eq('id', report.id);

        if (!updateError) {
          totalUpdated++;
          console.log(`✅ Rapport mis à jour: ${report.title} → Akdital`);
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
        message: 'Mise à jour des rapports Akdital terminée',
        totalFound: reportsToUpdate?.length || 0,
        totalUpdated: totalUpdated,
        details: {
          companyName: 'Akdital',
          companySymbol: 'CSEMA:AKDITAL',
          description: 'Rapport financier officiel d\'Akdital'
        }
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )

  } catch (error) {
    console.error('Erreur mise à jour rapports Akdital:', error)
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: 'Erreur lors de la mise à jour des rapports Akdital' 
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )
  }
})




















