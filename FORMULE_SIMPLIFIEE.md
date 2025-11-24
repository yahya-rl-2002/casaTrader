# 📐 Formule Simplifiée - Fear & Greed Index

## 🎯 Vue d'ensemble

Cette formule simplifiée calcule l'indice Fear & Greed pour la Bourse de Casablanca en utilisant une approche directe et intuitive.

### **Formule**

```
Score = (Volume moyen + Sentiment news + Performance marché) / Nombre d'actions × 10
```

## 📊 Composantes

### 1️⃣ **Volume Moyen (0-100)**
- **Source** : Volume journalier du MASI sur les 20 derniers jours
- **Calcul** : Normalisation min-max du volume moyen par rapport à la plage historique
- **Interprétation** :
  - `> 70` : Volume élevé → Forte activité sur le marché
  - `40-70` : Volume modéré → Activité normale
  - `< 40` : Volume faible → Peu d'activité

### 2️⃣ **Sentiment News (0-100)**
- **Source** : Articles médias des 4 sources marocaines
  - Medias24 (prioritaire)
  - BourseNews.ma (Espace Investisseurs)
  - Challenge.ma (12 sections financières)
  - La Vie Éco
- **Calcul** : Analyse NLP (spaCy fr_core_news_md) pour extraire le degré d'optimisme
- **Normalisation** : Polarité [-100, +100] → [0, 100]
- **Interprétation** :
  - `> 60` : Sentiment positif → Les médias sont optimistes
  - `40-60` : Sentiment neutre → Médias partagés
  - `< 40` : Sentiment négatif → Les médias sont pessimistes

### 3️⃣ **Performance Marché (0-100)**
- **Source** : Évolution du MASI sur les 5 derniers jours
- **Calcul** : 
  - Ratio de jours positifs vs négatifs
  - Ajustement selon l'amplitude des rendements (±20 points)
- **Interprétation** :
  - `> 60` : Performance positive → Plus d'actions en hausse
  - `40-60` : Performance mixte → Marché équilibré
  - `< 40` : Performance négative → Plus d'actions en baisse

### ➗ **Nombre d'Actions**
- **Valeur** : 76 (nombre approximatif d'actions cotées sur le MASI)
- **Rôle** : Diviseur pour normaliser le score final

## 📈 Échelle d'Interprétation

| Score | Niveau | Emoji | Interprétation | Conseil |
|-------|--------|-------|----------------|---------|
| 75-100 | **EXTREME GREED** | 🤑 | Le marché est très optimiste | Prudence recommandée, marché surévalué |
| 60-75 | **GREED** | 😊 | Le marché est optimiste | Surveiller les excès |
| 40-60 | **NEUTRAL** | 😐 | Le marché est équilibré | Bon moment pour analyser |
| 25-40 | **FEAR** | 😟 | Le marché est pessimiste | Opportunités possibles |
| 0-25 | **EXTREME FEAR** | 😱 | Le marché est très pessimiste | Occasion d'achat potentielle |

## 🧪 Exemple de Calcul

**Date** : 25 octobre 2025

### Données brutes :
- Volume moyen (20j) : 52.23 / 100
- Sentiment news (NLP) : 50.03 / 100
- Performance marché : 95.00 / 100
- Nombre d'actions MASI : 76

### Calcul :
```
Numérateur = 52.23 + 50.03 + 95.00 = 197.26
Score brut = 197.26 / 76 = 2.60
Score normalisé (×10) = 25.96 / 100
```

### Résultat :
**Score = 25.96** → **FEAR** 😟

**Interprétation** : Le marché est pessimiste, opportunités possibles

## 🌐 API Endpoints

### 1. Score Simplifié
```bash
GET /api/v1/simplified-v2/score
```

**Réponse :**
```json
{
  "score": 25.96,
  "volume_moyen": 52.23,
  "sentiment_news": 50.03,
  "performance_marche": 95.00,
  "nombre_actions": 76,
  "date": "2025-10-25",
  "formule": "(52.23 + 50.03 + 95.00) / 76",
  "interpretation": "FEAR - Le marché est pessimiste"
}
```

### 2. Détails Complets
```bash
GET /api/v1/simplified-v2/details
```

**Réponse :**
```json
{
  "score_final": 25.96,
  "date": "2025-10-25",
  "composantes": {
    "volume_moyen": {
      "valeur": 52.23,
      "description": "Volume journalier moyen MASI sur 20 jours",
      "echelle": "0-100"
    },
    "sentiment_news": {
      "valeur": 50.03,
      "description": "Degré d'optimisme des news (analyse NLP)",
      "echelle": "0-100"
    },
    "performance_marche": {
      "valeur": 95.00,
      "description": "Performance marché (jours positifs vs négatifs)",
      "echelle": "0-100"
    }
  },
  "denominateur": {
    "nombre_actions": 76,
    "description": "Nombre total d'actions cotées sur MASI"
  },
  "calcul": {
    "formule": "(52.23 + 50.03 + 95.00) / 76",
    "numerateur": 197.26,
    "score_final": 25.96
  },
  "interpretation": "FEAR - Le marché est pessimiste"
}
```

## 🚀 Utilisation

### Test de la formule
```bash
cd backend
source .venv/bin/activate
python test_formule_simplifiee.py
```

### Via API (avec backend lancé)
```bash
# Démarrer le backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Dans un autre terminal
curl http://localhost:8000/api/v1/simplified-v2/score
curl http://localhost:8000/api/v1/simplified-v2/details
```

## 💡 Avantages de cette Formule

1. **Simplicité** : Formule directe et compréhensible
2. **Transparence** : Chaque composante est clairement identifiable
3. **Adaptabilité** : Facile à ajuster les poids ou ajouter des composantes
4. **Temps réel** : Calcul rapide basé sur des données fraîches
5. **Interprétabilité** : Résultats faciles à expliquer aux utilisateurs

## 🔄 Comparaison avec l'Approche Complexe

| Aspect | Formule Simplifiée | Approche Complexe |
|--------|-------------------|-------------------|
| **Composantes** | 3 | 6 |
| **Calcul** | Division simple | Moyenne pondérée |
| **Normalisation** | Statique (0-100) | Dynamique (fenêtres glissantes) |
| **Vitesse** | Rapide | Plus lent |
| **Interprétation** | Intuitive | Plus technique |

## 📚 Documentation Complémentaire

- [Guide de démarrage rapide](./QUICK_START.md)
- [Architecture du système](./docs/architecture.md)
- [Tests complets](./backend/test_complet_systeme.py)







