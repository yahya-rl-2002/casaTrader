# Guide de Récupération des Rapports Financiers

Ce guide explique toutes les méthodes disponibles pour récupérer et ajouter des rapports financiers officiels des entreprises cotées à la Bourse de Casablanca.

## 📊 Méthodes de Récupération

### 1. **Récupération Automatique (Actuelle)**

Les rapports sont actuellement récupérés depuis **Supabase** :

```typescript
// Dans Reports.tsx
const { data, error } = await supabase
  .from('financial_reports')
  .select('*')
  .order('created_at', { ascending: false });
```

**Emplacement des données :**
- **Base de données** : Table `financial_reports` dans Supabase
- **Fichiers PDF** : Bucket `documents` dans Supabase Storage
- **URL publique** : Les fichiers sont accessibles via `file_url`

---

## 🔄 Méthodes pour Ajouter des Rapports

### **Méthode 1 : Upload Manuel via l'Interface**

**✅ Déjà disponible** - Utilisez le bouton "Ajouter un rapport" sur la page `/reports`

**Étapes :**
1. Cliquez sur "Ajouter un rapport"
2. Sélectionnez le fichier PDF (max 50MB)
3. Remplissez les informations :
   - Société (obligatoire)
   - Type de rapport (obligatoire)
   - Titre (obligatoire)
   - Description (optionnel)
   - Dates de publication et période
   - Tags (optionnel)
4. Cliquez sur "Ajouter le rapport"

**Fichier :** `src/components/FinancialReportUpload.tsx`

---

### **Méthode 2 : Script Python pour Scraping Automatique**

Créer un script pour télécharger automatiquement les rapports depuis les sites officiels des entreprises.

**Exemple de structure :**

```python
# backend/scripts/scrape_financial_reports.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class FinancialReportsScraper:
    """Scraper pour récupérer les rapports financiers officiels"""
    
    # URLs des pages de rapports par entreprise
    COMPANY_REPORTS_URLS = {
        'CSEMA:ATW': {
            'name': 'Attijariwafa Bank',
            'urls': [
                'https://www.attijariwafabank.com/fr/investisseurs/rapports-financiers',
                'https://www.attijariwafabank.com/fr/investisseurs/rapports-annuels'
            ]
        },
        'CSEMA:BCP': {
            'name': 'Banque Centrale Populaire',
            'urls': [
                'https://www.banquecentralepopulaire.ma/fr/investisseurs/rapports',
            ]
        },
        'CSEMA:IAM': {
            'name': 'Maroc Telecom',
            'urls': [
                'https://www.iam.ma/fr/investisseurs/rapports-financiers',
            ]
        },
        # Ajouter d'autres entreprises...
    }
    
    def scrape_company_reports(self, company_symbol: str):
        """Scraper les rapports d'une entreprise spécifique"""
        company_info = self.COMPANY_REPORTS_URLS.get(company_symbol)
        if not company_info:
            return []
        
        all_reports = []
        
        for url in company_info['urls']:
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les liens PDF
                pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
                
                for link in pdf_links:
                    pdf_url = link.get('href')
                    if not pdf_url.startswith('http'):
                        pdf_url = url + pdf_url if pdf_url.startswith('/') else url + '/' + pdf_url
                    
                    # Analyser le titre pour déterminer le type
                    title = link.get_text(strip=True) or link.get('title', '')
                    report_type = self._determine_report_type(title, pdf_url)
                    
                    # Extraire l'année
                    year_match = re.search(r'20\d{2}', title)
                    year = year_match.group() if year_match else None
                    
                    report = {
                        'company_symbol': company_symbol,
                        'company_name': company_info['name'],
                        'report_type': report_type,
                        'title': title,
                        'file_url': pdf_url,
                        'file_name': pdf_url.split('/')[-1],
                        'published_at': self._extract_date(soup, link),
                        'tags': self._extract_tags(title, report_type),
                        'featured': False
                    }
                    
                    all_reports.append(report)
                    
            except Exception as e:
                print(f"Erreur scraping {url}: {e}")
                continue
        
        return all_reports
    
    def _determine_report_type(self, title: str, url: str) -> str:
        """Déterminer le type de rapport depuis le titre/URL"""
        title_lower = title.lower()
        url_lower = url.lower()
        
        if 'annuel' in title_lower or 'annual' in title_lower:
            return 'rapport-annuel'
        elif 'trimestriel' in title_lower or 'quarterly' in title_lower or 't1' in title_lower or 't2' in title_lower or 't3' in title_lower or 't4' in title_lower:
            return 'rapport-trimestriel'
        elif 'semestriel' in title_lower or 'semiannual' in title_lower or 's1' in title_lower or 's2' in title_lower:
            return 'rapport-semestriel'
        elif 'resultat' in title_lower or 'result' in title_lower:
            return 'resultats'
        elif 'communique' in title_lower or 'communiqué' in title_lower:
            return 'communique'
        elif 'profit' in title_lower and 'warning' in title_lower:
            return 'profit-warning'
        else:
            return 'autre'
    
    def _extract_date(self, soup, link_element):
        """Extraire la date de publication"""
        # Chercher la date dans le parent ou les éléments proches
        parent = link_element.find_parent(['div', 'li', 'article'])
        if parent:
            date_text = parent.get_text()
            # Regex pour trouver les dates
            date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', date_text)
            if date_match:
                return datetime.strptime(date_match.group(), '%d/%m/%Y').isoformat()
        return None
    
    def _extract_tags(self, title: str, report_type: str) -> list:
        """Extraire des tags pertinents"""
        tags = [report_type, 'officiel', 'scraped']
        
        # Ajouter des tags basés sur le titre
        if '2024' in title:
            tags.append('2024')
        if '2023' in title:
            tags.append('2023')
        
        return tags
```

