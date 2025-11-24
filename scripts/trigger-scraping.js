// Script pour déclencher le scraping initial
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.SUPABASE_URL || 'https://zhyzjahvhctonjtebsff.supabase.co'
const supabaseKey = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpoeXpqYWh2aGN0b25qdGVic2ZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU5NzQ4MDAsImV4cCI6MjA1MTU1MDgwMH0.8K8Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q'

const supabase = createClient(supabaseUrl, supabaseKey)

async function triggerScraping() {
  try {
    console.log('🔄 Déclenchement du scraping initial...')
    
    const { data, error } = await supabase.functions.invoke('scrape-news', {
      body: { 
        maxPerSite: 20, 
        sites: ['Hespress', 'Boursenews', 'Medias24'] 
      }
    })
    
    if (error) {
      console.error('❌ Erreur:', error)
      return
    }
    
    console.log('✅ Scraping terminé:', JSON.stringify(data, null, 2))
    
  } catch (error) {
    console.error('❌ Erreur critique:', error)
  }
}

triggerScraping()
