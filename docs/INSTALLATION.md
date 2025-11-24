# 🚀 Guide d'Installation

## Prérequis

- **Python** 3.10 ou supérieur
- **Node.js** 18 ou supérieur
- **npm** ou **yarn**
- **Git**

### Optionnel (pour production)
- **PostgreSQL** 12+
- **Redis** 6+
- **Docker** et **Docker Compose**

---

## Installation Rapide

### 1. Cloner le Repository

```bash
git clone <repository-url>
cd casablanca-stock
```

### 2. Backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
# ou avec Poetry
poetry install
```

### 3. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et configurer :
# - DATABASE_URL
# - SECRET_KEY (générer une clé forte)
# - OPENAI_API_KEY (optionnel)
# - REDIS_URL (optionnel)
# - SUPABASE_* (optionnel)
```

**Générer une SECRET_KEY** :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Base de Données

#### SQLite (Développement - Par défaut)
Aucune configuration nécessaire. La base sera créée automatiquement.

#### PostgreSQL (Production)
```bash
# Créer la base de données
createdb fear_greed

# Configurer DATABASE_URL dans .env
DATABASE_URL=postgresql://user:password@localhost:5432/fear_greed
```

### 5. Migrations

```bash
# Appliquer les migrations
python scripts/migrate.py upgrade
```

### 6. Frontend

```bash
cd ../frontend  # ou src selon la structure

# Installer les dépendances
npm install
# ou
yarn install
```

---

## Démarrage

### Développement

#### Backend
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### Frontend
```bash
cd frontend  # ou src
npm run dev
# ou
yarn dev
```

### Production

Utiliser les scripts fournis :

```bash
# Démarrer tout
./start_all.sh

# Arrêter tout
./stop_all.sh
```

---

## Vérification

### Backend
```bash
curl http://localhost:8001/api/v1/health/ping
# Devrait retourner: {"status": "ok"}
```

### Frontend
Ouvrir http://localhost:8080 dans le navigateur.

### API Documentation
Ouvrir http://localhost:8001/docs pour la documentation interactive.

---

## Configuration Avancée

### Redis (Cache)

```bash
# Installer Redis
# macOS
brew install redis
redis-server

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Configurer dans .env
REDIS_URL=redis://localhost:6379/0
```

### PostgreSQL avec TimescaleDB

```bash
# Installer TimescaleDB
# Voir: https://docs.timescale.com/install

# Créer l'extension
psql -d fear_greed -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Configurer dans .env
DATABASE_URL=postgresql://user:password@localhost:5432/fear_greed
TIMESCALE_ENABLED=true
```

### Supabase (Optionnel)

```bash
# Configurer dans .env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

---

## Docker (Optionnel)

### Backend
```bash
cd backend
docker build -t fear-greed-backend .
docker run -p 8001:8001 --env-file .env fear-greed-backend
```

### Frontend
```bash
cd frontend
docker build -t fear-greed-frontend .
docker run -p 8080:80 fear-greed-frontend
```

### Docker Compose
```bash
docker-compose up -d
```

---

## Dépannage

### Port déjà utilisé

```bash
# Trouver le processus
lsof -ti:8001  # Backend
lsof -ti:8080  # Frontend

# Tuer le processus
lsof -ti:8001 | xargs kill -9
```

### Erreurs de dépendances

```bash
# Réinstaller les dépendances
cd backend
pip install --upgrade -r requirements.txt

cd ../frontend
npm install --force
```

### Erreurs de base de données

```bash
# Vérifier la connexion
cd backend
python -c "from app.models.database import engine; engine.connect()"

# Réinitialiser (⚠️ supprime les données)
rm fear_greed.db
python scripts/migrate.py upgrade
```

### Erreurs de cache

```bash
# Vérifier Redis
redis-cli ping
# Devrait retourner: PONG

# Si Redis n'est pas disponible, le système utilisera le cache en mémoire
```

---

## Tests

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

---

## Production

### Checklist

- [ ] SECRET_KEY changé et sécurisé
- [ ] DATABASE_URL configuré (PostgreSQL)
- [ ] REDIS_URL configuré
- [ ] CORS configuré avec les vraies URLs
- [ ] HTTPS activé
- [ ] Logs configurés
- [ ] Monitoring configuré (Prometheus)
- [ ] Backup de la base de données configuré

### Variables d'Environnement Production

```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<clé-forte-générée>
REDIS_URL=redis://host:6379/0
CORS_ORIGINS=https://yourdomain.com
```

---

**✅ Installation terminée ! Consultez [API.md](./API.md) pour l'utilisation de l'API.**



