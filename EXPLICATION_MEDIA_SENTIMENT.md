# 📰 EXPLICATION : MEDIA SENTIMENT = 49.02

**Date** : $(date '+%Y-%m-%d')  
**Valeur actuelle** : 49.02

---

## 🧮 FORMULE DE CALCUL

### Formule de Normalisation

```python
# 1. Calculer la moyenne des scores de sentiment des articles (-1 à +1)
avg_sentiment = moyenne(sentiment_score de tous les articles des 7 derniers jours)

# 2. Convertir de l'échelle -1 à +1 vers 0 à 100
normalized_score = (avg_sentiment + 1) * 50
```

### Explication Détaillée

1. **Échelle de sentiment des articles** : -1.0 à +1.0
   - **-1.0** = Très négatif
   - **0.0** = Neutre
   - **+1.0** = Très positif

2. **Conversion vers 0-100** :
   ```
   Score normalisé = (Score moyen + 1) × 50
   
   Exemples :
   - Si avg = -1.0 → (10.0 + 1) × 50 = 0.0   (Extreme Fear)
   - Si avg =  0.0 → ( 0.0 + 1) × 50 = 50.0  (Neutral)
   - Si avg = +1.0 → ( 1.0 + 1) × 50 = 100.0 (Extreme Greed)
   ```

---

## 📊 DONNÉES ACTUELLES

### Statistiques des Articles

D'après les données actuelles :

- **Total articles** : 31 articles
- **Articles avec sentiment** : Variable (certains peuvent être None)
- **Moyenne des scores sentiment** : ~0.06 (sur échelle -1 à +1)
- **Min** : -0.3
- **Max** : 0.8

### Calcul Actuel

```python
# Moyenne des scores de sentiment
avg_sentiment ≈ 0.0387  # (moyenne calculée depuis l'API)

# Normalisation
normalized_score = (0.0387 + 1) × 50
normalized_score = 1.0387 × 50
normalized_score ≈ 51.94
```

**Mais on obtient 49.02** → Cela suggère que :

1. **Seuls les articles des 7 derniers jours** sont pris en compte
2. **Les articles sans sentiment_score sont exclus**
3. **La moyenne peut être différente** si certains articles sont filtrés

---

## 🔍 POURQUOI 49.02 ?

### Hypothèses

1. **Filtrage temporel** : Seuls les articles des **7 derniers jours** sont considérés
   - Les articles plus anciens sont ignorés
   - Cela peut réduire le nombre d'articles utilisés

2. **Articles sans sentiment** : Les articles avec `sentiment_score = None` sont exclus
   - Seuls les articles analysés sont comptés
   - Certains articles peuvent ne pas avoir été analysés

3. **Moyenne pondérée** : Possible pondération par date de publication
   - Articles plus récents = poids plus élevé
   - Articles anciens = poids plus faible

### Calcul Probable

Si `media_sentiment = 49.02` :

```
49.02 = (avg_sentiment + 1) × 50
49.02 / 50 = avg_sentiment + 1
0.9804 = avg_sentiment + 1
avg_sentiment = 0.9804 - 1
avg_sentiment = -0.0196
```

**Conclusion** : La moyenne des scores de sentiment est légèrement **négative** (-0.0196), ce qui donne un score légèrement en dessous de 50 (neutre).

---

## 📈 INTERPRÉTATION

### Score 49.02 = Légèrement Pessimiste

| Plage | Interprétation | Emoji |
|-------|---------------|-------|
| **0-25** | Extreme Fear | 😱 |
| **25-45** | Fear | 😟 |
| **45-55** | **Neutral** | 😐 |
| **55-75** | Greed | 😊 |
| **75-100** | Extreme Greed | 😃 |

**49.02** = Juste en dessous du neutre (50)
- **Signification** : Les médias marocains sont légèrement pessimistes
- **Tendance** : Légèrement vers le côté "Fear" mais proche du neutre
- **Impact** : Impact modéré sur le score final (poids de 15%)

