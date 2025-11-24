# Système d'Auto-Update des Articles

Ce système permet de récupérer automatiquement les nouveaux articles et de les ajouter à la base de données, tout en gardant les anciens articles.

## 🚀 Fonctionnalités

- **Scraping automatique** : Récupère les articles des sites marocains
- **Nettoyage automatique** : Supprime les articles plus anciens que 30 jours
- **Mise à jour en temps réel** : L'interface se met à jour automatiquement
- **Gestion des doublons** : Évite les articles en double

## 📋 Configuration

### 1. Auto-update via l'interface web
Le système se met à jour automatiquement toutes les 30 minutes quand vous êtes sur la page d'actualités.

### 2. Auto-update via cron job (recommandé pour la production)
```bash
# Configurer le cron job (toutes les 10 minutes)
./scripts/setup-cron.sh

# Le scraping s'exécutera toutes les 10 minutes
```

### 3. Auto-update manuel
```bash
# Tester le système
node scripts/test-auto-update.js

# Exécuter l'auto-update manuellement
node scripts/auto-update-news.js
```

## 🔧 Fonctions Supabase

### `auto-update-news`
- **URL** : `/functions/v1/auto-update-news`
- **Méthode** : POST
- **Description** : Déclenche le scraping et nettoie les anciens articles

### `scrape-news`
- **URL** : `/functions/v1/scrape-news`
- **Méthode** : POST
- **Description** : Scrape les articles des sites configurés

## 📊 Sources configurées

- **Hespress** (Économie & Politique)
- **Boursenews** (Finance & Bourse)
- **Medias24** (Économie)
- **Le Matin** (Économie & Politique)
- **Le360** (Économie & Politique)
- **H24Info** (Économie & Politique)
- **Challenge** (Bourse & Finance)
- **LesEco** (Économie)

## 🕐 Planification

### Interface web
- **Fréquence** : Toutes les 30 minutes
- **Déclenchement** : Automatique quand la page est ouverte

### Cron job
- **Fréquence** : Toutes les 10 minutes
- **Logs** : `logs/auto-update.log`

## 📝 Logs et monitoring

```bash
# Voir les logs du cron job
tail -f logs/auto-update.log

# Vérifier le cron job
crontab -l

# Supprimer le cron job
crontab -e
```

## 🔍 Dépannage

### Problèmes courants

1. **Aucun article ne s'affiche**
   - Vérifier que la fonction `auto-update-news` est déployée
   - Vérifier les logs pour les erreurs

2. **Articles dupliqués**
   - Le système utilise `source_url` comme clé unique
   - Les doublons sont automatiquement évités

3. **Scraping lent**
   - Réduire `maxPerSite` et `limitSites` dans la configuration
   - Vérifier la connectivité internet

### Commandes utiles

```bash
# Tester le scraping
node scripts/test-auto-update.js

# Vérifier les articles dans la base
# (via l'interface Supabase ou SQL)

# Forcer une mise à jour
# (via le bouton "Actualiser maintenant" sur la page)
```

## 🎯 Résultat attendu

- **Nouveaux articles** : Ajoutés automatiquement à la base de données
- **Anciens articles** : Conservés (sauf ceux > 30 jours)
- **Interface** : Mise à jour automatique toutes les 30 minutes
- **Performance** : Optimisée avec nettoyage automatique
