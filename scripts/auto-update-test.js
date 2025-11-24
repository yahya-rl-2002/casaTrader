// Script de test pour l'actualisation automatique
const { createClient } = require('@supabase/supabase-js')

const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Variables d\'environnement manquantes')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

async function testAutoUpdate() {
  try {
    console.log('🔄 Test de l\'actualisation automatique...')
    
    const { data, error } = await supabase.functions.invoke('auto-update-news')
    
    if (error) {
      console.error('❌ Erreur:', error)
      return
    }
    
    console.log('✅ Résultat:', JSON.stringify(data, null, 2))
    
  } catch (error) {
    console.error('❌ Erreur critique:', error)
  }
}

testAutoUpdate()



















