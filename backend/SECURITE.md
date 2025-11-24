# 🔒 Améliorations de Sécurité

## ✅ Implémentations Réalisées

### 1. 🔑 Gestion Sécurisée des Clés API

**Problème résolu**: Clé API OpenAI en dur dans `start_all.sh`

**Solution**:
- ✅ Clé retirée du script
- ✅ Chargement depuis `.env` ou variables d'environnement
- ✅ Support dans `config.py` avec `openai_api_key`
- ✅ Priorité: paramètre > config > variable d'environnement

**Fichiers modifiés**:
- `start_all.sh` - Clé retirée, chargement depuis `.env`
- `backend/app/core/config.py` - `openai_api_key` ajouté
- `backend/app/services/llm_sentiment_service.py` - Utilise la config

**Utilisation**:
```bash
# Créer un fichier .env dans backend/
echo 'OPENAI_API_KEY=sk-proj-...' > backend/.env

# Ou utiliser une variable d'environnement
export OPENAI_API_KEY=sk-proj-...
```

### 2. 🔐 Authentification JWT

**Fichier**: `backend/app/core/security.py`

**Fonctionnalités**:
- ✅ Génération de tokens JWT
- ✅ Vérification de tokens
- ✅ Hash de mots de passe (bcrypt)
- ✅ Dépendances FastAPI pour protection d'endpoints

**Endpoints créés**:
- `POST /api/v1/auth/login` - Connexion et obtention d'un token
- `GET /api/v1/auth/me` - Informations utilisateur actuel
- `GET /api/v1/auth/verify` - Vérification de token

**Utilisation**:
```bash
# 1. Se connecter
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Réponse:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "expires_in": 1800
# }

# 2. Utiliser le token
curl http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Protection d'endpoints**:
```python
from app.core.security import get_current_user, TokenData

@router.get("/protected")
async def protected_endpoint(
    current_user: TokenData = Depends(get_current_user)
):
    # Seuls les utilisateurs authentifiés peuvent accéder
    return {"message": f"Hello {current_user.username}"}
```

### 3. ⚡ Rate Limiting

**Fichier**: `backend/app/core/rate_limiter.py`

**Fonctionnalités**:
- ✅ Limite par minute (défaut: 60 requêtes)
- ✅ Limite par heure (défaut: 1000 requêtes)
- ✅ Utilise Redis (ou mémoire) pour le comptage
- ✅ Headers HTTP standards (Retry-After, X-RateLimit-*)
- ✅ Détection automatique de l'IP client (support proxy)

**Configuration**:
```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

**Réponse en cas de limite dépassée**:
```json
{
  "detail": "Rate limit exceeded: 60 requests per minute",
  "retry_after": 45
}
```

**Headers**:
- `Retry-After`: Secondes à attendre
- `X-RateLimit-Limit`: Limite actuelle
- `X-RateLimit-Remaining`: Requêtes restantes
- `X-RateLimit-Reset`: Timestamp de réinitialisation

### 4. 🛡️ CORS Sécurisé

**Avant**:
```python
allow_methods=["*"]
allow_headers=["*"]
```

**Après**:
```python
allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
```

**Avantages**:
- ✅ Moins de surface d'attaque
- ✅ Headers spécifiques uniquement
- ✅ Méthodes HTTP limitées

### 5. ⚙️ Configuration Sécurisée

**Fichier**: `backend/app/core/config.py`

**Nouvelles configurations**:
- `secret_key`: Clé secrète pour JWT (⚠️ CHANGER EN PRODUCTION)
- `algorithm`: Algorithme JWT (HS256)
- `access_token_expire_minutes`: Expiration des tokens (30 min)
- `rate_limit_enabled`: Activer/désactiver le rate limiting
- `rate_limit_per_minute`: Limite par minute
- `rate_limit_per_hour`: Limite par heure

## 📋 Fichiers Créés/Modifiés

### Nouveaux Fichiers
- ✅ `backend/app/core/security.py` - Authentification JWT
- ✅ `backend/app/core/rate_limiter.py` - Rate limiting
- ✅ `backend/app/api/v1/endpoints/auth.py` - Endpoints d'authentification
- ✅ `backend/.env.example` - Template de configuration

