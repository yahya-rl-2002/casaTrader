import pytest
from datetime import date, datetime, timedelta
from app.services.component_calculator import ComponentCalculator, ComponentScores
from app.pipelines.ingestion.market_scraper import MASIHistoricalData
from app.pipelines.ingestion.media_scraper import MediaArticle


class TestComponentCalculator:
    """Test suite for ComponentCalculator"""
    
    def setup_method(self):
        """Setup for each test"""
        self.calculator = ComponentCalculator()
        self.sample_historical_data = self._create_sample_historical_data()
        self.sample_media_articles = self._create_sample_media_articles()
    
    def _create_sample_historical_data(self, days: int = 252) -> list[MASIHistoricalData]:
        """Create sample historical data for testing"""
        data = []
        base_price = 12000.0
        
        for i in range(days):
            current_date = date.today() - timedelta(days=days-i-1)
            
            # Generate realistic price movement
            daily_change = (hash(str(current_date)) % 200 - 100) / 10000.0  # -1% to +1%
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
            
            base_price = close_price
        
        return data
    
    def _create_sample_media_articles(self) -> list[MediaArticle]:
        """Create sample media articles for testing"""
        return [
            MediaArticle(
                title="Croissance exceptionnelle du marché marocain",
                summary="Le MASI affiche des performances remarquables avec une hausse significative",
                url="http://test.com/1",
                source="medias24",
                published_at=datetime.now() - timedelta(days=1),
                sentiment_score=0.7
            ),
            MediaArticle(
                title="Crise économique sur le marché financier",
                summary="Les difficultés s'accumulent avec une volatilité accrue",
                url="http://test.com/2",
                source="leconomiste",
                published_at=datetime.now() - timedelta(days=2),
                sentiment_score=-0.5
            )
        ]
    
    def test_calculate_all_components(self):
        """Test calculation of all components"""
        components = self.calculator.calculate_all_components(
            self.sample_historical_data,
            self.sample_media_articles
        )
        
        assert isinstance(components, ComponentScores)
        assert 0 <= components.momentum <= 100
        assert 0 <= components.price_strength <= 100
        assert 0 <= components.volume <= 100
        assert 0 <= components.volatility <= 100
        assert 0 <= components.equity_vs_bonds <= 100
        assert 0 <= components.media_sentiment <= 100
        assert isinstance(components.as_of, datetime)
    
    def test_calculate_momentum(self):
        """Test momentum calculation"""
        momentum = self.calculator._calculate_momentum(self.sample_historical_data, date.today())
        
        assert isinstance(momentum, float)
        assert 0 <= momentum <= 100
    
    def test_calculate_momentum_insufficient_data(self):
        """Test momentum calculation with insufficient data"""
        short_data = self.sample_historical_data[:10]  # Only 10 days
        momentum = self.calculator._calculate_momentum(short_data, date.today())
        
        assert momentum == 50.0  # Should return neutral score
    
    def test_calculate_price_strength(self):
        """Test price strength calculation"""
        price_strength = self.calculator._calculate_price_strength(self.sample_historical_data, date.today())
        
        assert isinstance(price_strength, float)
        assert 0 <= price_strength <= 100
    
    def test_calculate_price_strength_insufficient_data(self):
        """Test price strength calculation with insufficient data"""
        short_data = self.sample_historical_data[:100]  # Less than 1 year
        price_strength = self.calculator._calculate_price_strength(short_data, date.today())
        
        assert price_strength == 50.0  # Should return neutral score
    
    def test_calculate_volume(self):
        """Test volume calculation"""
        volume = self.calculator._calculate_volume(self.sample_historical_data, date.today())
        
        assert isinstance(volume, float)
        assert 0 <= volume <= 100
    
    def test_calculate_volume_insufficient_data(self):
        """Test volume calculation with insufficient data"""
        short_data = self.sample_historical_data[:10]  # Less than 30 days
        volume = self.calculator._calculate_volume(short_data, date.today())
        
        assert volume == 50.0  # Should return neutral score
    
    def test_calculate_volatility(self):
        """Test volatility calculation"""
        volatility = self.calculator._calculate_volatility(self.sample_historical_data, date.today())
        
        assert isinstance(volatility, float)
        assert 0 <= volatility <= 100
    
    def test_calculate_volatility_insufficient_data(self):
        """Test volatility calculation with insufficient data"""
        short_data = self.sample_historical_data[:10]  # Less than 30 days
        volatility = self.calculator._calculate_volatility(short_data, date.today())
        
        assert volatility == 50.0  # Should return neutral score
    
    def test_calculate_equity_vs_bonds(self):
        """Test equity vs bonds calculation"""
        equity_vs_bonds = self.calculator._calculate_equity_vs_bonds(self.sample_historical_data, date.today())
        
        assert isinstance(equity_vs_bonds, (int, float))
        assert 0 <= equity_vs_bonds <= 100
    
    def test_calculate_equity_vs_bonds_insufficient_data(self):
        """Test equity vs bonds calculation with insufficient data"""
        short_data = self.sample_historical_data[:10]  # Less than 20 days
        equity_vs_bonds = self.calculator._calculate_equity_vs_bonds(short_data, date.today())
        
        assert equity_vs_bonds == 50.0  # Should return neutral score
    
    def test_calculate_media_sentiment(self):
        """Test media sentiment calculation"""
        media_sentiment = self.calculator._calculate_media_sentiment(self.sample_media_articles, date.today())
        
        assert isinstance(media_sentiment, float)
        assert 0 <= media_sentiment <= 100
    
    def test_calculate_media_sentiment_no_articles(self):
        """Test media sentiment calculation with no articles"""
        media_sentiment = self.calculator._calculate_media_sentiment([], date.today())
        
        assert media_sentiment == 50.0  # Should return neutral score
    
    def test_calculate_media_sentiment_old_articles(self):
        """Test media sentiment calculation with old articles"""
        old_articles = [
            MediaArticle(
                title="Old article",
                summary="Old content",
                url="http://test.com/old",
                source="test",
                published_at=datetime.now() - timedelta(days=10),  # 10 days old
                sentiment_score=0.5
            )
        ]
        
        media_sentiment = self.calculator._calculate_media_sentiment(old_articles, date.today())
        
        assert media_sentiment == 50.0  # Should return neutral score (articles too old)
    
    def test_calculate_composite_score(self):
        """Test composite score calculation"""
        components = ComponentScores(
            momentum=60.0,
            price_strength=70.0,
            volume=50.0,
            volatility=40.0,
            equity_vs_bonds=80.0,
            media_sentiment=55.0,
            as_of=datetime.now()
        )
        
        composite_score = self.calculator.calculate_composite_score(components)
        
        assert isinstance(composite_score, float)
        assert 0 <= composite_score <= 100
        
        # Test that weights are applied correctly
        expected_score = (
            60.0 * 0.25 +  # momentum
            70.0 * 0.25 +  # price_strength
            50.0 * 0.15 +  # volume
            40.0 * 0.15 +  # volatility
            80.0 * 0.10 +  # equity_vs_bonds
            55.0 * 0.10    # media_sentiment
        )
        
        assert abs(composite_score - expected_score) < 0.01
    
    def test_component_boundaries(self):
        """Test that all components stay within 0-100 boundaries"""
        # Test with extreme values
        extreme_data = []
        for i in range(300):
            extreme_data.append(MASIHistoricalData(
                date=date.today() - timedelta(days=300-i),
                open_price=1000.0 + i * 10,
                high_price=1100.0 + i * 10,
                low_price=900.0 + i * 10,
                close_price=1000.0 + i * 10,
                volume=1000000 + i * 1000
            ))
        
        components = self.calculator.calculate_all_components(extreme_data, self.sample_media_articles)
        
        assert 0 <= components.momentum <= 100
        assert 0 <= components.price_strength <= 100
        assert 0 <= components.volume <= 100
        assert 0 <= components.volatility <= 100
        assert 0 <= components.equity_vs_bonds <= 100
        assert 0 <= components.media_sentiment <= 100
    
    def test_error_handling(self):
        """Test error handling in component calculations"""
        # Test with empty data
        components = self.calculator.calculate_all_components([], [])
        
        # Should return default neutral values
        assert components.momentum == 50.0
        assert components.price_strength == 50.0
        assert components.volume == 50.0
        assert components.volatility == 50.0
        assert components.equity_vs_bonds == 50.0
        assert components.media_sentiment == 50.0
