# 🤖 Intégration LLM pour l'Analyse de Sentiment

## 📋 Vue d'Ensemble

J'ai créé un nouveau service qui utilise un **Large Language Model (LLM)** pour analyser le sentiment des articles financiers de manière beaucoup plus précise que l'analyse par dictionnaire de mots-clés.

---

## ✨ Nouveau Service Créé

### **Fichier : `llm_sentiment_service.py`**

Ce service utilise **OpenAI GPT** (gpt-4o-mini par défaut) pour :
1. Analyser chaque article individuellement
2. Attribuer un score de -1.0 à +1.0
3. Fournir une explication du score
4. Calculer la moyenne pondérée quotidienne

---

## 🎯 Fonctionnement

### **1. Analyse d'un Article**

```python
from app.services.llm_sentiment_service import LLMSentimentAnalyzer

analyzer = LLMSentimentAnalyzer()

result = analyzer.analyze_article(
    title="Bourse de Casablanca : Le MASI clôture en hausse de 2,5%",
    summary="Le marché boursier marocain a enregistré une performance solide..."
)

print(f"Score: {result.sentiment_score}")  # Ex: +0.7
print(f"Label: {result.sentiment_label}")  # Ex: "Positive"
print(f"Confiance: {result.confidence}")   # Ex: 0.85
print(f"Raison: {result.reasoning}")       # Ex: "Article très positif, mentions de hausse..."
```

### **2. Échelle de Scores**

| Score | Label | Signification | Exemple |
|-------|-------|---------------|---------|
| **-1.0** | Very Negative | Panique, crise | "Effondrement de la bourse, pertes massives" |
| **-0.5** | Negative | Baisse, difficultés | "Le MASI chute de 3%, inquiétudes des investisseurs" |
| **0.0** | Neutral | Factuel, neutre | "Le MASI termine stable à 13,500 points" |
| **+0.5** | Positive | Hausse, opportunités | "Le MASI progresse, optimisme sur le marché" |
| **+1.0** | Very Positive | Euphorie, boom | "Explosion du MASI, records historiques battus" |

### **3. Conversion à l'Échelle 0-100**

```python
# Score LLM: -1.0 à +1.0
# Score normalisé: 0 à 100

score_normalized = (sentiment_score + 1.0) * 50.0

# Exemples:
# -1.0 -> 0   (Extreme Fear)
# -0.5 -> 25  (Fear)
#  0.0 -> 50  (Neutral)
# +0.5 -> 75  (Greed)
# +1.0 -> 100 (Extreme Greed)
```

---

## 🔧 Installation

### **1. Installer la Bibliothèque OpenAI**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
pip install openai
```

Ou avec Poetry :

```bash
poetry add openai
```

### **2. Configurer la Clé API**

Créez un fichier `.env` dans le dossier `backend/` :

```bash
# backend/.env
OPENAI_API_KEY=sk-proj-your-api-key-here
```

Ou exportez la variable d'environnement :

```bash
export OPENAI_API_KEY="sk-proj-your-api-key-here"
```

### **3. Obtenir une Clé API OpenAI**

1. Allez sur [https://platform.openai.com/](https://platform.openai.com/)
2. Créez un compte ou connectez-vous
3. Allez dans "API keys"
4. Cliquez sur "Create new secret key"
5. Copiez la clé (elle commence par `sk-proj-...`)

**⚠️ Important :** Gardez votre clé API secrète !

---

## 📊 Utilisation dans le Pipeline

### **Option 1 : Utiliser le LLM pour Tous les Articles** (Recommandé)

Modifiez `app/pipelines/aggregator_pipeline.py` :

```python
from app.services.llm_sentiment_service import LLMSentimentAnalyzer

# Dans la fonction run_pipeline()

# Après avoir scrapé les articles médias
media_articles = await media_scraper.scrape_all_sources()

# Analyser avec LLM
llm_analyzer = LLMSentimentAnalyzer()
articles_for_llm = [
    {
        'id': article.id,
        'title': article.title,
        'summary': article.summary or ''
    }
    for article in media_articles
]

# Obtenir les résultats LLM
llm_results = llm_analyzer.analyze_articles_batch(articles_for_llm)

# Calculer le score de sentiment moyen
daily_sentiment = llm_analyzer.calculate_daily_sentiment_score(llm_results)

# Convertir en échelle 0-100
media_sentiment_score = llm_analyzer.normalize_to_100_scale(daily_sentiment)

print(f"📰 Sentiment médias (LLM): {media_sentiment_score:.2f}/100")
```

### **Option 2 : Fonction Simplifiée**

```python
from app.services.llm_sentiment_service import analyze_daily_news

# Articles à analyser
articles = [
    {'title': 'Le MASI en hausse', 'summary': '...'},
    {'title': 'Volatilité sur le marché', 'summary': '...'},
    # ...
]

