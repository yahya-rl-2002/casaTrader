# ❓ Pourquoi le Dashboard Affiche 50 au lieu de 33.73 ?

## 🔍 Diagnostic Rapide

Votre dashboard affiche **50** (Neutral) au lieu du vrai score **33.73** (Fear) car :

### ❌ **Le Backend n'est PAS Lancé**

Le frontend essaie de se connecter à `http://localhost:8000` mais ne reçoit aucune réponse, donc il utilise les valeurs par défaut du store (50).

---

## ✅ Solution en 3 Étapes

### 1️⃣ **Fermez le Terminal Cursor**
Appuyez sur `Ctrl+C` dans le terminal où vous avez essayé de lancer le frontend.

### 2️⃣ **Ouvrez le Terminal Mac**
- Appuyez sur `Cmd + Espace`
- Tapez "Terminal"
- Appuyez sur `Entrée`

### 3️⃣ **Lancez cette Commande**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and" && ./start_system.sh
```

---

## 🎯 Résultat Attendu

Après le lancement, vous devriez voir **dans le dashboard** :

| Avant | Après |
|-------|-------|
| Score : **50** | Score : **33.73** |
| Niveau : **NEUTRAL** 😐 | Niveau : **FEAR** 😟 |
| Momentum : **50** | Momentum : **104.0** |
| Price Strength : **50** | Price Strength : **0.1** |
| Volume : **50** | Volume : **42.9** |
| Articles : **Vides** | Articles : **Liste réelle** |

---

## 🔍 Pourquoi 50 ?

### Code du Store Zustand

Le frontend a des valeurs par défaut définies dans `src/store/useDashboardStore.ts` :

```typescript
export const useDashboardStore = create<DashboardState>()((set) => ({
  latestScore: 50,           // ← Valeur par défaut !
  latestComponents: {
    momentum: 50,            // ← Valeur par défaut !
    price_strength: 50,      // ← Valeur par défaut !
    volume: 50,
    volatility: 50,
    equity_vs_bonds: 50,
    media_sentiment: 50,
  },
  // ...
}));
```

### Flux Normal

1. Frontend démarre → Valeurs par défaut = **50**
2. `DataLoader` fetch les données du backend
3. Si backend répond → Mise à jour avec vraies valeurs (**33.73**)
4. Si backend ne répond pas → Garde les valeurs par défaut (**50**)

**Dans votre cas :** Le backend ne répond pas car il n'est pas lancé !

---

## 🚫 Erreur Courante : EPERM dans Cursor

Vous avez vu cette erreur dans le terminal Cursor :

```
Error: listen EPERM: operation not permitted 0.0.0.0:3000
```

**Signification :** Le sandbox de Cursor ne permet pas de lancer des serveurs web.

**Solution :** Utilisez le Terminal Mac directement, pas Cursor.

---

## ✅ Vérifications Après Lancement

### 1. Vérifier que le Backend Répond

Dans un terminal, testez :
```bash
curl http://localhost:8000/api/v1/index/latest
```

**Réponse attendue :**
```json
{
  "as_of": "2025-10-25",
  "score": 33.73
}
```

Si vous voyez `{"score": 50}` ou une erreur de connexion → Le backend n'est pas lancé.

### 2. Vérifier la Console du Navigateur

1. Ouvrez http://localhost:3000
2. Appuyez sur `F12` (ou `Cmd+Option+I` sur Mac)
3. Allez dans l'onglet "Console"

**Messages attendus :**
```
[DataLoader] Latest score: {score: 33.73, as_of: "2025-10-25"}
[DataLoader] Components: {momentum: 104, price_strength: 0.1, ...}
[DataLoader] Historical data: 45 records
[DataLoader] Media feed: 41 articles
```

**Messages d'erreur à éviter :**
```
❌ Failed to fetch
❌ net::ERR_CONNECTION_REFUSED
❌ Access-Control-Allow-Origin (CORS)
```

Si vous voyez ces erreurs → Le backend n'est pas accessible.

### 3. Vérifier que le Scheduler Tourne

```bash
curl http://localhost:8000/api/v1/scheduler/status | jq
```

**Réponse attendue :**
```json
{
  "running": true,
  "jobs_count": 1,
  "jobs": [
    {
      "id": "index_update_10min",
      "name": "run_index_update_job",
      "next_run_time": "2025-10-25 15:30:00",
      "trigger": "interval[0:10:00]"
    }
  ]
}
```

---

## 🔧 Dépannage Avancé

### Problème : Le Backend Démarre mais le Score est Toujours 50

**Cause 1 : Pas de données dans la DB**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
python - <<'PY'
from app.models.database import get_session
from app.models.schemas import IndexScore
db = get_session()
count = db.query(IndexScore).count()
print(f"Scores en DB: {count}")
db.close()
PY
```

