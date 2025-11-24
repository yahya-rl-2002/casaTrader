#!/usr/bin/env python3
"""
Script pour ajouter la colonne content à la table media_articles
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.models.database import engine, get_session
from app.core.logging import get_logger

logger = get_logger(__name__)


def add_content_column():
    """Ajouter la colonne content à la table media_articles si elle n'existe pas"""
    try:
        db = get_session()
        
        try:
            # Vérifier si la colonne existe déjà
            result = db.execute(text("PRAGMA table_info(media_articles)"))
            columns = [row[1] for row in result]
            
            if 'content' in columns:
                logger.info("✅ La colonne 'content' existe déjà")
                return
            
            # Ajouter la colonne
            logger.info("Ajout de la colonne 'content' à la table media_articles...")
            db.execute(text("ALTER TABLE media_articles ADD COLUMN content TEXT"))
            db.commit()
            
            logger.info("✅ Colonne 'content' ajoutée avec succès")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erreur lors de l'ajout de la colonne: {e}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise


if __name__ == "__main__":
    add_content_column()




