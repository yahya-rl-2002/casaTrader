# 🔄 Bouton "Actualiser le Score" Ajouté !

## ✅ Ce qui a été fait

J'ai ajouté un **bouton "Actualiser le Score"** dans le header du dashboard qui permet de :

1. 📰 **Scraper de nouveaux articles** de presse
2. 🤖 **Analyser le sentiment** avec le LLM (ou dictionnaire)
3. 📊 **Recalculer le score** Fear & Greed Index
4. 🔄 **Rafraîchir automatiquement** le dashboard

---

## 🎨 Apparence du Bouton

Le bouton apparaît en haut à droite du dashboard avec :

```
┌─────────────────────────────────────────────────────┐
│ 📊 Fear & Greed Index         [🔄 Actualiser le Score] │
│ Bourse de Casablanca          [Status messages...]  │
│                               [• Système actif]      │
└─────────────────────────────────────────────────────┘
```

### États du Bouton

**1. État Normal (au repos)**
```
[🔄 Actualiser le Score]
```
- Couleur : Bleu dégradé
- Effet hover : Zoom + ombre

**2. État en cours d'actualisation**
```
[⏳ Actualisation...]
```
- Spinner animé
- Bouton grisé (désactivé)
- Messages de progression :
  - 📰 Scraping des articles de presse...
  - 🤖 Analyse de sentiment avec LLM...
  - 📊 Calcul du nouveau score...
  - ✅ Score mis à jour ! Rechargement...

**3. Barre de progression**
```
[████████████░░░░░░░░] 80%
```
- Progression visuelle de 0% à 100%

---

## 🚀 Comment Utiliser le Bouton

### Dans votre Navigateur

1. Allez sur **http://localhost:3000/dashboard**
2. Cliquez sur le bouton **"Actualiser le Score"** en haut à droite
3. Attendez la fin du processus (~30-60 secondes)
4. Le dashboard se rafraîchit automatiquement avec le nouveau score !

---

## 📊 Ce qui se passe quand vous cliquez

### Étape 1 : Scraping (20%)
```
📰 Scraping des articles de presse...
```
- Scrape Medias24, BourseNews, L'Économiste, Challenge, La Vie Éco
- Récupère les nouveaux articles financiers

### Étape 2 : Analyse LLM (50%)
```
🤖 Analyse de sentiment avec LLM...
```
- Analyse chaque article avec GPT-4o-mini (si disponible)
- Ou utilise l'analyse par dictionnaire (fallback)
- Calcule les scores de sentiment

### Étape 3 : Calcul du Score (80%)
```
📊 Calcul du nouveau score...
```
- Recalcule les 6 composantes :
  - Momentum
  - Price Strength
  - Volume
  - Volatility
  - Equity vs Bonds
  - Media Sentiment
- Agrège le score final

### Étape 4 : Rafraîchissement (100%)
```
✅ Score mis à jour ! Rechargement...
```
- Enregistre en base de données
- Recharge automatiquement le dashboard
- Affiche le nouveau score !

---

## 🎯 Exemple d'Utilisation

**Avant de cliquer :**
```
Fear & Greed Index
      55.60
      GREED
```

**Pendant l'actualisation :**
```
[⏳ Actualisation...]
🤖 Analyse de sentiment avec LLM...
[████████████░░░░░░░░] 60%
```

**Après actualisation :**
```
Fear & Greed Index
      58.30
      GREED
```

Le score a changé ! Les nouvelles données sont prises en compte.

---

## 🔧 Configuration du Backend

Le bouton appelle l'endpoint API :

```
POST http://localhost:8000/api/v1/scheduler/trigger
```

Cet endpoint déclenche le pipeline complet :
- ✅ Scraping des sources
- ✅ Analyse de sentiment
- ✅ Calcul du score
- ✅ Sauvegarde en base

---

## ⚠️ Notes Importantes

### 1. Durée de l'Actualisation

L'actualisation prend **30-60 secondes** car elle doit :
- Scraper 4-5 sources d'articles
- Analyser chaque article (LLM ou dictionnaire)
- Récupérer les données de marché (MASI)
- Calculer toutes les composantes

**Soyez patient !** Le processus ne peut pas être plus rapide.

---

### 2. Limite du LLM

Si vous voyez un message d'erreur comme :
```
⚠️ Rate limit exceeded
```

Cela signifie que vous avez atteint la limite gratuite d'OpenAI (200 requêtes/jour).

**Solution** :
- Le système bascule automatiquement sur le dictionnaire ✅
- Ou ajoutez une méthode de paiement sur OpenAI pour augmenter la limite

---

### 3. Fréquence d'Actualisation

**Recommandé** : Ne pas cliquer trop souvent (max 1 fois toutes les 10-15 minutes)

**Pourquoi ?**
- Les articles de presse ne changent pas toutes les minutes
- Le LLM a des limites de requêtes
- Cela consomme des ressources inutilement

**Note** : Le système s'actualise déjà automatiquement toutes les 10 minutes via le scheduler !

---

## 🎨 Personnalisation

Si vous voulez modifier le bouton, éditez :

**Fichier** : `/frontend/app/dashboard/components/RefreshButton.tsx`

**Vous pouvez changer** :
- Les couleurs (ligne 37-43)
- Les messages (ligne 21, 28, 34, 40)
- Le temps d'attente (ligne 35, 43)
- L'apparence du spinner (ligne 52-56)

---

## ✅ Avantages du Bouton

| Avantage | Description |
|----------|-------------|
| **🚀 Rapide** | Actualise en 30-60 secondes |
| **📊 Complet** | Recalcule TOUT (scraping + analyse + score) |
| **🎯 Précis** | Utilise les données les plus récentes |
| **👁️ Visuel** | Messages et barre de progression |
| **🔄 Automatique** | Rafraîchit le dashboard à la fin |
| **🛡️ Robuste** | Gère les erreurs gracieusement |

---

## 🆘 Dépannage

### Le bouton ne fait rien

**Vérifiez** :
```bash
# Backend actif ?
curl http://localhost:8000/api/v1/health

# Frontend actif ?
curl http://localhost:3000
```

---

### Message d'erreur "Erreur API: 404"

**Solution** :
```bash
# Redémarrez le backend
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Le bouton reste bloqué sur "Actualisation..."

**Solution** :
- Rafraîchissez la page (`F5`)
- Vérifiez les logs du backend pour voir s'il y a des erreurs

---

## 📊 Résumé

| Élément | Status |
|---------|--------|
| **Bouton créé** | ✅ RefreshButton.tsx |
| **Intégré au dashboard** | ✅ page.tsx |
| **Design moderne** | ✅ Dégradé bleu + animations |
| **Messages de statut** | ✅ Progression visible |
| **Barre de progression** | ✅ 0% → 100% |
| **Rechargement auto** | ✅ À la fin du processus |
| **Gestion d'erreurs** | ✅ Messages clairs |

---

## 🎉 C'est Prêt !

Le bouton est maintenant **actif dans votre dashboard** !

**Pour le voir** :

1. Redémarrez le frontend (si nécessaire) :
   ```bash
   cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
   npm run dev
   ```

2. Ouvrez http://localhost:3000/dashboard

3. Cherchez le bouton **"🔄 Actualiser le Score"** en haut à droite

4. Cliquez et regardez la magie opérer ! ✨

---

**Profitez de votre nouveau bouton d'actualisation ! 🚀**

