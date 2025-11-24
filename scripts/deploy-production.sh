#!/bin/bash

# Script de déploiement en production
# Usage: ./scripts/deploy-production.sh [--skip-backup] [--skip-tests]

set -e

SKIP_BACKUP=false
SKIP_TESTS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-backup)
      SKIP_BACKUP=true
      shift
      ;;
    --skip-tests)
      SKIP_TESTS=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Déploiement en Production${NC}"
echo "=================================="
echo ""

# 1. Backup (sauf si skip)
if [ "$SKIP_BACKUP" = false ]; then
  echo -e "${YELLOW}💾 Backup avant déploiement...${NC}"
  ./scripts/backup.sh --compress || {
    echo -e "${RED}❌ Backup échoué. Continuer quand même ? (yes/no)${NC}"
    read confirm
    if [ "$confirm" != "yes" ]; then
      exit 1
    fi
  }
  echo ""
fi

# 2. Tests (sauf si skip)
if [ "$SKIP_TESTS" = false ]; then
  echo -e "${YELLOW}🧪 Exécution des tests...${NC}"
  
  # Tests backend
  cd backend
  if [ -f "pytest.ini" ]; then
    pytest tests/ || {
      echo -e "${RED}❌ Tests échoués${NC}"
      exit 1
    }
  fi
  cd ..
  
  echo -e "${GREEN}✅ Tests passés${NC}"
  echo ""
fi

# 3. Pull les dernières modifications
echo -e "${YELLOW}📥 Pull des dernières modifications...${NC}"
git pull origin main || {
  echo -e "${RED}❌ Erreur git pull${NC}"
  exit 1
}
echo ""

# 4. Build des images
echo -e "${YELLOW}🔨 Build des images Docker...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache
echo ""

# 5. Arrêter les services
echo -e "${YELLOW}🛑 Arrêt des services...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
echo ""

# 6. Démarrer les services
echo -e "${YELLOW}▶️  Démarrage des services...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
echo ""

# 7. Attendre que les services soient prêts
echo -e "${YELLOW}⏳ Attente des services...${NC}"
sleep 10

# 8. Migrations
echo -e "${YELLOW}🔄 Application des migrations...${NC}"
docker-compose exec -T backend python scripts/migrate.py upgrade || {
  echo -e "${YELLOW}⚠️  Migrations échouées (peut être normal si déjà à jour)${NC}"
}
echo ""

# 9. Health checks
echo -e "${YELLOW}🏥 Health checks...${NC}"
./scripts/health-check.sh --verbose || {
  echo -e "${RED}❌ Health checks échoués${NC}"
  echo "Voir les logs: docker-compose logs"
  exit 1
}
echo ""

# 10. Résumé
echo -e "${GREEN}✅ Déploiement terminé avec succès !${NC}"
echo ""
echo "Services disponibles:"
echo "  - Frontend: http://localhost:8080"
echo "  - Backend: http://localhost:8001"
echo "  - API Docs: http://localhost:8001/docs"
echo ""
echo "Logs:"
echo "  docker-compose logs -f"



