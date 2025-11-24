"""
Migration: Ajouter la colonne sentiment_label à la table media_articles
"""
import sys
sys.path.append('.')

from app.models.database import engine
from sqlalchemy import text

print("="*80)
print("  🔄 MIGRATION: Ajout de sentiment_label à media_articles")
print("="*80)
print()

try:
    with engine.connect() as conn:
        # Vérifier si la colonne existe déjà
        result = conn.execute(text("PRAGMA table_info(media_articles)"))
        columns = [row[1] for row in result]
        
        if 'sentiment_label' in columns:
            print("✅ La colonne 'sentiment_label' existe déjà")
        else:
            print("🔧 Ajout de la colonne 'sentiment_label'...")
            conn.execute(text("ALTER TABLE media_articles ADD COLUMN sentiment_label VARCHAR"))
            conn.commit()
            print("✅ Colonne 'sentiment_label' ajoutée avec succès")
        
        # Vérifier si scraped_at existe
        if 'scraped_at' in columns:
            print("✅ La colonne 'scraped_at' existe déjà")
        else:
            print("🔧 Ajout de la colonne 'scraped_at'...")
            conn.execute(text("ALTER TABLE media_articles ADD COLUMN scraped_at DATETIME"))
            conn.commit()
            print("✅ Colonne 'scraped_at' ajoutée avec succès")
        
        print()
        print("="*80)
        print("  ✅ MIGRATION TERMINÉE AVEC SUCCÈS")
        print("="*80)
        
except Exception as e:
    print(f"❌ Erreur lors de la migration: {e}")
    sys.exit(1)

