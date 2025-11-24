#!/bin/bash

# Script de restauration depuis un backup
# Usage: ./scripts/restore.sh <backup_file>

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <backup_file>"
  echo "Exemple: $0 backups/backup_20251115_120000.tar.gz"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "❌ Fichier de backup non trouvé: $BACKUP_FILE"
  exit 1
fi

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}⚠️  ATTENTION: Cette opération va remplacer les données actuelles !${NC}"
read -p "Continuer ? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "Restauration annulée"
  exit 0
fi

# Créer un répertoire temporaire
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo -e "${GREEN}🔄 Démarrage de la restauration${NC}"
echo ""

# Décompresser si nécessaire
if [[ "$BACKUP_FILE" == *.tar.gz ]]; then
  echo -e "${YELLOW}📦 Décompression...${NC}"
  tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
  DB_FILE=$(find "$TEMP_DIR" -name "db_*.sql" | head -1)
  REDIS_FILE=$(find "$TEMP_DIR" -name "redis_*.rdb" | head -1)
else
  DB_FILE="$BACKUP_FILE"
fi

# Restaurer PostgreSQL
if [ -n "$DB_FILE" ] && [ -f "$DB_FILE" ]; then
  echo -e "${YELLOW}📊 Restauration PostgreSQL...${NC}"
  
  if docker ps | grep -q fear-greed-postgres; then
    # Arrêter l'application temporairement
    docker-compose stop backend || true
    
    # Restaurer
    docker exec -i fear-greed-postgres psql -U fear_greed_user -d fear_greed_db < "$DB_FILE"
    
    echo -e "${GREEN}✅ PostgreSQL restauré${NC}"
  else
    echo -e "${YELLOW}⚠️  PostgreSQL non trouvé, restauration SQLite...${NC}"
    if [[ "$DB_FILE" == *.db ]]; then
      cp "$DB_FILE" "backend/fear_greed.db"
      echo -e "${GREEN}✅ SQLite restauré${NC}"
    fi
  fi
fi

# Restaurer Redis (optionnel)
if [ -n "$REDIS_FILE" ] && [ -f "$REDIS_FILE" ]; then
  echo -e "${YELLOW}💾 Restauration Redis...${NC}"
  if docker ps | grep -q fear-greed-redis; then
    docker cp "$REDIS_FILE" fear-greed-redis:/data/dump.rdb
    docker exec fear-greed-redis redis-cli CONFIG SET SAVE ""
    echo -e "${GREEN}✅ Redis restauré${NC}"
  fi
fi

# Redémarrer les services
echo -e "${YELLOW}🔄 Redémarrage des services...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}✅ Restauration terminée avec succès !${NC}"
echo ""
echo "Vérification:"
echo "  curl http://localhost:8001/api/v1/health"



