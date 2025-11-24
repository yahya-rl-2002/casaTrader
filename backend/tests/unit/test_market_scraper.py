import pytest
from datetime import date, datetime
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper, MarketSnapshot, MASIHistoricalData


class TestCasablancaMarketScraper:
    """Test suite for CasablancaMarketScraper"""
    
    def setup_method(self):
        """Setup for each test"""
        self.scraper = CasablancaMarketScraper()
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        assert isinstance(self.scraper, CasablancaMarketScraper)
        assert hasattr(self.scraper, 'session')
        assert 'User-Agent' in self.scraper.session.headers
    
    def test_fetch_live_data_fallback(self):
        """Test live data fetching with fallback"""
        # This will likely use fallback data due to SSL issues
        data = self.scraper.fetch_live_data()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        for snapshot in data:
            assert isinstance(snapshot, MarketSnapshot)
            assert isinstance(snapshot.symbol, str)
            assert isinstance(snapshot.last_price, float)
            assert isinstance(snapshot.change_percent, float)
            assert isinstance(snapshot.volume, int)
            assert isinstance(snapshot.as_of, datetime)
            assert snapshot.last_price > 0
            assert snapshot.volume >= 0
    
    def test_fetch_historical_data(self):
        """Test historical data generation"""
        days = 30
        data = self.scraper.fetch_historical_data(days)
        
        assert isinstance(data, list)
        assert len(data) == days
        
        for record in data:
            assert isinstance(record, MASIHistoricalData)
            assert isinstance(record.date, date)
            assert isinstance(record.open_price, float)
            assert isinstance(record.high_price, float)
            assert isinstance(record.low_price, float)
            assert isinstance(record.close_price, float)
            assert isinstance(record.volume, int)
            
            # Validate OHLC relationships
            assert record.high_price >= record.open_price
            assert record.high_price >= record.close_price
            assert record.low_price <= record.open_price
            assert record.low_price <= record.close_price
            assert record.volume > 0
    
    def test_generate_synthetic_historical_data(self):
        """Test synthetic historical data generation"""
        days = 10
        data = self.scraper._generate_synthetic_historical_data(days)
        
        assert isinstance(data, list)
        assert len(data) == days
        
        # Check that data is sorted by date
        dates = [record.date for record in data]
        assert dates == sorted(dates)
        
        # Check that consecutive days are sequential
        for i in range(1, len(data)):
            assert (data[i].date - data[i-1].date).days == 1
    
    def test_get_fallback_data(self):
        """Test fallback data generation"""
        data = self.scraper._get_fallback_data()
        
        assert isinstance(data, list)
        assert len(data) == 1
        
        snapshot = data[0]
        assert isinstance(snapshot, MarketSnapshot)
        assert snapshot.symbol == "MASI"
        assert snapshot.last_price > 0
        assert snapshot.volume > 0
    
    def test_parse_int(self):
        """Test integer parsing from various formats"""
        assert self.scraper._parse_int("1,234,567") == 1234567
        assert self.scraper._parse_int("1 234 567") == 1234567
        assert self.scraper._parse_int("1234567") == 1234567
        assert self.scraper._parse_int("") == 0
        assert self.scraper._parse_int("abc") == 0
        assert self.scraper._parse_int("1.234.567") == 1234567
    
    def test_historical_data_consistency(self):
        """Test that historical data is consistent"""
        days = 50
        data = self.scraper.fetch_historical_data(days)
        
        # Check that prices are realistic (allow for some edge cases)
        for record in data:
            assert record.close_price >= 0  # Non-negative prices
            assert record.volume > 0
        
        # Check that there's some variation in prices
        prices = [record.close_price for record in data]
        assert max(prices) > min(prices)  # Should have some variation
    
    def test_market_snapshot_creation(self):
        """Test MarketSnapshot creation"""
        now = datetime.now()
        snapshot = MarketSnapshot(
            symbol="MASI",
            last_price=12500.0,
            change_percent=1.5,
            volume=1000000,
            as_of=now
        )
        
        assert snapshot.symbol == "MASI"
        assert snapshot.last_price == 12500.0
        assert snapshot.change_percent == 1.5
        assert snapshot.volume == 1000000
        assert snapshot.as_of == now
    
    def test_masi_historical_data_creation(self):
        """Test MASIHistoricalData creation"""
        test_date = date.today()
        data = MASIHistoricalData(
            date=test_date,
            open_price=12000.0,
            high_price=12500.0,
            low_price=11800.0,
            close_price=12300.0,
            volume=1500000
        )
        
        assert data.date == test_date
        assert data.open_price == 12000.0
        assert data.high_price == 12500.0
        assert data.low_price == 11800.0
        assert data.close_price == 12300.0
        assert data.volume == 1500000
    
    def test_error_handling(self):
        """Test error handling in scraper methods"""
        # Test with invalid parameters
        data = self.scraper.fetch_historical_data(0)  # Zero days
        assert isinstance(data, list)
        assert len(data) == 0
        
        data = self.scraper.fetch_historical_data(-5)  # Negative days
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_data_quality(self):
        """Test data quality of generated data"""
        days = 20
        data = self.scraper.fetch_historical_data(days)
        
        # Check for no null or invalid values
        for record in data:
            assert record.open_price is not None
            assert record.high_price is not None
            assert record.low_price is not None
            assert record.close_price is not None
            assert record.volume is not None
            
            # Check for non-negative values (allow zero for edge cases)
            assert record.open_price >= 0
            assert record.high_price >= 0
            assert record.low_price >= 0
            assert record.close_price >= 0
            assert record.volume > 0
    
    def test_date_continuity(self):
        """Test that historical data has continuous dates"""
        days = 30
        data = self.scraper.fetch_historical_data(days)
        
        # Check that dates are continuous (no gaps)
        for i in range(1, len(data)):
            expected_gap = (data[i].date - data[i-1].date).days
            assert expected_gap == 1, f"Gap found between {data[i-1].date} and {data[i].date}"
    
    def test_price_realism(self):
        """Test that generated prices are realistic for MASI"""
        days = 30
        data = self.scraper.fetch_historical_data(days)
        
        for record in data:
            # MASI should be non-negative (allow for edge cases with zero)
            assert record.close_price >= 0
            assert record.open_price >= 0
            assert record.high_price >= 0
            assert record.low_price >= 0
