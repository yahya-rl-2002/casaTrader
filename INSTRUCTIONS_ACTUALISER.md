# 🔄 Instructions : Actualiser les Articles avec Images

**Date**: Aujourd'hui  
**Objectif**: Obtenir de nouveaux articles avec leurs images

---

## ✅ Oui, cliquez sur "Actualiser" !

### 📋 Étapes à Suivre

1. **Cliquez sur le bouton "Actualiser"** dans la page News
   - Le bouton déclenchera automatiquement le scraping
   - Les nouveaux articles seront scrapés avec leurs images

2. **Attendez quelques secondes**
   - Le scraping prend quelques secondes (5-10 secondes)
   - Les articles sont scrapés depuis les 3 sources :
     - ✅ **Hespress**
     - ✅ **Medias24**  
     - ✅ **BourseNews**

3. **Vérifiez les résultats**
   - Les nouveaux articles apparaîtront avec leurs images
   - Chaque article aura sa propre image principale

---

## 🚀 Alternative : Déclencher via l'API

Si vous voulez déclencher le scraping manuellement via l'API :

```bash
# Déclencher le scraping
curl -X POST http://localhost:8001/api/v1/media/trigger-scraping

# Vérifier les articles avec images
curl http://localhost:8001/api/v1/media/latest?limit=10
```

---

## 📊 Ce qui se Passe

### 1. **Déclenchement du Scraping** 🔄

Quand vous cliquez sur "Actualiser" :
- ✅ Le système déclenche le scraping des 3 sources
- ✅ Chaque article est scrapé individuellement
- ✅ Le contenu complet est extrait
- ✅ **L'image principale est extraite automatiquement**

### 2. **Extraction des Images** 🖼️

Pour chaque article, l'image est extraite depuis :
1. **Open Graph** (`og:image`) - Priorité
2. **Twitter Card** (`twitter:image`)
3. **Image dans l'article** (balise `<img>` dans `<article>`)
4. **Première image de la page** (dernier recours)

### 3. **Sauvegarde** 💾

Les articles sont sauvegardés avec :
- ✅ Titre complet
- ✅ Contenu complet
- ✅ **Image URL** (prête à être affichée)
- ✅ Source (hespress, medias24, boursenews)
- ✅ Date de publication

### 4. **Affichage** 📱

Les articles s'affichent avec :
- ✅ Titre
- ✅ **Image principale** (si disponible)
- ✅ Résumé/Contenu
- ✅ Source
- ✅ Date

---

## ⚠️ Notes Importantes

1. **Premier Scraping** : Le premier scraping peut prendre 10-15 secondes
2. **Images Manquantes** : Si un article n'a pas d'image, le champ `image_url` sera `null`
3. **Auto-Scraping** : Le système déclenche aussi automatiquement le scraping si les articles sont anciens (> 1 heure)

---

## 🎯 Résultats Attendus

Après avoir cliqué sur "Actualiser", vous devriez voir :

### ✅ Articles avec Images

- Chaque article a sa propre image principale
- Les images sont extraites automatiquement
- Les images sont prêtes à être affichées sur le site

### ✅ Sources Scrapées

- **Hespress** : Articles économiques avec images
- **Medias24** : Actualités avec images (via cloudscraper)
- **BourseNews** : Actualités boursières avec images

---

## 🔧 Vérification

Pour vérifier que tout fonctionne :

1. ✅ Cliquez sur "Actualiser"
2. ✅ Attendez 10-15 secondes
3. ✅ Vérifiez que les nouveaux articles apparaissent
4. ✅ Vérifiez que les images s'affichent correctement

---

## 📝 Résumé

**Oui, cliquez sur "Actualiser" maintenant !** 

Le système va :
1. ✅ Scraper les 3 sources (Hespress, Medias24, BourseNews)
2. ✅ Extraire le contenu complet de chaque article
3. ✅ **Extraire l'image principale de chaque article**
4. ✅ Sauvegarder les articles avec leurs images
5. ✅ Afficher les articles avec leurs images sur le site

**Le système est maintenant prêt ! Cliquez sur "Actualiser" pour voir les articles avec leurs images !** 🚀




