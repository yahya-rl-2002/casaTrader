# 🔄 Comment Rafraîchir le Dashboard avec les Nouvelles Données

## 🎯 Problème

Le dashboard affiche **50** au lieu du score actuel **46.8** du backend.

---

## ✅ SOLUTION RAPIDE (3 étapes)

### 1️⃣ Forcer une mise à jour des données

Dans votre Terminal Mac :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Rendez le script exécutable
chmod +x refresh_dashboard.sh

# Exécutez-le
./refresh_dashboard.sh
```

Ce script va :
- ✅ Vérifier que le backend est actif
- ✅ Déclencher une nouvelle mise à jour du pipeline
- ✅ Attendre que les nouvelles données soient calculées
- ✅ Vous donner le nouveau score

---

### 2️⃣ Vider le cache du navigateur

Dans votre navigateur (sur http://localhost:3000/dashboard) :

**Option A : Rechargement forcé**
- Sur Mac : `Cmd + Shift + R`
- Sur Windows/Linux : `Ctrl + Shift + R`

**Option B : Vider le cache manuellement**
1. Appuyez sur `F12` pour ouvrir les outils de développement
2. Allez dans l'onglet **"Application"** (Chrome) ou **"Storage"** (Firefox)
3. Cliquez sur **"Clear storage"** ou supprimez **localStorage**
4. Rechargez la page (`F5`)

---

### 3️⃣ Vérifier que le frontend est bien connecté

Ouvrez la console du navigateur (`F12` > onglet "Console") et cherchez :

```
[DataLoader] Latest score: { score: 46.8, as_of: "2025-10-28" }
```

✅ **Si vous voyez ça** : Le frontend reçoit bien les données du backend !

❌ **Si vous voyez des erreurs** comme `Failed to fetch` :
- Vérifiez que le backend tourne sur http://localhost:8000
- Vérifiez que le frontend tourne sur http://localhost:3000

---

## 🔧 Si le Score ne Change Toujours Pas

### Vérifier le Backend

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

# Vérifier le dernier score enregistré
python << 'EOF'
from app.models.database import SessionLocal
from app.models.schemas import IndexScore
from sqlalchemy import desc

db = SessionLocal()
latest = db.query(IndexScore).order_by(desc(IndexScore.as_of)).first()

if latest:
    print(f"✅ Dernier score en base : {latest.score}")
    print(f"   Date : {latest.as_of}")
    print(f"   Momentum : {latest.momentum}")
    print(f"   Media Sentiment : {latest.media_sentiment}")
else:
    print("❌ Aucun score en base de données")

db.close()
EOF
```

---

### Forcer une Nouvelle Mise à Jour Manuelle

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

# Lancer le pipeline manuellement
python test_complet_systeme.py
```

Cela va :
1. Scraper les nouvelles données (MASI + articles de presse)
2. Analyser le sentiment avec le LLM 🤖
3. Calculer un nouveau score
4. L'enregistrer en base de données

---

### Vérifier l'API Backend

```bash
# Test 1 : Score actuel
curl http://localhost:8000/api/v1/index/latest

# Test 2 : Composantes
curl http://localhost:8000/api/v1/components/latest

# Test 3 : Articles médias
curl http://localhost:8000/api/v1/media/latest
```

Vous devriez voir des données JSON valides.

---

## 🚀 Redémarrer le Frontend

Si rien ne fonctionne, redémarrez le frontend :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"

# Arrêter le processus actuel (Ctrl+C dans le terminal où il tourne)

# Supprimer le cache de build
rm -rf .next

# Redémarrer
npm run dev
```

Puis ouvrez http://localhost:3000/dashboard et faites `Cmd+Shift+R`.

---

## 📊 Vérifier que le LLM est Utilisé

Dans les logs du backend, vous devriez voir :

```
🤖 Using LLM (GPT) for sentiment analysis...
✅ LLM sentiment analysis completed for 12 articles
📊 Average sentiment (LLM): +0.35 → 67.50/100
```

Si vous voyez `⚠️ LLM not available`, relancez avec :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"
source set_api_key.sh
./start_with_llm.sh
```

---

## 🎯 RÉSUMÉ - Commandes à Exécuter

```bash
# 1. Forcer la mise à jour
cd "/Volumes/YAHYA SSD/Documents/fear and"
chmod +x refresh_dashboard.sh
./refresh_dashboard.sh

# 2. Dans le navigateur : Cmd+Shift+R

# 3. Si ça ne marche pas, redémarrer le frontend
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
rm -rf .next
npm run dev
```

---

## ✅ Checklist

- [ ] Backend actif sur http://localhost:8000
- [ ] Frontend actif sur http://localhost:3000
- [ ] Script `refresh_dashboard.sh` exécuté
- [ ] Cache du navigateur vidé (`Cmd+Shift+R`)
- [ ] Console du navigateur ne montre pas d'erreurs
- [ ] Le score affiché correspond au score du backend

---

## 🎉 Résultat Attendu

Après avoir suivi ces étapes, le dashboard devrait afficher :

```
Fear & Greed Index
      46.8
     FEAR
```

Avec toutes les composantes mises à jour, incluant le **Media Sentiment calculé avec le LLM** ! 🤖

---

**Essayez maintenant ces commandes et dites-moi ce que vous voyez ! 🚀**

