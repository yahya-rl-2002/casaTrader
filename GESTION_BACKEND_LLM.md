# 🛑 Gestion du Backend Fear & Greed (LLM GPT) 

**Date** : 29 octobre 2025

---

## 🎯 **CONTRÔLE DU BACKEND**

Le backend Fear & Greed utilise l'**API OpenAI GPT** pour analyser le sentiment des articles de presse.

---

## 🛑 **ARRÊTER LE BACKEND (Pause LLM)**

### **Méthode 1 : Via le Port**

```bash
lsof -ti:8001 | xargs kill -9
```

**Résultat :** ✅ Backend arrêté, LLM en pause

### **Méthode 2 : Via le Processus**

```bash
# Trouver le processus
ps aux | grep uvicorn

# Tuer le processus (remplacez PID)
kill -9 <PID>
```

### **Méthode 3 : Dans le Terminal**

Si le backend tourne dans un terminal visible :

```bash
Ctrl + C
```

---

## ✅ **VÉRIFIER L'ÉTAT DU BACKEND**

```bash
# Vérifier si le backend tourne
lsof -i :8001

# Si vide → Backend arrêté ✅
# Si résultat → Backend en cours ⚠️
```

---

## 🚀 **REDÉMARRER LE BACKEND**

Quand vous voulez **réactiver le LLM** :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

**OU en arrière-plan :**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
nohup uvicorn app.main:app --host 0.0.0.0 --port 8001 > backend.log 2>&1 &
```

---

## 📊 **IMPACT DE L'ARRÊT**

### **Quand le Backend est ARRÊTÉ** ⏸️

- ❌ **Pas de nouvelles données** : Le score ne se met plus à jour
- ❌ **Pas de scraping** : Pas de nouveaux articles collectés
- ❌ **Pas d'analyse LLM** : Pas de sentiment analysé
- ❌ **Dashboard affiche erreur** : "Impossible de récupérer les données"
- ✅ **Pas de consommation API OpenAI** : Économie de crédits !

### **Quand le Backend est EN COURS** ▶️

- ✅ **Données en temps réel** : Score mis à jour automatiquement
- ✅ **Scraping actif** : Nouveaux articles toutes les 10 minutes
- ✅ **Analyse LLM active** : Sentiment analysé par GPT
- ✅ **Dashboard fonctionnel** : Toutes les données disponibles
- ⚠️ **Consommation API OpenAI** : Utilise vos crédits

---

## 💰 **ÉCONOMISER LES CRÉDITS API**

### **Stratégie 1 : Arrêt Nocturne**

Arrêtez le backend la nuit pour économiser :

```bash
# À 22h : Arrêter
lsof -ti:8001 | xargs kill -9

# À 8h : Redémarrer
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='...'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### **Stratégie 2 : Scraping Manuel**

Au lieu du scraping automatique toutes les 10 min :

1. Gardez le backend arrêté
2. Démarrez-le uniquement quand vous voulez actualiser
3. Cliquez sur "Actualiser le Score" dans le dashboard
4. Arrêtez-le après

### **Stratégie 3 : Mode Démo**

Utilisez les données déjà collectées sans scraper de nouveau :

- Backend arrêté
- Dashboard affiche "Données indisponibles"
- Mais les graphiques historiques restent visibles (localStorage)

---

## 🔄 **AUTOMATISATION**

### **Script de Démarrage**

Créez un script `start_backend.sh` :

```bash
#!/bin/bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

**Utilisation :**
```bash
chmod +x start_backend.sh
./start_backend.sh
```

### **Script d'Arrêt**

Créez un script `stop_backend.sh` :

```bash
#!/bin/bash
echo "🛑 Arrêt du backend Fear & Greed..."
lsof -ti:8001 | xargs kill -9
echo "✅ Backend arrêté"
```

**Utilisation :**
```bash
chmod +x stop_backend.sh
./stop_backend.sh
```

---

## 📱 **DASHBOARD SANS BACKEND**

Quand le backend est arrêté, le dashboard affiche :

```
┌─────────────────────────────────────┐
│ ⚠️ Impossible de récupérer les     │
│    données                          │
│                                     │
│ Assurez-vous que le backend est    │
│ démarré sur le port 8001            │
│                                     │
│ [Réessayer]                         │
└─────────────────────────────────────┘
```

**Pour réessayer :**
1. Redémarrez le backend
2. Cliquez sur "Réessayer" dans le dashboard
3. Ou rechargez la page (F5)

---

## 🎯 **RECOMMANDATIONS**

### **Pour le Développement**

- ✅ **Gardez le backend EN COURS** pour tester
- ✅ **Utilisez le bouton "Actualiser"** pour forcer une mise à jour
- ✅ **Surveillez les logs** : `tail -f backend.log`

### **Pour la Production**

- ✅ **Démarrez le backend en arrière-plan** avec `nohup`
- ✅ **Configurez un cron job** pour redémarrer automatiquement
- ✅ **Surveillez la consommation API** OpenAI

### **Pour Économiser**

- ✅ **Arrêtez le backend la nuit**
- ✅ **Désactivez le scraping automatique** (modifier le code)
- ✅ **Utilisez uniquement en journée** (heures de trading)

---

## 🔧 **DÉSACTIVER LE SCRAPING AUTOMATIQUE**

Si vous voulez garder le backend EN COURS mais **sans scraper automatiquement** :

### **Méthode 1 : Modifier le Scheduler**

Éditez `/Volumes/YAHYA SSD/Documents/fear and/backend/app/services/scheduler.py` :

```python
# Commentez cette ligne :
# scheduler.add_job(run_daily_update, ...)
```

### **Méthode 2 : Augmenter l'Intervalle**

Changez l'intervalle de 10 min à 24h :

```python
scheduler.add_job(
    run_daily_update,
    trigger=IntervalTrigger(hours=24),  # Au lieu de minutes=10
    id="daily_update",
)
```

---

## 📊 **MONITORING**

### **Vérifier les Logs**

```bash
# Logs du backend
tail -f "/Volumes/YAHYA SSD/Documents/fear and/backend/backend.log"

# Chercher les appels LLM
grep "LLM" "/Volumes/YAHYA SSD/Documents/fear and/backend/backend.log"

# Compter les appels API
grep "OpenAI" "/Volumes/YAHYA SSD/Documents/fear and/backend/backend.log" | wc -l
```

### **Vérifier la Consommation API**

Allez sur : https://platform.openai.com/usage

---

## 🎯 **RÉSUMÉ RAPIDE**

| Action | Commande |
|--------|----------|
| **Arrêter** | `lsof -ti:8001 \| xargs kill -9` |
| **Vérifier** | `lsof -i :8001` |
| **Démarrer** | `uvicorn app.main:app --host 0.0.0.0 --port 8001` |
| **Logs** | `tail -f backend.log` |

---

## ✅ **ÉTAT ACTUEL**

```
✅ Backend arrêté
✅ Port 8001 libre
✅ LLM en pause
✅ Pas de consommation API
```

**Pour réactiver, lancez :**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

---

**Le backend Fear & Greed est maintenant en pause ! 🛑**

**Aucune consommation d'API OpenAI jusqu'à ce que vous le redémarriez ! 💰**

