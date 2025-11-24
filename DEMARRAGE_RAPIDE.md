# 🚀 Démarrage Rapide - Fear & Greed Index

## 📋 Prérequis

✅ Python 3.10+  
✅ Node.js 18+  
✅ Environnement virtuel Python activé  
✅ Dépendances npm installées  

---

## 🎯 Méthode 1 : Script Automatique (Recommandé)

### Démarrage du système complet

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"
./start_system.sh
```

Le script va automatiquement :
- ✅ Vérifier les prérequis
- ✅ Démarrer le backend FastAPI sur `http://127.0.0.1:8000`
- ✅ Démarrer le frontend Next.js sur `http://localhost:3000`
- ✅ Ouvrir le dashboard dans votre navigateur

### Arrêt du système

```bash
./stop_system.sh
```

Ou appuyez sur **Ctrl+C** dans le terminal où tourne `start_system.sh`

---

## ⚙️ Méthode 2 : Démarrage Manuel

### Backend (Terminal 1)

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ Backend disponible : `http://127.0.0.1:8000`  
📚 Documentation API : `http://127.0.0.1:8000/docs`

### Frontend (Terminal 2)

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
npm run dev
```

✅ Dashboard disponible : `http://localhost:3000`

---

## 📊 Accès au Dashboard

Une fois le système démarré, ouvrez votre navigateur :

🌐 **http://localhost:3000**

### Ce que vous verrez :

1. **🎯 Jauge principale** - Score Fear & Greed (0-100)
2. **📐 Formule simplifiée** - Détail du calcul avec composantes
3. **📈 Graphique historique** - Évolution sur 90 jours
4. **📊 Décomposition** - 6 composantes avec contributions
5. **📰 Feed médias** - Articles récents avec sentiment
6. **🗺️ Heatmap volume** - Visualisation du trading

---

## 🧪 Tests et Pipelines

### Test complet du système

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
python test_complet_systeme.py
```

### Test de la formule simplifiée

```bash
python test_formule_simplifiee.py
```

### Lancer le pipeline manuellement

```bash
python -c "import asyncio; from app.services.pipeline_service import PipelineService; asyncio.run(PipelineService().run_full_pipeline())"
```

---

## 🔌 Endpoints API Disponibles

### Indice Principal

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/index/latest` | Dernier score F&G |
| `GET /api/v1/index/history?range=90d` | Historique (30d, 90d, 180d, 1y, all) |
| `GET /api/v1/components/latest` | Détail des 6 composantes |

### Formule Simplifiée (Nouvelle !)

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/simplified-v2/score` | Score simplifié avec détails |
| `GET /api/v1/simplified-v2/details` | Calcul complet décomposé |

### Backtest & Analyse

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/backtest/run?range=90d` | Backtest corrélation |
| `GET /api/v1/media/latest` | Feed des articles médias |
| `GET /api/v1/volume/latest` | Données de volume |

### Pipeline

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/pipeline/run` | Lancer le pipeline |
| `GET /api/v1/pipeline/status` | Statut du pipeline |

---

## 🔧 Résolution de Problèmes

### ❌ Backend ne démarre pas

**Symptôme** : `ModuleNotFoundError` ou `ImportError`

**Solution** :
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt  # ou poetry install
```

### ❌ Frontend ne démarre pas

**Symptôme** : `Module not found` ou `npm ERR!`

**Solution** :
```bash
cd frontend
npm install
npm run dev
```

### ❌ CORS Error dans le navigateur

**Symptôme** : `Access-Control-Allow-Origin` error

**Solution** : Vérifier que `NEXT_PUBLIC_API_BASE_URL` dans `.env.local` pointe vers `http://localhost:8000/api/v1`

### ❌ Aucune donnée n'apparaît

**Symptôme** : Dashboard vide ou valeurs par défaut (50)

**Solution** :
```bash
# Lancer le pipeline pour générer des données
cd backend
source .venv/bin/activate
python test_complet_systeme.py
```

### ❌ Port déjà utilisé

**Symptôme** : `Error: listen EADDRINUSE`

**Solution** :
```bash
# Trouver et tuer le processus utilisant le port
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:8000 | xargs kill -9  # Backend
```

---

## 📁 Structure des Logs

Lorsque vous utilisez `start_system.sh`, les logs sont sauvegardés :

- **Backend** : `/tmp/fear-greed-backend.log`
- **Frontend** : `/tmp/fear-greed-frontend.log`

Pour voir les logs en temps réel :
```bash
tail -f /tmp/fear-greed-backend.log
tail -f /tmp/fear-greed-frontend.log
```

---

## 🔄 Mise à Jour des Données

Le système se met à jour automatiquement toutes les **5 minutes**.

Pour forcer une mise à jour immédiate :

### Option 1 : Via l'API
```bash
curl -X POST http://localhost:8000/api/v1/pipeline/run
```

### Option 2 : Via le terminal
```bash
cd backend
source .venv/bin/activate
python -c "import asyncio; from app.services.pipeline_service import PipelineService; asyncio.run(PipelineService().run_full_pipeline())"
```

---

## 📊 Données Sources

Le système collecte des données de :

1. **Marché** : Bourse de Casablanca (MASI)
   - Volume journalier
   - Prix (open, high, low, close)
   - Historique 252 jours

2. **Médias** (20-30 articles) :
   - 📰 Medias24.com (prioritaire)
   - 📊 BourseNews.ma (Espace Investisseurs)
   - 📌 Challenge.ma (12 sections)
   - 🌍 La Vie Éco

3. **Sentiment** : Analyse NLP (spaCy fr_core_news_md)

---

## 🎯 Prochaines Étapes

Une fois le système lancé :

1. ✅ Vérifier que le dashboard affiche des données réelles
2. ✅ Tester les endpoints API via `http://localhost:8000/docs`
3. ✅ Lancer le backtest pour voir les corrélations
4. ✅ Configurer le scheduler pour des mises à jour automatiques

---

## 💡 Astuces

### Démarrage Rapide au Boot

Ajouter à votre `.zshrc` ou `.bashrc` :

```bash
alias fear-start='cd "/Volumes/YAHYA SSD/Documents/fear and" && ./start_system.sh'
alias fear-stop='cd "/Volumes/YAHYA SSD/Documents/fear and" && ./stop_system.sh'
```

Ensuite :
```bash
fear-start  # Démarrer
fear-stop   # Arrêter
```

### Monitoring en Temps Réel

```bash
# Terminal 1: Logs backend
tail -f /tmp/fear-greed-backend.log

# Terminal 2: Logs frontend
tail -f /tmp/fear-greed-frontend.log

# Terminal 3: Monitoring système
watch -n 5 'curl -s http://localhost:8000/api/v1/index/latest | jq'
```

---

## 📞 Support

En cas de problème :

1. Consulter les logs : `/tmp/fear-greed-*.log`
2. Vérifier les prérequis
3. Relancer le script d'installation
4. Consulter la documentation : `http://localhost:8000/docs`

---

**🎉 Système prêt ! Bon trading ! 📈**