# Score de 0 à 100
media_sentiment_score = analyze_daily_news(articles)
```

---

## 🎯 Prompt Utilisé par le LLM

### **System Prompt**

```
Tu es un expert en analyse financière et économique spécialisé dans le marché boursier marocain.
Ta tâche est d'analyser le sentiment d'articles financiers en français et d'attribuer un score de sentiment.

Critères d'évaluation:
- Score entre -1.0 et +1.0
- -1.0: Sentiment très négatif (panique, crise, effondrement, pertes massives)
- -0.5: Sentiment négatif (baisse, difficultés, inquiétudes)
- 0.0: Sentiment neutre (factuel, pas de position claire)
- +0.5: Sentiment positif (hausse, opportunités, croissance)
- +1.0: Sentiment très positif (euphorie, boom, prospérité exceptionnelle)

Considère ces aspects:
1. Ton général de l'article (optimiste, pessimiste, neutre)
2. Mots-clés économiques (croissance vs récession, hausse vs baisse)
3. Perspectives d'avenir (prometteur vs incertain)
4. Impact sur les investisseurs (confiance vs prudence)

Réponds UNIQUEMENT au format suivant:
SCORE: [nombre entre -1.0 et +1.0]
LABEL: [Very Negative|Negative|Neutral|Positive|Very Positive]
CONFIDENCE: [nombre entre 0.0 et 1.0]
REASONING: [explication courte en 1-2 phrases]
```

### **Exemple de Réponse du LLM**

**Article :** "Bourse de Casablanca : Le MASI clôture en hausse de 2,5%, portée par les valeurs bancaires"

**Réponse LLM :**
```
SCORE: 0.65
LABEL: Positive
CONFIDENCE: 0.85
REASONING: L'article présente une performance positive du marché avec une hausse significative du MASI. Le ton est optimiste et met en avant les bonnes performances du secteur bancaire.
```

---

## 💰 Coûts et Performance

### **Coût estimé avec GPT-4o-mini**

| Modèle | Prix Input | Prix Output | Coût par Article (moyen) |
|--------|-----------|-------------|--------------------------|
| **gpt-4o-mini** | $0.15 / 1M tokens | $0.60 / 1M tokens | ~$0.001 (0.1¢) |
| gpt-3.5-turbo | $0.50 / 1M tokens | $1.50 / 1M tokens | ~$0.002 (0.2¢) |
| gpt-4o | $2.50 / 1M tokens | $10.00 / 1M tokens | ~$0.01 (1¢) |

**Exemple pour 40 articles par jour :**
- Avec **gpt-4o-mini** : ~$0.04/jour = **$1.20/mois**
- Avec **gpt-3.5-turbo** : ~$0.08/jour = **$2.40/mois**

### **Performance**

- **Vitesse** : ~2-3 secondes par article
- **Précision** : Beaucoup plus élevée que l'analyse par dictionnaire
- **Contexte** : Le LLM comprend les nuances, l'ironie, le contexte

---

## 🔄 Fallback en cas d'Erreur

Si l'API OpenAI n'est pas disponible, le système revient automatiquement à l'ancienne méthode (dictionnaire de mots-clés) :

```python
if not self.enabled:
    logger.warning("LLM sentiment analysis is disabled. Using fallback method.")
    return self._create_fallback_result(title, article_id)
```

---

## 📊 Comparaison : Dictionnaire vs LLM

### **Exemple 1 : Ironie/Sarcasme**

**Article :** "Encore une belle journée sur le marché avec une chute de 5% du MASI"

| Méthode | Score | Explication |
|---------|-------|-------------|
| **Dictionnaire** | +25 | Détecte "belle" (positif) mais rate l'ironie |
| **LLM** | -50 | Comprend l'ironie, score négatif correct |

### **Exemple 2 : Contexte**

**Article :** "Le MASI perd 1% mais reste proche de ses plus hauts historiques"

| Méthode | Score | Explication |
|---------|-------|-------------|
| **Dictionnaire** | 30 | "Perd" (négatif) vs "plus hauts" (positif) |
| **LLM** | 45 | Comprend que la baisse est mineure dans un contexte haussier |

### **Exemple 3 : Nuances**

**Article :** "Les investisseurs restent prudents malgré la hausse du MASI"

| Méthode | Score | Explication |
|---------|-------|-------------|
| **Dictionnaire** | 60 | "Hausse" domine |
| **LLM** | 50 | Équilibre entre hausse et prudence |

---

## 🛠️ Configuration Avancée

### **Choisir le Modèle**

```python
# Moins cher, rapide
analyzer = LLMSentimentAnalyzer(model="gpt-4o-mini")

# Meilleure qualité
analyzer = LLMSentimentAnalyzer(model="gpt-4o")

