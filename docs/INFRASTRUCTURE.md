# 🏗️ Infrastructure - Guide Complet

## 📋 Qu'est-ce que l'Infrastructure ?

L'**infrastructure** regroupe tous les éléments techniques qui permettent de :
- 🐳 **Conteneuriser** l'application (Docker)
- 🚀 **Déployer** en production facilement
- ⚖️ **Scaler** (gérer la charge)
- 🔒 **Sécuriser** (SSL, firewall)
- 📊 **Monitorer** (Prometheus, Grafana)
- 💾 **Sauvegarder** automatiquement
- 🔄 **Automatiser** les déploiements (CI/CD)

**En simple** : L'infrastructure, c'est comme les fondations d'une maison. Sans infrastructure solide, l'application ne peut pas fonctionner correctement en production.

---

## 🎯 Architecture Actuelle

```
┌─────────────────┐
│   Nginx         │  Reverse Proxy (Port 80/443)
│   (SSL/TLS)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼───┐  ┌───▼───┐  ┌───▼───┐
│Frontend│ │Backend│ │PostgreSQL│ │ Redis │
│ :3000  │ │ :8001 │ │  :5432  │ │ :6379 │
└───────┘ └───────┘ └─────────┘ └───────┘
    │         │
    │         │
┌───▼─────────▼───┐
│   Prometheus    │  Monitoring (Port 9090)
│   + Grafana     │  Dashboards (Port 3001)
└─────────────────┘
```

---

## 🐳 Docker & Conteneurisation

### Docker Compose

Le fichier `docker-compose.yml` orchestre tous les services :

**Services** :
- **PostgreSQL** : Base de données avec TimescaleDB
- **Redis** : Cache et tâches asynchrones
- **Backend** : API FastAPI
- **Frontend** : Application React
- **Nginx** : Reverse proxy
- **Prometheus** : Métriques
- **Grafana** : Dashboards

### Utilisation

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down

# Rebuild après modifications
docker-compose up -d --build
```

---

## 🚀 Déploiement

### Développement Local

```bash
# Option 1 : Scripts de démarrage
./start_all.sh

# Option 2 : Docker Compose
docker-compose up -d
```

### Production

#### Prérequis

- Serveur avec Docker et Docker Compose
- Domaine configuré
- Certificats SSL (Let's Encrypt)

#### Étapes

1. **Cloner le repository**
```bash
git clone <repo-url>
cd casablanca-stock
```

2. **Configurer les variables d'environnement**
```bash
cp backend/.env.example backend/.env
# Éditer .env avec les valeurs de production
```

3. **Démarrer les services**
```bash
docker-compose up -d
```

4. **Vérifier**
```bash
docker-compose ps
curl http://localhost/api/v1/health
```

---

## 🔒 Sécurité

### SSL/TLS

**Configuration Nginx avec Let's Encrypt** :

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... reste de la config
}
```

**Obtenir un certificat SSL** :
```bash
certbot certonly --nginx -d yourdomain.com
```

### Firewall

```bash
# Autoriser uniquement les ports nécessaires
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp  # SSH
ufw enable
```

### Secrets

- ✅ Ne jamais commiter les `.env` files
- ✅ Utiliser des secrets managers (Vault, AWS Secrets Manager)
- ✅ Rotation régulière des clés

---

## 📊 Monitoring

### Prometheus

**Configuration** : `monitoring/prometheus.yml`

**Accès** : http://localhost:9090

**Métriques collectées** :
- Requêtes HTTP
- Latence
- Erreurs
- Utilisation CPU/RAM
- Base de données
- Cache

### Grafana

**Accès** : http://localhost:3001

**Dashboards** :
- Performance API
- Santé du système
- Métriques métier
- Alertes

---

## 💾 Backup & Recovery

### Backup Automatique

**Script de backup** :

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup PostgreSQL
docker exec fear-greed-postgres pg_dump -U fear_greed_user fear_greed_db > \
  "$BACKUP_DIR/db_$DATE.sql"

