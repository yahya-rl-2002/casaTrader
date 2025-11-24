#!/bin/bash

# Script pour configurer les tâches cron automatiques
# Usage: ./scripts/setup-cron.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}⏰ Configuration des tâches cron${NC}"
echo ""

# Créer le fichier cron
CRON_FILE="/tmp/fear_greed_cron"

cat > "$CRON_FILE" <<EOF
# Fear & Greed Index - Tâches automatiques
# Généré le $(date)

# Backup quotidien à 2h du matin
0 2 * * * cd $PROJECT_DIR && ./scripts/backup.sh --compress >> $PROJECT_DIR/logs/backup.log 2>&1

# Health check toutes les heures
0 * * * * cd $PROJECT_DIR && ./scripts/health-check.sh >> $PROJECT_DIR/logs/health.log 2>&1

# Nettoyage hebdomadaire (dimanche à 3h)
0 3 * * 0 cd $PROJECT_DIR && ./scripts/maintenance.sh clean >> $PROJECT_DIR/logs/maintenance.log 2>&1

# Renouvellement SSL (Let's Encrypt) - 2 fois par mois
0 4 1,15 * * certbot renew --quiet --deploy-hook "docker-compose restart nginx"
EOF

echo "Tâches cron à installer:"
echo "========================"
cat "$CRON_FILE"
echo ""

read -p "Installer ces tâches cron ? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
  # Ajouter au crontab
  crontab -l 2>/dev/null | grep -v "Fear & Greed Index" | cat - "$CRON_FILE" | crontab -
  
  echo -e "${GREEN}✅ Tâches cron installées${NC}"
  echo ""
  echo "Vérifier avec: crontab -l"
else
  echo "Installation annulée"
  echo "Pour installer manuellement:"
  echo "  crontab -e"
  echo "  (copier le contenu de $CRON_FILE)"
fi

rm "$CRON_FILE"
