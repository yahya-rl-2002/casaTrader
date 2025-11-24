# 🚀 Démarrage Unifié - Tout sur le Port 8080 !

**Date** : 29 octobre 2025  
**Statut** : ✅ **CONFIGURATION TERMINÉE**

---

## 🎯 **CE QUI A CHANGÉ**

✅ **Proxy Vite configuré** : Tous les appels `/api/v1/*` sont redirigés vers le backend (port 8001)

✅ **Frontend et Backend sur le même port** : Accédez à tout via `http://localhost:8080`

✅ **Scripts de démarrage unifiés** :
- `start_all.sh` → Lance backend + frontend
- `stop_all.sh` → Arrête tout

✅ **Pas de problèmes CORS** : Le proxy gère tout !

---

## 🚀 **DÉMARRAGE RAPIDE**

### **Option 1 : Script Automatique (Recommandé)**

```bash
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
./start_all.sh
```

Le script va :
1. Démarrer le backend Fear & Greed sur le port 8001
2. Démarrer le frontend SaaS sur le port 8080 (avec proxy)
3. Afficher les URLs d'accès

### **Option 2 : Manuel**

**Terminal 1 - Backend :**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend :**
```bash
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
npm run dev
```

---

## 🌐 **ACCÈS AUX SERVICES**

**Tout passe par le port 8080 maintenant !**

| Service | URL | Description |
|---------|-----|-------------|
| **SaaS Principal** | http://localhost:8080 | Page d'accueil |
| **Fear & Greed Card** | http://localhost:8080/fear-greed | Carte cliquable |
| **Dashboard Complet** | http://localhost:8080/fear-greed-dashboard | Analyse détaillée |
| **API (via proxy)** | http://localhost:8080/api/v1/index/latest | Score actuel |
| **Backend Direct** | http://localhost:8001 | (Optionnel) |

---

