# 📚 Documentation Complète

Bienvenue dans la documentation du système **Fear & Greed Index - Bourse de Casablanca**.

---

## 📖 Guides Disponibles

### 🚀 [Installation](./INSTALLATION.md)
Guide complet d'installation et de configuration du système.

**Contenu** :
- Prérequis
- Installation pas à pas
- Configuration
- Dépannage

---

### 📡 [API Documentation](./API.md)
Documentation complète de l'API REST.

**Contenu** :
- Tous les endpoints disponibles
- Exemples de requêtes
- Codes d'erreur
- Authentification
- Rate limiting

---

### 💻 [Guide de Développement](./DEVELOPMENT.md)
Guide pour les développeurs.

**Contenu** :
- Structure du projet
- Workflow de développement
- Ajouter des fonctionnalités
- Tests
- Code style

---

### 🏗️ [Architecture](./ARCHITECTURE.md)
Architecture et design du système.

**Contenu** :
- Vue d'ensemble
- Composants principaux
- Flux de données
- Patterns utilisés
- Scalabilité

---

## 📋 Documentation Technique

### Backend

- **[Migrations](../backend/MIGRATIONS.md)** - Gestion des migrations de base de données
- **[Monitoring](../backend/MONITORING.md)** - Monitoring et observabilité
- **[Sécurité](../backend/SECURITE.md)** - Sécurité et authentification
- **[Cache et Performance](../backend/CACHE_ET_PERFORMANCE.md)** - Optimisations

### Frontend

- Documentation frontend à venir

---

## 🔍 Recherche Rapide

### Par Sujet

**Installation** :
- [Installation Guide](./INSTALLATION.md)
- [Configuration](../backend/.env.example)

**API** :
- [API Documentation](./API.md)
- [Swagger UI](http://localhost:8001/docs)

**Développement** :
- [Development Guide](./DEVELOPMENT.md)
- [Architecture](./ARCHITECTURE.md)

**Base de données** :
- [Migrations](../backend/MIGRATIONS.md)
- [Models](../backend/app/models/schemas.py)

**Monitoring** :
- [Monitoring](../backend/MONITORING.md)
- [Health Checks](./API.md#-monitoring)

---

## 🆘 Support

### Problèmes Courants

**Backend ne démarre pas** :
→ Voir [Installation Guide](./INSTALLATION.md#dépannage)

**Erreurs de base de données** :
→ Voir [Migrations](../backend/MIGRATIONS.md#dépannage)

**Problèmes d'authentification** :
→ Voir [Sécurité](../backend/SECURITE.md)

**Métriques non visibles** :
→ Voir [Monitoring](../backend/MONITORING.md#dépannage)

---

## 📞 Ressources

- **API Interactive** : http://localhost:8001/docs
- **Health Check** : http://localhost:8001/api/v1/monitoring/health
- **Métriques** : http://localhost:8001/api/v1/monitoring/metrics

---

## 🔄 Mises à Jour

Cette documentation est maintenue à jour avec le code. En cas de divergence, le code fait foi.

**Dernière mise à jour** : 2025-11-15

---

**💡 Astuce** : Utilisez la recherche de votre éditeur (Cmd/Ctrl + F) pour trouver rapidement des informations dans cette documentation.
