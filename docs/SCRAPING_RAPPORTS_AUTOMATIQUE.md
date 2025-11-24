# Système de Scraping Automatique des Rapports Financiers

## 📋 Vue d'ensemble

Ce système permet de scraper automatiquement les rapports financiers officiels de toutes les entreprises cotées à la Bourse de Casablanca, de les télécharger, de les uploader vers Supabase Storage, et de les afficher automatiquement sur le site.

## 🚀 Fonctionnalités

✅ **Scraping automatique** des rapports depuis les sites officiels  
✅ **Téléchargement et upload** des PDFs vers Supabase Storage  
✅ **Sauvegarde automatique** des métadonnées dans Supabase  
✅ **Job programmé** quotidien à 02:00 AM  
✅ **API REST** pour déclencher le scraping manuellement  
✅ **Déduplication** automatique (évite les doublons)  

## 📁 Structure des Fichiers

```
backend/
├── app/
│   ├── services/
│   │   └── financial_reports_scraper.py  # Service principal de scraping
│   ├── api/v1/endpoints/
│   │   └── financial_reports.py          # Endpoints API
│   └── tasks/
│       └── jobs.py                       # Job automatique
```

## 🔧 Configuration

### 1. Variables d'environnement

Assurez-vous d'avoir configuré Supabase dans `backend/.env` :

```bash
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_SERVICE_KEY=votre-service-key
# ou
SUPABASE_ANON_KEY=votre-anon-key
```

### 2. Entreprises configurées

Les entreprises sont configurées dans `backend/app/services/financial_reports_scraper.py` :

```python
COMPANY_REPORTS_CONFIG = {
    'CSEMA:ATW': {
        'name': 'Attijariwafa Bank',
        'urls': [
            'https://www.attijariwafabank.com/fr/investisseurs/rapports-financiers',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    # ... autres entreprises
}
```

## 🎯 Utilisation

### Méthode 1 : Scraping Automatique (Recommandé)

Le système s'exécute **automatiquement tous les jours à 02:00 AM** via le scheduler.

**Aucune action requise** - les rapports seront automatiquement :
1. Scrapés depuis les sites officiels
2. Téléchargés et uploadés vers Supabase Storage
3. Sauvegardés dans la table `financial_reports`
4. Affichés sur le site

### Méthode 2 : Déclencher via API

#### Scraper toutes les entreprises

```bash
curl -X POST "http://localhost:8001/api/v1/financial-reports/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "download_pdfs": true,
    "max_reports_per_company": 50
  }'
```

#### Scraper une entreprise spécifique

```bash
curl -X POST "http://localhost:8001/api/v1/financial-reports/scrape/CSEMA:ATW" \
  -H "Content-Type: application/json" \
  -d '{
    "download_pdfs": true,
    "max_reports": 50
  }'
```

#### Liste des entreprises configurées

```bash
curl "http://localhost:8001/api/v1/financial-reports/companies"
```

### Méthode 3 : Depuis le code Python

```python
from app.services.financial_reports_scraper import FinancialReportsScraper

# Initialiser le scraper
scraper = FinancialReportsScraper()

# Scraper toutes les entreprises
stats = await scraper.scrape_all_companies(
    company_symbols=None,  # Toutes
    download_pdfs=True,
    max_reports_per_company=50
)

# Scraper une entreprise spécifique
stats = await scraper.scrape_and_save_company(
    company_symbol='CSEMA:ATW',
    download_pdfs=True,
    max_reports=50
)
```

## 📊 Format des Données

Chaque rapport scraper contient :

```python
{
    'company_symbol': 'CSEMA:ATW',
    'company_name': 'Attijariwafa Bank',
    'report_type': 'rapport-annuel',  # ou 'resultats', 'communique', etc.
    'title': 'Rapport Annuel 2024',
    'description': 'Rapport financier officiel de Attijariwafa Bank',
    'file_url': 'https://supabase.co/storage/.../rapport.pdf',
    'file_name': 'rapport-annuel-2024.pdf',
    'file_size': 2500000,  # en bytes
    'file_type': 'application/pdf',
    'published_at': '2024-03-15T00:00:00',
    'period_start': '2024-01-01',
    'period_end': '2024-12-31',
    'tags': ['officiel', 'scraped', 'rapport-annuel', '2024'],
    'featured': True
}
```