## ⚙️ **ARCHITECTURE UNIFIÉE**

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  Navigateur  http://localhost:8080                   │
│                                                        │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│                                                        │
│  Frontend Vite (Port 8080)                            │
│  ├─ Pages React (SaaS)                                │
│  ├─ /fear-greed                                       │
│  ├─ /fear-greed-dashboard                             │
│  └─ Proxy: /api/v1/* → http://localhost:8001         │
│                                                        │
└───────────────────┬────────────────────────────────────┘
                    │
                    │ Proxy automatique
                    │ (pas de CORS !)
                    ▼
┌────────────────────────────────────────────────────────┐
│                                                        │
│  Backend FastAPI (Port 8001)                          │
│  ├─ GET /api/v1/index/latest                          │
│  ├─ GET /api/v1/components/latest                     │
│  ├─ GET /api/v1/media/latest                          │
│  └─ Base de données SQLite                            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🔧 **CONFIGURATION DU PROXY**

Dans `vite.config.ts` :

```typescript
server: {
  host: true,
  port: 8080,
  proxy: {
    '/api/v1': {
      target: 'http://localhost:8001',
      changeOrigin: true,
      secure: false,
    },
  },
}
```

**Ce que ça fait :**
- Requête : `http://localhost:8080/api/v1/index/latest`
- Proxy → `http://localhost:8001/api/v1/index/latest`
- Réponse renvoyée au frontend

**Avantages :**
✅ Pas de CORS
✅ Même origine (localhost:8080)
✅ URLs simplifiées
✅ Prêt pour la production

---

## 📊 **MODIFICATION DES COMPOSANTS**

Les composants utilisent maintenant des **URLs relatives** :

**Avant :**
```typescript
const API_BASE_URL = 'http://localhost:8001/api/v1';
```

**Après :**
```typescript
const API_BASE_URL = '/api/v1';  // Proxy automatique !
```

**Fichiers modifiés :**
- `src/pages/FearGreedIndex.tsx`
- `src/pages/FearGreedDashboard.tsx`

---

## 🛑 **ARRÊTER LES SERVEURS**

### **Option 1 : Script Automatique**

```bash
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
./stop_all.sh
```

### **Option 2 : Manuel**

```bash
# Arrêter tous les serveurs sur les ports 8001 et 8080
lsof -ti:8001,8080 | xargs kill -9
```

---

## 📝 **LOGS**

Les logs sont sauvegardés dans :

```
/Volumes/YAHYA SSD/Téléchargements/casablanca-stock/logs/
├── backend.log    # Logs du backend FastAPI
├── frontend.log   # Logs du frontend Vite
├── backend.pid    # PID du processus backend
└── frontend.pid   # PID du processus frontend
```

**Voir les logs en temps réel :**

```bash
# Backend
tail -f logs/backend.log

# Frontend
tail -f logs/frontend.log

# Les deux en même temps
tail -f logs/*.log
```

---

## 🔍 **VÉRIFIER QUE TOUT FONCTIONNE**

### **1. Vérifier les ports**

```bash
lsof -i :8001,8080
```

Vous devriez voir :
```
COMMAND   PID USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
Python   1234 user    3u  IPv4  0x1234      0t0  TCP *:8001 (LISTEN)
node     5678 user   18u  IPv6  0x5678      0t0  TCP *:8080 (LISTEN)
```

### **2. Tester l'API via le proxy**

```bash
curl http://localhost:8080/api/v1/index/latest
```

Devrait retourner :
```json
{
  "score": 52.30,
  "label": "NEUTRAL",
  "as_of": "2025-10-29T..."
}
```

### **3. Tester dans le navigateur**

1. Allez sur : http://localhost:8080/fear-greed
2. Ouvrez **DevTools** (F12) → **Network**
3. Actualisez la page
4. Vérifiez que `/api/v1/index/latest` est appelé **sans erreur CORS**

---

## 🚨 **DÉPANNAGE**

### **Erreur : "Failed to fetch"**

**Cause** : Le backend n'est pas démarré

**Solution** :
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='...'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### **Erreur : "Address already in use"**

**Cause** : Un serveur est déjà en cours

**Solution** :
```bash
# Voir quel processus utilise le port
lsof -i :8001  # ou :8080

# Tuer le processus
kill -9 <PID>

# Ou tuer tous les processus sur ces ports
lsof -ti:8001,8080 | xargs kill -9
```

### **Le proxy ne fonctionne pas**

**Cause** : Vite n'a pas redémarré après modification du config

**Solution** :
```bash
# Arrêter Vite (Ctrl+C dans le terminal)
# Relancer
npm run dev
```

### **Erreur 502 Bad Gateway**

**Cause** : Le backend est arrêté ou n'écoute pas sur le bon port

**Solution** : Vérifiez que le backend est bien sur le port 8001 :
```bash
curl http://localhost:8001/api/v1/index/latest
```

---

## 🎉 **AVANTAGES DE CETTE CONFIGURATION**

✅ **Simplicité** : Un seul port (8080) pour tout

✅ **Pas de CORS** : Le proxy Vite gère la communication

✅ **Production-ready** : Configuration similaire à Nginx/Apache

✅ **Développement rapide** : HMR (Hot Module Replacement) fonctionne

✅ **Logs centralisés** : Tout dans `logs/`

✅ **Scripts automatiques** : Démarrage/arrêt en 1 commande

---

## 🔜 **PROCHAINES ÉTAPES**

1. ✅ **Tester les pages** : http://localhost:8080/fear-greed
2. ⏳ **Ajouter au menu** de navigation
3. ⏳ **Personnaliser** le design
4. ⏳ **Ajouter** des graphiques historiques
5. ⏳ **Déployer** en production

---

## 📚 **FICHIERS CRÉÉS/MODIFIÉS**

**Nouveaux fichiers :**
- `start_all.sh` - Démarrage unifié
- `stop_all.sh` - Arrêt unifié
- `logs/` - Dossier de logs

**Fichiers modifiés :**
- `vite.config.ts` - Ajout du proxy
- `src/pages/FearGreedIndex.tsx` - URL relative
- `src/pages/FearGreedDashboard.tsx` - URL relative

---

## 🎯 **EN RÉSUMÉ**

**Avant :**
- Frontend : http://localhost:8080
- Backend : http://localhost:8001
- Problèmes CORS
- 2 commandes de démarrage

**Après :**
- **Tout** : http://localhost:8080
- Proxy Vite
- Pas de CORS
- **1 commande** : `./start_all.sh`

---

## ✨ **C'EST PRÊT !**

Lancez simplement :

```bash
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
./start_all.sh
```

Et ouvrez : **http://localhost:8080/fear-greed** ! 🚀