Si `count = 0` → Générez des données :
```bash
python test_complet_systeme.py
```

**Cause 2 : CORS bloqué**

Vérifiez dans `backend/app/main.py` ligne 15-21 :
```python
application.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Cause 3 : Mauvaise URL dans le Frontend**

Vérifiez `frontend/.env.local` :
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 📊 Comparaison Visuelle

### Dashboard avec Valeurs par Défaut (50)

```
┌─────────────────────────────────────┐
│   Fear & Greed Index                │
│                                     │
│         50                          │
│       NEUTRAL                       │
│         😐                          │
│                                     │
│   Momentum:        50 / 100        │
│   Price Strength:  50 / 100        │
│   Volume:          50 / 100        │
│   ...                              │
└─────────────────────────────────────┘
```

### Dashboard avec Vraies Données (33.73)

```
┌─────────────────────────────────────┐
│   Fear & Greed Index                │
│                                     │
│        33.73                        │
│         FEAR                        │
│         😟                          │
│                                     │
│   Momentum:       104.0 / 100      │
│   Price Strength:   0.1 / 100      │
│   Volume:          42.9 / 100      │
│   ...                              │
└─────────────────────────────────────┘
```

---

## 🎯 Checklist de Résolution

- [ ] J'ai fermé le terminal Cursor
- [ ] J'ai ouvert le Terminal Mac (application Terminal de macOS)
- [ ] J'ai exécuté : `cd "/Volumes/YAHYA SSD/Documents/fear and" && ./start_system.sh`
- [ ] Le backend démarre (je vois "Uvicorn running on http://127.0.0.1:8000")
- [ ] Le frontend démarre (je vois "Ready in X.Xs")
- [ ] Le navigateur s'ouvre sur http://localhost:3000
- [ ] Je vois le score **33.73** dans le dashboard
- [ ] La console du navigateur (F12) affiche les logs `[DataLoader]`
- [ ] `curl http://localhost:8000/api/v1/index/latest` retourne `33.73`

---

## 💡 Astuce : Créer un Raccourci

Pour éviter de taper la commande complète à chaque fois :

```bash
# Ajouter à ~/.zshrc
echo 'alias fear="cd \"/Volumes/YAHYA SSD/Documents/fear and\" && ./start_system.sh"' >> ~/.zshrc
source ~/.zshrc
```

Maintenant vous pouvez juste taper :
```bash
fear
```

---

## 📞 Besoin d'Aide ?

Si après avoir suivi toutes ces étapes, le dashboard affiche toujours 50 :

1. **Vérifier les logs :**
   ```bash
   tail -f /tmp/fear-greed-backend.log
   tail -f /tmp/fear-greed-frontend.log
   ```

2. **Tester manuellement :**
   ```bash
   # Test backend
   curl http://localhost:8000/api/v1/index/latest
   
   # Test scheduler
   curl http://localhost:8000/api/v1/scheduler/status
   ```

3. **Regénérer les données :**
   ```bash
   cd backend
   source .venv/bin/activate
   python test_complet_systeme.py
   ```

---

## ✅ Résumé

**Pourquoi 50 ?**
- ❌ Backend pas lancé
- ❌ Lancé dans le terminal Cursor (EPERM)
- ❌ Pas de données dans la DB

**Solution :**
1. Ouvrir Terminal Mac
2. `cd "/Volumes/YAHYA SSD/Documents/fear and" && ./start_system.sh`
3. Ouvrir http://localhost:3000
4. Voir le score **33.73** 🎯

**Le vrai score est 33.73 (FEAR), pas 50 (NEUTRAL) !**

---

**📖 Plus d'infos :** [LANCER_LE_SYSTEME.md](./LANCER_LE_SYSTEME.md)







