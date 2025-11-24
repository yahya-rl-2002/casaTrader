"""
Service automatique pour scraper les rapports financiers officiels
de toutes les entreprises cotées à la Bourse de Casablanca
"""
from __future__ import annotations

import re
import os
import asyncio
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from urllib.parse import urljoin, urlparse
import tempfile

import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)

# Configuration des URLs de rapports par entreprise
# Format: {symbol: {name, urls: [liste des URLs à scraper]}}
COMPANY_REPORTS_CONFIG = {
    'CSEMA:ATW': {
        'name': 'Attijariwafa Bank',
        'urls': [
            'https://ir.attijariwafabank.com/news-releases',
        ],
        'selectors': {
            'pdf_links': 'a[href*="/static-files/"]',  # Les PDFs sont dans /static-files/
            'title': 'a',
        }
    },
    'CSEMA:BCP': {
        'name': 'Banque Centrale Populaire',
        'urls': [
            'https://www.groupebcp.com/fr/Pages/Finance.aspx#',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:BOA': {
        'name': 'Bank of Africa',
        'urls': [
            'https://www.ir-bankofafrica.ma/information-financiere-et-extra-financiere/communiques-financiers',
            'https://www.ir-bankofafrica.ma/information-financiere-et-extra-financiere/etats-financiers-consolides-et-notes-annexes',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:CIH': {
        'name': 'CIH Bank',
        'urls': [
            'https://www.cihbank.ma/espace-financier/resultats-financiers',
            'https://www.cihbank.ma/espace-financier/communiques',
            'https://www.cihbank.ma/espace-financier/rapports-activites',
            'https://www.cihbank.ma/espace-financier/note-informations',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:IAM': {
        'name': 'Maroc Telecom',
        'urls': [
            'https://www.iam.ma/groupe-maroc-telecom/rapports-publications/financial-releases/647529',
            'https://www.iam.ma/groupe-maroc-telecom/rapports-publications/presentation-des-resultats/647532',
            'https://www.iam.ma/groupe-maroc-telecom/rapports-publications/rapports-financiers/647526',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:AKT': {
        'name': 'Akdital',
        'urls': [
            'https://akdital.ma/fr/communiques-de-presse/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:MAN': {
        'name': 'Managem',
        'urls': [
            'https://www.managemgroup.com/medias/communiques-et-publications',
            'https://www.managemgroup.com/investisseurs/managem/rapports-annuels',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:TGCC': {
        'name': 'TGCC',
        'urls': [
            'https://www.tgcc.ma/informations-financieres/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:DOU': {
        'name': 'Douja Prom Addoha',
        'urls': [
            'https://ir.groupeaddoha.com/publication?societe=ADDOHA',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:AFI': {
        'name': 'Afric Industries',
        'urls': [
            'https://www.africindustries.com/communication-financiere/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:AFR': {
        'name': 'Afriquia Gaz',
        'urls': [
            'https://www.afriquiagaz.com/index.php/communiques-de-presse',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:ADI': {
        'name': 'Alliances',
        'urls': [
            'https://www.alliances.co.ma/publications',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:ALM': {
        'name': 'Aluminium Du Maroc',
        'urls': [
            'https://aluminiumdumaroc.com/finance/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:ARD': {
        'name': 'Aradei Capital',
        'urls': [
            'https://www.aradeicapital.com/investisseurs/communication-financiere/communiques-de-presse/',
            'https://www.aradeicapital.com/investisseurs/communication-financiere/resultats-trimestriels/',
            'https://www.aradeicapital.com/investisseurs/communication-financiere/resultats-semestriels/',
            'https://www.aradeicapital.com/investisseurs/communication-financiere/resultats-annuels/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:ATL': {
        'name': 'AtlantaSanad',
        'urls': [
            'https://www.atlantasanad.ma/apropos-atlantasanad/publications',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:AUT': {
        'name': 'Auto Hall',
        'urls': [
            'https://www.autohall.ma/fr/investisseur',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:BMCI': {
        'name': 'BMCI',
        'urls': [
            'https://www.bmci.ma/nous-connaitre/le-groupe-bmci/communication-financiere/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:CAR': {
        'name': 'Cartier Saada',
        'urls': [
            'https://m.saadacorporate.com/index.php/fr/publications-financieres',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:CFG': {
        'name': 'CFG Bank',
        'urls': [
            'https://www.cfgbank.com/particuliers/cfg-bank-et-moi/communication-financiere/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:CIM': {
        'name': 'Ciments du Maroc',
        'urls': [
            'https://www.cimentsdumaroc.com/fr/communiques-financiers',
            'https://www.cimentsdumaroc.com/fr/rapports-financiers-annuels',
            'https://www.cimentsdumaroc.com/fr/rapports-financiers-semestriels',
            'https://www.cimentsdumaroc.com/fr/assemblees-generales',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:MIN': {
        'name': 'Compagnie Minière de Touissit (CMT)',
        'urls': [
            'https://www.cmt.ma/etats-financiers/',
            'https://www.cmt.ma/rapports-annuels/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:COL': {
        'name': 'Colorado',
        'urls': [
            'https://www.colorado.ma/corporate/fr/communiques-financiers',
            'https://www.colorado.ma/corporate/fr/etats-financiers',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:COS': {
        'name': 'Cosumar',
        'urls': [
            'https://www.cosumar.co.ma/publications/',
            'https://www.cosumar.co.ma/publications/?t=Communiqué+de+presse',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:CDM': {
        'name': 'Crédit du Maroc',
        'urls': [
            'https://www.creditdumaroc.ma/institutionnel/publications-financieres',
            'https://www.creditdumaroc.ma/institutionnel/rapports-annuels',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:EQD': {
        'name': 'Eqdom',
        'urls': [
            'https://institutionnel.eqdom.ma',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:CTM': {
        'name': 'CTM',
        'urls': [
            'https://ctm.ma/publications/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:DEL': {
        'name': 'Delta Holding',
        'urls': [
            'https://www.deltaholding.ma/communiques/',
            'https://www.deltaholding.ma/etats-financers/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:DIS': {
        'name': 'Disty Technologies',
        'urls': [
            'https://www.distytechnologies.com/information-financiere',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:ENN': {
        'name': 'Ennakl',
        'urls': [
            'https://www.ennakl.com/publication',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:FEN': {
        'name': 'Fenie Brossette',
        'urls': [
            'https://www.feniebrossette.ma/etats-financiers/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:HPS': {
        'name': 'HPS',
        'urls': [
            'https://www.hps-worldwide.com/investor-relations/press-releases',
            'https://www.hps-worldwide.com/investor-relations/annual-reports',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:IMO': {
        'name': 'Immorente Invest',
        'urls': [
            'https://immorente.ma/relations-investisseurs/communication_financiere/',
            'https://immorente.ma/relations-investisseurs/assemblee-generale/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:INV': {
        'name': 'Involys',
        'urls': [
            'https://involys.com/communication-financiere/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:JET': {
        'name': 'Jet Contractors',
        'urls': [
            'https://www.jet-contractors.com/communique-de-presse/',
            'https://www.jet-contractors.com/resultats-etat-de-synthese-2025/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:LAB': {
        'name': 'Label Vie',
        'urls': [
            'https://labelvie.ma/finance/communiques-financiers/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:LAF': {
        'name': 'LafargeHolcim Maroc',
        'urls': [
            'https://www.lafargeholcim.ma/fr/CP-Investisseurs',
            'https://www.lafargeholcim.ma/fr/comptes-et-resultats-lhm',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:LES': {
        'name': 'Lesieur Cristal',
        'urls': [
            'https://lesieur-cristal.com/communication_financiere/rapports-financiers/',
            'https://lesieur-cristal.com/communication_financiere/etats-financiers/',
            'https://lesieur-cristal.com/communication_financiere/documentation-assemblee-generale/',
            'https://lesieur-cristal.com/communication_financiere/communiques-de-presse/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:M2M': {
        'name': 'M2M Group',
        'urls': [
            'https://m2mgroup.com/fr/e-paiements/relations-avec-les-investisseurs/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:MOX': {
        'name': 'Maghreb Oxygene',
        'urls': [
            'https://www.maghreboxygene.ma/communiques-de-presse/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:MSA': {
        'name': 'Marsa Maroc',
        'urls': [
            'https://www.marsamaroc.co.ma/fr/publications-financieres',
            'https://www.marsamaroc.co.ma/fr/communique-de-presse',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:MIC': {
        'name': 'Microdata',
        'urls': [
            'https://www.microdata.ma/exercices-financiers',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:MUT': {
        'name': 'Mutandis SCA',
        'urls': [
            'https://mutandis.com/investisseurs/informations-financieres/',
            'https://mutandis.com/investisseurs/informations-financieres/communiques-financiers/',
            'https://mutandis.com/investisseurs/informations-financieres/presentations-investisseurs-analystes/',
            'https://mutandis.com/investisseurs/informations-financieres/rapports-financiers/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:RIS': {
        'name': 'Risma',
        'urls': [
            'https://risma.com/investisseurs/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:SAH': {
        'name': 'Sanlam Maroc',
        'urls': [
            'https://sanlam.ma/fr/communiques-financiers/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:SBM': {
        'name': 'Société des Boissons du Maroc',
        'urls': [
            'https://www.boissons-maroc.com/communication-hp-financiere/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:SNP': {
        'name': 'SNEP',
        'urls': [
            'https://snep.ma/espace-investisseurs/rapports-financiers/',
            'https://snep.ma/espace-investisseurs/communiques-financiers/?jsf=jet-engine&tax=annee:150',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:SID': {
        'name': 'Sonasid',
        'urls': [
            'https://www.sonasid.ma/fr/publications-financieres',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:S2M': {
        'name': 'S2M',
        'urls': [
            'https://s2mworldwide.com/category/documentation-financiere/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:SRM': {
        'name': 'Realis. Mecaniques (SRM)',
        'urls': [
            'https://www.groupe-premium.com/srm/srm/publications-financieres/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:SNA': {
        'name': 'Stokvis Nord Afrique',
        'urls': [
            'https://www.stokvis.ma/investisseurs-3/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:STR': {
        'name': 'Stroc Industrie',
        'urls': [
            'https://www.stroc.com/articles-2/',
            'https://www.stroc.com/articles/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:TQM': {
        'name': 'Taqa Morocco',
        'urls': [
            'https://www.taqamorocco.ma/fr/investisseurs/publications-financieres',
            'https://www.taqamorocco.ma/fr/investisseurs/communiques-et-comptes',
            'https://www.taqamorocco.ma/fr/investisseurs/rapports-financiers-et-presentations',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:TMA': {
        'name': 'TotalEnergies Marketing Maroc',
        'urls': [
            'https://totalenergies.com/fr/actualites/communiques-presse',
            'https://totalenergies.com/fr/investisseurs/resultats',
            'https://totalenergies.com/fr/investisseurs/rapports',
            'https://totalenergies.com/fr/investisseurs/presentations-investisseurs',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:VCN': {
        'name': 'Vicenne',
        'urls': [
            'https://vicenne.com/investisseurs/',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
    'CSEMA:WAA': {
        'name': 'Wafa Assurance',
        'urls': [
            'https://www.wafaassurance.ma/fr/compagnie-assurance-maroc/communication-financiere',
        ],
        'selectors': {
            'pdf_links': 'a[href$=".pdf"]',
            'title': 'a',
        }
    },
}


class FinancialReportsScraper:
    """
    Service pour scraper automatiquement les rapports financiers
    depuis les sites officiels des entreprises
    """
    
    def __init__(self):
        """Initialiser le scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialiser Supabase client pour upload
        self.supabase_client = self._init_supabase()
        
        logger.info("✅ FinancialReportsScraper initialisé")
    
    def _init_supabase(self) -> Optional[Client]:
        """Initialiser le client Supabase"""
        try:
            supabase_url = settings.supabase_url or os.getenv("SUPABASE_URL")
            supabase_key = (
                settings.supabase_service_key or 
                os.getenv("SUPABASE_SERVICE_KEY") or
                settings.supabase_anon_key or 
                os.getenv("SUPABASE_ANON_KEY")
            )
            
            if not supabase_url or not supabase_key:
                logger.warning("⚠️  Supabase non configuré - upload désactivé")
                return None
            
            client = create_client(supabase_url, supabase_key)
            logger.info("✅ Client Supabase initialisé pour upload")
            return client
        except Exception as e:
            logger.error(f"❌ Erreur initialisation Supabase: {e}")
            return None
    
    def scrape_company_reports(
        self, 
        company_symbol: str,
        max_reports: int = 50
    ) -> List[Dict]:
        """
        Scraper les rapports financiers d'une entreprise
        
        Args:
            company_symbol: Symbole de l'entreprise (ex: CSEMA:ATW)
            max_reports: Nombre maximum de rapports à scraper
        
        Returns:
            Liste des rapports trouvés avec métadonnées
        """
        company_config = COMPANY_REPORTS_CONFIG.get(company_symbol)
        if not company_config:
            logger.warning(f"⚠️  Configuration non trouvée pour {company_symbol}")
            return []
        
        all_reports = []
        
        logger.info(f"🔍 Scraping des rapports pour {company_config['name']} ({company_symbol})")
        
        for url in company_config['urls']:
            try:
                logger.debug(f"   Scraping: {url}")
                reports = self._scrape_url(
                    url=url,
                    company_symbol=company_symbol,
                    company_name=company_config['name'],
                    selectors=company_config.get('selectors', {}),
                    max_reports=max_reports
                )
                all_reports.extend(reports)
                
                # Délai entre les requêtes
                import time
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Erreur scraping {url}: {e}")
                continue
        
        # Dédupliquer par URL
        unique_reports = {}
        for report in all_reports:
            url = report.get('file_url')
            if url and url not in unique_reports:
                unique_reports[url] = report
        
        logger.info(f"✅ {len(unique_reports)} rapports uniques trouvés pour {company_config['name']}")
        return list(unique_reports.values())
    
    def _scrape_url(
        self,
        url: str,
        company_symbol: str,
        company_name: str,
        selectors: Dict,
        max_reports: int = 50
    ) -> List[Dict]:
        """Scraper une URL spécifique"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les liens PDF
            pdf_selector = selectors.get('pdf_links', 'a[href$=".pdf"]')
            pdf_links = soup.select(pdf_selector)
            
            reports = []
            for link in pdf_links[:max_reports]:
                try:
                    pdf_href = link.get('href', '')
                    if not pdf_href:
                        continue
                    
                    # Construire l'URL complète
                    pdf_url = urljoin(url, pdf_href)
                    
                    # Pour Attijariwafa Bank, les liens /static-files/ sont des PDFs même sans extension
                    if 'attijariwafabank.com' in url and '/static-files/' in pdf_url and not pdf_url.lower().endswith('.pdf'):
                        # Vérifier si c'est vraiment un PDF en testant le Content-Type
                        try:
                            head_response = self.session.head(pdf_url, timeout=10, allow_redirects=True)
                            content_type = head_response.headers.get('Content-Type', '').lower()
                            if 'pdf' not in content_type:
                                # Si ce n'est pas un PDF, passer au suivant
                                continue
                        except:
                            # Si on ne peut pas vérifier, assumer que c'est un PDF
                            pass
                    
                    # Extraire le titre - chercher dans le parent et les éléments proches
                    title = link.get_text(strip=True) or link.get('title', '')
                    
                    # Si le titre est vide ou trop court, chercher dans le parent
                    if not title or len(title) < 5 or title.lower() in ['télécharger', 'download', 'voir', 'voir le document']:
                        # Chercher dans le parent
                        parent = link.find_parent(['div', 'li', 'article', 'p', 'h3', 'h4', 'h5'])
                        if parent:
                            # Prendre le texte du parent mais exclure le texte du lien lui-même
                            parent_text = parent.get_text(strip=True)
                            link_text = link.get_text(strip=True)
                            if parent_text and parent_text != link_text:
                                # Extraire le texte avant le lien
                                title = parent_text.replace(link_text, '').strip()
                        
                        # Si toujours vide, chercher dans les éléments précédents
                        if not title or len(title) < 5:
                            prev_sibling = link.find_previous_sibling(['div', 'p', 'h3', 'h4', 'h5', 'span'])
                            if prev_sibling:
                                title = prev_sibling.get_text(strip=True)
                        
                        # Si toujours vide, utiliser le nom de fichier depuis l'URL
                        if not title or len(title) < 5:
                            file_name_from_url = pdf_url.split('/')[-1]
                            # Nettoyer le nom de fichier pour en faire un titre
                            title = file_name_from_url.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()
                    
                    # Nettoyer le titre
                    title = title.strip()
                    if not title:
                        title = pdf_url.split('/')[-1].replace('.pdf', '').replace('_', ' ').title()
                    
                    # Analyser le titre pour déterminer le type et les dates
                    report_info = self._analyze_report(title, pdf_url)
                    
                    # Extraire le nom de fichier complet depuis l'URL
                    file_name_full = pdf_url.split('/')[-1]
                    # Décoder les URLs encodées
                    if '%' in file_name_full:
                        from urllib.parse import unquote
                        file_name_full = unquote(file_name_full)
                    
                    report = {
                        'company_symbol': company_symbol,
                        'company_name': company_name,
                        'report_type': report_info['type'],
                        'title': title,
                        'description': f"Rapport financier officiel de {company_name} - {title}",
                        'file_url': pdf_url,  # URL externe temporaire
                        'file_name': file_name_full,  # Nom de fichier complet préservé
                        'file_size': None,  # Sera rempli après téléchargement
                        'file_type': 'application/pdf',
                        'published_at': report_info.get('published_at'),
                        'period_start': report_info.get('period_start'),
                        'period_end': report_info.get('period_end'),
                        'tags': report_info.get('tags', []),
                        'featured': report_info.get('featured', False),
                    }
                    
                    reports.append(report)
                    
                except Exception as e:
                    logger.debug(f"   Erreur traitement lien: {e}")
                    continue
            
            return reports
            
        except Exception as e:
            logger.error(f"❌ Erreur scraping {url}: {e}")
            return []
    
    def _analyze_report(self, title: str, url: str) -> Dict:
        """
        Analyser le titre et l'URL pour extraire les métadonnées
        
        Returns:
            Dict avec type, dates, tags, etc.
        """
        title_lower = title.lower()
        url_lower = url.lower()
        
        # Déterminer le type de rapport
        report_type = 'autre'
        if any(word in title_lower for word in ['annuel', 'annual', 'ra']):
            report_type = 'rapport-annuel'
        elif any(word in title_lower for word in ['trimestriel', 'quarterly', 't1', 't2', 't3', 't4', 'q1', 'q2', 'q3', 'q4']):
            report_type = 'rapport-trimestriel'
        elif any(word in title_lower for word in ['semestriel', 'semiannual', 's1', 's2']):
            report_type = 'rapport-semestriel'
        elif any(word in title_lower for word in ['resultat', 'result', 'résultat']):
            report_type = 'resultats'
        elif any(word in title_lower for word in ['communique', 'communiqué', 'communique']):
            report_type = 'communique'
        elif 'profit' in title_lower and 'warning' in title_lower:
            report_type = 'profit-warning'
        
        # Extraire l'année
        year_match = re.search(r'20\d{2}', title + ' ' + url)
        year = year_match.group() if year_match else None
        
        # Extraire les dates
        published_at = None
        period_start = None
        period_end = None
        
        if year:
            try:
                # Essayer d'extraire une date complète
                date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', title + ' ' + url)
                if date_match:
                    day, month, year_str = date_match.groups()
                    published_at = datetime(int(year_str), int(month), int(day)).isoformat()
                else:
                    # Sinon, utiliser le 1er janvier de l'année trouvée
                    published_at = datetime(int(year), 1, 1).isoformat()
                
                # Pour les rapports annuels, période = année complète
                if report_type == 'rapport-annuel':
                    period_start = f"{year}-01-01"
                    period_end = f"{year}-12-31"
                    
            except Exception as e:
                logger.debug(f"   Erreur extraction date: {e}")
        
        # Générer les tags
        tags = ['officiel', 'scraped', report_type]
        if year:
            tags.append(year)
        if 'annuel' in title_lower:
            tags.append('annuel')
        
        # Mettre en avant les rapports annuels récents
        featured = report_type == 'rapport-annuel' and year and int(year) >= 2023
        
        return {
            'type': report_type,
            'published_at': published_at,
            'period_start': period_start,
            'period_end': period_end,
            'tags': tags,
            'featured': featured,
        }
    
    async def download_and_upload(
        self,
        report: Dict,
        company_symbol: str
    ) -> Optional[str]:
        """
        Télécharger un PDF et l'uploader vers Supabase Storage
        
        Args:
            report: Dictionnaire avec les métadonnées du rapport
            company_symbol: Symbole de l'entreprise
        
        Returns:
            URL publique du fichier uploadé, ou None en cas d'erreur
        """
        if not self.supabase_client:
            logger.warning("⚠️  Supabase non configuré - retour URL externe")
            return report.get('file_url')
        
        pdf_url = report.get('file_url')
        if not pdf_url:
            return None
        
        try:
            # Télécharger le PDF
            logger.debug(f"   Téléchargement: {pdf_url}")
            response = self.session.get(pdf_url, timeout=60, stream=True)
            response.raise_for_status()
            
            # Lire le contenu
            pdf_content = response.content
            file_size = len(pdf_content)
            
            if file_size > 50 * 1024 * 1024:  # 50MB max
                logger.warning(f"   Fichier trop volumineux ({file_size} bytes): {pdf_url}")
                return report.get('file_url')  # Retourner l'URL externe
            
            # Préserver le nom de fichier original complet
            original_file_name = report.get('file_name', pdf_url.split('/')[-1])
            # Décoder les URLs encodées
            if '%' in original_file_name:
                from urllib.parse import unquote
                original_file_name = unquote(original_file_name)
            
            # Nettoyer uniquement les caractères problématiques pour le stockage
            # Mais garder le nom lisible
            safe_file_name = re.sub(r'[<>:"|?*]', '_', original_file_name)
            file_ext = safe_file_name.split('.')[-1] if '.' in safe_file_name else 'pdf'
            
            # Créer un nom unique mais préserver le nom original dans le nom de fichier
            # Format: SYMBOL_YYYYMMDD_original-filename.pdf
            date_prefix = datetime.now().strftime('%Y%m%d')
            unique_name = f"{company_symbol.replace(':', '_')}_{date_prefix}_{safe_file_name}"
            # Limiter la longueur totale
            if len(unique_name) > 200:
                name_part = safe_file_name[:150]
                unique_name = f"{company_symbol.replace(':', '_')}_{date_prefix}_{name_part}.{file_ext}"
            
            file_path = f"financial-reports/{company_symbol.replace(':', '_')}/{unique_name}"
            
            # Upload vers Supabase Storage
            logger.debug(f"   Upload vers Supabase: {file_path}")
            result = self.supabase_client.storage.from_('documents').upload(
                file_path,
                pdf_content,
                file_options={"content-type": "application/pdf"}
            )
            
            if result:
                # Obtenir l'URL publique
                public_url_result = self.supabase_client.storage.from_('documents').get_public_url(file_path)
                public_url = public_url_result if isinstance(public_url_result, str) else public_url_result.get('publicUrl', '')
                
                logger.info(f"   ✅ Upload réussi: {file_name} ({file_size / 1024 / 1024:.2f} MB)")
                return public_url
            else:
                logger.warning(f"   ⚠️  Upload échoué, utilisation URL externe")
                return report.get('file_url')
                
        except Exception as e:
            logger.error(f"   ❌ Erreur téléchargement/upload {pdf_url}: {e}")
            # En cas d'erreur, retourner l'URL externe
            return report.get('file_url')
    
    async def save_report_to_supabase(
        self,
        report: Dict,
        uploaded_url: str
    ) -> bool:
        """
        Sauvegarder les métadonnées du rapport dans Supabase
        
        Args:
            report: Métadonnées du rapport
            uploaded_url: URL du fichier uploadé
        
        Returns:
            True si succès, False sinon
        """
        if not self.supabase_client:
            return False
        
        try:
            # Préparer les données - préserver le nom de fichier original complet
            original_file_name = report.get('file_name', '')
            if '%' in original_file_name:
                from urllib.parse import unquote
                original_file_name = unquote(original_file_name)
            
            report_data = {
                'company_symbol': report['company_symbol'],
                'company_name': report['company_name'],
                'report_type': report['report_type'],
                'title': report['title'],
                'description': report.get('description'),
                'file_url': uploaded_url,
                'file_name': original_file_name,  # Nom de fichier complet préservé
                'file_size': report.get('file_size'),
                'file_type': report.get('file_type', 'application/pdf'),
                'published_at': report.get('published_at'),
                'period_start': report.get('period_start'),
                'period_end': report.get('period_end'),
                'tags': report.get('tags', []),
                'featured': report.get('featured', False),
            }
            
            # Vérifier si le rapport existe déjà (par URL)
            existing = self.supabase_client.table('financial_reports').select('id').eq(
                'file_url', uploaded_url
            ).execute()
            
            if existing.data:
                # Mettre à jour
                report_id = existing.data[0]['id']
                result = self.supabase_client.table('financial_reports').update(
                    report_data
                ).eq('id', report_id).execute()
                logger.debug(f"   ✅ Rapport mis à jour: {report['title'][:50]}")
            else:
                # Insérer
                result = self.supabase_client.table('financial_reports').insert(
                    report_data
                ).execute()
                logger.debug(f"   ✅ Rapport ajouté: {report['title'][:50]}")
            
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Erreur sauvegarde Supabase: {e}")
            return False
    
    async def scrape_and_save_company(
        self,
        company_symbol: str,
        download_pdfs: bool = True,
        max_reports: int = 50
    ) -> Dict:
        """
        Scraper, télécharger et sauvegarder les rapports d'une entreprise
        
        Args:
            company_symbol: Symbole de l'entreprise
            download_pdfs: Si True, télécharge et upload les PDFs
            max_reports: Nombre maximum de rapports
        
        Returns:
            Statistiques du scraping
        """
        stats = {
            'company_symbol': company_symbol,
            'scraped': 0,
            'downloaded': 0,
            'saved': 0,
            'errors': []
        }
        
        try:
            # Scraper les rapports
            reports = self.scrape_company_reports(company_symbol, max_reports)
            stats['scraped'] = len(reports)
            
            logger.info(f"📊 {len(reports)} rapports trouvés pour {company_symbol}")
            
            # Traiter chaque rapport
            for report in reports:
                try:
                    uploaded_url = report.get('file_url')
                    
                    # Télécharger et uploader si demandé
                    if download_pdfs:
                        uploaded_url = await self.download_and_upload(report, company_symbol)
                        if uploaded_url and uploaded_url != report.get('file_url'):
                            stats['downloaded'] += 1
                            report['file_url'] = uploaded_url
                    
                    # Sauvegarder dans Supabase
                    if await self.save_report_to_supabase(report, uploaded_url):
                        stats['saved'] += 1
                    else:
                        stats['errors'].append(f"Erreur sauvegarde: {report.get('title', 'Unknown')}")
                    
                    # Délai entre les rapports
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    error_msg = f"Erreur traitement rapport {report.get('title', 'Unknown')}: {e}"
                    logger.error(f"   ❌ {error_msg}")
                    stats['errors'].append(error_msg)
                    continue
            
            logger.info(f"✅ {company_symbol}: {stats['saved']}/{stats['scraped']} rapports sauvegardés")
            
        except Exception as e:
            logger.error(f"❌ Erreur scraping {company_symbol}: {e}")
            stats['errors'].append(str(e))
        
        return stats
    
    async def scrape_all_companies(
        self,
        company_symbols: Optional[List[str]] = None,
        download_pdfs: bool = True,
        max_reports_per_company: int = 50
    ) -> Dict:
        """
        Scraper les rapports de toutes les entreprises (ou une liste spécifique)
        
        Args:
            company_symbols: Liste des symboles à scraper (None = toutes)
            download_pdfs: Si True, télécharge et upload les PDFs
            max_reports_per_company: Nombre max de rapports par entreprise
        
        Returns:
            Statistiques globales
        """
        if company_symbols is None:
            company_symbols = list(COMPANY_REPORTS_CONFIG.keys())
        
        logger.info(f"🚀 Démarrage du scraping pour {len(company_symbols)} entreprises")
        
        all_stats = {
            'total_companies': len(company_symbols),
            'companies': {},
            'total_scraped': 0,
            'total_downloaded': 0,
            'total_saved': 0,
            'total_errors': 0
        }
        
        for company_symbol in company_symbols:
            try:
                stats = await self.scrape_and_save_company(
                    company_symbol=company_symbol,
                    download_pdfs=download_pdfs,
                    max_reports=max_reports_per_company
                )
                
                all_stats['companies'][company_symbol] = stats
                all_stats['total_scraped'] += stats['scraped']
                all_stats['total_downloaded'] += stats['downloaded']
                all_stats['total_saved'] += stats['saved']
                all_stats['total_errors'] += len(stats['errors'])
                
                # Délai entre les entreprises
                await asyncio.sleep(3)
                
            except Exception as e:
                logger.error(f"❌ Erreur entreprise {company_symbol}: {e}")
                all_stats['companies'][company_symbol] = {
                    'error': str(e),
                    'scraped': 0,
                    'saved': 0
                }
                continue
        
        logger.info(f"✅ Scraping terminé: {all_stats['total_saved']} rapports sauvegardés")
        return all_stats

