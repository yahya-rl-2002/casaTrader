# 🔧 Guide : Résoudre le Problème RLS Supabase

**Problème**: Erreur "new row violates row-level security policy"  
**Solution**: Utiliser la clé SERVICE de Supabase

---

## 🎯 Solution Rapide

### 1. Trouver la Clé Service Supabase

1. Allez sur https://supabase.com/dashboard
2. Sélectionnez votre projet
3. Allez dans **Settings** → **API**
4. Dans la section **"service_role"**, copiez la clé **"service_role" key** (c'est la clé secrète)

### 2. Ajouter dans backend/.env

Ajoutez cette ligne dans `backend/.env` :

```env
SUPABASE_SERVICE_KEY=votre-clé-service-ici
```

**Important** : Remplacez `votre-clé-service-ici` par la vraie clé service que vous avez copiée.

### 3. Synchroniser les Articles

```bash
cd backend
python sync_to_supabase.py
```

---

## ✅ Vérification

Après la synchronisation, vérifiez que les articles sont dans Supabase :

```python
from app.services.supabase_sync_service import SupabaseSyncService

sync_service = SupabaseSyncService()
if sync_service.client:
    result = sync_service.client.table('articles').select('source').limit(100).execute()
    # Compter par source
```

---

## 🚀 Résultat

Après avoir configuré la clé service et synchronisé :

- ✅ Tous les articles (Hespress, Medias24, BourseNews) seront dans Supabase
- ✅ Tous les articles s'afficheront sur le site
- ✅ Les images seront aussi synchronisées

---

## ⚠️ Sécurité

**Important** : La clé service est **secrète**. Ne la partagez jamais et ne la commitez pas dans Git.

Le fichier `.env` est normalement dans `.gitignore`, donc c'est sécurisé.

---

## 📝 Résumé

1. ✅ Copier la clé service depuis Supabase Dashboard
2. ✅ Ajouter `SUPABASE_SERVICE_KEY=...` dans `backend/.env`
3. ✅ Exécuter `python sync_to_supabase.py`
4. ✅ Vérifier que tous les articles s'affichent sur le site

**C'est tout !** 🚀




