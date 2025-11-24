#!/usr/bin/env python3
"""
Script de gestion des migrations Alembic
"""
import sys
import subprocess
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def run_alembic_command(command: list[str]) -> int:
    """
    Exécute une commande Alembic
    
    Args:
        command: Liste des arguments de la commande Alembic
    
    Returns:
        Code de retour (0 = succès)
    """
    # Utiliser le virtualenv si disponible
    if Path(".venv/bin/alembic").exists():
        alembic_cmd = [".venv/bin/alembic"] + command
    else:
        alembic_cmd = ["alembic"] + command
    
    logger.info(f"Exécution: {' '.join(alembic_cmd)}")
    result = subprocess.run(alembic_cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def main():
    """Point d'entrée principal"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/migrate.py <command> [args...]")
        print()
        print("Commandes disponibles:")
        print("  upgrade [revision]  - Appliquer les migrations (défaut: head)")
        print("  downgrade [revision] - Annuler les migrations")
        print("  current              - Afficher la version actuelle")
        print("  history              - Afficher l'historique des migrations")
        print("  create <message>     - Créer une nouvelle migration")
        print("  autogenerate <msg>   - Créer une migration auto-générée")
        print()
        print("Exemples:")
        print("  python scripts/migrate.py upgrade")
        print("  python scripts/migrate.py create 'add new column'")
        print("  python scripts/migrate.py autogenerate 'update schema'")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    print(f"🔄 Migration: {command}")
    print(f"📊 Database: {settings.database_url}")
    print()
    
    if command == "upgrade":
        revision = args[0] if args else "head"
        return run_alembic_command(["upgrade", revision])
    
    elif command == "downgrade":
        revision = args[0] if args else "-1"
        return run_alembic_command(["downgrade", revision])
    
    elif command == "current":
        return run_alembic_command(["current"])
    
    elif command == "history":
        return run_alembic_command(["history"])
    
    elif command == "create":
        if not args:
            print("❌ Erreur: Message de migration requis")
            print("   Usage: python scripts/migrate.py create 'message'")
            return 1
        message = args[0]
        return run_alembic_command(["revision", "-m", message])
    
    elif command == "autogenerate":
        message = args[0] if args else "Auto-generated migration"
        return run_alembic_command(["revision", "--autogenerate", "-m", message])
    
    else:
        print(f"❌ Commande inconnue: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())



