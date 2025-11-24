# ⚡ Quick Start - Fear & Greed Index

> **📌 Pour la documentation complète, voir [README_FINAL.md](./README_FINAL.md)**

---

# ⚡ Quick Start - Fear & Greed Index (Version Courte)

## 🚀 Démarrage en 2 Minutes

### **Étape 1 : Démarrer le Backend**

Ouvrez un **nouveau terminal** et exécutez :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
python init_db.py  # Première fois seulement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend prêt sur:** http://localhost:8000
📚 **Documentation API:** http://localhost:8000/docs

---

### **Étape 2 : Démarrer le Frontend**

Ouvrez un **deuxième terminal** et exécutez :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
npm run dev
```

✅ **Frontend prêt sur:** http://localhost:3000
📊 **Dashboard:** http://localhost:3000/dashboard

---

## 🎯 Accéder au Dashboard

1. **Ouvrez votre navigateur**
2. **Allez sur:** `http://localhost:3000/dashboard`
3. **Vous verrez:**
   - 📊 Gauge Fear & Greed (score 0-100)
   - 📈 Graphique historique
   - 🔢 Breakdown des composants
   - 📰 Feed de sentiment média
   - 🗺️ Heatmap de volume

---

## 🔄 Charger des Données Réelles

Une fois que le backend et frontend tournent :

### **Option 1 : Via l'API (Terminal 3)**

```bash
# Lancer le pipeline de données réelles
curl -X POST http://localhost:8000/api/v1/pipeline/run

# Vérifier le statut
curl http://localhost:8000/api/v1/pipeline/status

# Voir le score
curl http://localhost:8000/api/v1/index/latest
```

### **Option 2 : Via le Frontend**

1. Allez sur http://localhost:3000/dashboard
2. Le frontend se rafraîchit automatiquement toutes les 60 secondes
3. Ou rafraîchissez manuellement (F5)

---

## 📊 Ce que Vous Verrez

### **Gauge Principal**
```
┌─────────────────────────────┐
│   FEAR & GREED INDEX        │
│                             │
│         Score: 64.8         │
│                             │
│      Status: GREED 😊       │
│                             │
└─────────────────────────────┘
```

### **Composants**
- 📈 Momentum: 50/100
- 💪 Price Strength: 50/100
- 📊 Volume: 100/100
- 📉 Volatility: 50/100
- 💰 Equity vs Bonds: 50/100
- 📰 Media Sentiment: 50/100

### **Données en Temps Réel**
- ✅ 15 actions de la Bourse de Casablanca
- ✅ 27 articles de 3 sources média
- ✅ 42 points de données réelles

---

## ⚠️ Résolution de Problèmes

### **Backend ne démarre pas**
```bash
# Vérifier Python
python --version  # Doit être 3.9+

# Réinstaller les dépendances
cd backend
poetry install
```

### **Frontend ne démarre pas**
```bash
# Vérifier Node
node --version  # Doit être 18+

# Réinstaller
cd frontend
npm install
```

### **Port déjà utilisé**
```bash
# Tuer le processus sur le port 8000
lsof -ti:8000 | xargs kill -9

# Tuer le processus sur le port 3000
lsof -ti:3000 | xargs kill -9
```

---

## 🎊 C'est Tout !

Votre système Fear & Greed Index est maintenant **opérationnel** avec :

- ✅ 15 actions réelles
- ✅ 27 articles de presse
- ✅ 3 sources média
- ✅ Sentiment analysis
- ✅ Dashboard interactif
- ✅ API REST complète

**Profitez-en ! 🚀**

---

## 📚 Pour Aller Plus Loin

- **Documentation complète:** [START_SYSTEM.md](./START_SYSTEM.md)
- **Guide de déploiement:** [README_DEPLOYMENT.md](./README_DEPLOYMENT.md)
- **Architecture:** [docs/architecture.md](./docs/architecture.md)


