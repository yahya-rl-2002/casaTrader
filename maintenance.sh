#!/bin/bash

# Fear & Greed Index - Maintenance Script
# This script provides maintenance operations for the deployed system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Show help
show_help() {
    echo "Fear & Greed Index - Maintenance Script"
    echo "======================================"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  status      - Show system status"
    echo "  logs        - Show logs for all services"
    echo "  logs-backend - Show backend logs"
    echo "  logs-frontend - Show frontend logs"
    echo "  restart     - Restart all services"
    echo "  restart-backend - Restart backend service"
    echo "  restart-frontend - Restart frontend service"
    echo "  backup      - Backup database"
    echo "  restore     - Restore database from backup"
    echo "  update      - Update and restart services"
    echo "  clean       - Clean up unused containers and images"
    echo "  health      - Check health of all services"
    echo "  pipeline    - Run pipeline manually"
    echo "  help        - Show this help"
}

# Show system status
show_status() {
    print_status "System Status:"
    echo ""
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running"
        docker-compose ps
    else
        print_error "No services are running"
    fi
    
    echo ""
    
    # Check health endpoints
    print_status "Health Checks:"
    
    # Backend health
    if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
        print_success "Backend API: Healthy"
    else
        print_error "Backend API: Unhealthy"
    fi
    
    # Frontend health
    if curl -f http://localhost:3000 &> /dev/null; then
        print_success "Frontend: Healthy"
    else
        print_error "Frontend: Unhealthy"
    fi
    
    # Database health
    if docker-compose exec postgres pg_isready -U fear_greed_user -d fear_greed_db &> /dev/null; then
        print_success "Database: Healthy"
    else
        print_error "Database: Unhealthy"
    fi
    
    # Redis health
    if docker-compose exec redis redis-cli ping &> /dev/null; then
        print_success "Redis: Healthy"
    else
        print_error "Redis: Unhealthy"
    fi
}

# Show logs
show_logs() {
    local service=${1:-""}
    
    if [ -z "$service" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $service..."
        docker-compose logs -f "$service"
    fi
}

# Restart services
restart_services() {
    local service=${1:-""}
    
    if [ -z "$service" ]; then
        print_status "Restarting all services..."
        docker-compose restart
    else
        print_status "Restarting $service..."
        docker-compose restart "$service"
    fi
    
    print_success "Services restarted"
}

# Backup database
backup_database() {
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    
    print_status "Creating database backup: $backup_file"
    
    docker-compose exec postgres pg_dump -U fear_greed_user -d fear_greed_db > "backups/$backup_file"
    
    print_success "Database backed up to backups/$backup_file"
}

# Restore database
restore_database() {
    local backup_file=$1
    
    if [ -z "$backup_file" ]; then
        print_error "Please specify backup file"
        echo "Usage: $0 restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "backups/$backup_file" ]; then
        print_error "Backup file not found: backups/$backup_file"
        exit 1
    fi
    
    print_warning "This will replace the current database. Are you sure? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_status "Restore cancelled"
        exit 0
    fi
    
    print_status "Restoring database from $backup_file"
    
    docker-compose exec -T postgres psql -U fear_greed_user -d fear_greed_db < "backups/$backup_file"
    
    print_success "Database restored from $backup_file"
}

# Update services
update_services() {
    print_status "Updating services..."
    
    # Pull latest images
    docker-compose pull
    
    # Rebuild and restart
    docker-compose up --build -d
    
    print_success "Services updated"
}

# Clean up
clean_up() {
    print_status "Cleaning up unused containers and images..."
    
    # Remove unused containers
    docker container prune -f
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes
    docker volume prune -f
    
    print_success "Cleanup completed"
}

# Check health
check_health() {
    print_status "Checking health of all services..."
    
    # Check each service
    services=("postgres" "redis" "backend" "frontend" "nginx" "prometheus" "grafana")
    
    for service in "${services[@]}"; do
        if docker-compose ps "$service" | grep -q "Up"; then
            print_success "$service: Running"
        else
            print_error "$service: Not running"
        fi
    done
}

# Run pipeline manually
run_pipeline() {
    print_status "Running pipeline manually..."
    
    docker-compose exec backend python -c "
from app.services.pipeline_service import PipelineService
import asyncio

async def run_pipeline():
    pipeline = PipelineService()
    result = await pipeline.run_full_pipeline()
    print(f'Pipeline result: {result}')

asyncio.run(run_pipeline())
"
    
    print_success "Pipeline completed"
}

# Main function
main() {
    local command=${1:-"help"}
    
    case $command in
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "logs-backend")
            show_logs "backend"
            ;;
        "logs-frontend")
            show_logs "frontend"
            ;;
        "restart")
            restart_services
            ;;
        "restart-backend")
            restart_services "backend"
            ;;
        "restart-frontend")
            restart_services "frontend"
            ;;
        "backup")
            backup_database
            ;;
        "restore")
            restore_database "$2"
            ;;
        "update")
            update_services
            ;;
        "clean")
            clean_up
            ;;
        "health")
            check_health
            ;;
        "pipeline")
            run_pipeline
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function
main "$@"







