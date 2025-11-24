# 🔧 Configuration de la Synchronisation Supabase

**Date**: Aujourd'hui  
**Objectif**: Synchroniser les articles de SQLite vers Supabase

---

## ✅ Installation

Le client Supabase est déjà installé :

```bash
pip install supabase
```

---

## 🔧 Configuration des Variables d'Environnement

### 1. Trouver les Credentials Supabase

Les credentials Supabase sont normalement dans le frontend. Vérifiez dans :
- `src/integrations/supabase/client.ts`
- Variables d'environnement du frontend (`.env` ou `.env.local`)

### 2. Ajouter les Variables au Backend

Ajoutez dans votre fichier `.env` du backend :

```env
# Supabase Configuration
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_ANON_KEY=votre-clé-anon
# OU utilisez la clé service pour plus de permissions
SUPABASE_SERVICE_KEY=votre-clé-service
```

### 3. Exemple de Configuration

```env
# Exemple (remplacez par vos vraies valeurs)
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

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
4. **Erreurs** : Si la synchronisation échoue, les articles restent dans SQLite et peuvent être synchronisés plus tard

---

## 🔧 Vérification

Pour vérifier que tout fonctionne :

1. ✅ Installez le client Supabase : `pip install supabase` (déjà fait)
2. ✅ Configurez les variables d'environnement Supabase dans `.env`
3. ✅ Cliquez sur "Actualiser" dans la page News
4. ✅ Vérifiez que les articles de toutes les sources apparaissent
5. ✅ Vérifiez que les images s'affichent correctement

---

## 📝 Résumé

**Problème** : Le frontend lit depuis Supabase, mais le scraping sauvegarde dans SQLite.

**Solution** : 
- ✅ Service de synchronisation créé
- ✅ Synchronisation automatique après scraping
- ✅ Script de synchronisation manuelle disponible

**Actions Requises** :
1. ✅ Installer le client Supabase (déjà fait)
2. ⏳ Configurer SUPABASE_URL et SUPABASE_ANON_KEY dans `.env`
3. ✅ Cliquer sur "Actualiser" pour synchroniser

**Résultat** : Tous les articles (Hespress, Medias24, BourseNews) avec leurs images apparaissent maintenant sur le site ! 🚀




