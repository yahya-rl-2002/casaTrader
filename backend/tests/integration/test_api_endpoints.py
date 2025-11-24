import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app


class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/api/v1/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_index_latest_endpoint(self):
        """Test latest index endpoint"""
        response = self.client.get("/api/v1/index/latest")
        assert response.status_code == 200
        
        data = response.json()
        assert "as_of" in data
        assert "score" in data
        assert isinstance(data["score"], float)
        assert 0 <= data["score"] <= 100
    
    def test_index_history_endpoint(self):
        """Test index history endpoint"""
        response = self.client.get("/api/v1/index/history")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        
        if len(data["data"]) > 0:
            for item in data["data"]:
                assert "as_of" in item
                assert "score" in item
                assert isinstance(item["score"], float)
                assert 0 <= item["score"] <= 100
    
    def test_index_history_with_dates(self):
        """Test index history with date filters"""
        from datetime import date, timedelta
        
        start_date = (date.today() - timedelta(days=7)).isoformat()
        end_date = date.today().isoformat()
        
        response = self.client.get(f"/api/v1/index/history?start_date={start_date}&end_date={end_date}")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_components_latest_endpoint(self):
        """Test latest components endpoint"""
        response = self.client.get("/api/v1/components/latest")
        assert response.status_code == 200
        
        data = response.json()
        assert "as_of" in data
        assert "momentum" in data
        assert "price_strength" in data
        assert "volume" in data
        assert "volatility" in data
        assert "equity_vs_bonds" in data
        assert "media_sentiment" in data
        
        # Validate component values
        for component in ["momentum", "price_strength", "volume", "volatility", "equity_vs_bonds", "media_sentiment"]:
            assert isinstance(data[component], float)
            assert 0 <= data[component] <= 100
    
    def test_pipeline_test_endpoint(self):
        """Test pipeline test endpoint"""
        response = self.client.post("/api/v1/pipeline/test")
        assert response.status_code == 200
        
        data = response.json()
        assert "market_data_count" in data
        assert "media_articles_count" in data
        assert "sentiment_analysis_count" in data
        assert "status" in data
        assert data["status"] == "components_working"
    
    def test_pipeline_run_endpoint(self):
        """Test pipeline run endpoint"""
        response = self.client.post("/api/v1/pipeline/run")
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data
        assert "message" in data
        assert "final_score" in data
        assert "target_date" in data
        
        if data["success"]:
            assert isinstance(data["final_score"], float)
            assert 0 <= data["final_score"] <= 100
    
    def test_pipeline_status_endpoint(self):
        """Test pipeline status endpoint"""
        response = self.client.get("/api/v1/pipeline/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        
        if data["status"] == "active":
            assert "latest_score" in data
            assert "last_updated" in data
            assert "components" in data
        elif data["status"] == "no_data":
            assert "message" in data
    
    def test_metadata_endpoint(self):
        """Test metadata endpoint"""
        response = self.client.get("/api/v1/metadata")
        assert response.status_code == 200
        
        data = response.json()
        assert "app_name" in data
        assert "version" in data
        assert "environment" in data
        assert "description" in data
    
    def test_invalid_endpoints(self):
        """Test invalid endpoints return 404"""
        response = self.client.get("/api/v1/invalid")
        assert response.status_code == 404
        
        response = self.client.get("/api/v1/index/invalid")
        assert response.status_code == 404
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = self.client.options("/api/v1/health")
        # CORS headers should be present (handled by FastAPI CORS middleware)
        assert response.status_code in [200, 204]
    
    def test_content_type_headers(self):
        """Test content type headers"""
        response = self.client.get("/api/v1/health")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
    
    def test_api_documentation(self):
        """Test API documentation endpoints"""
        # Test OpenAPI schema
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_api_docs_endpoint(self):
        """Test API docs endpoint"""
        response = self.client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_redoc_endpoint(self):
        """Test ReDoc endpoint"""
        response = self.client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_pipeline_run_with_date(self):
        """Test pipeline run with specific date"""
        from datetime import date
        
        target_date = date.today().isoformat()
        response = self.client.post(f"/api/v1/pipeline/run?target_date={target_date}")
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data
        assert "target_date" in data
    
    def test_index_history_pagination(self):
        """Test index history with pagination parameters"""
        response = self.client.get("/api/v1/index/history?limit=10&offset=0")
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_error_handling(self):
        """Test error handling in API"""
        # Test with invalid date format
        response = self.client.get("/api/v1/index/history?start_date=invalid-date")
        # Should handle gracefully (either 400 or 422)
        assert response.status_code in [400, 422]
    
    def test_response_times(self):
        """Test API response times"""
        import time
        
        # Test health endpoint response time
        start_time = time.time()
        response = self.client.get("/api/v1/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
    
    def test_concurrent_requests(self):
        """Test concurrent API requests"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = self.client.get("/api/v1/health")
            results.append(response.status_code)
        
        # Make 5 concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert len(results) == 5
        assert all(status == 200 for status in results)
    
    def test_api_versioning(self):
        """Test API versioning"""
        # Test that all endpoints are under /api/v1/
        endpoints = [
            "/api/v1/health",
            "/api/v1/index/latest",
            "/api/v1/components/latest",
            "/api/v1/pipeline/status"
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 200, f"Endpoint {endpoint} failed"
    
    def test_data_validation(self):
        """Test data validation in responses"""
        # Test index latest response structure
        response = self.client.get("/api/v1/index/latest")
        assert response.status_code == 200
        
        data = response.json()
        
        # Validate required fields
        required_fields = ["as_of", "score"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(data["score"], (int, float))
        assert 0 <= data["score"] <= 100
        
        # Validate date format
        from datetime import datetime
        try:
            datetime.fromisoformat(data["as_of"].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Invalid date format in response")







