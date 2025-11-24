# 🔧 Solution à l'Erreur "Load failed"

## ❌ Problème

Le bouton "Actualiser le Score" affiche :
```
❌ Erreur: Load failed
```

**Cause** : Le **backend n'est pas démarré** ou n'est pas accessible sur `http://localhost:8000`.

---

## ✅ SOLUTION RAPIDE

### **Étape 1 : Démarrer le Backend**

Ouvrez votre **Terminal Mac** et exécutez :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

# Configurer la clé API (important !)
export OPENAI_API_KEY='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'

# Démarrer le backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Vous devriez voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Le backend est maintenant actif !**

---

### **Étape 2 : Vérifier que le Backend Fonctionne**

Dans un **autre Terminal**, testez :

```bash
curl http://localhost:8000/api/v1/health
```

Devrait retourner :
```json
{"status":"healthy"}
```

✅ **Si vous voyez ça, le backend est OK !**

---

### **Étape 3 : Rafraîchir le Dashboard**

1. Allez sur http://localhost:3000/dashboard
2. Appuyez sur `Cmd + Shift + R` (Mac) pour forcer le rechargement
3. Cliquez sur le bouton **"🔄 Actualiser le Score"**

Cette fois, ça devrait fonctionner ! 🎉

---

## 🚀 MÉTHODE ALTERNATIVE : Script de Démarrage

Si vous voulez démarrer backend + frontend en même temps :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Configurer la clé API
source set_api_key.sh

# Démarrer le système complet
chmod +x start_with_llm.sh
./start_with_llm.sh
```

Ce script démarre automatiquement :
- ✅ Backend sur http://localhost:8000
- ✅ Frontend sur http://localhost:3000
- ✅ Scheduler (update auto toutes les 10 min)

---

## 🔍 Vérification Complète

### 1. Backend est actif ?

```bash
curl http://localhost:8000/api/v1/health
```

✅ Devrait retourner : `{"status":"healthy"}`

---

### 2. Frontend est actif ?

```bash
curl http://localhost:3000
```

✅ Devrait retourner du HTML

---

### 3. Endpoint du scheduler existe ?

```bash
curl -X POST http://localhost:8000/api/v1/scheduler/trigger
```

✅ Devrait retourner : `{"message":"Pipeline triggered successfully"}`

---

## ⚠️ Erreurs Fréquentes

### Erreur 1 : "Connection refused"

**Cause** : Le backend n'est pas démarré

**Solution** :
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='sk-proj-...'
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Erreur 2 : "404 Not Found"

**Cause** : L'endpoint `/scheduler/trigger` n'existe pas

**Solution** : Vérifier que le backend est à jour
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
git status  # Vérifier les modifications
```

---

### Erreur 3 : "Port 8000 already in use"

**Cause** : Un autre processus utilise le port 8000

**Solution** :
```bash
# Trouver le processus
lsof -ti:8000

# Le tuer
kill -9 $(lsof -ti:8000)

# Redémarrer le backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Ce qui devrait se passer après la correction

### 1. Le bouton fonctionne

```
[⏳ Actualisation...]
📰 Scraping des articles de presse...
[████████████░░░░] 60%
```

### 2. Messages de progression

```
🤖 Analyse de sentiment avec LLM...
📊 Calcul du nouveau score...
✅ Score mis à jour ! Rechargement...
```

### 3. Dashboard rafraîchi

Le score se met à jour automatiquement !

---

## 🎯 RÉSUMÉ - Commandes à Exécuter

**Terminal 1 - Backend :**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend (si pas déjà lancé) :**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
npm run dev
```

**Navigateur :**
- http://localhost:3000/dashboard
- Cliquez sur "🔄 Actualiser le Score"

---

## ✅ Checklist

- [ ] Backend démarré (port 8000)
- [ ] Frontend démarré (port 3000)
- [ ] Test `curl http://localhost:8000/api/v1/health` → OK
- [ ] Dashboard accessible (http://localhost:3000/dashboard)
- [ ] Bouton "Actualiser le Score" visible
- [ ] Clic sur le bouton → Messages de progression
- [ ] Score mis à jour après ~60 secondes

---

## 🎉 Une fois corrigé

Vous pourrez cliquer sur le bouton et voir :

1. **Progression en temps réel** avec messages
2. **Barre de progression** de 0% à 100%
3. **Nouveaux articles** scrapés
4. **Nouveau score** calculé
5. **Dashboard** rafraîchi automatiquement

---

**Suivez ces étapes et le bouton fonctionnera ! 🚀**

