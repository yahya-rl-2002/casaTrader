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
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    )

    console.log('🗑️ Suppression de tous les articles...')
    
    // Supprimer tous les articles
    const { error: articlesError } = await supabaseClient
      .from('articles')
      .delete()
      .neq('id', '00000000-0000-0000-0000-000000000000') // Supprime tout

    if (articlesError) {
      console.error('Erreur suppression articles:', articlesError)
      throw articlesError
    }

    console.log('🗑️ Suppression de tous les rapports financiers...')
    
    // Supprimer tous les rapports financiers
    const { error: reportsError } = await supabaseClient
      .from('financial_reports')
      .delete()
      .neq('id', '00000000-0000-0000-0000-000000000000') // Supprime tout

    if (reportsError) {
      console.error('Erreur suppression rapports:', reportsError)
      throw reportsError
    }

    console.log('🗑️ Suppression de tous les documents financiers...')
    
    // Supprimer tous les documents financiers
    const { error: docsError } = await supabaseClient
      .from('financial_docs')
      .delete()
      .neq('id', '00000000-0000-0000-0000-000000000000') // Supprime tout

    if (docsError) {
      console.error('Erreur suppression documents:', docsError)
      throw docsError
    }

    console.log('✅ Toutes les données supprimées avec succès')

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Toutes les données ont été supprimées avec succès',
        deleted: {
          articles: 'tous',
          financial_reports: 'tous', 
          financial_docs: 'tous'
        }
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      },
    )

  } catch (error) {
    console.error('❌ Erreur lors de la suppression:', error)
    
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
        message: 'Erreur lors de la suppression des données'
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      },
    )
  }
})



















