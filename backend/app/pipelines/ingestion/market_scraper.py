from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Any, Optional
import json
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

from app.core.logging import get_logger


logger = get_logger(__name__)


@dataclass(slots=True)
class MarketSnapshot:
    symbol: str
    last_price: float
    change_percent: float
    volume: int
    as_of: datetime


@dataclass(slots=True)
class MASIHistoricalData:
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int


class CasablancaMarketScraper:
    MARKET_URL = "https://www.casablanca-bourse.com/fr/live-market/indices/MASI"
    HISTORICAL_URL = "https://www.casablanca-bourse.com/fr/indices/MASI/historique"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        # Désactiver la vérification SSL pour le développement
        # En production, utilisez des certificats valides
        self.session.verify = False
        # Supprimer les warnings SSL uniquement en développement
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_live_data(self) -> list[MarketSnapshot]:
        """Fetch current market data"""
        logger.info("Fetching MASI live market data", extra={"url": self.MARKET_URL})
        try:
            response = self.session.get(self.MARKET_URL, timeout=30)
            response.raise_for_status()
            return self._parse_live_data(response.text)
        except Exception as e:
            logger.error(f"Error fetching live data: {e}")
            return self._get_fallback_data()

    def fetch_historical_data(self, days: int = 30) -> list[MASIHistoricalData]:
        """Fetch historical MASI data"""
        logger.info(f"Fetching MASI historical data for {days} days")
        try:
            # For now, generate synthetic historical data
            # In production, this would scrape the historical page
            return self._generate_synthetic_historical_data(days)
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return []

    def _parse_live_data(self, html: str) -> list[MarketSnapshot]:
        """Parse live market data from HTML - VERSION AMÉLIORÉE"""
        soup = BeautifulSoup(html, "html.parser")
        
        # Méthode 1: Parser les tables avec classes spécifiques Casablanca Bourse
        tables = soup.find_all("table", class_=["w-full", "max-w-screen", "border", "border-gray-600"])
        
        if not tables:
            logger.warning("No market tables found with specific classes")
            return self._get_fallback_data()
        
        results: list[MarketSnapshot] = []
        now = datetime.utcnow()
        
        # Parser chaque table trouvée
        for table_idx, table in enumerate(tables):
            logger.info(f"Parsing table #{table_idx}")
            
            # Trouver les headers pour comprendre la structure
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            logger.info(f"Table headers: {headers}")
            
            # Trouver toutes les lignes (skip header row)
            rows = table.find_all("tr")[1:]  # Skip first row (headers)
            
            for row_idx, row in enumerate(rows):
                columns = [col.get_text(strip=True) for col in row.find_all("td")]
                
                if len(columns) < 3:
                    continue
                
                try:
                    # Table 1: Données de l'indice MASI (Valeur, Veille, Variation%)
                    # Table 2: Données des instruments (Instrument, Cours, Cours Veille, Variation, Volume, Quantité)
                    
                    if 'Instrument' in headers:
                        # Table des instruments individuels
                        symbol = columns[0]  # Instrument
                        last_price_str = columns[1].replace(" ", "").replace(",", ".")  # Cours (MAD)
                        change_str = columns[3].replace("%", "").replace(",", ".")  # Variation
                        volume_str = columns[4].replace(" ", "")  # Volume
                        
                        # Parser les valeurs
                        last_price = float(last_price_str) if last_price_str else 0.0
                        change_percent = float(change_str) if change_str and change_str != '-' else 0.0
                        
                        # Parser le volume (format: "66 750,10" ou "-")
                        if volume_str and volume_str != '-':
                            volume = self._parse_float_volume(volume_str)
                        else:
                            volume = 0
                        
                        if symbol and last_price > 0:
                            results.append(
                                MarketSnapshot(
                                    symbol=symbol,
                                    last_price=last_price,
                                    change_percent=change_percent,
                                    volume=volume,
                                    as_of=now,
                                )
                            )
                            logger.debug(f"Parsed: {symbol} = {last_price} MAD ({change_percent:+.2f}%)")
                    
                    elif 'Valeur' in headers:
                        # Table de l'indice MASI principal
                        if len(columns) >= 3:
                            valeur = columns[0].replace(" ", "").replace(",", ".")
                            variation = columns[2].replace("%", "").replace(",", ".")
                            
                            if valeur:
                                last_price = float(valeur) if valeur else 0.0
                                change_percent = float(variation) if variation else 0.0
                                
                                if last_price > 0:
                                    results.append(
                                        MarketSnapshot(
                                            symbol="MASI",
                                            last_price=last_price,
                                            change_percent=change_percent,
                                            volume=0,
                                            as_of=now,
                                        )
                                    )
                                    logger.info(f"Parsed MASI Index: {last_price} MAD ({change_percent:+.2f}%)")
                
                except (ValueError, IndexError) as e:
                    logger.warning(f"Skipping row {row_idx} due to parsing error: {e}", extra={"row": columns})
                    continue
        
        if results:
            logger.info(f"✅ Successfully parsed {len(results)} real market records from Casablanca Bourse")
            return results
        else:
            logger.warning("No data could be parsed, using fallback")
            return self._get_fallback_data()

    def _extract_masi_data(self, soup: BeautifulSoup) -> Optional[MarketSnapshot]:
        """Extract MASI specific data"""
        # Look for MASI index specifically
        masi_elements = soup.find_all(text=lambda text: text and "MASI" in text.upper())
        if not masi_elements:
            return None
            
        # Try to find price and change data near MASI text
        for element in masi_elements:
            parent = element.parent
            if parent:
                # Look for price and change in nearby elements
                price_text = parent.find_next(text=lambda t: t and any(char.isdigit() for char in t))
                if price_text:
                    try:
                        price = float(price_text.strip().replace(",", "."))
                        return MarketSnapshot(
                            symbol="MASI",
                            last_price=price,
                            change_percent=0.0,  # Would need to extract from page
                            volume=0,
                            as_of=datetime.utcnow()
                        )
                    except ValueError:
                        continue
        return None

    def _get_fallback_data(self) -> list[MarketSnapshot]:
        """Generate fallback data when scraping fails"""
        logger.info("Using fallback market data")
        return [
            MarketSnapshot(
                symbol="MASI",
                last_price=12500.0 + (datetime.now().hour % 10) * 50,  # Simulate some variation
                change_percent=0.5,
                volume=1000000,
                as_of=datetime.utcnow()
            )
        ]

    def _generate_synthetic_historical_data(self, days: int) -> list[MASIHistoricalData]:
        """Generate synthetic historical data for development"""
        logger.info(f"Generating {days} days of synthetic MASI data")
        
        data = []
        base_price = 12000.0
        
        for i in range(days):
            current_date = date.today() - pd.Timedelta(days=i)
            
            # Generate realistic price movement
            daily_change = (hash(str(current_date)) % 200 - 100) / 100.0  # -1% to +1%
            price = base_price * (1 + daily_change)
            
            # Generate OHLC data
            open_price = price * (1 + (hash(str(current_date) + "open") % 20 - 10) / 1000)
            high_price = max(open_price, price) * (1 + abs(hash(str(current_date) + "high") % 50) / 10000)
            low_price = min(open_price, price) * (1 - abs(hash(str(current_date) + "low") % 30) / 10000)
            close_price = price
            
            volume = 800000 + (hash(str(current_date)) % 400000)
            
            data.append(MASIHistoricalData(
                date=current_date,
                open_price=round(open_price, 2),
                high_price=round(high_price, 2),
                low_price=round(low_price, 2),
                close_price=round(close_price, 2),
                volume=volume
            ))
            
            base_price = close_price  # Next day starts from previous close
        
        return sorted(data, key=lambda x: x.date)

    @staticmethod
    def _parse_int(value: str) -> int:
        """Parse integer from string, handling various formats"""
        if not value:
            return 0
        cleaned = value.replace(" ", "").replace(",", "").replace(".", "")
        try:
            return int(cleaned)
        except ValueError:
            return 0
    
    @staticmethod
    def _parse_float_volume(value: str) -> int:
        """Parse volume in float format (e.g., '66 750,10') to integer"""
        if not value or value == '-':
            return 0
        try:
            # Remove spaces and replace comma with dot
            cleaned = value.replace(" ", "").replace(",", ".")
            # Convert to float then to int
            return int(float(cleaned))
        except ValueError:
            return 0


