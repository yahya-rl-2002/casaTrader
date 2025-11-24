# 🚀 DÉMARRAGE IMMÉDIAT DU SYSTÈME

## ⚡ Option A : Configuration Permanente (RECOMMANDÉE)

### Étape 1 : Configurer la Clé API (1 minute)

Ouvrez votre **Terminal Mac** (pas dans Cursor, mais votre vrai Terminal Mac) et exécutez ces commandes :

```bash
# Option 1a : Script automatique (le plus simple)
cd "/Volumes/YAHYA SSD/Documents/fear and"
chmod +x setup_api_key.sh
./setup_api_key.sh
```

**OU**

```bash
# Option 1b : Commande manuelle
echo "export OPENAI_API_KEY='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'" >> ~/.zshrc

# Rechargez votre profil
source ~/.zshrc

# Vérifiez
echo $OPENAI_API_KEY
```

Vous devriez voir : `sk-proj-t3lX-X4Hqxxm...`

✅ **C'est fait !** Votre clé API est maintenant permanente.

---

### Étape 2 : Démarrer le Système (2 minutes)

Dans le même Terminal Mac :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Rendez le script exécutable
chmod +x start_with_llm.sh

# Lancez le système
./start_with_llm.sh
```

Le script va :
1. ✅ Vérifier votre clé API
2. ✅ Démarrer le backend (avec LLM activé)
3. ✅ Démarrer le frontend
4. ✅ Configurer le scheduler (update tous les 10 min)
5. ✅ Ouvrir le dashboard automatiquement

**Dashboard** : http://localhost:3000/dashboard

---

## ⚡ Option B : Démarrage Rapide (Sans Configuration Permanente)

Si vous voulez tester rapidement sans modifier votre `.zshrc` :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Définir la clé pour cette session uniquement
export OPENAI_API_KEY='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'

# Lancer le système
chmod +x start_with_llm.sh
./start_with_llm.sh
```

⚠️ **Note** : Avec cette option, vous devrez redéfinir `OPENAI_API_KEY` à chaque fois que vous ouvrez un nouveau Terminal.

---

## 🔍 Vérifier que le LLM Fonctionne

### Dans les Logs du Backend

Vous verrez :
```
🤖 Using LLM (GPT) for sentiment analysis...
✅ LLM sentiment analysis completed for 12 articles
📊 Average sentiment (LLM): +0.35 → 67.50/100
```

Si vous voyez **🤖**, c'est bon ! Le LLM est actif ! 🎉

---

### Dans le Dashboard

Accédez à : **http://localhost:3000/dashboard**

Vous verrez :
- 📊 Jauge principale avec le score Fear & Greed Index
- 📈 Graphique historique
- 📰 Articles de presse avec scores de sentiment LLM
- 🔥 Composantes détaillées

---

## 🚨 Si vous avez un Problème

### Problème : "Permission denied" sur start_with_llm.sh

**Solution** :
```bash
chmod +x start_with_llm.sh
./start_with_llm.sh
```

---

### Problème : Le LLM n'est pas utilisé (logs montrent "⚠️ LLM not available")

**Solution** :
```bash
# Vérifiez que la clé est définie
echo $OPENAI_API_KEY

# Si elle est vide, redéfinissez-la
export OPENAI_API_KEY='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'

# Relancez le système
./start_with_llm.sh
```

---

### Problème : Port déjà utilisé

**Solution** :
```bash
# Arrêtez le système actuel
./stop_system.sh

# Relancez
./start_with_llm.sh
```

---

## 📊 Ce que Vous Allez Voir

