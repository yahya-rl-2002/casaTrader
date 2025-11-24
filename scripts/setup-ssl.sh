#!/bin/bash

# Script de configuration SSL/TLS avec Let's Encrypt
# Usage: ./scripts/setup-ssl.sh <domain>

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <domain>"
  echo "Exemple: $0 yourdomain.com"
  exit 1
fi

DOMAIN="$1"
EMAIL="${SSL_EMAIL:-admin@$DOMAIN}"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔒 Configuration SSL/TLS pour $DOMAIN${NC}"
echo ""

# Vérifier si certbot est installé
if ! command -v certbot &> /dev/null; then
  echo -e "${YELLOW}📦 Installation de certbot...${NC}"
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y certbot python3-certbot-nginx
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install certbot
  else
    echo "❌ OS non supporté. Installez certbot manuellement."
    exit 1
  fi
fi

# Obtenir le certificat
echo -e "${YELLOW}📜 Obtention du certificat SSL...${NC}"
sudo certbot certonly \
  --nginx \
  --non-interactive \
  --agree-tos \
  --email "$EMAIL" \
  -d "$DOMAIN" \
  -d "www.$DOMAIN"

# Créer le répertoire SSL dans nginx
mkdir -p nginx/ssl

# Copier les certificats
echo -e "${YELLOW}📁 Copie des certificats...${NC}"
sudo cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" nginx/ssl/cert.pem
sudo cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" nginx/ssl/key.pem
sudo chmod 644 nginx/ssl/cert.pem
sudo chmod 600 nginx/ssl/key.pem

# Mettre à jour nginx.conf avec SSL
echo -e "${YELLOW}⚙️  Mise à jour de la configuration Nginx...${NC}"

# Créer une configuration SSL
cat > nginx/ssl.conf <<EOF
# SSL Configuration for $DOMAIN
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Redirection HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    # SSL certificates
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://backend:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

echo -e "${GREEN}✅ Configuration SSL créée dans nginx/ssl.conf${NC}"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Intégrer nginx/ssl.conf dans nginx/nginx.conf"
echo "2. Redémarrer Nginx: docker-compose restart nginx"
echo "3. Vérifier: https://$DOMAIN"
echo ""
echo "🔄 Renouvellement automatique:"
echo "   sudo certbot renew --dry-run"