# Backup Redis (si nécessaire)
docker exec fear-greed-redis redis-cli SAVE
docker cp fear-greed-redis:/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb"

# Compression
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$BACKUP_DIR/db_$DATE.sql" "$BACKUP_DIR/redis_$DATE.rdb"

# Nettoyage (garder 30 jours)
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete
```

**Cron job** (tous les jours à 2h du matin) :
```bash
0 2 * * * /path/to/backup.sh
```

### Restauration

```bash
# Restaurer PostgreSQL
docker exec -i fear-greed-postgres psql -U fear_greed_user fear_greed_db < backup.sql
```

---

## 🔄 CI/CD (Continuous Integration/Continuous Deployment)

### GitHub Actions

**Workflow de déploiement** : `.github/workflows/deploy.yml`

**Étapes** :
1. Tests automatiques
2. Build des images Docker
3. Push vers registry
4. Déploiement sur serveur
5. Health checks

### Exemple Workflow

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and deploy
        run: |
          docker-compose build
          docker-compose up -d
```

---

## ⚖️ Scaling

### Horizontal Scaling

**Plusieurs instances backend** :

```yaml
backend:
  deploy:
    replicas: 3
  # ... config
```

**Load Balancer** :

```nginx
upstream backend {
    least_conn;
    server backend1:8001;
    server backend2:8001;
    server backend3:8001;
}
```

### Vertical Scaling

- Augmenter les ressources (CPU, RAM)
- Optimiser les requêtes DB
- Utiliser le cache efficacement

---

## 📝 Logs

### Centralisation

**ELK Stack** (Elasticsearch, Logstash, Kibana) ou **Loki + Grafana**

**Configuration Docker** :

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Rotation des Logs

```bash
# Logrotate configuration
/path/to/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 🛠️ Maintenance

### Mises à Jour

```bash
# Pull les dernières modifications
git pull

# Rebuild et redémarrage
docker-compose up -d --build

# Migrations
docker exec fear-greed-backend python scripts/migrate.py upgrade
```

### Health Checks

```bash
# Vérifier tous les services
docker-compose ps

# Health check API
curl http://localhost/api/v1/monitoring/health

# Vérifier les logs
docker-compose logs --tail=100
```

### Nettoyage

```bash
# Nettoyer les images inutilisées
docker system prune -a

# Nettoyer les volumes
docker volume prune
```

---

## 🌐 Configuration Nginx

### Reverse Proxy

**Configuration** : `nginx/nginx.conf`

**Fonctions** :
- Routage des requêtes
- SSL/TLS termination
- Compression
- Cache statique
- Rate limiting

### Exemple Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirection HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL config
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://backend:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔧 Scripts Utilitaires

### Déploiement

**`deploy.sh`** : Script de déploiement automatisé

```bash
./deploy.sh production
```

### Backup

**`backup.sh`** : Script de backup automatique

```bash
./backup.sh
```

### Maintenance

**`maintenance.sh`** : Script de maintenance

```bash
./maintenance.sh
```

---

## 📊 Métriques d'Infrastructure

### À Surveiller

- **CPU** : < 80%
- **RAM** : < 80%
- **Disk** : < 85%
- **Network** : Latence < 100ms
- **Database** : Connections < 80% du max
- **Cache** : Hit rate > 70%

### Alertes

Configurer des alertes pour :
- CPU élevé
- RAM insuffisante
- Disk plein
- Service down
- Erreurs élevées

---

## 🚨 Disaster Recovery

### Plan de Récupération

1. **Identification** : Détecter l'incident
2. **Isolation** : Isoler le problème
3. **Restauration** : Restaurer depuis backup
4. **Vérification** : Vérifier le fonctionnement
5. **Documentation** : Documenter l'incident

### RTO (Recovery Time Objective)

**Objectif** : < 1 heure

### RPO (Recovery Point Objective)

**Objectif** : < 24 heures (backup quotidien)

---

## 📚 Ressources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

---

**📖 Pour plus de détails, consultez les fichiers dans `infra/` et `monitoring/`**



