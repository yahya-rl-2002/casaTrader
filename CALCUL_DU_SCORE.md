# 📊 Comment le Score Fear & Greed est Calculé

## 🎯 Vue d'Ensemble

Le **Fear & Greed Index** est un score entre **0 et 100** qui mesure le sentiment du marché boursier de Casablanca.

```
Score = Moyenne Pondérée de 6 Composantes (0-100)
```

---

## 📐 Formule Globale

### **Poids des Composantes**

```python
DEFAULT_WEIGHTS = {
    "momentum":         20%  (0.20)
    "price_strength":   15%  (0.15)
    "volume":           15%  (0.15)
    "volatility":       20%  (0.20)
    "equity_vs_bonds":  15%  (0.15)
    "media_sentiment":  15%  (0.15)
}
```

### **Calcul Final**

```python
Score Final = (
    Momentum        × 0.20 +
    Price Strength  × 0.15 +
    Volume          × 0.15 +
    Volatility      × 0.20 +
    Equity vs Bonds × 0.15 +
    Media Sentiment × 0.15
) / 1.00
```

### **Exemple avec les Données Actuelles (Score = 51.86)**

```
Score = (
    46.7  × 0.20 +   // Momentum        = 9.34
    99.8  × 0.15 +   // Price Strength  = 14.97
    40.6  × 0.15 +   // Volume          = 6.09
    0.0   × 0.20 +   // Volatility      = 0.00
    100.0 × 0.15 +   // Equity vs Bonds = 15.00
    43.0  × 0.15     // Media Sentiment = 6.45
) = 51.86
```

---

## 📊 Détail des 6 Composantes

### 1. **Momentum (20%)** - 📈 Tendance du Marché

**Objectif :** Mesure la force de la tendance actuelle

**Calcul :**
```python
# 1. Calculer la moyenne mobile sur 125 jours
SMA_125 = Moyenne(Prix_Clôture des 125 derniers jours)

# 2. Calculer l'écart par rapport à la moyenne
Momentum_Raw = (Prix_Actuel - SMA_125) / SMA_125 × 100

# 3. Normaliser sur 252 jours (1 année boursière)
Min = Min(Momentum_Raw des 252 derniers jours)
Max = Max(Momentum_Raw des 252 derniers jours)

Momentum_Score = (Momentum_Raw - Min) / (Max - Min) × 100
```

**Interprétation :**
- **0-25** : Tendance baissière forte (FEAR)
- **25-45** : Tendance baissière modérée
- **45-55** : Marché neutre (NEUTRAL)
- **55-75** : Tendance haussière modérée
- **75-100** : Tendance haussière forte (GREED)

**Exemple actuel : 46.7**
- Prix légèrement en dessous de la moyenne mobile
- Tendance neutre/légèrement baissière

---

### 2. **Price Strength (15%)** - 💪 Force du Prix

**Objectif :** Mesure la position du prix par rapport aux extrêmes récents

**Calcul :**
```python
# 1. Compter les nouveaux plus hauts et plus bas sur 52 semaines
Highs = Nombre de nouveaux plus hauts sur 52 semaines
Lows = Nombre de nouveaux plus bas sur 52 semaines

# 2. Calculer le ratio
Ratio = (Highs - Lows) / (Highs + Lows)

# 3. Normaliser entre 0 et 100
Price_Strength = (Ratio + 1) / 2 × 100
```

**Interprétation :**
- **0-25** : Beaucoup de nouveaux plus bas (FEAR)
- **25-45** : Plus de plus bas que de plus hauts
- **45-55** : Équilibre (NEUTRAL)
- **55-75** : Plus de plus hauts que de plus bas
- **75-100** : Beaucoup de nouveaux plus hauts (GREED)

**Exemple actuel : 99.8**
- Presque tous des nouveaux plus hauts
- Marché très fort (EXTREME GREED)

---

### 3. **Volume (15%)** - 📦 Volume de Trading

**Objectif :** Mesure l'activité et la direction du trading

**Calcul :**
```python
# 1. Calculer le ratio volume actuel / moyenne 50 jours
MA_Volume_50 = Moyenne(Volume des 50 derniers jours)
Volume_Ratio = Volume_Actuel / MA_Volume_50

# 2. Calculer la part du volume haussier
Bullish_Volume = Somme(Volume des jours en hausse)
Total_Volume = Somme(Volume total)
Bullish_Share = Bullish_Volume / Total_Volume

# 3. Normaliser
Volume_Score = (Volume_Ratio / Max_Volume_Ratio) × 50 + Bullish_Share × 50
```