### Fichiers Modifiés
- ✅ `start_all.sh` - Clé API retirée
- ✅ `backend/app/core/config.py` - Configurations de sécurité
- ✅ `backend/app/main.py` - Rate limiting middleware + CORS sécurisé
- ✅ `backend/app/api/v1/router.py` - Route auth ajoutée
- ✅ `backend/app/services/llm_sentiment_service.py` - Utilise config
- ✅ `backend/pyproject.toml` - Dépendances JWT ajoutées

## 🚀 Installation

### 1. Installer les Dépendances

```bash
cd backend
poetry install
# ou
pip install python-jose[cryptography] passlib[bcrypt]
```

### 2. Configurer les Variables d'Environnement

```bash
# Copier le template
cp .env.example .env

# Éditer .env et remplir les valeurs
nano .env
```

**Variables importantes**:
```env
# ⚠️  CRITIQUE : Changez en production !
SECRET_KEY=your-very-strong-random-secret-key-here

# OpenAI (optionnel)
OPENAI_API_KEY=sk-proj-...

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

### 3. Générer une Clé Secrète Forte

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

## 🔐 Utilisation

### Authentification

**1. Se connecter**:
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**2. Utiliser le token**:
```bash
TOKEN="votre-token-jwt"

curl http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Protection d'Endpoints

**Exemple**:
```python
from app.core.security import get_current_user, TokenData

@router.post("/sensitive-action")
async def sensitive_action(
    current_user: TokenData = Depends(get_current_user)
):
    # Seuls les utilisateurs authentifiés peuvent accéder
    return {"message": "Action effectuée"}
```

### Rate Limiting

Le rate limiting est **automatique** sur tous les endpoints.

**Vérifier les limites**:
```bash
# Faire 61 requêtes rapidement
for i in {1..61}; do
  curl http://localhost:8001/api/v1/index/latest
done

# La 61ème retournera 429 Too Many Requests
```

## ⚠️ Sécurité en Production

### Checklist Production

- [ ] **SECRET_KEY** changé (générer une clé forte)
- [ ] **OPENAI_API_KEY** dans `.env` (pas dans le code)
- [ ] **CORS** configuré avec les vraies URLs de production
- [ ] **Rate limiting** activé et ajusté
- [ ] **HTTPS** activé (pas HTTP)
- [ ] **Mots de passe** utilisateurs changés (pas "admin123")
- [ ] **Base de données** utilisateurs réelle (pas SIMPLE_USERS)
- [ ] **Logs** ne contiennent pas de secrets
- [ ] **Variables d'environnement** sécurisées (pas commitées)

### Recommandations

1. **Utilisateurs**:
   - Remplacer `SIMPLE_USERS` par une vraie table en DB
   - Implémenter la gestion des rôles (admin, user, etc.)
   - Ajouter la réinitialisation de mot de passe

2. **Tokens**:
   - Implémenter refresh tokens
   - Ajouter la révocation de tokens
   - Logout avec blacklist de tokens

3. **Rate Limiting**:
   - Limites différentes par endpoint
   - Whitelist pour certaines IPs
   - Monitoring des tentatives d'abus

4. **Monitoring**:
   - Alertes sur tentatives d'intrusion
   - Logs des authentifications
   - Métriques de rate limiting

## 🐛 Dépannage

### Token invalide

**Erreur**: `Could not validate credentials`

**Solution**:
1. Vérifier que le token est bien dans le header: `Authorization: Bearer <token>`
2. Vérifier que le token n'est pas expiré
3. Vérifier que `SECRET_KEY` est le même partout

### Rate limit toujours actif

**Problème**: Rate limit bloque même les requêtes légitimes

**Solution**:
```env
# Désactiver temporairement
RATE_LIMIT_ENABLED=false

# Ou augmenter les limites
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_PER_HOUR=5000
```

### CORS bloque les requêtes

**Erreur**: `CORS policy: No 'Access-Control-Allow-Origin'`

**Solution**:
1. Ajouter l'origine dans `allowed_origins` dans `main.py`
2. Vérifier que `allow_credentials=True` si nécessaire

## 📊 Métriques de Sécurité

### Avant
- ❌ Clé API en dur dans le code
- ❌ Pas d'authentification
- ❌ Pas de rate limiting
- ❌ CORS trop permissif

### Après
- ✅ Clés API dans variables d'environnement
- ✅ Authentification JWT
- ✅ Rate limiting actif
- ✅ CORS sécurisé
- ✅ Validation des entrées
- ✅ Headers de sécurité

---

**Date**: 2025-11-13  
**Version**: 1.0.0  
**Statut**: ✅ Implémenté



