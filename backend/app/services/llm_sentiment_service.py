"""
LLM-based Sentiment Analysis Service for Financial News
Uses OpenAI GPT models to analyze sentiment of financial articles
"""
from __future__ import annotations

import os
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class LLMSentimentResult:
    """Result of LLM sentiment analysis"""
    article_id: Optional[int]
    title: str
    sentiment_score: float  # -1.0 to +1.0
    sentiment_label: str  # "Very Negative", "Negative", "Neutral", "Positive", "Very Positive"
    confidence: float  # 0.0 to 1.0
    reasoning: str  # Explanation from LLM
    analyzed_at: datetime


class LLMSentimentAnalyzer:
    """
    Analyze financial news sentiment using Large Language Models (OpenAI GPT)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize LLM Sentiment Analyzer
        
        Args:
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
            model: Model to use (gpt-4o-mini, gpt-4o, gpt-3.5-turbo)
        """
        # Priorité: paramètre > config > variable d'environnement
        from app.core.config import settings
        self.api_key = api_key or settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            logger.warning("⚠️ No OpenAI API key found. LLM sentiment analysis will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"✅ LLM Sentiment Analyzer initialized with model: {model}")
    
    def analyze_article(self, title: str, summary: str = "", article_id: Optional[int] = None) -> LLMSentimentResult:
        """
        Analyze sentiment of a single article using LLM
        
        Args:
            title: Article title
            summary: Article summary/content (optional)
            article_id: Article ID for tracking
            
        Returns:
            LLMSentimentResult with score from -1.0 to +1.0
        """
        if not self.enabled:
            logger.warning("LLM sentiment analysis is disabled. Returning neutral score.")
            return self._create_fallback_result(title, article_id)
        
        try:
            # Import OpenAI here to avoid dependency if not used
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Prepare the text for analysis
            text_to_analyze = f"{title}"
            if summary:
                text_to_analyze += f"\n\n{summary}"
            
            # Create the prompt for sentiment analysis
            prompt = self._create_sentiment_prompt(text_to_analyze)
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Low temperature for consistent results
                max_tokens=200
            )
            
            # Parse the response
            result_text = response.choices[0].message.content.strip()
            sentiment_score, sentiment_label, confidence, reasoning = self._parse_llm_response(result_text)
            
            logger.info(f"📊 LLM Sentiment for '{title[:50]}...': {sentiment_score:.2f} ({sentiment_label})")
            
            return LLMSentimentResult(
                article_id=article_id,
                title=title,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                confidence=confidence,
                reasoning=reasoning,
                analyzed_at=datetime.now()
            )
            
        except ImportError:
            logger.error("❌ OpenAI library not installed. Install with: pip install openai")
            return self._create_fallback_result(title, article_id)
        
        except Exception as e:
            logger.error(f"❌ Error analyzing sentiment with LLM: {e}")
            return self._create_fallback_result(title, article_id)
    
    def analyze_articles_batch(self, articles: List[dict]) -> List[LLMSentimentResult]:
        """
        Analyze sentiment for multiple articles
        
        Args:
            articles: List of dicts with 'title', 'summary', and optionally 'id'
            
        Returns:
            List of LLMSentimentResult
        """
        results = []
        
        for article in articles:
            title = article.get('title', '')
            summary = article.get('summary', '')
            article_id = article.get('id')
            
            if not title:
                continue
            
            result = self.analyze_article(title, summary, article_id)
            results.append(result)
        
        return results
    
    def calculate_daily_sentiment_score(self, results: List[LLMSentimentResult]) -> float:
        """
        Calculate the average daily sentiment score from multiple articles
        
        Args:
            results: List of LLMSentimentResult
            
        Returns:
            Average sentiment score from -1.0 to +1.0
        """
        if not results:
            return 0.0
        
        # Calculate weighted average based on confidence
        total_weight = sum(r.confidence for r in results)
        
        if total_weight == 0:
            # Simple average if no confidence scores
            return sum(r.sentiment_score for r in results) / len(results)
        
        # Weighted average
        weighted_sum = sum(r.sentiment_score * r.confidence for r in results)
        return weighted_sum / total_weight
    
    def normalize_to_100_scale(self, sentiment_score: float) -> float:
        """
        Convert sentiment score from [-1, +1] to [0, 100] scale
        
        Args:
            sentiment_score: Score from -1.0 to +1.0
            
        Returns:
            Score from 0 to 100
        """
        # -1.0 -> 0
        #  0.0 -> 50
        # +1.0 -> 100
        return (sentiment_score + 1.0) * 50.0
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the LLM with Moroccan context"""
        return """Tu es un expert en analyse financière et économique spécialisé dans le marché boursier MAROCAIN.
