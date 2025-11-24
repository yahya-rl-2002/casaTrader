# 🖼️ Extraction et Affichage des Images des Articles

**Date**: Aujourd'hui  
**Fonctionnalité**: Chaque article scrapé a maintenant sa propre image

---

## ✅ Modifications Apportées

### 1. **Ajout de la colonne `image_url` dans la base de données**

- ✅ Colonne `image_url` ajoutée au modèle `MediaArticle`
- ✅ Migration de la base de données pour ajouter la colonne
- ✅ Les images sont maintenant sauvegardées avec chaque article

### 2. **Amélioration de l'extraction d'images**

L'extraction d'images utilise maintenant plusieurs méthodes de fallback :

1. **Open Graph Image** (priorité) : `og:image` meta tag
2. **Twitter Card Image** : `twitter:image` meta tag
3. **Image dans l'article** : Cherche dans les balises `<article>`, `<main>`, ou divs avec classes `content/article/post`
4. **Première image de la page** : Dernier recours

### 3. **Filtrage intelligent**

Les images sont filtrées pour exclure :
- Les icônes (`icon`, `logo`, `avatar`, `favicon`, `sprite`)
- Les images trop petites (probablement des icônes)

### 4. **Normalisation des URLs**

Les URLs d'images sont normalisées :
- URLs relatives → URLs absolues
- URLs avec `//` → URLs complètes avec `https:`
- URLs avec `/` → URLs complètes avec le domaine

### 5. **API mise à jour**

L'API retourne maintenant le champ `image_url` pour chaque article :

```json
{
  "data": [
    {
      "id": 1,
      "title": "Titre de l'article",
      "url": "https://...",
      "image_url": "https://.../image.jpg",
      "content": "...",
      ...
    }
  ]
}
```

---

## 📊 Sources Configurées

### 1. **Hespress** ✅
- Extraction d'images via le scraper générique amélioré
- Images extraites depuis les balises `<img>` dans les articles

### 2. **Medias24** ✅
- Extraction d'images via le scraper spécialisé + scraper générique
- Images extraites lors du scraping du contenu complet

### 3. **BourseNews** ✅
- Extraction d'images via le scraper spécialisé + scraper générique
- Images extraites lors du scraping du contenu complet

---

## 🔧 Code Modifié

### 1. Modèle de base de données (`app/models/schemas.py`)

```python
class MediaArticle(Base):
    ...
    image_url = Column(String, nullable=True)  # URL de l'image principale
    ...
```

### 2. Extraction d'images (`app/pipelines/ingestion/enhanced_media_scraper.py`)

```python
# Image - Méthode améliorée avec plusieurs fallbacks
# 1. Open Graph image (priorité)
# 2. Twitter Card image
# 3. Image dans l'article
# 4. Première image de la page
```

### 3. Sauvegarde (`app/services/enhanced_media_service.py`)

```python
new_article = MediaArticle(
    ...
    image_url=article.image_url,  # Sauvegarder l'image
    ...
)
```

### 4. API (`app/api/v1/endpoints/media.py`)

```python
{
    ...
    "image_url": getattr(article, 'image_url', None),  # URL de l'image principale
    ...
}
```

---

## 🚀 Utilisation

### Via l'API

```bash
curl http://localhost:8001/api/v1/media/latest
```

Réponse :

```json
{
  "data": [
    {
      "id": 1,
      "title": "Titre de l'article",
      "url": "https://...",
      "image_url": "https://.../image.jpg",
      "content": "...",
      "source": "hespress",
      ...
    }
  ]
}
```

### Affichage sur le Frontend

Le frontend peut maintenant afficher les images des articles :

```jsx
{article.image_url && (
  <img 
    src={article.image_url} 
    alt={article.title}
    className="article-image"
  />
)}
```

---

## ✅ Résultats

- ✅ Colonne `image_url` ajoutée à la base de données
- ✅ Extraction d'images améliorée avec plusieurs fallbacks
- ✅ Images sauvegardées avec chaque article
- ✅ API retourne les images
- ✅ Prêt pour l'affichage sur le frontend

---

## 📝 Notes

1. **Images manquantes** : Si un article n'a pas d'image, le champ `image_url` sera `null`
2. **URLs relatives** : Toutes les URLs relatives sont converties en URLs absolues
3. **Filtrage** : Les icônes et logos sont automatiquement exclus
4. **Performance** : L'extraction d'images n'ajoute pas de surcharge significative au scraping

---

## 🎯 Prochaines Étapes

1. ✅ Extraction d'images implémentée
2. ✅ Sauvegarde en base de données
3. ✅ API retourne les images
4. ⏳ Affichage sur le frontend (à faire)

Le système est maintenant prêt pour afficher les images des articles sur le site ! 🚀




