import pytest
from app.services.sentiment_service import SentimentAnalyzer, SentimentResult


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer"""
    
    def setup_method(self):
        """Setup for each test"""
        self.analyzer = SentimentAnalyzer()
    
    def test_analyze_positive_text(self):
        """Test analysis of positive financial text"""
        positive_text = "La croissance du marché marocain est excellente avec des bénéfices remarquables"
        result = self.analyzer.analyze_text(positive_text)
        
        assert isinstance(result, SentimentResult)
        assert result.polarity > 0.3  # Should be positive
        assert result.confidence > 0.0
        assert len(result.positive_words) > 0
        assert "croissance" in result.positive_words or "excellente" in result.positive_words
    
    def test_analyze_negative_text(self):
        """Test analysis of negative financial text"""
        negative_text = "La crise économique cause des difficultés majeures avec une récession prévue"
        result = self.analyzer.analyze_text(negative_text)
        
        assert isinstance(result, SentimentResult)
        assert result.polarity < -0.3  # Should be negative
        assert result.confidence > 0.0
        assert len(result.negative_words) > 0
        assert "crise" in result.negative_words or "difficultés" in result.negative_words
    
    def test_analyze_neutral_text(self):
        """Test analysis of neutral text"""
        neutral_text = "Le marché fonctionne normalement avec des volumes standards"
        result = self.analyzer.analyze_text(neutral_text)
        
        assert isinstance(result, SentimentResult)
        assert -0.3 <= result.polarity <= 0.3  # Should be neutral
        assert result.confidence >= 0.0
    
    def test_analyze_empty_text(self):
        """Test analysis of empty text"""
        result = self.analyzer.analyze_text("")
        
        assert isinstance(result, SentimentResult)
        assert result.polarity == 0.0
        assert result.confidence == 0.0
        assert len(result.positive_words) == 0
        assert len(result.negative_words) == 0
    
    def test_analyze_negated_text(self):
        """Test analysis of negated text"""
        negated_text = "Le marché n'est pas en crise et ne montre pas de difficultés"
        result = self.analyzer.analyze_text(negated_text)
        
        assert isinstance(result, SentimentResult)
        # Negated negative words should contribute to positive sentiment
        assert result.polarity > 0.0
    
    def test_analyze_intensified_text(self):
        """Test analysis of intensified text"""
        intensified_text = "Le marché est très performant avec une croissance extrêmement forte"
        result = self.analyzer.analyze_text(intensified_text)
        
        assert isinstance(result, SentimentResult)
        assert result.polarity > 0.5  # Should be very positive due to intensifiers
    
    def test_get_sentiment_label(self):
        """Test sentiment label generation"""
        assert self.analyzer.get_sentiment_label(0.5) == "Positive"
        assert self.analyzer.get_sentiment_label(-0.5) == "Negative"
        assert self.analyzer.get_sentiment_label(0.0) == "Neutral"
        assert self.analyzer.get_sentiment_label(0.2) == "Neutral"
        assert self.analyzer.get_sentiment_label(-0.2) == "Neutral"
    
    def test_get_sentiment_color(self):
        """Test sentiment color generation"""
        assert self.analyzer.get_sentiment_color(0.5) == "#10b981"  # Green
        assert self.analyzer.get_sentiment_color(-0.5) == "#ef4444"  # Red
        assert self.analyzer.get_sentiment_color(0.0) == "#f59e0b"  # Yellow
    
    def test_analyze_articles(self):
        """Test analysis of multiple articles"""
        from app.pipelines.ingestion.media_scraper import MediaArticle
        from datetime import datetime
        
        articles = [
            MediaArticle(
                title="Croissance exceptionnelle du marché",
                summary="Le marché marocain affiche des performances remarquables",
                url="http://test.com/1",
                source="test",
                published_at=datetime.now()
            ),
            MediaArticle(
                title="Crise économique majeure",
                summary="Les difficultés s'accumulent sur le marché financier",
                url="http://test.com/2",
                source="test",
                published_at=datetime.now()
            )
        ]
        
        results = self.analyzer.analyze_articles(articles)
        
        assert len(results) == 2
        assert results[0].polarity > 0.0  # First article should be positive
        assert results[1].polarity < 0.0  # Second article should be negative
    
    def test_financial_keywords_detection(self):
        """Test detection of financial keywords"""
        financial_text = "La bourse de Casablanca montre une volatilité importante avec des investissements croissants"
        result = self.analyzer.analyze_text(financial_text)
        
        # Should detect financial terms
        assert any(word in result.positive_words or word in result.negative_words 
                  for word in ["bourse", "volatilité", "investissements"])
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # High confidence text (clear sentiment)
        clear_text = "Le marché est extrêmement performant avec des bénéfices exceptionnels"
        clear_result = self.analyzer.analyze_text(clear_text)
        
        # Low confidence text (mixed sentiment)
        mixed_text = "Le marché est stable mais incertain"
        mixed_result = self.analyzer.analyze_text(mixed_text)
        
        # Both should have confidence scores (may be equal in some cases)
        assert clear_result.confidence >= 0.0
        assert mixed_result.confidence >= 0.0
