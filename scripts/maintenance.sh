#!/bin/bash

# Script de maintenance pour Fear & Greed Index
# Usage: ./scripts/maintenance.sh [clean|update|migrate|restart]

set -e

ACTION="${1:-help}"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

case "$ACTION" in
  clean)
    echo -e "${BLUE}🧹 Nettoyage...${NC}"
    
    # Nettoyer les images Docker inutilisées
    echo "Nettoyage des images Docker..."
    docker system prune -f
    
    # Nettoyer les logs anciens
    echo "Nettoyage des logs..."
    find ./logs -name "*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Nettoyer les backups anciens
    echo "Nettoyage des backups..."
    find ./backups -name "backup_*" -mtime +30 -delete 2>/dev/null || true
    
    echo -e "${GREEN}✅ Nettoyage terminé${NC}"
    ;;
    
  update)
    echo -e "${BLUE}🔄 Mise à jour...${NC}"
    
    # Pull les dernières modifications
    echo "Pull des dernières modifications..."
    git pull origin main
    
    # Rebuild les images
    echo "Rebuild des images Docker..."
    docker-compose build --no-cache
    
    # Redémarrer
    echo "Redémarrage des services..."
    docker-compose up -d
    
    echo -e "${GREEN}✅ Mise à jour terminée${NC}"
    ;;
    
  migrate)
    echo -e "${BLUE}🔄 Migrations...${NC}"
    
    # Appliquer les migrations
    echo "Application des migrations..."
    docker-compose exec backend python scripts/migrate.py upgrade
    
    echo -e "${GREEN}✅ Migrations appliquées${NC}"
    ;;
    
  restart)
    echo -e "${BLUE}🔄 Redémarrage...${NC}"
    
    docker-compose restart
    
    echo -e "${GREEN}✅ Services redémarrés${NC}"
    ;;
    
  status)
    echo -e "${BLUE}📊 Statut des services...${NC}"
    echo ""
    
    docker-compose ps
    
    echo ""
    echo "Health checks:"
    curl -s http://localhost:8001/api/v1/health/ping | jq . || echo "Backend non accessible"
    ;;
    
  logs)
    SERVICE="${2:-}"
    if [ -z "$SERVICE" ]; then
      docker-compose logs -f --tail=100
    else
      docker-compose logs -f --tail=100 "$SERVICE"
    fi
    ;;
    
  *)
    echo "Usage: $0 {clean|update|migrate|restart|status|logs [service]}"
    echo ""
    echo "Actions:"
    echo "  clean    - Nettoyer les fichiers inutilisés"
    echo "  update   - Mettre à jour et redémarrer"
    echo "  migrate  - Appliquer les migrations DB"
    echo "  restart  - Redémarrer tous les services"
    echo "  status   - Afficher le statut"
    echo "  logs     - Voir les logs (optionnel: service name)"
    exit 1
    ;;
esac



