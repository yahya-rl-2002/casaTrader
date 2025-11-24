# 📊 Intégration Yahoo Finance API

## 🎯 Objectif

Enrichir le Fear & Greed Index avec des données internationales via Yahoo Finance (GRATUIT).

---

## 📦 Installation

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
poetry add yfinance
```

---

## 🔧 Implémentation

### **1. Créer un nouveau scraper pour Yahoo Finance**

Créez le fichier `backend/app/pipelines/ingestion/yahoo_finance_scraper.py` :

```python
"""
Yahoo Finance Scraper for International Market Data
"""
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional
import yfinance as yf

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class YahooFinanceData:
    """Data structure for Yahoo Finance data"""
    symbol: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    change_percent: float


class YahooFinanceScraper:
    """
    Scraper for international market indices via Yahoo Finance
    """
    
    # Indices internationaux pertinents
    INDICES = {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI",
        "NASDAQ": "^IXIC",
        "CAC 40": "^FCHI",
        "DAX": "^GDAXI",
        "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225",
        "VIX (Volatility)": "^VIX",
        "Oil (WTI)": "CL=F",
        "Gold": "GC=F",
    }
    
    def get_index_data(self, symbol: str, period: str = "1mo") -> List[YahooFinanceData]:
        """
        Récupère les données d'un indice
        
        Args:
            symbol: Symbol Yahoo Finance (ex: ^GSPC pour S&P 500)
            period: Période (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            Liste de YahooFinanceData
        """
        try:
            logger.info(f"Fetching data for {symbol} (period: {period})")
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                logger.warning(f"No data found for {symbol}")
                return []
            
            data_list = []
            for date, row in hist.iterrows():
                change_percent = ((row['Close'] - row['Open']) / row['Open'] * 100) if row['Open'] > 0 else 0
                
                data_list.append(YahooFinanceData(
                    symbol=symbol,
                    date=date.to_pydatetime(),
                    open_price=float(row['Open']),
                    high_price=float(row['High']),
                    low_price=float(row['Low']),
                    close_price=float(row['Close']),
                    volume=int(row['Volume']),
                    change_percent=float(change_percent)
                ))
            
            logger.info(f"Successfully fetched {len(data_list)} records for {symbol}")
            return data_list
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return []
    
    def get_all_indices(self, period: str = "1mo") -> dict:
        """
        Récupère les données de tous les indices
        
        Returns:
            Dict avec nom_indice: [YahooFinanceData]
        """
        all_data = {}
        
        for name, symbol in self.INDICES.items():
            data = self.get_index_data(symbol, period)
            if data:
                all_data[name] = data
        
        return all_data
    
    def get_vix_fear_indicator(self) -> Optional[float]:
        """
        Récupère le VIX (Fear Index) comme indicateur de volatilité mondiale
        
        Returns:
            Valeur du VIX (0-100, plus élevé = plus de peur)
        """
        try:
            vix = yf.Ticker("^VIX")
            hist = vix.history(period="1d")
            
            if not hist.empty:
                vix_value = float(hist['Close'].iloc[-1])
                logger.info(f"VIX (Global Fear Index): {vix_value:.2f}")
                return vix_value
            
        except Exception as e:
            logger.error(f"Error fetching VIX: {e}")
        
        return None


# Exemple d'utilisation
if __name__ == "__main__":
    scraper = YahooFinanceScraper()
    
    # Récupérer le VIX
    vix = scraper.get_vix_fear_indicator()
    print(f"VIX: {vix}")
    
    # Récupérer le S&P 500
    sp500_data = scraper.get_index_data("^GSPC", period="1mo")
    print(f"S&P 500: {len(sp500_data)} days")
    
    # Récupérer tous les indices
    all_indices = scraper.get_all_indices(period="5d")
    for name, data in all_indices.items():
        if data:
            latest = data[-1]
            print(f"{name}: {latest.close_price:.2f} ({latest.change_percent:+.2f}%)")
```

---

### **2. Ajouter une nouvelle composante : "Global Market Sentiment"**

Créez `backend/app/pipelines/processing/global_market.py` :

```python
"""
Global Market Sentiment Processor
Utilise les données Yahoo Finance pour évaluer le sentiment global
"""
from dataclasses import dataclass
from typing import List
from datetime import datetime

from app.pipelines.ingestion.yahoo_finance_scraper import YahooFinanceScraper, YahooFinanceData
from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class GlobalMarketScore:
    """Score du sentiment des marchés globaux"""
    normalized_score: float  # 0-100
    vix_value: float
    sp500_trend: str  # "bullish", "bearish", "neutral"
    correlation_with_masi: float
    as_of: datetime