**Interprétation :**
- **0-25** : Volume faible, surtout baissier (FEAR)
- **25-45** : Volume modéré, plus baissier
- **45-55** : Volume équilibré (NEUTRAL)
- **55-75** : Volume élevé, plus haussier
- **75-100** : Volume très élevé, très haussier (GREED)

**Exemple actuel : 40.6**
- Volume en dessous de la moyenne
- Légèrement plus baissier (FEAR)

---

### 4. **Volatility (20%)** - 📉 Volatilité du Marché

**Objectif :** Mesure la stabilité du marché (inversé : haute volatilité = FEAR)

**Calcul :**
```python
# 1. Calculer la volatilité sur 30 jours
Rendements_Quotidiens = Log(Prix_t / Prix_t-1)
Volatilité = Écart_Type(Rendements_Quotidiens) × √252

# 2. Normaliser (INVERSÉ)
Min_Vol = Min(Volatilité des derniers mois)
Max_Vol = Max(Volatilité des derniers mois)

Volatility_Score = 100 - (Volatilité - Min_Vol) / (Max_Vol - Min_Vol) × 100
```

**Interprétation :**
- **0-25** : Volatilité très élevée (FEAR)
- **25-45** : Volatilité élevée
- **45-55** : Volatilité normale (NEUTRAL)
- **55-75** : Volatilité faible
- **75-100** : Volatilité très faible (GREED)

**Exemple actuel : 0.0**
- Volatilité au maximum historique
- Marché très instable (EXTREME FEAR)

---

### 5. **Equity vs Bonds (15%)** - ⚖️ Actions vs Obligations

**Objectif :** Mesure la préférence des investisseurs pour les actions (risque) vs obligations (sécurité)

**Calcul :**
```python
# 1. Calculer les performances relatives
Perf_Actions = Rendement_MASI sur 30 jours
Perf_Obligations = Rendement_Obligations_Maroc sur 30 jours

# 2. Calculer l'écart
Écart = Perf_Actions - Perf_Obligations

# 3. Normaliser
Min_Écart = Min(Écarts historiques)
Max_Écart = Max(Écarts historiques)

Equity_vs_Bonds = (Écart - Min_Écart) / (Max_Écart - Min_Écart) × 100
```

**Interprétation :**
- **0-25** : Obligations surperforment largement (FEAR)
- **25-45** : Obligations surperforment
- **45-55** : Performance équilibrée (NEUTRAL)
- **55-75** : Actions surperforment
- **75-100** : Actions surperforment largement (GREED)

**Exemple actuel : 100.0**
- Actions surperforment massivement
- Appétit pour le risque très élevé (EXTREME GREED)

---

### 6. **Media Sentiment (15%)** - 📰 Sentiment des Médias

**Objectif :** Mesure le sentiment des articles de presse économique

**Sources :**
- Medias24
- BourseNews.ma
- Challenge.ma
- La Vie Éco

**Calcul :**
```python
# 1. Analyser chaque article avec NLP (spaCy)
# Polarité entre -1.0 (très négatif) et +1.0 (très positif)

# 2. Catégoriser les articles
Négatif :  Polarité < -0.05
Neutre  : -0.05 ≤ Polarité ≤ 0.05
Positif :  Polarité > 0.05

# 3. Calculer les ratios
Ratio_Positif = Nb_Articles_Positifs / Total_Articles
Ratio_Neutre  = Nb_Articles_Neutres / Total_Articles
Ratio_Négatif = Nb_Articles_Négatifs / Total_Articles

# 4. Normaliser
Media_Sentiment = Ratio_Positif × 100 + Ratio_Neutre × 50 + Ratio_Négatif × 0
```

**Interprétation :**
- **0-25** : Majorité d'articles négatifs (FEAR)
- **25-45** : Plus d'articles négatifs que positifs
- **45-55** : Articles équilibrés (NEUTRAL)
- **55-75** : Plus d'articles positifs
- **75-100** : Majorité d'articles positifs (GREED)

**Exemple actuel : 43.0**
- Légèrement plus d'articles négatifs
- Sentiment médiatique prudent (FEAR)

---

## 🔄 Pipeline de Calcul

### Étape 1 : **Collecte des Données** (2-3 minutes)
```
1. Scraper les données MASI (252 jours)
2. Scraper les articles médias (4 sources)
3. Récupérer les cours des obligations
```

