# 🤖 LLM Sentiment Analysis - Guide Rapide

## ✅ Installation Terminée !

Le système Fear & Greed Index intègre maintenant un Large Language Model (LLM) pour l'analyse de sentiment des articles de presse. 🎉

---

## 🚀 Démarrage Rapide (3 étapes)

### 1️⃣ Obtenir une clé API OpenAI

Allez sur **https://platform.openai.com/api-keys** et :
1. Créez un compte (ou connectez-vous)
2. Cliquez sur **"Create new secret key"**
3. Copiez la clé (commence par `sk-proj-...`)
4. Ajoutez $5 de crédits minimum

---

### 2️⃣ Configurer la clé API

Ouvrez votre Terminal Mac et exécutez :

```bash
# Configurez votre clé API (remplacez par votre vraie clé)
export OPENAI_API_KEY='sk-proj-VOTRE_CLE_ICI'

# Vérifiez que c'est configuré
echo $OPENAI_API_KEY
```

**Note** : Cette configuration est temporaire. Pour la rendre permanente, ajoutez-la dans votre `~/.zshrc` :

```bash
echo "export OPENAI_API_KEY='sk-proj-VOTRE_CLE_ICI'" >> ~/.zshrc
source ~/.zshrc
```

---

### 3️⃣ Tester le LLM

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

# Test LLM uniquement
python test_llm_sentiment.py

# Test du pipeline complet
python test_complet_systeme.py
```

**Résultat attendu** :
```
🤖 Test du LLM Sentiment Analyzer
================================

📰 Article 1/3
   Titre : La BMCI affiche une croissance record au T3 2025
   Score : +0.750 (Très Positif)
   Explication : L'article met en avant une forte croissance...

📊 Score moyen : +0.23 → 61.50/100
✅ Test réussi !
```

---

## 🎯 Démarrer le Système Complet

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Assurez-vous que la clé API est configurée
export OPENAI_API_KEY='sk-proj-...'

# Démarrez le système avec LLM
./start_with_llm.sh
```

Le système :
- ✅ Démarre le backend (avec LLM activé)
- ✅ Démarre le frontend
- ✅ Configure le scheduler (update toutes les 10 minutes)
- ✅ Ouvre le dashboard automatiquement

---

## 📊 Comment ça Marche ?

### Ancienne Méthode (Dictionnaire)
```python
# Analyse basée sur des mots-clés
"hausse" → Positif ✅
"baisse" → Négatif ✅
"hausse des défaillances" → Positif ❌  # ERREUR !
```

### Nouvelle Méthode (LLM GPT)
```python
# Analyse contextuelle avec IA
"hausse" → +0.3 (Positif) ✅
"baisse" → -0.3 (Négatif) ✅
"hausse des défaillances" → -0.7 (Négatif) ✅  # CORRECT !

# Le LLM comprend :
- Le contexte complet de l'article
- Les nuances du français
- Le sarcasme et l'ironie
- Le ton général (alarmiste, optimiste, neutre)
```

---

## 💰 Coûts

| Articles/jour | Coût/mois | Modèle |
|---------------|-----------|--------|
| 50 | **$0.09** 💚 | gpt-4o-mini (recommandé) |
| 100 | **$0.18** 💚 | gpt-4o-mini (recommandé) |
| 200 | **$0.36** 💚 | gpt-4o-mini (recommandé) |

**Moins cher qu'un café par mois !** ☕

---

## 🔍 Vérifier que le LLM Fonctionne

### Option 1 : Vérifier les logs
```bash
tail -f "/Volumes/YAHYA SSD/Documents/fear and/backend.log"
```

Cherchez ces indicateurs :
- ✅ `🤖 Using LLM (GPT) for sentiment analysis...` → LLM actif
- ⚠️ `⚠️ LLM not available` → Clé API non configurée
- ❌ `❌ Error analyzing sentiment` → Erreur API

---

### Option 2 : Vérifier la base de données
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

python << 'EOF'
from app.models.database import SessionLocal
from app.models.schemas import MediaArticle

db = SessionLocal()
articles = db.query(MediaArticle).order_by(MediaArticle.scraped_at.desc()).limit(3).all()

print("📰 Derniers articles avec sentiment LLM :\n")
for article in articles:
    print(f"Titre : {article.title[:50]}...")
    print(f"Score : {article.sentiment_score:+.3f} ({article.sentiment_label})")
    print()

db.close()
EOF
```

---

## 🚨 Problèmes Fréquents

### "Incorrect API key provided"
**Solution** : Vérifiez votre clé API
```bash
echo $OPENAI_API_KEY  # Doit commencer par sk-proj- ou sk-
```

### "Rate limit exceeded"
**Solution** : Ajoutez des crédits sur https://platform.openai.com/account/billing

### Le LLM n'est pas utilisé
**Solution** : Configurez la clé API et redémarrez
```bash
export OPENAI_API_KEY='sk-proj-...'
./start_with_llm.sh
```

---

## 📚 Documentation Complète

- **Guide détaillé** : `TESTER_LLM_SENTIMENT.md`
- **Intégration complète** : `INTEGRATION_LLM_COMPLETE.md`
- **Calcul du score** : `CALCUL_DU_SCORE.md`
- **Démarrage rapide** : `QUICK_START.md`

---

## 🎉 Félicitations !

Votre Fear & Greed Index utilise maintenant l'intelligence artificielle ! 🤖

**Prochaine étape** : Obtenez votre clé API sur https://platform.openai.com/api-keys

**Questions ?** Relisez les guides dans le dossier `/Volumes/YAHYA SSD/Documents/fear and/backend/` 📖

