#!/usr/bin/env python3
"""
Demo script to showcase the Fear & Greed Index pipeline
"""
import asyncio
import sys
from datetime import date

# Add the app directory to the path
sys.path.append('.')

from app.services.pipeline_service import PipelineService
from app.core.logging import get_logger


logger = get_logger(__name__)


async def demo_pipeline():
    """Demonstrate the Fear & Greed Index pipeline"""
    print("🚀 Fear & Greed Index Pipeline Demo")
    print("=" * 50)
    
    pipeline_service = PipelineService()
    
    try:
        # Run the full pipeline
        print("📊 Running Fear & Greed Index pipeline...")
        result = await pipeline_service.run_full_pipeline()
        
        if result["success"]:
            print(f"✅ Pipeline completed successfully!")
            print(f"📈 Final Score: {result['final_score']}")
            print(f"📅 Target Date: {result['target_date']}")
            print(f"📊 Market Data Points: {result['market_data_count']}")
            print(f"📰 Media Articles: {result['media_articles_count']}")
            
            # Get the latest score from database
            latest_data = await pipeline_service.get_latest_score()
            if latest_data:
                print("\n🎯 Latest Index Data:")
                print(f"   Score: {latest_data['score']}")
                print(f"   Date: {latest_data['as_of']}")
                print(f"   Components:")
                for component, value in latest_data['components'].items():
                    print(f"     - {component}: {value:.2f}")
        else:
            print(f"❌ Pipeline failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.error(f"Demo error: {e}")


async def demo_components():
    """Demonstrate individual components"""
    print("\n🔧 Testing Individual Components")
    print("=" * 50)
    
    pipeline_service = PipelineService()
    
    try:
        # Test market scraper
        print("📈 Testing Market Scraper...")
        market_data = pipeline_service.market_scraper.fetch_historical_data(days=30)
        print(f"   Generated {len(market_data)} days of market data")
        
        # Test media scraper
        print("📰 Testing Media Scraper...")
        media_data = pipeline_service.media_scraper.scrape_all_sources(max_articles_per_source=3)
        print(f"   Found {len(media_data)} media articles")
        
        # Test sentiment analysis
        if media_data:
            print("🧠 Testing Sentiment Analysis...")
            sentiment_results = pipeline_service.sentiment_analyzer.analyze_articles(media_data[:2])
            for i, result in enumerate(sentiment_results):
                print(f"   Article {i+1}: Polarity={result.polarity:.3f}, Confidence={result.confidence:.3f}")
        
        # Test component calculator
        print("⚙️ Testing Component Calculator...")
        components = pipeline_service.component_calculator.calculate_all_components(
            market_data, media_data
        )
        print(f"   Calculated components:")
        print(f"     - Momentum: {components.momentum:.2f}")
        print(f"     - Price Strength: {components.price_strength:.2f}")
        print(f"     - Volume: {components.volume:.2f}")
        print(f"     - Volatility: {components.volatility:.2f}")
        print(f"     - Equity vs Bonds: {components.equity_vs_bonds:.2f}")
        print(f"     - Media Sentiment: {components.media_sentiment:.2f}")
        
        # Calculate final score
        final_score = pipeline_service.component_calculator.calculate_composite_score(components)
        print(f"   Final Composite Score: {final_score:.2f}")
        
    except Exception as e:
        print(f"❌ Component demo failed: {e}")
        logger.error(f"Component demo error: {e}")


async def main():
    """Main demo function"""
    print("🎯 Casablanca Fear & Greed Index - Pipeline Demo")
    print("=" * 60)
    
    # Run component demo first
    await demo_components()
    
    # Run full pipeline demo
    await demo_pipeline()
    
    print("\n🎉 Demo completed!")
    print("💡 You can now:")
    print("   - Check the API at http://localhost:8000/docs")
    print("   - View the dashboard at http://localhost:3000/dashboard")
    print("   - Run the pipeline via: curl -X POST http://localhost:8000/api/v1/pipeline/run")


if __name__ == "__main__":
    asyncio.run(main())







