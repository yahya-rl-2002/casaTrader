# 🚀 Fear & Greed Index - Guide de Déploiement

## 📋 Vue d'Ensemble

Ce guide vous permet de déployer le système Fear & Greed Index complet en production avec monitoring, alertes et maintenance automatisée.

## 🏗️ Architecture de Déploiement

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   PostgreSQL    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (TimescaleDB) │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Worker        │    │   Redis         │
│   (Reverse      │    │   (Scraping)    │    │   (Cache)       │
│   Proxy)        │    │                 │    │   Port: 6379    │
│   Port: 80/443  │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Prometheus    │    │   Grafana       │
│   (Metrics)     │    │   (Dashboards)  │
│   Port: 9090    │    │   Port: 3001    │
└─────────────────┘    └─────────────────┘
```

## 🚀 Déploiement Rapide

### Prérequis
- Docker et Docker Compose installés
- 4GB RAM minimum
- 10GB espace disque

### 1. Déploiement Automatique
```bash
# Cloner le projet
git clone <repository-url>
cd fear-and-greed-index

# Déployer automatiquement
./deploy.sh
```

### 2. Déploiement Manuel
```bash
# Créer les répertoires
mkdir -p logs data/{postgres,redis,prometheus,grafana} backups

# Démarrer les services
docker-compose up -d

# Vérifier le statut
docker-compose ps
```

## 🌐 Accès aux Services

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interface utilisateur |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Documentation Swagger |
| **Prometheus** | http://localhost:9090 | Métriques système |
| **Grafana** | http://localhost:3001 | Dashboards (admin/admin123) |

## 🔧 Maintenance

### Script de Maintenance
```bash
# Voir le statut du système
./maintenance.sh status

# Voir les logs
./maintenance.sh logs

# Redémarrer les services
./maintenance.sh restart

# Sauvegarder la base de données
./maintenance.sh backup

# Vérifier la santé des services
./maintenance.sh health

# Exécuter le pipeline manuellement
./maintenance.sh pipeline
```

### Commandes Docker Compose
```bash
# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend

# Mettre à jour les services
docker-compose pull && docker-compose up -d

# Arrêter tous les services
docker-compose down

# Nettoyer les ressources
docker system prune -a
```

## 📊 Monitoring

### Métriques Disponibles
- **Performance API** : Temps de réponse, débit
- **Utilisation Ressources** : CPU, RAM, Disque
- **Base de Données** : Connexions, requêtes
- **Pipeline** : Exécutions, erreurs
- **Frontend** : Temps de chargement, erreurs

### Alertes Configurées
- Taux d'erreur élevé (>10%)
- Temps de réponse élevé (>1s)
- Services indisponibles
- Utilisation mémoire élevée (>90%)
- Utilisation CPU élevée (>80%)
- Espace disque faible (<10%)

## 🗄️ Base de Données

### PostgreSQL + TimescaleDB
- **Base** : `fear_greed_db`
- **Utilisateur** : `fear_greed_user`
- **Mot de passe** : `fear_greed_password`
- **Port** : 5432

### Sauvegarde
```bash
# Sauvegarde automatique
./maintenance.sh backup

# Sauvegarde manuelle
docker-compose exec postgres pg_dump -U fear_greed_user -d fear_greed_db > backup.sql
```

### Restauration
```bash
# Restaurer depuis une sauvegarde
./maintenance.sh restore backup_20241224_143000.sql
```

## 🔒 Sécurité

### Configuration Sécurisée
- Reverse proxy Nginx avec rate limiting
- Headers de sécurité HTTP
- CORS configuré
- Utilisateurs non-root dans les conteneurs
- Secrets dans les variables d'environnement

### Recommandations
1. **Changer les mots de passe par défaut**
2. **Configurer SSL/TLS** pour la production
3. **Restreindre l'accès** aux ports de monitoring
4. **Sauvegarder régulièrement** la base de données
5. **Monitorer les logs** pour détecter les anomalies

## 📈 Performance

### Optimisations Incluses
- **Compression Gzip** pour les réponses HTTP
- **Cache Redis** pour les données fréquentes
- **Pool de connexions** base de données
- **Rate limiting** pour éviter les abus
- **Monitoring continu** des performances

### Scaling
- **Horizontal** : Ajouter des instances backend
- **Vertical** : Augmenter les ressources des conteneurs
- **Base de données** : Répliques de lecture

## 🚨 Dépannage

### Problèmes Courants

#### Services ne démarrent pas
```bash
# Vérifier les logs
docker-compose logs

# Vérifier les ressources
docker stats

# Redémarrer les services
docker-compose restart
```

#### Base de données inaccessible
```bash
# Vérifier la connexion
docker-compose exec postgres pg_isready -U fear_greed_user -d fear_greed_db

# Redémarrer PostgreSQL
docker-compose restart postgres
```

#### API ne répond pas
```bash
# Vérifier la santé
curl http://localhost:8000/api/v1/health

# Vérifier les logs backend
docker-compose logs backend
```

### Logs Importants
- **Backend** : `docker-compose logs backend`
- **Frontend** : `docker-compose logs frontend`
- **Base de données** : `docker-compose logs postgres`
- **Nginx** : `docker-compose logs nginx`

## 📞 Support

### Informations Système
```bash
# Version Docker
docker --version
docker-compose --version

# Statut des services
./maintenance.sh status

# Santé du système
./maintenance.sh health
```

### Logs de Debug
```bash
# Logs détaillés
docker-compose logs --tail=100 -f

# Logs d'un service spécifique
docker-compose logs --tail=100 -f backend
```

## 🎯 Prochaines Étapes

1. **Configuration SSL** pour HTTPS
2. **Authentification** utilisateur
3. **API Rate Limiting** avancé
4. **Backup automatique** programmé
5. **Alertes par email/Slack**
6. **Scaling automatique**

---

**🎉 Félicitations !** Votre système Fear & Greed Index est maintenant déployé et opérationnel en production !