### 1. Dans le Terminal (Backend)
```
========================================================================
🤖 FEAR & GREED INDEX - Démarrage avec LLM
========================================================================

✅ Clé API OpenAI configurée
   Clé : sk-proj-t3lX-X4Hqxxm...

========================================================================
📦 ÉTAPE 1 : Démarrage du Backend (FastAPI + LLM)
========================================================================

🚀 Démarrage du serveur backend sur http://localhost:8000
✅ Backend démarré (PID: 12345)
   URL : http://localhost:8000
   Docs : http://localhost:8000/docs

========================================================================
🎨 ÉTAPE 2 : Démarrage du Frontend (Next.js)
========================================================================

🚀 Démarrage du serveur frontend sur http://localhost:3000
✅ Frontend démarré (PID: 67890)
   URL : http://localhost:3000

========================================================================
🤖 ÉTAPE 3 : Configuration du LLM Sentiment Analysis
========================================================================

✅ LLM Sentiment Analysis activé
   Modèle : gpt-4o-mini
   Coût estimé : ~$0.20/mois

========================================================================
⏰ ÉTAPE 4 : Scheduler automatique
========================================================================

✅ Scheduler actif
   Fréquence : Toutes les 10 minutes
   - L'analyse de sentiment avec GPT 🤖

========================================================================
🎉 SYSTÈME DÉMARRÉ AVEC SUCCÈS !
========================================================================

📊 Dashboard : http://localhost:3000/dashboard
🔧 API Backend : http://localhost:8000/docs

Pour arrêter le système :
   ./stop_system.sh

🤖 LLM Sentiment Analysis : ACTIF
```

---

### 2. Dans le Dashboard (http://localhost:3000/dashboard)

Vous verrez :

📊 **Jauge Principale**
```
Fear & Greed Index
      54.52
    NEUTRAL
```

📈 **Graphique Historique**
- Ligne montrant l'évolution du score sur 30 jours

📰 **Articles de Presse** (avec sentiment LLM !)
```
😊 +0.75  La BMCI affiche une croissance record
😐 +0.12  Le secteur bancaire maintient sa stabilité
😟 -0.50  Craintes de récession sur le marché
```

🔥 **Composantes Détaillées**
```
Momentum          ████████░░ 46.7%
Price Strength    ██████████ 99.8%
Volume           ████████░░ 58.4%
Volatility       ░░░░░░░░░░  0.0%
Equity vs Bonds  ██████████ 100%
Media Sentiment  ████████░░ 67.5%  ← Calculé avec LLM ! 🤖
```

---

## ⏰ Automatisation

Une fois le système démarré, il se met à jour **automatiquement toutes les 10 minutes** :

1. 📰 Scrape les articles de presse (4 sources)
2. 🤖 Analyse le sentiment avec GPT
3. 📊 Recalcule le score Fear & Greed Index
4. 💾 Sauvegarde en base de données
5. 🔄 Rafraîchit le dashboard

**Vous n'avez rien à faire !** Le système tourne tout seul. 🎉

---

## 💰 Coûts

- **Articles analysés/jour** : ~50-100
- **Coût/mois** : **~$0.18** 💚
- **Surveillez vos coûts** : https://platform.openai.com/usage

---

## 🎯 Commandes Utiles

```bash
# Démarrer le système
./start_with_llm.sh

# Arrêter le système
./stop_system.sh

# Voir les logs en temps réel
tail -f backend.log
tail -f frontend.log

# Forcer une mise à jour manuelle
curl -X POST http://localhost:8000/api/v1/scheduler/trigger

# Tester le LLM manuellement
cd backend
source .venv/bin/activate
python test_llm_sentiment.py
```

---

## ✅ Checklist Finale

- [ ] **Terminal Mac ouvert** (pas Cursor)
- [ ] **Clé API configurée** (Option A ou B ci-dessus)
- [ ] **Vérification** : `echo $OPENAI_API_KEY` montre la clé
- [ ] **Script exécutable** : `chmod +x start_with_llm.sh`
- [ ] **Système lancé** : `./start_with_llm.sh`
- [ ] **Dashboard ouvert** : http://localhost:3000/dashboard
- [ ] **Logs montrent 🤖** (LLM actif)
- [ ] **Articles avec scores** dans le dashboard

---

## 🎉 C'est Tout !

Votre Fear & Greed Index équipé d'**intelligence artificielle** est maintenant **opérationnel** ! 🤖

**Prêt ? Allez-y !**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"
./setup_api_key.sh  # Configuration permanente
./start_with_llm.sh # Démarrage du système
```

**🚀 Let's go !**

