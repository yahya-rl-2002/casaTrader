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
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? ''
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''

    if (!supabaseUrl || !serviceKey) {
      console.error('❌ Supabase credentials missing')
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Missing Supabase credentials',
          message: 'Configure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY'
        }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500,
        },
      )
    }

    const supabaseClient = createClient(supabaseUrl, serviceKey)

    console.log('🔄 Début de l\'actualisation automatique programmée...')
    
    // 1. Supprimer les anciens articles (plus de 7 jours)
    console.log('🗑️ Suppression des anciens articles...')
    const sevenDaysAgo = new Date()
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
    
    const { error: deleteError } = await supabaseClient
      .from('articles')
      .delete()
      .lt('published_at', sevenDaysAgo.toISOString())

    if (deleteError) {
      console.error('Erreur suppression anciens articles:', deleteError)
    } else {
      console.log('✅ Anciens articles supprimés')
    }

    // 2. Appeler la fonction de scraping RSS
    console.log('📰 Appel du scraping RSS...')
    const { data: scrapeData, error: scrapeError } = await supabaseClient.functions.invoke('scrape-rss-news')
    
    if (scrapeError) {
      console.error('Erreur scraping RSS:', scrapeError)
      throw scrapeError
    }

    const scrapeResult = scrapeData as { 
      success: boolean; 
      articlesCount: number; 
      sources: string[]; 
      timestamp: string 
    }

    console.log(`✅ Scraping terminé: ${scrapeResult.articlesCount} articles depuis ${scrapeResult.sources.join(', ')}`)

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Actualisation automatique programmée terminée',
        stats: {
          articlesAdded: scrapeResult.articlesCount,
          sourcesProcessed: scrapeResult.sources.length,
          oldArticlesDeleted: true,
          timestamp: new Date().toISOString()
        }
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      },
    )

  } catch (error) {
    console.error('❌ Erreur lors de l\'actualisation automatique programmée:', error)
    
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
        message: 'Erreur lors de l\'actualisation automatique programmée'
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      },
    )
  }
})



















