// Script simple pour déclencher l'auto-update
// Utilise directement l'API Supabase

import { createClient } from '@supabase/supabase-js';

// Configuration (remplacez par vos vraies valeurs)
const supabaseUrl = process.env.VITE_SUPABASE_URL || 'YOUR_SUPABASE_URL';
const supabaseKey = process.env.VITE_SUPABASE_PUBLISHABLE_KEY || 'YOUR_SUPABASE_ANON_KEY';

const supabase = createClient(supabaseUrl, supabaseKey);

async function triggerAutoUpdate() {
  try {
    console.log('🔄 Déclenchement de l\'auto-update...');
    
    const { data, error } = await supabase.functions.invoke('auto-update-news');
    
    if (error) {
      throw new Error(`Erreur Supabase: ${error.message}`);
    }
    
    console.log('✅ Auto-update déclenché avec succès!');
    console.log('📊 Résultats:', data);
    
    if (data.success) {
      console.log(`📰 Articles ajoutés: ${data.articles_added}`);
      console.log(`🗑️ Articles nettoyés: ${data.articles_cleaned}`);
      console.log(`📊 Sources traitées: ${data.sources_processed?.join(', ')}`);
    } else {
      console.error('❌ Auto-update échoué:', data.error);
    }
    
  } catch (error) {
    console.error('❌ Erreur:', error);
    process.exit(1);
  }
}

// Exécuter le script
triggerAutoUpdate();















