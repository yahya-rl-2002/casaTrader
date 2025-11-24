# 🏗️ Infrastructure - Guide Rapide

## 📋 Vue d'Ensemble

L'infrastructure permet de déployer, monitorer et maintenir l'application en production de manière professionnelle.

---

## 🚀 Démarrage Rapide

### Développement

```bash
# Démarrer tous les services
./start_all.sh

# Ou avec Docker
docker-compose up -d
```

### Production

```bash
# Déploiement complet
./scripts/deploy-production.sh

# Avec Docker Compose production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 📦 Services Disponibles

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 8080 | Application React |
| Backend API | 8001 | API FastAPI |
| PostgreSQL | 5432 | Base de données |
| Redis | 6379 | Cache |
| Prometheus | 9090 | Métriques |
| Grafana | 3001 | Dashboards |

---

## 🔧 Scripts Utilitaires

### Backup

```bash
# Backup simple
./scripts/backup.sh

# Backup compressé
./scripts/backup.sh --compress

# Backup avec upload S3
BACKUP_S3_BUCKET=my-bucket ./scripts/backup.sh --compress --upload
```

### Restauration

```bash
./scripts/restore.sh backups/backup_20251115_120000.tar.gz
```

### Health Check

```bash
# Check simple
./scripts/health-check.sh

# Check détaillé
./scripts/health-check.sh --verbose
```

### Maintenance

```bash
# Nettoyage
./scripts/maintenance.sh clean

# Mise à jour
./scripts/maintenance.sh update

# Migrations
./scripts/maintenance.sh migrate

# Redémarrage
./scripts/maintenance.sh restart

# Statut
./scripts/maintenance.sh status

# Logs
./scripts/maintenance.sh logs backend
```

### SSL/TLS

```bash
# Configuration SSL avec Let's Encrypt
./scripts/setup-ssl.sh yourdomain.com
```

### Cron Jobs

```bash
# Installer les tâches automatiques
./scripts/setup-cron.sh
```

---

## 🔄 CI/CD

### GitHub Actions

Les workflows sont dans `.github/workflows/` :

- **`ci.yml`** : Tests et linting automatiques
- **`deploy.yml`** : Déploiement automatique en production

**Déclenchement** :
- Push sur `main` → Déploiement automatique
- Pull Request → Tests automatiques

---

## 💾 Backup Automatique

### Configuration

Les backups sont configurés via cron (voir `setup-cron.sh`) :

- **Quotidien** : 2h du matin
- **Rétention** : 30 jours par défaut
- **Compression** : Automatique

### Restauration

```bash
# Lister les backups
ls -lh backups/

# Restaurer
./scripts/restore.sh backups/backup_YYYYMMDD_HHMMSS.tar.gz
```

---

## 🏥 Monitoring

### Prometheus

**Accès** : http://localhost:9090

**Métriques** :
- Requêtes HTTP
- Latence
- Erreurs
- Utilisation ressources

### Grafana

**Accès** : http://localhost:3001

**Login** : `admin` / `admin123` (⚠️ changer en production)

**Dashboards** :
- Performance API
- Santé système
- Métriques métier

---

## 🔒 Sécurité

### SSL/TLS

```bash
# Configuration automatique
./scripts/setup-ssl.sh yourdomain.com
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

- ✅ Ne jamais commiter `.env` files
- ✅ Utiliser des secrets managers en production
- ✅ Rotation régulière des clés

---

## 📊 Scaling

### Horizontal (Plus d'instances)

Modifier `docker-compose.yml` :

```yaml
backend:
  deploy:
    replicas: 3
```

### Vertical (Plus de ressources)

Modifier `docker-compose.prod.yml` :

```yaml
backend:
  deploy:
    resources:
      limits:
        memory: 4G
        cpus: '4'
```

---

## 🛠️ Dépannage

### Services ne démarrent pas

```bash
# Voir les logs
docker-compose logs

# Vérifier les conteneurs
docker-compose ps

# Redémarrer
docker-compose restart
```

### Base de données inaccessible

```bash
# Vérifier PostgreSQL
docker-compose exec postgres pg_isready

# Vérifier les connexions
docker-compose exec postgres psql -U fear_greed_user -d fear_greed_db -c "SELECT 1"
```

### Performance dégradée

```bash
# Vérifier les ressources
docker stats

# Vérifier les logs
docker-compose logs --tail=100 backend
```

---

## 📚 Documentation Complète

- **Guide complet** : `docs/INFRASTRUCTURE.md`
- **Architecture** : `docs/ARCHITECTURE.md`
- **Déploiement** : `README_DEPLOYMENT.md`

---

## 🎯 Checklist Production

- [ ] Variables d'environnement configurées
- [ ] SSL/TLS configuré
- [ ] Firewall configuré
- [ ] Backups automatiques activés
- [ ] Monitoring configuré
- [ ] Health checks fonctionnels
- [ ] Logs centralisés
- [ ] Secrets sécurisés
- [ ] Scaling configuré (si nécessaire)

---

**📖 Pour plus de détails, consultez `docs/INFRASTRUCTURE.md`**



