# 📰 Intégration du Scraping Fear & Greed dans Actualités

**Date** : 29 octobre 2025

---

## 🎯 **OBJECTIF**

Utiliser le **même système de scraping** du projet Fear & Greed Index pour alimenter la page **Actualités** de votre SaaS.

---

## 🔧 **2 OPTIONS POSSIBLES**

### **Option A : Connexion Directe au Backend Fear & Greed** ⭐ **RECOMMANDÉ**

**Avantages :**
- ✅ Réutilise le scraping existant
- ✅ Pas de duplication de code
- ✅ Articles déjà scrapés disponibles
- ✅ Analyse LLM incluse

**Inconvénient :**
- ⚠️ Nécessite que le backend soit en cours (port 8001)

### **Option B : Migration vers Supabase**

**Avantages :**
- ✅ Pas besoin du backend Fear & Greed
- ✅ Intégration avec votre infrastructure actuelle
- ✅ Stockage persistent dans Supabase

**Inconvénient :**
- ⚠️ Nécessite de migrer tout le code de scraping
- ⚠️ Duplication de la logique
- ⚠️ Plus complexe à maintenir

---

## 🚀 **OPTION A : Connexion Directe (Recommandé)**

### **Architecture**

```
Page Actualités (SaaS)
     ↓
Fetch /api/v1/media/latest
     ↓
Proxy Vite (port 8080)
     ↓
Backend Fear & Greed (port 8001)
     ↓
Articles scrapés avec sentiment LLM
```

### **Endpoints Disponibles**

Le backend Fear & Greed expose déjà ces endpoints :

1. **`GET /api/v1/media/latest`**
   - Retourne les derniers articles scrapés
   - Paramètre : `?limit=50` (par défaut 10)
   - Inclut : titre, source, URL, sentiment LLM, date

2. **`GET /api/v1/media/latest?source=Medias24`**
   - Filtrer par source spécifique

3. **`POST /api/v1/scheduler/trigger`**
   - Déclenche un nouveau scraping manuel
   - Scrape toutes les sources (Medias24, BourseNews, L'Économiste, etc.)

### **Données Retournées**

```json
{
  "data": [
    {
      "id": 123,
      "title": "Akdital investit 1.4 milliard DH",
      "source": "Medias24",
      "url": "https://...",
      "sentiment_score": 0.75,
      "sentiment_label": "Positif",
      "published_at": "2025-10-29T10:30:00",
      "scraped_at": "2025-10-29T10:31:00",
      "summary": null
    },
    ...
  ],
  "count": 109
}
```

---

## 📝 **IMPLÉMENTATION**

### **1. Créer un Composant Articles Fear & Greed**

Je vais créer un composant qui :
- Fetch les articles depuis `/api/v1/media/latest`
- Affiche les articles avec leur sentiment
- Permet de filtrer par source
- Bouton "Actualiser" pour trigger le scraping

### **2. Remplacer ou Compléter la Page News**

Deux approches :

**A. Remplacer complètement** (simple)
- Supprimer le code Supabase
- Utiliser uniquement le backend Fear & Greed

**B. Onglets (hybride)**
- Onglet 1 : Articles Supabase (actuels)
- Onglet 2 : Articles Fear & Greed (nouveaux)

---

## 🎨 **AVANTAGES DU SCRAPING FEAR & GREED**

### **Sources Disponibles**

- ✅ **Medias24** - Actualités économiques
- ✅ **BourseNews** - Marché boursier
- ✅ **L'Économiste** - Économie et finance
- ✅ **Challenge.ma** - Business et économie
- ✅ **La Vie Éco** - Économie marocaine

### **Données Enrichies**

- ✅ **Sentiment LLM** - Analysé par GPT-4o-mini
- ✅ **Score de -1 à +1** - Négatif → Positif
- ✅ **Label** - Très Négatif / Négatif / Neutre / Positif / Très Positif
- ✅ **Date de publication**
- ✅ **Source originale**
- ✅ **URL vers l'article**

---

## 💡 **PROPOSITION D'INTERFACE**

```
┌──────────────────────────────────────────────────────┐
│ 📰 Actualités Financières                           │
│                                                      │
│ [Tout] [Medias24] [BourseNews] [L'Économiste]      │
│                                    [🔄 Actualiser]   │
├──────────────────────────────────────────────────────┤
│                                                      │
│ ┌──────────────────────────────────────────────────┐│
│ │ 😊 Akdital investit 1.4 milliard DH              ││
│ │ Medias24 - 29 oct 2025                           ││
│ │ Sentiment: Positif (+0.75)                       ││
│ └──────────────────────────────────────────────────┘│
│                                                      │
│ ┌──────────────────────────────────────────────────┐│
│ │ 😐 Baisse des prix des viandes rouges           ││
│ │ L'Économiste - 29 oct 2025                       ││
│ │ Sentiment: Neutre (0.05)                         ││
│ └──────────────────────────────────────────────────┘│
│                                                      │
│ ┌──────────────────────────────────────────────────┐│
│ │ 😟 Récession dans le secteur immobilier         ││
│ │ Challenge.ma - 28 oct 2025                       ││
│ │ Sentiment: Négatif (-0.60)                       ││
│ └──────────────────────────────────────────────────┘│
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🔄 **WORKFLOW UTILISATEUR**

### **Chargement Initial**

1. User va sur `/news`
2. Composant fetch `/api/v1/media/latest?limit=50`
3. Affichage des 50 derniers articles scrapés
4. Articles triés par date (plus récent en premier)

### **Actualisation Manuelle**

1. User clique sur "Actualiser"
2. POST `/api/v1/scheduler/trigger`
3. Backend scrape toutes les sources
4. Analyse LLM des nouveaux articles
5. Refresh automatique de la liste
6. Toast de confirmation : "15 nouveaux articles ajoutés"

### **Filtrage par Source**

1. User clique sur "Medias24"
2. Fetch `/api/v1/media/latest?source=Medias24&limit=50`
3. Affichage uniquement des articles de Medias24

---

## ⚙️ **CONFIGURATION**

### **Backend Requis**

Pour que ça fonctionne, le **backend Fear & Greed** doit être EN COURS :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='sk-proj-...'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### **Proxy Vite**

Le proxy est déjà configuré dans `vite.config.ts` :

```typescript
proxy: {
  '/api/v1': {
    target: 'http://127.0.0.1:8001',
    changeOrigin: true,
    secure: false,
  },
}
```

**Donc les appels à `/api/v1/media/latest` sont automatiquement redirigés vers le backend !** ✅

---

## 🎯 **PROCHAINES ÉTAPES**

### **1. Créer le Composant FearGreedNews**

```typescript
// src/components/fear-greed/FearGreedNews.tsx

const FearGreedNews = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch('/api/v1/media/latest?limit=50')
      .then(res => res.json())
      .then(data => setArticles(data.data))
      .finally(() => setLoading(false));
  }, []);
  
  // ... render
};
```

### **2. Intégrer dans la Page News**

Deux options :

**A. Remplacement Total**
```typescript
// src/pages/News.tsx
import FearGreedNews from "@/components/fear-greed/FearGreedNews";

