#!/usr/bin/env python3
"""
Script pour synchroniser les articles de SQLite vers Supabase
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncio
from app.services.supabase_sync_service import SupabaseSyncService
from app.core.logging import get_logger

logger = get_logger(__name__)


async def sync_articles():
    """Synchroniser les articles vers Supabase"""
    try:
        sync_service = SupabaseSyncService()
        
        if not sync_service.client:
            print("❌ Client Supabase non initialisé")
            print("💡 Définissez SUPABASE_URL et SUPABASE_ANON_KEY dans votre .env")
            return
        
        print("🔄 Synchronisation des articles vers Supabase...")
        print("="*60)
        
        # Synchroniser uniquement les 3 sources configurées
        stats = sync_service.sync_articles_to_supabase(
            sources=["hespress", "medias24", "boursenews"],
            limit=None  # Synchroniser tous les articles
        )
        
        print("\n" + "="*60)
        print("📊 RÉSULTATS DE LA SYNCHRONISATION")
        print("="*60)
        
        if stats.get("success"):
            print(f"✅ Articles synchronisés: {stats['synced']}")
            
            if stats.get("sources"):
                print("\n📰 Par source:")
                for source, count in stats["sources"].items():
                    print(f"  - {source.upper()}: {count} articles")
            
            if stats.get("errors"):
                print(f"\n⚠️  Erreurs: {len(stats['errors'])}")
                for error in stats["errors"][:5]:
                    print(f"  - {error.get('url', '')[:50]}...: {error.get('error', '')[:50]}")
        else:
            print(f"❌ Erreur: {stats.get('error', 'Erreur inconnue')}")
        
        print("="*60)
        
    except Exception as e:
        logger.error(f"Erreur lors de la synchronisation: {e}", exc_info=True)
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    asyncio.run(sync_articles())