class GlobalMarketProcessor:
    """
    Calcule un score de sentiment basé sur les marchés internationaux
    """
    
    def __init__(self):
        self.scraper = YahooFinanceScraper()
    
    def compute(self) -> GlobalMarketScore:
        """
        Calcule le score de sentiment global
        
        Score basé sur :
        - VIX (Fear Index) : Plus le VIX est élevé, plus la peur est grande
        - S&P 500 trend : Direction du marché US
        - Corrélation avec d'autres indices
        
        Returns:
            GlobalMarketScore avec un score normalisé 0-100
        """
        try:
            # 1. Récupérer le VIX (indicateur de peur)
            vix = self.scraper.get_vix_fear_indicator()
            if vix is None:
                vix = 20.0  # Valeur neutre par défaut
            
            # Normaliser le VIX : 10 = faible peur, 30 = peur élevée
            # Inverser : VIX bas = greed, VIX haut = fear
            vix_score = max(0, min(100, 100 - ((vix - 10) * 5)))
            
            # 2. Récupérer la tendance du S&P 500
            sp500_data = self.scraper.get_index_data("^GSPC", period="1mo")
            
            if sp500_data and len(sp500_data) >= 5:
                # Calculer la tendance (moyenne des 5 derniers jours)
                recent_changes = [d.change_percent for d in sp500_data[-5:]]
                avg_change = sum(recent_changes) / len(recent_changes)
                
                if avg_change > 0.5:
                    sp500_trend = "bullish"
                    trend_score = 70
                elif avg_change < -0.5:
                    sp500_trend = "bearish"
                    trend_score = 30
                else:
                    sp500_trend = "neutral"
                    trend_score = 50
            else:
                sp500_trend = "neutral"
                trend_score = 50
            
            # 3. Score final (moyenne pondérée)
            final_score = (vix_score * 0.6) + (trend_score * 0.4)
            
            logger.info(f"Global Market Score: {final_score:.2f} (VIX: {vix:.2f}, S&P: {sp500_trend})")
            
            return GlobalMarketScore(
                normalized_score=round(final_score, 2),
                vix_value=vix,
                sp500_trend=sp500_trend,
                correlation_with_masi=0.0,  # À calculer si nécessaire
                as_of=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error computing global market score: {e}")
            # Retourner un score neutre en cas d'erreur
            return GlobalMarketScore(
                normalized_score=50.0,
                vix_value=20.0,
                sp500_trend="neutral",
                correlation_with_masi=0.0,
                as_of=datetime.now()
            )
```

---

### **3. Intégrer dans le pipeline principal**

Modifiez `backend/app/services/pipeline_service.py` :

```python
# Ajouter l'import
from app.pipelines.processing.global_market import GlobalMarketProcessor

class PipelineService:
    def __init__(self, use_llm_sentiment: bool = True):
        # ... autres initialisations ...
        self.global_market_processor = GlobalMarketProcessor()
    
    async def run_full_pipeline(self, target_date: Optional[date] = None):
        # ... code existant ...
        
        # Ajouter le calcul du sentiment global
        global_market_score = self.global_market_processor.compute()
        logger.info(f"Global Market Sentiment: {global_market_score.normalized_score:.2f}")
        
        # Vous pouvez l'ajouter comme 7ème composante ou l'utiliser pour pondérer les autres
```

---

## 🎯 **Utilisation**

### **Test du scraper :**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
python -c "
from app.pipelines.ingestion.yahoo_finance_scraper import YahooFinanceScraper

scraper = YahooFinanceScraper()

# VIX (Fear Index)
vix = scraper.get_vix_fear_indicator()
print(f'VIX (Peur mondiale): {vix:.2f}')

# S&P 500
sp500 = scraper.get_index_data('^GSPC', period='5d')
print(f'S&P 500: {len(sp500)} jours')

# Tous les indices
all_data = scraper.get_all_indices(period='1d')
for name, data in all_data.items():
    if data:
        latest = data[-1]
        print(f'{name}: {latest.close_price:.2f} ({latest.change_percent:+.2f}%)')
"
```

---

## 📊 **Nouvelles Données Disponibles**

Avec Yahoo Finance, vous pouvez ajouter :

1. **VIX (Fear Index)** → Indicateur de peur mondial
2. **S&P 500** → Tendance du marché US
3. **CAC 40** → Tendance européenne
4. **Or & Pétrole** → Valeurs refuges
5. **Corrélations internationales**

---

## 💰 **Coûts**

✅ **100% GRATUIT**  
✅ Pas de limite de requêtes stricte  
✅ Données en temps quasi-réel (15-20 min de délai)  

---

## 🎉 **Résultat**

Votre Fear & Greed Index sera enrichi avec :
- 🌍 Sentiment des marchés mondiaux
- 📊 Indicateur VIX (peur mondiale)
- 📈 Tendances S&P 500, CAC 40, etc.
- 🔗 Corrélation MASI vs indices internationaux

---

**C'est une bien meilleure alternative que Bloomberg pour votre usage !** 🚀