## 🔍 Types de Rapports Détectés

Le système détecte automatiquement le type de rapport depuis le titre/URL :

- **rapport-annuel** : Rapports annuels
- **rapport-trimestriel** : Rapports trimestriels (T1, T2, T3, T4)
- **rapport-semestriel** : Rapports semestriels (S1, S2)
- **resultats** : Résultats financiers
- **communique** : Communiqués
- **profit-warning** : Profit warnings
- **autre** : Autres types

## 📝 Ajouter une Nouvelle Entreprise

Pour ajouter une nouvelle entreprise au scraping :

1. **Trouver l'URL** de la page des rapports financiers
2. **Ajouter la configuration** dans `COMPANY_REPORTS_CONFIG` :

```python
'CSEMA:SYMBOL': {
    'name': 'Nom de l\'entreprise',
    'urls': [
        'https://www.entreprise.ma/investisseurs/rapports',
    ],
    'selectors': {
        'pdf_links': 'a[href$=".pdf"]',  # Sélecteur CSS pour les liens PDF
        'title': 'a',  # Sélecteur pour le titre
    }
}
```

3. **Tester** avec l'API :

```bash
curl -X POST "http://localhost:8001/api/v1/financial-reports/scrape/CSEMA:SYMBOL"
```

## 🛠️ Dépannage

### Erreur : "Supabase non configuré"

**Solution** : Vérifiez que `SUPABASE_URL` et `SUPABASE_SERVICE_KEY` sont définis dans `backend/.env`

### Erreur : "Aucun PDF trouvé"

**Solution** : 
1. Vérifiez que l'URL de l'entreprise est correcte
2. Vérifiez que le sélecteur CSS `pdf_links` est correct
3. Testez manuellement en visitant l'URL

### Erreur : "Upload échoué"

**Solution** :
1. Vérifiez que le bucket `documents` existe dans Supabase Storage
2. Vérifiez les permissions du bucket
3. Vérifiez que le fichier ne dépasse pas 50MB

### Les rapports ne s'affichent pas sur le site

**Solution** :
1. Vérifiez que les rapports sont bien dans Supabase (`financial_reports` table)
2. Vérifiez que le frontend charge bien depuis Supabase
3. Vérifiez les logs du backend pour les erreurs

## 📈 Monitoring

Les statistiques de scraping sont loggées :

```
✅ Financial reports scraping completed
   - total_companies: 9
   - total_scraped: 45
   - total_downloaded: 45
   - total_saved: 45
   - total_errors: 0
```

## 🔄 Workflow Complet

1. **Scraping** : Le scraper visite les URLs configurées
2. **Détection** : Les liens PDF sont détectés via les sélecteurs CSS
3. **Analyse** : Les métadonnées sont extraites (type, dates, tags)
4. **Téléchargement** : Les PDFs sont téléchargés
5. **Upload** : Les PDFs sont uploadés vers Supabase Storage
6. **Sauvegarde** : Les métadonnées sont sauvegardées dans `financial_reports`
7. **Affichage** : Les rapports apparaissent automatiquement sur `/reports`

## 🎯 Prochaines Améliorations

- [ ] Support pour d'autres formats (DOCX, XLSX)
- [ ] Extraction de texte depuis les PDFs (OCR)
- [ ] Analyse automatique du contenu des rapports
- [ ] Notifications par email pour nouveaux rapports
- [ ] Dashboard de monitoring du scraping
- [ ] Support pour plus d'entreprises

## 📚 Documentation API

Voir `/api/v1/docs` pour la documentation complète de l'API Swagger.