Ta tâche est d'analyser le sentiment d'articles en français en tenant compte de ce qui est BÉNÉFIQUE pour le MAROC.

CRITÈRES IMPORTANTS - CONTEXTE MAROCAIN :
✅ POSITIF POUR LE MAROC (score +0.5 à +1.0) :
- Nouvelles bénéfiques pour le Maroc : reconnaissance internationale, soutien, appui
- Investissements au Maroc, création d'emplois, projets de développement
- Accords économiques, partenariats, coopération internationale favorable au Maroc
- Croissance économique, hausse du MASI, performance des entreprises marocaines
- Nouvelles positives sur le Sahara marocain : reconnaissance, soutien, autonomie
- Résolution de conflits, normalisation de relations diplomatiques
- Progrès sociaux, réformes réussies, modernisation
- Tourisme, exportations, commerce extérieur en hausse
- Création d'emplois, embauche, développement des compétences

❌ NÉGATIF POUR LE MAROC (score -1.0 à -0.5) :
- Nouvelles contre le Maroc : contestation, remise en question, rejet
- Sanctions, embargo, boycott contre le Maroc
- Perte d'investissements, fermeture d'entreprises, licenciements massifs
- Crise économique, récession, chute de la croissance
- Instabilité politique, tensions sociales, grèves, manifestations
- Corruptions, scandales financiers
- Menaces sécuritaires, attentats, terrorisme
- Nouvelles négatives sur le Sahara : contestation, remise en question de la souveraineté
- Tensions diplomatiques, gel de relations, ruptures
- Désinvestissement, délocalisation, départ d'entreprises

NEUTRE (score -0.05 à +0.05) :
- Articles factuels sans impact positif ou négatif pour le Maroc
- Informations générales sans contexte marocain spécifique

