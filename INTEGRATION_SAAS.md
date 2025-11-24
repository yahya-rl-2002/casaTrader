# 🚀 Intégration du Fear & Greed Index dans votre SaaS

Ce projet a été copié depuis `/Volumes/YAHYA SSD/Documents/fear and/` vers `/Volumes/YAHYA SSD/Téléchargements/casablanca-stock/` pour intégration dans votre SaaS.

---

## 📦 **CONTENU DU PROJET**

### **Backend (FastAPI)**
- **API REST** : Endpoints pour récupérer le score Fear & Greed, les composants, l'historique
- **Scraping automatique** : 4 sources de presse marocaine (Medias24, L'Économiste, Challenge, BourseNews)
- **Analyse LLM** : Sentiment des articles avec OpenAI GPT-4o-mini
- **Scheduler** : Mise à jour automatique toutes les 10 minutes
- **Base de données** : SQLite (facilement migratable vers PostgreSQL)

### **Frontend (Next.js)**
- **Dashboard moderne** : Affichage du score avec barre gradient
- **Graphiques** : Historique, breakdown des composants
- **Feed de presse** : Articles récents avec sentiment
- **Dark theme** : Interface professionnelle

---

## 🔑 **CONFIGURATION REQUISE**

### **1. Backend**

```bash
cd /Volumes/YAHYA\ SSD/Téléchargements/casablanca-stock/backend

# Créer l'environnement virtuel
poetry install
# OU
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configurer la clé API OpenAI (pour le LLM)
export OPENAI_API_KEY='votre-clé-api'

# Démarrer le backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **2. Frontend**

```bash
cd /Volumes/YAHYA\ SSD/Téléchargements/casablanca-stock/frontend

# Installer les dépendances
npm install

# Configurer l'URL du backend
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1" > .env.local

# Démarrer le frontend
npm run dev
```

---

## 🔗 **INTÉGRATION DANS VOTRE SAAS**

### **Option 1 : Intégration complète**

Utilisez le backend et le frontend comme **module standalone** dans votre SaaS :

```
votre-saas/
├── modules/
│   └── fear-greed-index/
│       ├── backend/      ← Copier depuis casablanca-stock/backend
│       └── frontend/     ← Copier depuis casablanca-stock/frontend
```

### **Option 2 : API uniquement**

Utilisez uniquement le **backend** comme service API et créez votre propre UI :

```bash
# Démarrer le backend sur un port dédié
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

**Endpoints disponibles :**

```
GET  /api/v1/index/latest          # Score actuel
GET  /api/v1/index/history         # Historique (30d, 90d, 180d, 1y, all)
GET  /api/v1/components/latest     # Détails des 6 composants
GET  /api/v1/media/latest          # Articles de presse récents
GET  /api/v1/volume/latest         # Données de volume
POST /api/v1/scheduler/trigger     # Déclencher une mise à jour manuelle
GET  /api/v1/scheduler/status      # État du scheduler
```

### **Option 3 : Widgets réutilisables**

Extrayez les **composants React** pour les intégrer dans votre UI :

**Composants disponibles :**
- `FearGreedGauge.tsx` : Affichage du score avec barre gradient
- `ComponentBreakdown.tsx` : Breakdown des 6 composants
- `HistoricalChart.tsx` : Graphique historique
- `SentimentFeed.tsx` : Feed d'articles avec sentiment
- `VolumeHeatmap.tsx` : Heatmap des volumes (30 jours)

**Exemple d'utilisation :**

```tsx
import FearGreedGauge from './modules/fear-greed-index/components/FearGreedGauge';

export default function YourDashboard() {
  return (
    <div>
      <h1>Mon SaaS</h1>
      <FearGreedGauge />
    </div>
  );
}
```

---

## 🔧 **PERSONNALISATION**

### **Changer les sources de données**

Modifiez `backend/app/pipelines/ingestion/media_scraper.py` pour ajouter/retirer des sources :

```python
def scrape_all_sources(max_articles_per_source: int = 20) -> List[MediaArticle]:
    # Ajoutez vos propres scrapers ici
    all_articles = []
    
    # Source 1
    all_articles.extend(scrape_medias24())
    
    # Source 2 (votre source custom)
    all_articles.extend(scrape_your_custom_source())
    
    return all_articles
```

### **Modifier la formule du score**

Éditez `backend/app/services/component_calculator.py` pour ajuster les poids :

```python
# Formule actuelle
final_score = (
    momentum * 0.20 +
    price_strength * 0.15 +
    volume * 0.15 +
    volatility * 0.20 +
    equity_vs_bonds * 0.15 +
    media_sentiment * 0.15
)

# Exemple : donner plus de poids au sentiment média
final_score = (
    momentum * 0.15 +
    price_strength * 0.15 +
    volume * 0.10 +
    volatility * 0.15 +
    equity_vs_bonds * 0.15 +
    media_sentiment * 0.30  # 30% au lieu de 15%
)
```

### **Changer le design**

Modifiez les couleurs et le style dans `frontend/app/dashboard/components/` :

```tsx
// FearGreedGauge.tsx - Ligne 56
background: 'linear-gradient(to right, #ef4444 0%, #f97316 25%, #fbbf24 50%, #84cc16 75%, #10b981 100%)'

// Changez par vos couleurs :
background: 'linear-gradient(to right, #votre-rouge, #votre-jaune, #votre-vert)'
```

---

## 🗄️ **MIGRATION VERS POSTGRESQL**

Pour utiliser PostgreSQL au lieu de SQLite :

1. **Installer psycopg2** :
```bash
pip install psycopg2-binary
```

2. **Modifier `backend/app/models/database.py`** :
```python
# Au lieu de SQLite
DATABASE_URL = "sqlite:///./fear_greed_index.db"

# Utilisez PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost/fear_greed_db"
```

3. **Créer la base de données** :
```sql
CREATE DATABASE fear_greed_db;
```

---

## 📊 **DÉPLOIEMENT EN PRODUCTION**

### **Avec Docker Compose**

```bash
cd /Volumes/YAHYA\ SSD/Téléchargements/casablanca-stock
docker-compose up -d
```

### **Sur un serveur (Nginx + Systemd)**

Utilisez les fichiers fournis :
- `deploy.sh` : Script de déploiement
- `nginx/nginx.conf` : Configuration Nginx
- `maintenance.sh` : Script de maintenance

---

## 🔐 **SÉCURITÉ**

### **Variables d'environnement à configurer**

```bash
# Backend
export OPENAI_API_KEY='sk-proj-...'
export DATABASE_URL='postgresql://...'
export SECRET_KEY='your-secret-key'

# Frontend
export NEXT_PUBLIC_API_BASE_URL='https://api.votre-saas.com/fear-greed'
```

### **CORS**

Modifiez `backend/app/main.py` pour autoriser votre domaine :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-saas.com"],  # Votre domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 **PERFORMANCE**

### **Optimisations recommandées**

1. **Cache Redis** : Pour les scores calculés
2. **CDN** : Pour le frontend statique
3. **PostgreSQL** : Pour de meilleures performances en production
4. **Rate limiting** : Pour l'API

---

## 🧪 **TESTS**

```bash
# Backend
cd backend
pytest

# Tests spécifiques
python test_llm_sentiment.py       # Test LLM
python test_complet_systeme.py     # Test complet
```

---

## 📚 **DOCUMENTATION COMPLÈTE**

Consultez les fichiers de documentation :
- `README.md` : Vue d'ensemble
- `CALCUL_DU_SCORE.md` : Explication de la formule
- `INTEGRATION_LLM_COMPLETE.md` : Détails sur le LLM
- `AUTOMATISATION.md` : Système de scheduler

---

## 🆘 **SUPPORT**

### **Problèmes courants**

#### **Le score affiche 50**
- Le pipeline n'a pas encore été exécuté
- Solution : `POST /api/v1/scheduler/trigger`

#### **Erreur OpenAI API**
- Clé API non configurée ou expirée
- Solution : `export OPENAI_API_KEY='nouvelle-clé'`

#### **Articles non scrapés**
- Sites source indisponibles
- Solution : Vérifier les logs avec `tail -f backend.log`

---

## 🚀 **DÉMARRAGE RAPIDE**

```bash
# 1. Aller dans le projet
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"

# 2. Configurer la clé API
export OPENAI_API_KEY='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'

# 3. Démarrer tout le système
./start_with_llm.sh

# 4. Accéder au dashboard
# http://localhost:3000/dashboard
```

---

## ✅ **CHECKLIST D'INTÉGRATION**

- [ ] Backend installé et fonctionnel
- [ ] Frontend installé et fonctionnel
- [ ] Clé API OpenAI configurée
- [ ] Base de données initialisée
- [ ] Premier score calculé
- [ ] Scheduler actif (toutes les 10 min)
- [ ] Dashboard accessible
- [ ] Articles scrapés et analysés
- [ ] Tests passent
- [ ] CORS configuré pour votre domaine
- [ ] Variables d'environnement en production
- [ ] Monitoring configuré (optionnel)

---

## 🎯 **PROCHAINES ÉTAPES**

1. **Tester localement** avec `./start_with_llm.sh`
2. **Personnaliser le design** selon votre charte graphique
3. **Intégrer l'API** dans votre SaaS
4. **Configurer le déploiement** en production
5. **Activer le monitoring** (Prometheus + Grafana)

---

**Bonne intégration ! 🚀**

Si vous avez besoin d'aide, consultez les fichiers de documentation ou les scripts fournis.