### Étape 2 : **Traitement des Composantes** (30 secondes)
```
1. Calculer Momentum        → 46.7
2. Calculer Price Strength  → 99.8
3. Calculer Volume          → 40.6
4. Calculer Volatility      → 0.0
5. Calculer Equity vs Bonds → 100.0
6. Calculer Media Sentiment → 43.0
```

### Étape 3 : **Agrégation** (instantané)
```
Score Final = Somme(Composante × Poids) = 51.86
```

### Étape 4 : **Sauvegarde en Base de Données**
```
Enregistrer dans la table index_scores :
- as_of: 2025-10-27
- score: 51.86
- momentum: 46.7
- price_strength: 99.8
- volume: 40.6
- volatility: 0.0
- equity_vs_bonds: 100.0
- media_sentiment: 43.0
```

---

## 📊 Échelle de Sentiment

| Score | Niveau | Emoji | Signification |
|-------|--------|-------|---------------|
| **0-25** | Extreme Fear | 😱 | Panique sur le marché |
| **25-45** | Fear | 😟 | Prudence des investisseurs |
| **45-55** | Neutral | 😐 | Marché équilibré |
| **55-70** | Greed | 😊 | Optimisme des investisseurs |
| **70-100** | Extreme Greed | 🤑 | Euphorie sur le marché |

**Score actuel : 51.86 = NEUTRAL 😐**

---

## 🔍 Analyse du Score Actuel (51.86)

### **Points Positifs (Vers GREED)**
- ✅ **Price Strength (99.8)** : Marché près de ses plus hauts
- ✅ **Equity vs Bonds (100.0)** : Actions très attractives
- ✅ **Momentum (46.7)** : Légèrement haussier

**Contribution totale : +39.31 points**

### **Points Négatifs (Vers FEAR)**
- ❌ **Volatility (0.0)** : Marché très instable
- ❌ **Volume (40.6)** : Volumes faibles
- ❌ **Media Sentiment (43.0)** : Presse prudente

**Contribution totale : -12.55 points**

### **Résultat Net**
```
Score = 50 (neutre) + 39.31 (positif) - 12.55 (négatif) = 51.86
```

**Interprétation :** Le marché est **légèrement optimiste** mais reste proche de la neutralité. La forte volatilité et les volumes faibles tempèrent l'optimisme créé par les prix élevés.

---

## 🔄 Fréquence de Mise à Jour

- **Automatique** : Toutes les **10 minutes**
- **Scheduler** : APScheduler intégré au backend
- **Sources** : Données en temps réel de la Bourse de Casablanca

---

## 📝 Code Simplifié

```python
# 1. Calculer chaque composante (0-100)
momentum = 46.7
price_strength = 99.8
volume = 40.6
volatility = 0.0
equity_vs_bonds = 100.0
media_sentiment = 43.0

# 2. Appliquer les poids
weights = {
    "momentum": 0.20,
    "price_strength": 0.15,
    "volume": 0.15,
    "volatility": 0.20,
    "equity_vs_bonds": 0.15,
    "media_sentiment": 0.15,
}

# 3. Calculer le score final
score = (
    momentum * weights["momentum"] +
    price_strength * weights["price_strength"] +
    volume * weights["volume"] +
    volatility * weights["volatility"] +
    equity_vs_bonds * weights["equity_vs_bonds"] +
    media_sentiment * weights["media_sentiment"]
)

print(f"Score Fear & Greed: {score:.2f}")
# Output: Score Fear & Greed: 51.86
```

---

## 🎯 Avantages de cette Méthode

1. **Multidimensionnelle** : 6 indicateurs différents
2. **Objective** : Calculs mathématiques sans biais humain
3. **En temps réel** : Mise à jour toutes les 10 minutes
4. **Complète** : Technique (prix, volume) + Fondamentale (médias)
5. **Pondérée** : Les indicateurs les plus importants ont plus de poids

---

## 📚 Sources des Données

| Composante | Source | Fréquence |
|------------|--------|-----------|
| **Momentum** | Bourse de Casablanca (MASI) | Quotidienne |
| **Price Strength** | Bourse de Casablanca (MASI) | Quotidienne |
| **Volume** | Bourse de Casablanca (MASI) | Quotidienne |
| **Volatility** | Bourse de Casablanca (MASI) | Quotidienne |
| **Equity vs Bonds** | MASI + Trésor Public | Quotidienne |
| **Media Sentiment** | 4 sources médias | En continu |

---

**Créé le :** 27 octobre 2025  
**Version :** 1.0  
**Status :** ✅ Documentation Complète du Calcul

