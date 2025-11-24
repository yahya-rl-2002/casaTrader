# 🚀 Guide de Démarrage du Système Fear & Greed Index

## 📋 Prérequis

✅ Python 3.9+ installé
✅ Node.js 18+ installé
✅ Poetry installé (backend)
✅ NPM installé (frontend)

---

## 🔧 Démarrage Rapide

### **Option 1 : Démarrage Manuel (Recommandé pour développement)**

#### **1. Backend (Terminal 1)**

```bash
# Aller dans le dossier backend
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"

# Activer l'environnement virtuel
source .venv/bin/activate

# Initialiser la base de données (première fois seulement)
python init_db.py

# Démarrer le serveur backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend disponible sur:** `http://localhost:8000`
**Documentation API:** `http://localhost:8000/docs`

#### **2. Frontend (Terminal 2)**

```bash
# Aller dans le dossier frontend
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"

# Démarrer le serveur Next.js
npm run dev
```

**Frontend disponible sur:** `http://localhost:3000`

---

### **Option 2 : Démarrage avec Docker (Production)**

```bash
# À la racine du projet
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Démarrer tous les services
docker-compose up -d

# Vérifier les services
docker-compose ps

# Voir les logs
docker-compose logs -f
```

**Services disponibles:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`

---

## 🧪 Tester le Système

### **1. Vérifier le Backend**

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Dernière valeur de l'indice
curl http://localhost:8000/api/v1/index/latest

# Composants
curl http://localhost:8000/api/v1/components/latest
```

### **2. Vérifier le Frontend**

Ouvrir dans le navigateur: `http://localhost:3000/dashboard`

---

## 📊 Initialiser avec des Données

### **Données de Sample (Développement)**

```bash
cd backend
source .venv/bin/activate

# Initialiser la DB avec des données de test
python init_db.py
```

### **Données Réelles (Production)**

```bash
# Lancer le pipeline pour récupérer les vraies données
curl -X POST http://localhost:8000/api/v1/pipeline/run

# Vérifier le statut
curl http://localhost:8000/api/v1/pipeline/status
```

---

## 🎯 URLs Importantes

### **Frontend**
- Dashboard: `http://localhost:3000/dashboard`
- Page d'accueil: `http://localhost:3000`

### **Backend API**
- Health Check: `http://localhost:8000/api/v1/health`
- Documentation Interactive: `http://localhost:8000/docs`
- Index Latest: `http://localhost:8000/api/v1/index/latest`
- Components Latest: `http://localhost:8000/api/v1/components/latest`
- Index History: `http://localhost:8000/api/v1/index/history`
- Metadata: `http://localhost:8000/api/v1/metadata`
- Pipeline Run: `http://localhost:8000/api/v1/pipeline/run` (POST)
- Pipeline Status: `http://localhost:8000/api/v1/pipeline/status`
- Simplified Score: `http://localhost:8000/api/v1/simplified/score`

---

## 🛠️ Dépannage

### **Backend ne démarre pas**

```bash
# Vérifier les dépendances
cd backend
poetry install

# Vérifier Python
python --version  # Doit être 3.9+

# Vérifier la DB
ls -la fear_greed.db

# Réinitialiser la DB
rm fear_greed.db
python init_db.py
```

### **Frontend ne démarre pas**

```bash
# Réinstaller les dépendances
cd frontend
rm -rf node_modules package-lock.json
npm install

# Vérifier Node
node --version  # Doit être 18+

# Nettoyer le cache Next.js
rm -rf .next
```

### **Erreurs de connexion**

```bash
# Vérifier que le backend tourne
curl http://localhost:8000/api/v1/health

# Vérifier les ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Tuer les processus si nécessaire
kill -9 <PID>
```

---

## 📝 Commandes Utiles

### **Backend**

```bash
# Tests
cd backend
pytest tests/

# Tests avec coverage
pytest --cov=app tests/

# Linter
flake8 app/

# Formater le code
black app/
```

### **Frontend**

```bash
# Build production
npm run build

# Linter
npm run lint

# Type checking
npm run type-check
```

---

## 🔄 Mise à Jour des Données

### **Automatique (Cron)**

Le système peut être configuré pour mettre à jour automatiquement les données:

```python
# Dans app/services/scheduler.py
# Configure pour run à 16h00 heure de Casablanca
```

### **Manuel**

```bash
# Lancer le pipeline manuellement
curl -X POST http://localhost:8000/api/v1/pipeline/run

# Ou via Python
cd backend
python -c "
from app.services.pipeline_service import PipelineService
from app.models.database import SessionLocal

db = SessionLocal()
service = PipelineService(db)
import asyncio
asyncio.run(service.run_pipeline())
"
```

---

## 🎊 Système Prêt !

Une fois démarré, vous devriez voir:

### **Backend**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### **Frontend**
```
ready - started server on 0.0.0.0:3000
```

**Ouvrez votre navigateur sur:**
👉 **http://localhost:3000/dashboard**

Et profitez de votre **Fear & Greed Index** avec des **données réelles** ! 🎉

---

## 📞 Support

- Documentation: `/docs` dans le projet
- Tests: `pytest tests/`
- Logs Backend: Console du terminal backend
- Logs Frontend: Console du navigateur (F12)

**Bon développement ! 🚀**








