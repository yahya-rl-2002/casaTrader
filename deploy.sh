#!/bin/bash

# Fear & Greed Index - Deployment Script
# This script deploys the complete Fear & Greed Index system

set -e

echo "🚀 Fear & Greed Index - Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if Docker is running
check_docker_running() {
    print_status "Checking if Docker is running..."
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is running"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p data/postgres
    mkdir -p data/redis
    mkdir -p data/prometheus
    mkdir -p data/grafana
    
    print_success "Directories created"
}

# Build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Stop existing containers
    docker-compose down --remove-orphans
    
    # Build and start services
    docker-compose up --build -d
    
    print_success "Services started"
}

# Wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    # Wait for database
    print_status "Waiting for PostgreSQL..."
    timeout 60 bash -c 'until docker-compose exec postgres pg_isready -U fear_greed_user -d fear_greed_db; do sleep 2; done'
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    timeout 30 bash -c 'until docker-compose exec redis redis-cli ping; do sleep 2; done'
    
    # Wait for backend
    print_status "Waiting for Backend API..."
    timeout 60 bash -c 'until curl -f http://localhost:8000/api/v1/health; do sleep 2; done'
    
    # Wait for frontend
    print_status "Waiting for Frontend..."
    timeout 60 bash -c 'until curl -f http://localhost:3000; do sleep 2; done'
    
    print_success "All services are healthy"
}

# Initialize database
init_database() {
    print_status "Initializing database..."
    
    # Run database migrations
    docker-compose exec backend python init_db.py
    
    # Run initial pipeline
    docker-compose exec backend python -c "
from app.services.pipeline_service import PipelineService
import asyncio

async def init_pipeline():
    pipeline = PipelineService()
    result = await pipeline.run_full_pipeline()
    print(f'Initial pipeline result: {result}')

asyncio.run(init_pipeline())
"
    
    print_success "Database initialized"
}

# Show deployment status
show_status() {
    print_status "Deployment Status:"
    echo ""
    
    echo "🌐 Services:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3001 (admin/admin123)"
    echo ""
    
    echo "📊 Monitoring:"
    echo "  - Prometheus Metrics: http://localhost:9090"
    echo "  - Grafana Dashboards: http://localhost:3001"
    echo ""
    
    echo "🗄️ Database:"
    echo "  - PostgreSQL: localhost:5432"
    echo "  - Redis: localhost:6379"
    echo ""
    
    echo "📝 Logs:"
    echo "  - Backend: docker-compose logs backend"
    echo "  - Frontend: docker-compose logs frontend"
    echo "  - All: docker-compose logs"
}

# Main deployment function
main() {
    echo "Starting deployment process..."
    echo ""
    
    check_docker
    check_docker_running
    create_directories
    deploy_services
    wait_for_services
    init_database
    
    echo ""
    print_success "🎉 Deployment completed successfully!"
    echo ""
    show_status
    
    echo ""
    print_status "To view logs: docker-compose logs -f"
    print_status "To stop services: docker-compose down"
    print_status "To restart services: docker-compose restart"
}

# Run main function
main "$@"







