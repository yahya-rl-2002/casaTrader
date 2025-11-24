import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.3';

// CORS headers for Supabase Functions
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface ScrapeResult {
  success: boolean;
  articlesCount: number;
  sources: string[];
  error?: string;
}

// Fonction pour déclencher le scraping automatique
async function triggerAutoScraping(): Promise<ScrapeResult> {
  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? Deno.env.get('PROJECT_URL');
    const supabaseKey = Deno.env.get('SERVICE_ROLE_KEY') ?? Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
    
    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Supabase credentials not set');
    }
    
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Déclencher le scraping avec des paramètres optimisés
    const { data, error } = await supabase.functions.invoke('scrape-news', {
      body: {
        maxPerSite: 5, // Récupérer 5 articles par site
        limitSites: 8, // Limiter à 8 sites pour éviter les timeouts
        sites: ['Hespress', 'Boursenews', 'Medias24', 'Le Matin', 'Le360', 'H24Info', 'Challenge', 'LesEco']
      }
    });
    
    if (error) {
      throw new Error(`Scraping error: ${error.message}`);
    }
    
    return {
      success: data.success,
      articlesCount: data.articlesCount || 0,
      sources: data.processed || []
    };
    
  } catch (error) {
    console.error('Auto-scraping error:', error);
    return {
      success: false,
      articlesCount: 0,
      sources: [],
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// Fonction pour nettoyer les anciens articles (garder seulement les 30 derniers jours)
async function cleanupOldArticles(): Promise<number> {
  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? Deno.env.get('PROJECT_URL');
    const supabaseKey = Deno.env.get('SERVICE_ROLE_KEY') ?? Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
    
    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Supabase credentials not set');
    }
    
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Supprimer les articles plus anciens que 30 jours
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    const { data, error } = await supabase
      .from('articles')
      .delete()
      .lt('published_at', thirtyDaysAgo.toISOString())
      .select('id');
    
    if (error) {
      console.error('Cleanup error:', error);
      return 0;
    }
    
    return data?.length || 0;
    
  } catch (error) {
    console.error('Cleanup error:', error);
    return 0;
  }
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    console.log('🔄 Démarrage de l\'auto-update des articles...');
    
    // 1. Déclencher le scraping
    const scrapeResult = await triggerAutoScraping();
    
    // 2. Nettoyer les anciens articles
    const cleanedCount = await cleanupOldArticles();
    
    // 3. Préparer la réponse
    const response = {
      success: scrapeResult.success,
      timestamp: new Date().toISOString(),
      articles_added: scrapeResult.articlesCount,
      articles_cleaned: cleanedCount,
      sources_processed: scrapeResult.sources,
      error: scrapeResult.error
    };
    
    console.log('✅ Auto-update terminé:', response);
    
    return new Response(
      JSON.stringify(response),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 }
    );
    
  } catch (error) {
    console.error('❌ Auto-update error:', error);
    
    return new Response(
      JSON.stringify({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});