# 🤖 Guide d'Installation et Test du LLM Sentiment Analysis

## ✅ Vérification de l'Installation

Le système LLM a été intégré avec succès ! Voici comment l'utiliser :

---

## 📋 Étapes d'Installation

### 1️⃣ Installer le package OpenAI

Le package `openai` est **déjà installé** dans votre environnement Poetry.

Pour vérifier :
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
poetry show openai
```

Si ce n'est pas installé, ajoutez-le :
```bash
poetry add openai
```

---

### 2️⃣ Obtenir votre clé API OpenAI

#### Option A : Si vous avez déjà un compte OpenAI
1. Allez sur https://platform.openai.com/api-keys
2. Connectez-vous
3. Cliquez sur **"Create new secret key"**
4. Copiez la clé (commence par `sk-proj-...`)

#### Option B : Si vous n'avez pas de compte
1. Créez un compte sur https://platform.openai.com/signup
2. Ajoutez des crédits (minimum $5)
3. Générez une clé API

⚠️ **Important** : Gardez votre clé secrète ! Ne la partagez jamais.

---

### 3️⃣ Configurer la Clé API

#### Option A : Variable d'environnement temporaire (pour tester)
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

# Remplacez YOUR_API_KEY par votre vraie clé
export OPENAI_API_KEY='sk-proj-...'

# Vérification
echo $OPENAI_API_KEY
```

#### Option B : Fichier .env permanent (recommandé)
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"

# Créez un fichier .env
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-...
EOF

# Assurez-vous que .env est dans .gitignore
echo ".env" >> .gitignore
```

Puis modifiez `app/services/llm_sentiment_service.py` pour charger le `.env` :
```python
from dotenv import load_dotenv
load_dotenv()  # Ajouter au début du fichier
```

Installez python-dotenv si nécessaire :
```bash
poetry add python-dotenv
```

---

## 🧪 Tester le LLM

### Test 1 : Script de Test Unitaire
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

# Configurez votre clé (si pas déjà fait)
export OPENAI_API_KEY='sk-proj-...'

# Lancez le test
python test_llm_sentiment.py
```

**Résultat attendu** :
```
🤖 Test du LLM Sentiment Analyzer
================================

📝 Analyse de l'article 1/3...
Titre: La BMCI affiche une croissance record au T3 2025
Score: +0.75 (Très Positif)
Explication: L'article met en avant une forte croissance...

📝 Analyse de l'article 2/3...
Titre: Craintes de récession sur le marché marocain
Score: -0.68 (Négatif)
Explication: Le ton de l'article est alarmiste...

📊 Moyenne des sentiments: +0.23 → 61.50/100
✅ Test réussi !
```

---

### Test 2 : Pipeline Complet avec LLM
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='sk-proj-...'

python test_complet_systeme.py
```

**Logs attendus** :
```
🤖 Using LLM (GPT) for sentiment analysis...
✅ LLM sentiment analysis completed for 12 articles
📊 Average sentiment (LLM): +0.35 → 67.50/100
```

---

## 🔍 Comment Vérifier que le LLM Fonctionne

### 1. Vérifier les logs
Cherchez ces emojis dans les logs :
- `🤖` = LLM est activé
- `⚠️` = LLM désactivé, utilise le dictionnaire
- `❌` = Erreur LLM
- `🔄` = Fallback vers dictionnaire

### 2. Comparer les scores
**Sans LLM (dictionnaire)** :
- Basé sur des mots-clés français simples
- Score moyen souvent neutre (~50)
- Exemple : "hausse", "croissance" → positif

**Avec LLM (GPT)** :
- Analyse contextuelle avancée
- Comprend les nuances et le sarcasme
- Scores plus précis et variés
- Exemple : Peut détecter qu'un article sur "hausse des défaillances" est négatif

### 3. Vérifier dans la base de données
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate

python << 'EOF'
from app.models.database import SessionLocal
from app.models.schemas import MediaArticle

db = SessionLocal()
articles = db.query(MediaArticle).order_by(MediaArticle.scraped_at.desc()).limit(5).all()

for article in articles:
    print(f"📰 {article.title[:50]}...")
    print(f"   Score: {article.sentiment_score:+.3f} | Label: {article.sentiment_label}")
    print()

db.close()
EOF
```

---

## ⚙️ Configuration Avancée

