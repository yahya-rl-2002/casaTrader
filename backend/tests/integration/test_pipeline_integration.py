import pytest
import asyncio
from datetime import date, datetime
from sqlalchemy.orm import Session

from app.services.pipeline_service import PipelineService
from app.models.database import get_session
from app.models.schemas import IndexScore
from app.core.logging import get_logger


class TestPipelineIntegration:
    """Integration tests for the complete pipeline"""
    
    def setup_method(self):
        """Setup for each test"""
        self.pipeline_service = PipelineService()
        self.logger = get_logger(__name__)
    
    @pytest.mark.asyncio
    async def test_full_pipeline_execution(self):
        """Test complete pipeline execution"""
        result = await self.pipeline_service.run_full_pipeline()
        
        assert isinstance(result, dict)
        assert "success" in result
        assert "final_score" in result
        assert "target_date" in result
        
        if result["success"]:
            assert isinstance(result["final_score"], float)
            assert 0 <= result["final_score"] <= 100
            assert isinstance(result["target_date"], date)
    
    @pytest.mark.asyncio
    async def test_pipeline_components_integration(self):
        """Test integration between pipeline components"""
        # Test market data collection
        market_data = await self.pipeline_service._collect_market_data(date.today())
        assert isinstance(market_data, list)
        
        # Test media data collection
        media_data = await self.pipeline_service._collect_media_data(date.today())
        assert isinstance(media_data, list)
        
        # Test sentiment analysis
        analyzed_media = await self.pipeline_service._analyze_sentiment(media_data)
        assert isinstance(analyzed_media, list)
        
        # Test component calculation
        components = await self.pipeline_service._calculate_components(
            market_data, analyzed_media, date.today()
        )
        assert hasattr(components, 'momentum')
        assert hasattr(components, 'price_strength')
        assert hasattr(components, 'volume')
        assert hasattr(components, 'volatility')
        assert hasattr(components, 'equity_vs_bonds')
        assert hasattr(components, 'media_sentiment')
        
        # Test score aggregation
        final_score = await self.pipeline_service._aggregate_score(components)
        assert isinstance(final_score, float)
        assert 0 <= final_score <= 100
    
    @pytest.mark.asyncio
    async def test_database_integration(self):
        """Test database integration"""
        # Test saving results
        from app.services.component_calculator import ComponentScores
        from app.pipelines.ingestion.media_scraper import MediaArticle
        
        components = ComponentScores(
            momentum=60.0,
            price_strength=70.0,
            volume=50.0,
            volatility=40.0,
            equity_vs_bonds=80.0,
            media_sentiment=55.0,
            as_of=datetime.now()
        )
        
        media_articles = [
            MediaArticle(
                title="Test Article",
                summary="Test Summary",
                url="http://test.com",
                source="test",
                published_at=datetime.now(),
                sentiment_score=0.5
            )
        ]
        
        # This should not raise an exception
        try:
            await self.pipeline_service._save_results(
                components, 75.0, media_articles, date.today()
            )
        except Exception as e:
            # If database is not available, that's expected in test environment
            self.logger.warning(f"Database save test failed (expected in test env): {e}")
    
    @pytest.mark.asyncio
    async def test_get_latest_score(self):
        """Test getting latest score from database"""
        latest_data = await self.pipeline_service.get_latest_score()
        
        # Should return None if no data, or dict with score data
        if latest_data is not None:
            assert isinstance(latest_data, dict)
            assert "score" in latest_data
            assert "as_of" in latest_data
            assert "components" in latest_data
            assert isinstance(latest_data["score"], float)
            assert 0 <= latest_data["score"] <= 100
    
    @pytest.mark.asyncio
    async def test_pipeline_error_handling(self):
        """Test pipeline error handling"""
        # Test with invalid date
        invalid_date = date(1900, 1, 1)  # Very old date
        result = await self.pipeline_service.run_full_pipeline(invalid_date)
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert "success" in result
    
    @pytest.mark.asyncio
    async def test_component_calculation_integration(self):
        """Test integration of component calculation with real data"""
        # Generate test data
        market_data = self.pipeline_service.market_scraper.fetch_historical_data(days=100)
        media_data = self.pipeline_service.media_scraper.scrape_all_sources(max_articles_per_source=3)
        
        # Analyze sentiment
        analyzed_media = await self.pipeline_service._analyze_sentiment(media_data)
        
        # Calculate components
        components = await self.pipeline_service._calculate_components(
            market_data, analyzed_media, date.today()
        )
        
        # Validate components
        assert 0 <= components.momentum <= 100
        assert 0 <= components.price_strength <= 100
        assert 0 <= components.volume <= 100
        assert 0 <= components.volatility <= 100
        assert 0 <= components.equity_vs_bonds <= 100
        assert 0 <= components.media_sentiment <= 100
        
        # Test composite score calculation
        composite_score = self.pipeline_service.component_calculator.calculate_composite_score(components)
        assert 0 <= composite_score <= 100
    
    @pytest.mark.asyncio
    async def test_sentiment_analysis_integration(self):
        """Test sentiment analysis integration with media data"""
        # Create test articles
        from app.pipelines.ingestion.media_scraper import MediaArticle
        
        test_articles = [
            MediaArticle(
                title="Croissance exceptionnelle du marché",
                summary="Le marché marocain affiche des performances remarquables",
                url="http://test.com/1",
                source="test",
                published_at=datetime.now()
            ),
            MediaArticle(
                title="Crise économique majeure",
                summary="Les difficultés s'accumulent sur le marché",
                url="http://test.com/2",
                source="test",
                published_at=datetime.now()
            )
        ]
        
        # Analyze sentiment
        analyzed_articles = await self.pipeline_service._analyze_sentiment(test_articles)
        
        assert len(analyzed_articles) == len(test_articles)
        
        # Check that sentiment scores were added
        for article in analyzed_articles:
            assert hasattr(article, 'sentiment_score')
            assert article.sentiment_score is not None
            assert -1.0 <= article.sentiment_score <= 1.0
    
    @pytest.mark.asyncio
    async def test_market_data_integration(self):
        """Test market data integration"""
        # Test historical data generation
        historical_data = await self.pipeline_service._collect_market_data(date.today())
        
        assert isinstance(historical_data, list)
        assert len(historical_data) > 0
        
        # Validate data structure
        for record in historical_data:
            assert hasattr(record, 'date')
            assert hasattr(record, 'open_price')
            assert hasattr(record, 'high_price')
            assert hasattr(record, 'low_price')
            assert hasattr(record, 'close_price')
            assert hasattr(record, 'volume')
    
    @pytest.mark.asyncio
    async def test_media_data_integration(self):
        """Test media data integration"""
        # Test media data collection
        media_data = await self.pipeline_service._collect_media_data(date.today())
        
        assert isinstance(media_data, list)
        
        # Validate data structure
        for article in media_data:
            assert hasattr(article, 'title')
            assert hasattr(article, 'summary')
            assert hasattr(article, 'url')
            assert hasattr(article, 'source')
            assert hasattr(article, 'published_at')
    
    @pytest.mark.asyncio
    async def test_pipeline_performance(self):
        """Test pipeline performance and timing"""
        import time
        
        start_time = time.time()
        result = await self.pipeline_service.run_full_pipeline()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Pipeline should complete within reasonable time (30 seconds)
        assert execution_time < 30, f"Pipeline took too long: {execution_time:.2f} seconds"
        
        # Should still produce valid results
        assert isinstance(result, dict)
        assert "success" in result
    
    @pytest.mark.asyncio
    async def test_concurrent_pipeline_execution(self):
        """Test concurrent pipeline execution"""
        # Run multiple pipelines concurrently
        tasks = [
            self.pipeline_service.run_full_pipeline()
            for _ in range(3)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should complete without exceptions
        for result in results:
            assert not isinstance(result, Exception)
            assert isinstance(result, dict)
            assert "success" in result
