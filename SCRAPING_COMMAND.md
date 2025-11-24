# 🚀 Commande de Scraping des Rapports Financiers

## ✅ Vérifications effectuées

- ✅ Module `supabase` installé
- ✅ `FinancialReportsScraper` importé correctement
- ✅ Endpoint API configuré
- ✅ Router enregistré

## 📋 Commandes de Scraping

### Option 1 : Scraper une entreprise spécifique (Recommandé pour tester)

```bash
curl -X POST 'http://localhost:8001/api/v1/financial-reports/scrape/company?company_symbol=CSEMA:ATW&download_pdfs=true&max_reports=50'
```

**Entreprises disponibles :**
- `CSEMA:ATW` - Attijariwafa Bank
- `CSEMA:BCP` - Banque Centrale Populaire
- `CSEMA:BOA` - Bank of Africa
- `CSEMA:CIH` - CIH Bank
- `CSEMA:IAM` - Maroc Telecom
- `CSEMA:AKT` - Akdital
- `CSEMA:MAN` - Managem
- `CSEMA:OCP` - OCP Group

### Option 2 : Scraper toutes les entreprises

```bash
curl -X POST 'http://localhost:8001/api/v1/financial-reports/scrape' \
  -H "Content-Type: application/json" \
  -d '{
    "download_pdfs": true,
    "max_reports_per_company": 50
  }'
```

### Option 3 : Liste des entreprises configurées

```bash
curl 'http://localhost:8001/api/v1/financial-reports/companies'
```

## ⚠️ Important

1. **Assurez-vous que le backend est démarré** :
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8001
   ```

2. **Vérifiez que Supabase est configuré** dans `backend/.env` :
   ```
   SUPABASE_URL=https://votre-projet.supabase.co
   SUPABASE_SERVICE_KEY=votre-service-key
   ```

3. **Le scraping s'exécute en arrière-plan** - vous recevrez une réponse immédiate, mais le processus continue en background.

4. **Vérifiez les logs du backend** pour voir la progression du scraping.

## 📊 Résultat attendu

Après exécution, vous devriez recevoir :
```json
{
  "success": true,
  "message": "Scraping démarré pour CSEMA:ATW",
  "stats": null
}
```

Les rapports seront automatiquement :
- ✅ Scrapés depuis les sites officiels
- ✅ Téléchargés et uploadés vers Supabase Storage
- ✅ Sauvegardés dans la table `financial_reports`
- ✅ Affichés sur `/reports` dans le frontend

## 🔍 Vérifier les résultats

1. **Dans Supabase** : Vérifiez la table `financial_reports`
2. **Sur le site** : Visitez `/reports` pour voir les rapports
3. **Dans les logs** : Regardez les logs du backend pour les statistiques



