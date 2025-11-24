# 🔍 Problème : Seuls les Articles Hespress s'Affichent

**Date**: Aujourd'hui  
**Problème**: Le site affiche seulement les articles de Hespress, pas tous les articles

---

## 🔍 Cause du Problème

Le problème vient du fait que **deux systèmes de base de données sont utilisés** :

1. **SQLite (FastAPI)** : Le système de scraping sauvegarde les articles dans SQLite (base de données locale)
2. **Supabase** : Le frontend récupère les articles depuis Supabase (`supabase.from('articles')`)

**Résultat** : Les articles scrapés sont sauvegardés dans SQLite, mais le frontend ne les voit pas car il lit depuis Supabase !

---

## ✅ Solution Implémentée

### 1. **Service de Synchronisation**

J'ai créé un service de synchronisation (`SupabaseSyncService`) qui :
- ✅ Récupère les articles de SQLite (FastAPI)
- ✅ Les synchronise vers Supabase
- ✅ Met à jour les articles existants ou crée de nouveaux articles

### 2. **Synchronisation Automatique**

La synchronisation se fait maintenant **automatiquement** après chaque scraping :
- ✅ Après le scraping, les articles sont synchronisés vers Supabase
- ✅ Les 3 sources (Hespress, Medias24, BourseNews) sont synchronisées
- ✅ Les images sont aussi synchronisées

### 3. **Script de Synchronisation Manuel**

Un script est disponible pour synchroniser manuellement :

```bash
cd backend
python sync_to_supabase.py
```

---

## 🔧 Configuration Requise

### 1. Installer le Client Supabase

```bash
cd backend
pip install supabase
```

### 2. Configurer les Variables d'Environnement

Ajoutez dans votre fichier `.env` du backend :

```env
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_ANON_KEY=votre-clé-anon
# OU
SUPABASE_SERVICE_KEY=votre-clé-service
```

### 3. Vérifier les Credentials Supabase

Les credentials Supabase sont normalement déjà dans le frontend. Vérifiez dans :
- `src/integrations/supabase/client.ts`
- Variables d'environnement du frontend

---

## 🚀 Utilisation

### Synchronisation Automatique

La synchronisation se fait **automatiquement** après chaque scraping :
1. ✅ Cliquez sur "Actualiser" dans la page News
2. ✅ Le scraping se déclenche (Hespress, Medias24, BourseNews)
3. ✅ Les articles sont sauvegardés dans SQLite
4. ✅ **Les articles sont automatiquement synchronisés vers Supabase**
5. ✅ Les articles apparaissent sur le site avec leurs images

### Synchronisation Manuelle

Si vous voulez synchroniser manuellement :

```bash
cd backend
python sync_to_supabase.py
```

---

## 📊 Résultats Attendus

Après la synchronisation, vous devriez voir :

### ✅ Articles de Toutes les Sources

- ✅ **Hespress** : Articles économiques avec images
- ✅ **Medias24** : Actualités avec images
- ✅ **BourseNews** : Actualités boursières avec images

### ✅ Articles avec Images

- ✅ Chaque article a sa propre image principale
- ✅ Les images sont extraites et synchronisées
- ✅ Les images s'affichent correctement sur le site

---

## ⚠️ Notes Importantes

1. **Première Synchronisation** : La première synchronisation peut prendre quelques secondes
2. **Variables d'Environnement** : Assurez-vous que les credentials Supabase sont configurés
3. **Doublons** : Le système évite les doublons en vérifiant l'URL de l'article

---

## 🔧 Vérification

Pour vérifier que tout fonctionne :

1. ✅ Installez le client Supabase : `pip install supabase`
2. ✅ Configurez les variables d'environnement Supabase
3. ✅ Cliquez sur "Actualiser" dans la page News
4. ✅ Vérifiez que les articles de toutes les sources apparaissent
5. ✅ Vérifiez que les images s'affichent correctement

---

## 📝 Résumé

**Problème** : Le frontend lit depuis Supabase, mais le scraping sauvegarde dans SQLite.

**Solution** : Synchronisation automatique des articles de SQLite vers Supabase après chaque scraping.

**Résultat** : Tous les articles (Hespress, Medias24, BourseNews) avec leurs images apparaissent maintenant sur le site ! 🚀




