Objectif
- Mettre à jour automatiquement les actualités (Hespress, Boursenews, Medias24) toutes les heures, sans clic.

Fonctions utilisées
- `scrape-news`: Scraper HTML (avec fallback) des sites cibles et insérer en base (`articles`).
- `scrape-rss-news`: Scraper via RSS (fallback rapide et stable).
- `auto-update-news`: Orchestration: purge des vieux articles, scrape des 3 sources, nettoyage des doublons.

Prérequis
- Remplir `supabase/.secrets.functions` (clé Service Role + Firecrawl facultatif).
- Avoir le CLI Supabase connecté au bon projet (`supabase/config.toml` -> `project_id`).

Déploiement des Edge Functions
- supabase functions deploy scrape-news --no-verify-jwt --env-file supabase/.secrets.functions
- supabase functions deploy scrape-rss-news --no-verify-jwt --env-file supabase/.secrets.functions
- supabase functions deploy auto-update-news --no-verify-jwt --env-file supabase/.secrets.functions

Planification (toutes les heures)
Option 1 — Dashboard (recommandé):
- Supabase Dashboard → Edge Functions → Schedules → New schedule
- Function: `auto-update-news`
- Cron: `0 * * * *` (toutes les heures)

Option 2 — CLI (si activé sur votre compte):
- supabase functions schedule create auto-update-news-hourly --cron "0 * * * *" --function auto-update-news

Vérification rapide
- node scripts/auto-update-test.js
- ou: appeler la page Actualités et cliquer sur “Actualiser” (utilise `scrape-rss-news`).

Nettoyage des articles
- Doublons: `cleanup_duplicate_articles()` (migration 20250120000009) supprime les doublons par `source_url`.
- Anciens: `auto-update-news` supprime les articles de plus de 7 jours (configurable dans le code si besoin).

Notes
- La page `src/pages/News.tsx` affiche maintenant l’heure réelle de la dernière mise à jour (carte “Dernière MAJ”).
- Les fonctions sont configurées avec `verify_jwt = false` dans `supabase/config.toml` pour permettre l’exécution par le scheduler.
