// Script pour tester le système d'auto-update
import { autoUpdateNews } from './auto-update-news.js';

async function testAutoUpdate() {
  console.log('🧪 Test du système d\'auto-update...');
  console.log('⏰ Heure de début:', new Date().toLocaleString('fr-FR'));
  
  try {
    const result = await autoUpdateNews();
    
    console.log('\n📊 Résultats du test:');
    console.log('✅ Succès:', result.success);
    console.log('📰 Articles ajoutés:', result.articles_added);
    console.log('🗑️ Articles nettoyés:', result.articles_cleaned);
    console.log('📊 Sources traitées:', result.sources_processed?.join(', '));
    
    if (result.error) {
      console.log('❌ Erreur:', result.error);
    }
    
    console.log('\n🎉 Test terminé avec succès!');
    
  } catch (error) {
    console.error('❌ Test échoué:', error);
    process.exit(1);
  }
}

// Exécuter le test
testAutoUpdate();
