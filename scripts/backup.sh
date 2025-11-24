#!/bin/bash

# Script de backup automatique pour Fear & Greed Index
# Usage: ./scripts/backup.sh [--compress] [--upload]

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS="${RETENTION_DAYS:-30}"
COMPRESS=false
UPLOAD=false

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --compress)
      COMPRESS=true
      shift
      ;;
    --upload)
      UPLOAD=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo -e "${GREEN}🔄 Démarrage du backup${NC}"
echo "Date: $(date)"
echo ""

# Créer le répertoire de backup
mkdir -p "$BACKUP_DIR"

# 1. Backup PostgreSQL
echo -e "${YELLOW}📊 Backup PostgreSQL...${NC}"
if docker ps | grep -q fear-greed-postgres; then
  docker exec fear-greed-postgres pg_dump -U fear_greed_user fear_greed_db > \
    "$BACKUP_DIR/db_$DATE.sql"
  
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backup PostgreSQL réussi${NC}"
    DB_SIZE=$(du -h "$BACKUP_DIR/db_$DATE.sql" | cut -f1)
    echo "   Taille: $DB_SIZE"
  else
    echo -e "${RED}❌ Erreur backup PostgreSQL${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}⚠️  PostgreSQL non trouvé, backup SQLite...${NC}"
  if [ -f "backend/fear_greed.db" ]; then
    cp "backend/fear_greed.db" "$BACKUP_DIR/db_$DATE.db"
    echo -e "${GREEN}✅ Backup SQLite réussi${NC}"
  fi
fi

# 2. Backup Redis (si utilisé)
echo -e "${YELLOW}💾 Backup Redis...${NC}"
if docker ps | grep -q fear-greed-redis; then
  docker exec fear-greed-redis redis-cli SAVE
  docker cp fear-greed-redis:/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb" 2>/dev/null || true
  
  if [ -f "$BACKUP_DIR/redis_$DATE.rdb" ]; then
    echo -e "${GREEN}✅ Backup Redis réussi${NC}"
  else
    echo -e "${YELLOW}⚠️  Redis backup optionnel (non critique)${NC}"
  fi
fi

# 3. Backup fichiers de configuration
echo -e "${YELLOW}📁 Backup configuration...${NC}"
mkdir -p "$BACKUP_DIR/config_$DATE"
cp -r backend/.env "$BACKUP_DIR/config_$DATE/.env" 2>/dev/null || true
cp docker-compose.yml "$BACKUP_DIR/config_$DATE/" 2>/dev/null || true
cp nginx/nginx.conf "$BACKUP_DIR/config_$DATE/" 2>/dev/null || true

echo -e "${GREEN}✅ Configuration sauvegardée${NC}"

# 4. Compression
if [ "$COMPRESS" = true ]; then
  echo -e "${YELLOW}🗜️  Compression...${NC}"
  tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" \
    "$BACKUP_DIR/db_$DATE.sql" \
    "$BACKUP_DIR/redis_$DATE.rdb" \
    "$BACKUP_DIR/config_$DATE" \
    2>/dev/null || true
  
  # Supprimer les fichiers non compressés
  rm -f "$BACKUP_DIR/db_$DATE.sql" "$BACKUP_DIR/redis_$DATE.rdb"
  rm -rf "$BACKUP_DIR/config_$DATE"
  
  BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"
  echo -e "${GREEN}✅ Compression réussie${NC}"
else
  BACKUP_FILE="$BACKUP_DIR/backup_$DATE"
fi

# 5. Upload (optionnel - S3, etc.)
if [ "$UPLOAD" = true ] && [ -n "$BACKUP_S3_BUCKET" ]; then
  echo -e "${YELLOW}☁️  Upload vers S3...${NC}"
  if command -v aws &> /dev/null; then
    aws s3 cp "$BACKUP_FILE" "s3://$BACKUP_S3_BUCKET/backups/" || true
    echo -e "${GREEN}✅ Upload réussi${NC}"
  else
    echo -e "${YELLOW}⚠️  AWS CLI non installé, upload ignoré${NC}"
  fi
fi

# 6. Nettoyage des anciens backups
echo -e "${YELLOW}🧹 Nettoyage des anciens backups...${NC}"
find "$BACKUP_DIR" -name "backup_*" -type f -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "db_*.sql" -type f -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "redis_*.rdb" -type f -mtime +$RETENTION_DAYS -delete

echo -e "${GREEN}✅ Nettoyage terminé${NC}"

# 7. Résumé
echo ""
echo -e "${GREEN}✅ Backup terminé avec succès !${NC}"
echo "Fichier: $BACKUP_FILE"
if [ "$COMPRESS" = true ]; then
  BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
  echo "Taille: $BACKUP_SIZE"
fi
echo ""
echo "Pour restaurer:"
echo "  ./scripts/restore.sh $BACKUP_FILE"