Critères d'évaluation:
- Score entre -1.0 et +1.0
- -1.0: Très négatif pour le Maroc (sanctions, crises majeures, menaces)
- -0.5: Négatif pour le Maroc (difficultés, inquiétudes, tensions)
- 0.0: Neutre (factuel, pas d'impact clair)
- +0.5: Positif pour le Maroc (bonnes nouvelles, opportunités, croissance)
- +1.0: Très positif pour le Maroc (succès majeurs, reconnaissance internationale, investissements importants)

Considère ces aspects:
1. Impact sur le Maroc (est-ce bénéfique ou négatif pour le pays ?)
2. Ton général (optimiste, pessimiste, neutre)
3. Mots-clés économiques ET géopolitiques (croissance, investissement, reconnaissance, sanctions, etc.)
4. Perspectives d'avenir pour le Maroc (prometteur vs incertain)
5. Impact sur les investisseurs marocains (confiance vs prudence)

EXEMPLE : 
- "Guterres sur le Sahara marocain : 'C'est un moment historique pour résoudre ce conflit'" 
  → POSITIF (+0.7) : Résolution favorable au Maroc
- "Reconnaissance américaine du Sahara marocain"
  → TRÈS POSITIF (+1.0) : Reconnaissance internationale bénéfique
- "Sanctions européennes contre le Maroc"
  → TRÈS NÉGATIF (-1.0) : Sanction contre le Maroc

Réponds UNIQUEMENT au format suivant (une ligne par élément):
SCORE: [nombre entre -1.0 et +1.0]
LABEL: [Very Negative|Negative|Neutral|Positive|Very Positive]
CONFIDENCE: [nombre entre 0.0 et 1.0]
REASONING: [explication courte en 1-2 phrases avec contexte marocain]"""
    
    def _create_sentiment_prompt(self, text: str) -> str:
        """Create the user prompt for sentiment analysis with Moroccan context"""
        return f"""Analyse le sentiment de cet article en tenant compte de ce qui est BÉNÉFIQUE pour le MAROC :

"{text}"

Questions à te poser :
- Cette nouvelle est-elle POSITIVE pour le Maroc ? (investissement, croissance, reconnaissance, partenariat, création d'emplois, etc.)
- Cette nouvelle est-elle NÉGATIVE pour le Maroc ? (sanctions, crise, perte d'emplois, tensions, contestation, etc.)
- Quel est l'impact sur l'économie marocaine, les entreprises marocaines, les investisseurs ?
- S'agit-il d'une nouvelle géopolitique favorable au Maroc ? (reconnaissance, soutien, normalisation)

Fournis ton analyse au format demandé en expliquant pourquoi c'est positif, négatif ou neutre pour le Maroc."""
    
    def _parse_llm_response(self, response: str) -> tuple[float, str, float, str]:
        """
        Parse the LLM response to extract sentiment information
        
        Returns:
            (sentiment_score, sentiment_label, confidence, reasoning)
        """
        try:
            lines = response.strip().split('\n')
            
            sentiment_score = 0.0
            sentiment_label = "Neutral"
            confidence = 0.5
            reasoning = ""
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("SCORE:"):
                    score_str = line.split(":", 1)[1].strip()
                    sentiment_score = float(score_str)
                    # Clamp to [-1, +1]
                    sentiment_score = max(-1.0, min(1.0, sentiment_score))
                
                elif line.startswith("LABEL:"):
                    sentiment_label = line.split(":", 1)[1].strip()
                
                elif line.startswith("CONFIDENCE:"):
                    conf_str = line.split(":", 1)[1].strip()
                    confidence = float(conf_str)
                    # Clamp to [0, 1]
                    confidence = max(0.0, min(1.0, confidence))
                
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
            
            return sentiment_score, sentiment_label, confidence, reasoning
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return 0.0, "Neutral", 0.5, "Could not parse LLM response"
    
    def _create_fallback_result(self, title: str, article_id: Optional[int] = None) -> LLMSentimentResult:
        """Create a fallback neutral result when LLM is unavailable"""
        return LLMSentimentResult(
            article_id=article_id,
            title=title,
            sentiment_score=0.0,
            sentiment_label="Neutral",
            confidence=0.0,
            reasoning="LLM analysis unavailable, defaulting to neutral",
            analyzed_at=datetime.now()
        )


# Convenience functions
def analyze_article_sentiment(title: str, summary: str = "") -> float:
    """
    Quick function to analyze a single article and return normalized score (0-100)
    
    Args:
        title: Article title
        summary: Article summary
        
    Returns:
        Sentiment score from 0 to 100
    """
    analyzer = LLMSentimentAnalyzer()
    result = analyzer.analyze_article(title, summary)
    return analyzer.normalize_to_100_scale(result.sentiment_score)


def analyze_daily_news(articles: List[dict]) -> float:
    """
    Analyze all news articles from a day and return average sentiment score (0-100)
    
    Args:
        articles: List of article dicts with 'title' and optionally 'summary'
        
    Returns:
        Average sentiment score from 0 to 100
    """
    analyzer = LLMSentimentAnalyzer()
    results = analyzer.analyze_articles_batch(articles)
    avg_sentiment = analyzer.calculate_daily_sentiment_score(results)
    return analyzer.normalize_to_100_scale(avg_sentiment)