export default function News() {
  return <FearGreedNews />;
}
```

**B. Onglets (Hybride)**
```typescript
<Tabs>
  <Tab label="Articles Supabase">
    {/* Code actuel */}
  </Tab>
  <Tab label="Articles Fear & Greed">
    <FearGreedNews />
  </Tab>
</Tabs>
```

---

## 💰 **GESTION DES COÛTS API**

### **Scraping Sans LLM** (Économique)

Le scraping actuel des articles **ne consomme PAS de tokens GPT** !

Les tokens sont uniquement utilisés pour :
- ✅ L'analyse de sentiment (optionnelle)
- ✅ Le calcul du score Fear & Greed

**Donc vous pouvez scraper autant d'articles que vous voulez sans consommer de crédits !**

### **Analyse LLM** (Optionnelle)

Si vous voulez le sentiment LLM :
- Backend EN COURS
- Scraping avec analyse automatique
- ~100-200 tokens par article
- ~$0.001 par article

**Stratégie économique :**
1. Scraper sans backend (pas de sentiment)
2. Activer le backend uniquement pour Fear & Greed
3. Utiliser les articles scrapés sans analyse

---

## 🚨 **BACKEND ARRÊTÉ = PAS D'ARTICLES ?**

### **Avec Backend Arrêté** 🛑

- ❌ Pas de nouveaux articles
- ❌ Pas de sentiment LLM
- ❌ Endpoint `/api/v1/media/latest` indisponible

**Solution :** Garder la page Supabase comme fallback

### **Avec Backend EN COURS** ▶️

- ✅ Nouveaux articles toutes les 10 min
- ✅ Sentiment LLM disponible
- ✅ Endpoint `/api/v1/media/latest` accessible

---

## 📊 **COMPARAISON**

| Feature | Supabase (Actuel) | Fear & Greed API |
|---------|-------------------|------------------|
| **Sources** | Hespress, Boursenews, Medias24 | Medias24, BourseNews, L'Économiste, Challenge, La Vie Éco |
| **Sentiment** | Non | ✅ LLM GPT |
| **Stockage** | Supabase DB | SQLite (backend) |
| **Coût** | Supabase free tier | Gratuit (sauf LLM) |
| **Autonome** | ✅ Oui | ⚠️ Nécessite backend |
| **Enrichissement** | Basique | ✅ Score sentiment |

---

## 🎯 **RECOMMANDATION**

### **Option Hybride** ⭐

1. **Garder Supabase** pour les articles existants
2. **Ajouter un onglet "Sentiment du Marché"** avec les articles Fear & Greed
3. **Avantage :** Double source d'articles + Sentiment LLM
4. **Flexibilité :** Fonctionne même si backend arrêté

### **Implémentation**

```
┌────────────────────────────────────────────┐
│ 📰 Actualités                              │
│                                            │
│ [Toutes les News] [Sentiment du Marché]   │
├────────────────────────────────────────────┤
│ Onglet 1: Articles Supabase (109 articles)│
│ Onglet 2: Articles Fear & Greed (avec LLM)│
└────────────────────────────────────────────┘
```

---

## ✅ **PRÊT À IMPLÉMENTER ?**

Je peux créer :

1. ✅ **Composant FearGreedNews** - Affichage des articles avec sentiment
2. ✅ **Bouton Actualiser** - Trigger le scraping
3. ✅ **Filtres par source** - Medias24, BourseNews, etc.
4. ✅ **Intégration onglets** - Dans la page News existante

**Voulez-vous que je crée ce composant maintenant ?** 🚀