---

### **Méthode 3 : API Backend pour Scraping**

Créer un endpoint FastAPI pour déclencher le scraping :

```python
# backend/app/api/v1/endpoints/financial_reports.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.database import get_db
from sqlalchemy.orm import Session
from app.services.financial_reports_scraper import FinancialReportsScraper
from app.services.supabase_sync_service import SupabaseSyncService

router = APIRouter()

@router.post("/scrape/{company_symbol}")
async def scrape_company_reports(
    company_symbol: str,
    db: Session = Depends(get_db)
):
    """Scraper les rapports financiers d'une entreprise"""
    scraper = FinancialReportsScraper()
    reports = scraper.scrape_company_reports(company_symbol)
    
    # Sauvegarder dans Supabase
    sync_service = SupabaseSyncService()
    saved_count = 0
    
    for report in reports:
        try:
            # Vérifier si existe déjà
            existing = db.query(FinancialReport).filter(
                FinancialReport.file_url == report['file_url']
            ).first()
            
            if not existing:
                # Insérer dans Supabase
                await sync_service.insert_financial_report(report)
                saved_count += 1
        except Exception as e:
            logger.error(f"Erreur sauvegarde rapport: {e}")
            continue
    
    return {
        "success": True,
        "scraped": len(reports),
        "saved": saved_count,
        "company": company_symbol
    }

@router.post("/scrape-all")
async def scrape_all_companies(db: Session = Depends(get_db)):
    """Scraper les rapports de toutes les entreprises"""
    scraper = FinancialReportsScraper()
    results = {}
    
    for company_symbol in scraper.COMPANY_REPORTS_URLS.keys():
        try:
            reports = scraper.scrape_company_reports(company_symbol)
            # Sauvegarder...
            results[company_symbol] = len(reports)
        except Exception as e:
            results[company_symbol] = f"Erreur: {e}"
    
    return {"results": results}
```

---

### **Méthode 4 : Fonction Supabase Edge (Déjà existante)**

Il existe déjà des fonctions Supabase pour scraper Akdital :
- `supabase/functions/scrape-akdital-python/index.ts`
- `supabase/functions/scrape-real-akdital/index.ts`

**Pour les étendre à d'autres entreprises :**

1. Créer une nouvelle fonction : `supabase/functions/scrape-financial-reports/index.ts`
2. Ajouter les URLs de toutes les entreprises
3. Déclencher via cron job ou API

---

## 🛠️ Implémentation Recommandée

### **Option A : Script Python Standalone**

Créer un script Python qui :
1. Scrape les rapports depuis les sites officiels
2. Télécharge les PDFs
3. Upload vers Supabase Storage
4. Insère les métadonnées dans la table `financial_reports`

**Avantages :**
- Contrôle total
- Peut être exécuté manuellement ou via cron
- Facile à déboguer

### **Option B : Service Backend Intégré**

Créer un service dans le backend FastAPI :
- `backend/app/services/financial_reports_scraper.py`
- Endpoint API : `/api/v1/financial-reports/scrape/{company_symbol}`
- Peut être déclenché via l'interface ou automatiquement

**Avantages :**
- Intégré dans l'architecture existante
- Accessible via API
- Peut être programmé avec APScheduler

### **Option C : Fonction Supabase Edge**

Créer une fonction Deno qui :
- Scrape les rapports
- Upload directement dans Supabase
- Déclenchable via cron ou webhook

**Avantages :**
- Pas besoin de serveur backend
- Scalable automatiquement
- Gratuit pour usage modéré

---

## 📝 Sources Officielles des Rapports

### **Banques :**
- **Attijariwafa Bank** : https://www.attijariwafabank.com/fr/investisseurs/rapports-financiers
- **BCP** : https://www.banquecentralepopulaire.ma/fr/investisseurs/rapports
- **Bank of Africa** : https://www.bankofafrica.ma/fr/investisseurs/rapports
- **CIH Bank** : https://www.cihbank.ma/fr/investisseurs/rapports

### **Télécoms :**
- **Maroc Telecom** : https://www.iam.ma/fr/investisseurs/rapports-financiers

### **Autres Secteurs :**
- **OCP** : https://www.ocpgroup.ma/fr/investisseurs/rapports
- **Managem** : https://www.managemgroup.com/fr/investisseurs/rapports

---

## 🚀 Prochaines Étapes

1. **Créer le scraper Python** pour toutes les entreprises
2. **Ajouter un endpoint API** pour déclencher le scraping
3. **Programmer un job automatique** (quotidien ou hebdomadaire)
4. **Ajouter une interface admin** pour gérer les scrapings

Souhaitez-vous que je crée le script de scraping automatique pour toutes les entreprises ?



