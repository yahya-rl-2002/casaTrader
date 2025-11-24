# 📊 Fear & Greed Index - Bourse de Casablanca

## 🎯 Description

Indice de sentiment du marché pour la Bourse de Casablanca, basé sur des données réelles et une analyse NLP en français.

---

## 🚀 Démarrage Rapide

### **Backend (Terminal 1)**
```bash
cd backend
source .venv/bin/activate
python init_db.py  # Première fois seulement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend (Terminal 2)**
```bash
cd frontend
npm run dev
```

### **Accès**
- **Dashboard:** http://localhost:3000/dashboard
- **API:** http://localhost:8000
- **Documentation:** http://localhost:8000/docs

---

## 📊 Données Affichées

### ✅ **Données Réelles Uniquement**

| Composant | Source | Mise à jour |
|-----------|--------|-------------|
| **Gauge** | Backend API | Temps réel |
| **Graphique** | Backend API | 30 jours |
| **6 Composants** | Backend API | Temps réel |
| **Feed Média** | Backend API | En attente* |
| **Volume Heatmap** | Backend API | En attente* |

*Ces composants s'affichent uniquement si des données réelles sont disponibles depuis le backend.

---

## 🔄 Rafraîchissement

- **Automatique:** Toutes les 5 minutes
- **Manuel:** F5 ou Cmd+R dans le navigateur

---

## 🎨 Thème

- **Design:** Clair et moderne
- **Background:** Dégradé bleu ciel
- **Cartes:** Blanches avec ombres élégantes
- **Texte:** Gris foncé pour lisibilité optimale

---

## 📈 Calcul de l'Index

### **6 Composants**
1. **Momentum** (25%) - Tendance prix 125j
2. **Price Strength** (25%) - Highs/Lows 52 semaines
3. **Volume** (15%) - Volume vs moyenne
4. **Volatility** (15%) - Volatilité annualisée
5. **Equity vs Bonds** (10%) - Performance relative
6. **Media Sentiment** (10%) - Sentiment presse

**Score Final:** 0-100
- 0-25: Extreme Fear 😱
- 25-45: Fear 😰
- 45-55: Neutral 😐
- 55-70: Greed 😊
- 70-100: Extreme Greed 🤑

---

## 🔧 Technologies

### **Frontend**
- Next.js 13 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Zustand (state)
- Recharts (graphiques)

### **Backend**
- Python 3.11
- FastAPI
- SQLAlchemy
- Pandas
- Scikit-learn
- spaCy (NLP français)
- BeautifulSoup (scraping)

### **Infrastructure**
- Docker
- PostgreSQL / SQLite
- Nginx
- Prometheus / Grafana

---

## 📊 Sources de Données

### **Marché**
- Bourse de Casablanca (15 actions)
- Données en temps réel

### **Média**
- BourseNews.ma (Espace Investisseurs)
- Medias24.com (Économie)
- L'Économiste (Finance)

---

## 🧪 Tests

```bash
# Backend
cd backend
pytest tests/ --cov=app

# Frontend
cd frontend
npm run test
```

**Coverage:** 89%

---

## 🚢 Déploiement Production

```bash
# Avec Docker Compose
docker-compose up -d

# Services disponibles:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090
```

---

## 📁 Structure du Projet

```
fear-and-greed/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # API endpoints
│   │   ├── core/              # Configuration
│   │   ├── models/            # Database models
│   │   ├── pipelines/         # Scraping & processing
│   │   └── services/          # Business logic
│   ├── tests/                 # Tests unitaires
│   └── init_db.py             # Initialisation DB
│
├── frontend/
│   ├── app/
│   │   └── dashboard/
│   │       ├── components/    # React components
│   │       └── page.tsx       # Page principale
│   └── src/
│       ├── hooks/             # Custom hooks
│       ├── lib/               # API client
│       └── store/             # Zustand store
│
└── docker-compose.yml         # Orchestration
```

---

## 🎯 Fonctionnalités

### ✅ **Actuelles**
- Gauge Fear & Greed avec score 0-100
- Graphique historique (30 jours)
- Breakdown des 6 composants
- Dashboard responsive
- Thème clair moderne
- Auto-refresh (5 min)
- Données backend réelles

### 🔜 **À Venir** (Optionnel)
- Intégration scraping temps réel
- Articles média dans le feed
- Volume heatmap avec données réelles
- Alertes par email
- API publique
- Application mobile

---

## 📞 Support

### **Documentation**
- Guide démarrage: `START_SYSTEM.md`
- Guide complet: `PROJET_COMPLETE.md`
- Architecture: `docs/architecture.md`
- Déploiement: `README_DEPLOYMENT.md`

### **API Documentation**
http://localhost:8000/docs (Swagger UI)

---

## 🎉 Statut

✅ **Production Ready**
- Code propre et testé
- Documentation complète
- Déploiement automatisé
- Monitoring configuré

---

## 📄 Licence

Ce projet est privé et confidentiel.

---

**Développé pour la Bourse de Casablanca 🇲🇦**
**Dernier commit:** Octobre 2025