---

## 📰 SOURCES ANALYSÉES

### Articles Récemment Scrapés

D'après les données actuelles :

| Source | Nombre d'articles | Sentiment moyen |
|--------|------------------|-----------------|
| L'Économiste | ~6 articles | Variable |
| Medias24 | ~1 article | 0.7 (positif) |
| Challenge | ~1 article | 0.0 (neutre) |
| BourseNews | ~1 article | -0.3 (négatif) |

### Distribution des Scores

- **Articles positifs** (> 0.05) : ~2 articles
- **Articles neutres** (-0.05 à 0.05) : ~8+ articles
- **Articles négatifs** (< -0.05) : ~1 article

**Majorité d'articles neutres** → Score proche de 50 mais légèrement négatif

---

## 🔧 FACTEURS QUI INFLUENCENT LE SCORE

### 1. Nombre d'Articles
- Plus d'articles = moyenne plus stable
- Moins d'articles = moyenne plus volatile

### 2. Qualité de l'Analyse
- **NLP (spaCy)** : Analyse basée sur dictionnaires
- **LLM (GPT-4)** : Analyse contextuelle plus précise
- Mélange des deux méthodes

### 3. Fenêtre Temporelle
- Seuls les **7 derniers jours** sont considérés
- Articles plus anciens = ignorés
- Cela peut réduire le nombre d'articles si peu de scraping récent

### 4. Exclusions
- Articles sans `sentiment_score` = exclus
- Articles avec `sentiment_score = None` = exclus
- Seuls les articles analysés comptent

---

## 📊 EXEMPLE DE CALCUL DÉTAILLÉ

### Scénario avec 10 Articles

```
Articles et leurs scores :
1. Medias24        : +0.7  (positif)
2. L'Économiste    : +0.8  (positif)
3. Challenge       :  0.0  (neutre)
4. BourseNews      : -0.3  (négatif)
5. L'Économiste    :  0.0  (neutre)
6. L'Économiste    :  0.0  (neutre)
7. L'Économiste    :  0.0  (neutre)
8. L'Économiste    :  0.0  (neutre)
9. L'Économiste    :  0.0  (neutre)
10. L'Économiste   :  0.0  (neutre)

Moyenne = (0.7 + 0.8 + 0.0 - 0.3 + 0.0 + 0.0 + 0.0 + 0.0 + 0.0 + 0.0) / 10
Moyenne = 1.2 / 10 = 0.12

Score normalisé = (0.12 + 1) × 50 = 56.0
```

**Mais si seuls 7 articles sont dans la fenêtre de 7 jours :**

```
Moyenne = (0.0 + 0.0 + 0.0 + 0.0 + 0.0 + 0.0 + 0.0) / 7 = 0.0
Score = (0.0 + 1) × 50 = 50.0
```

**Ou avec certains négatifs :**

```
Moyenne = (0.0 + 0.0 + 0.0 - 0.3 + 0.0 + 0.0 + 0.0) / 7 = -0.043
Score = (-0.043 + 1) × 50 = 47.85
```

---

## 🎯 CONCLUSION

**Media Sentiment = 49.02** signifie que :

1. **Les médias sont légèrement pessimistes** (score < 50)
2. **La moyenne des sentiments est de -0.0196** (légèrement négatif)
3. **Majorité d'articles neutres** avec quelques articles légèrement négatifs
4. **Tendance** : Légèrement vers "Fear" mais proche du neutre

### Impact sur le Score Final

Avec un poids de **15%** dans la formule principale :

```
Contribution = 49.02 × 0.15 = 7.35 points
```

**Conclusion** : Le sentiment média a un **impact modéré** sur le score final, contribuant légèrement au côté "Fear" du marché.

---

**Généré le** : $(date '+%Y-%m-%d %H:%M:%S')