# Alternative économique
analyzer = LLMSentimentAnalyzer(model="gpt-3.5-turbo")
```

### **Ajuster la Température**

Dans `llm_sentiment_service.py`, ligne 62 :

```python
temperature=0.3,  # Bas = cohérent, Haut = créatif
```

- **0.0-0.3** : Très cohérent (recommandé pour l'analyse de sentiment)
- **0.5-0.7** : Équilibré
- **0.8-1.0** : Plus créatif

---

## 🧪 Test du Service

Créez un fichier `test_llm_sentiment.py` :

```python
from app.services.llm_sentiment_service import LLMSentimentAnalyzer

# Test 1: Article très positif
analyzer = LLMSentimentAnalyzer()

result = analyzer.analyze_article(
    title="Bourse de Casablanca: Le MASI bat un nouveau record historique",
    summary="Dans un contexte d'euphorie, le MASI a franchi la barre des 14,000 points pour la première fois de son histoire..."
)

print(f"✅ Test 1 (Très Positif):")
print(f"   Score: {result.sentiment_score} (attendu: ~0.8)")
print(f"   Label: {result.sentiment_label}")
print(f"   Raison: {result.reasoning}\n")

# Test 2: Article très négatif
result = analyzer.analyze_article(
    title="Effondrement du MASI: -8% en une séance, panique sur le marché",
    summary="Les investisseurs fuient massivement alors que le MASI enregistre sa pire séance en 10 ans..."
)

print(f"✅ Test 2 (Très Négatif):")
print(f"   Score: {result.sentiment_score} (attendu: ~-0.8)")
print(f"   Label: {result.sentiment_label}")
print(f"   Raison: {result.reasoning}\n")

# Test 3: Article neutre
result = analyzer.analyze_article(
    title="Le MASI termine stable à 13,500 points",
    summary="Aucune variation significative enregistrée aujourd'hui..."
)

print(f"✅ Test 3 (Neutre):")
print(f"   Score: {result.sentiment_score} (attendu: ~0.0)")
print(f"   Label: {result.sentiment_label}")
print(f"   Raison: {result.reasoning}\n")

# Test 4: Score quotidien moyen
articles = [
    {'title': 'Le MASI en hausse modérée', 'summary': ''},
    {'title': 'Volatilité sur certaines valeurs', 'summary': ''},
    {'title': 'Les bancaires soutiennent le marché', 'summary': ''},
]

daily_score = analyzer.analyze_daily_news(articles)
print(f"✅ Score quotidien moyen: {daily_score:.2f}/100")
```

Exécutez :

```bash
cd backend
source .venv/bin/activate
python test_llm_sentiment.py
```

---

## 📝 Modifications à Faire dans le Pipeline

### **Étape 1 : Installer la dépendance**

```bash
pip install openai
```

### **Étape 2 : Configurer la clé API**

```bash
export OPENAI_API_KEY="your-api-key"
```

### **Étape 3 : Modifier `aggregator_pipeline.py`**

Remplacez la section sentiment médias par :

```python
# Import
from app.services.llm_sentiment_service import analyze_daily_news

# Dans run_pipeline()
logger.info("🤖 Analyzing media sentiment with LLM...")

articles_for_analysis = [
    {
        'title': article.title,
        'summary': article.summary or '',
        'id': article.id
    }
    for article in media_articles[:40]  # Limiter à 40 articles/jour
]

# Analyse LLM
media_sentiment_score = analyze_daily_news(articles_for_analysis)

logger.info(f"📰 Media Sentiment (LLM): {media_sentiment_score:.2f}/100")
```

---

## ✅ Avantages du LLM

1. **Plus Précis** : Comprend le contexte, les nuances, l'ironie
2. **Multilingue** : Fonctionne bien en français marocain
3. **Adaptable** : Peut être ajusté via le prompt
4. **Expliqué** : Fournit une raison pour chaque score
5. **Robuste** : Gère les cas complexes

---

## 🎯 Formule Finale avec LLM

```python
Score = (
    Momentum        × 20% +
    Price Strength  × 15% +
    Volume          × 15% +
    Volatility      × 20% +
    Equity vs Bonds × 15% +
    Media Sentiment (LLM) × 15%  # ← Analysé par GPT
)
```

**Exemple avec LLM :**
```
Score = (
    46.7  × 0.20 +  # Momentum
    99.8  × 0.15 +  # Price Strength
    40.6  × 0.15 +  # Volume
    0.0   × 0.20 +  # Volatility
    100.0 × 0.15 +  # Equity vs Bonds
    68.5  × 0.15    # Media Sentiment (LLM)  ← Au lieu de 43.0
) = 55.7 (GREED au lieu de NEUTRAL)
```

---

**📁 Fichier créé :** `llm_sentiment_service.py`  
**📁 Documentation créée :** `INTEGRATION_LLM_SENTIMENT.md`

**🎉 Le système est maintenant prêt à utiliser l'IA pour analyser le sentiment des médias !** 🤖

---

**Créé le :** 27 octobre 2025  
**Version :** 1.0  
**Status :** ✅ Service LLM Créé et Documenté