### Changer le modèle GPT
Dans `app/services/llm_sentiment_service.py` :
```python
def __init__(self, model: str = "gpt-4o-mini"):  # Par défaut
    # Options :
    # - gpt-4o-mini : Rapide et économique (recommandé)
    # - gpt-4o : Plus précis mais plus cher
    # - gpt-3.5-turbo : Économique mais moins bon en français
```

### Désactiver temporairement le LLM
Dans `app/services/pipeline_service.py` :
```python
def __init__(self, use_llm_sentiment: bool = False):  # Mettre False
```

Ou via variable d'environnement :
```bash
unset OPENAI_API_KEY  # Désactive automatiquement le LLM
```

---

## 💰 Coûts Estimés

**Modèle gpt-4o-mini** (recommandé) :
- **Prix** : $0.150 / 1M input tokens, $0.600 / 1M output tokens
- **Exemple** : 100 articles/jour × 200 tokens/article
  - Input : ~20,000 tokens/jour = $0.003/jour
  - Output : ~5,000 tokens/jour = $0.003/jour
  - **Total : ~$0.18/mois** 📉

**Modèle gpt-4o** :
- Plus cher (~10x), mais analyse plus fine
- **Total : ~$2/mois**

---

## 🚨 Dépannage

### Erreur : "Incorrect API key provided"
```bash
# Vérifiez que votre clé est correcte
echo $OPENAI_API_KEY

# La clé doit commencer par sk-proj- ou sk-...
```

### Erreur : "Rate limit exceeded"
- Vous avez dépassé votre quota gratuit
- Ajoutez des crédits sur https://platform.openai.com/account/billing

### Le LLM n'est pas utilisé
```bash
# Vérifiez que la clé est définie
echo $OPENAI_API_KEY

# Vérifiez les logs pour voir "🤖 Using LLM"
# Si vous voyez "⚠️ LLM not available", la clé n'est pas configurée
```

### Erreur : "Module 'openai' not found"
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
poetry add openai
source .venv/bin/activate
```

---

## 🎯 Recommandations

### Pour le développement
1. **Utilisez le LLM** pour des analyses précises
2. **Gardez le dictionnaire** comme fallback
3. **Testez régulièrement** avec `test_llm_sentiment.py`

### Pour la production
1. **Configurez .env** avec votre clé API
2. **Activez le LLM** dans `pipeline_service.py`
3. **Surveillez les coûts** sur https://platform.openai.com/usage

### Pour économiser
1. **Utilisez gpt-4o-mini** (rapide + économique)
2. **Limitez les articles** analysés (ex: 50/jour)
3. **Cachez les résultats** pour ne pas réanalyser les mêmes articles

---

## 📊 Comparaison : Dictionnaire vs LLM

| Critère | Dictionnaire | LLM (GPT) |
|---------|--------------|-----------|
| **Coût** | ✅ Gratuit | 💰 ~$0.20/mois |
| **Vitesse** | ✅ Instantané | ⏱ 1-2s/article |
| **Précision** | ⭐⭐ Basique | ⭐⭐⭐⭐⭐ Excellente |
| **Contexte** | ❌ Ignore | ✅ Comprend |
| **Nuances** | ❌ Simples | ✅ Fines |
| **Français** | ⚠️ Limité | ✅ Natif |
| **Setup** | ✅ Aucun | ⚙️ Clé API |

---

## ✅ Checklist Finale

Avant de mettre en production :

- [ ] Package `openai` installé (`poetry show openai`)
- [ ] Clé API OpenAI configurée (`echo $OPENAI_API_KEY`)
- [ ] Test unitaire réussi (`python test_llm_sentiment.py`)
- [ ] Pipeline complet OK (`python test_complet_systeme.py`)
- [ ] Logs montrent `🤖 Using LLM`
- [ ] Articles dans la DB ont des scores LLM
- [ ] Fallback fonctionne si pas de clé
- [ ] Coûts surveillés sur OpenAI Platform

---

## 🎉 Prochaines Étapes

Une fois le LLM testé avec succès :

1. **Automatisation** : Le scheduler exécutera le pipeline avec LLM toutes les 10 minutes
2. **Dashboard** : Les scores LLM seront affichés dans le frontend
3. **Monitoring** : Surveillez les coûts OpenAI dans votre tableau de bord

Voulez-vous que je vous aide à configurer votre clé API maintenant ? 🚀

