#!/bin/bash

# Script de health check complet
# Usage: ./scripts/health-check.sh [--verbose]

set -e

VERBOSE=false
if [[ "$1" == "--verbose" ]]; then
  VERBOSE=true
fi

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Compteurs
TOTAL=0
PASSED=0
FAILED=0

check_service() {
  local name=$1
  local url=$2
  local expected_status=${3:-200}
  
  TOTAL=$((TOTAL + 1))
  
  if [ "$VERBOSE" = true ]; then
    echo -n "Vérification $name... "
  fi
  
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" || echo "000")
  
  if [ "$HTTP_CODE" = "$expected_status" ]; then
    if [ "$VERBOSE" = true ]; then
      echo -e "${GREEN}✅ OK${NC}"
    fi
    PASSED=$((PASSED + 1))
    return 0
  else
    if [ "$VERBOSE" = true ]; then
      echo -e "${RED}❌ FAILED (HTTP $HTTP_CODE)${NC}"
    fi
    FAILED=$((FAILED + 1))
    return 1
  fi
}

check_docker() {
  local container=$1
  
  TOTAL=$((TOTAL + 1))
  
  if [ "$VERBOSE" = true ]; then
    echo -n "Vérification Docker $container... "
  fi
  
  if docker ps | grep -q "$container"; then
    STATUS=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "unknown")
    if [ "$STATUS" = "running" ]; then
      if [ "$VERBOSE" = true ]; then
        echo -e "${GREEN}✅ Running${NC}"
      fi
      PASSED=$((PASSED + 1))
      return 0
    else
      if [ "$VERBOSE" = true ]; then
        echo -e "${RED}❌ Not running (status: $STATUS)${NC}"
      fi
      FAILED=$((FAILED + 1))
      return 1
    fi
  else
    if [ "$VERBOSE" = true ]; then
      echo -e "${RED}❌ Container not found${NC}"
    fi
    FAILED=$((FAILED + 1))
    return 1
  fi
}

echo "🏥 Health Check - Fear & Greed Index"
echo "======================================"
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
  echo -e "${RED}❌ Docker non installé${NC}"
  exit 1
fi

# Vérifier les conteneurs Docker
check_docker "fear-greed-backend"
check_docker "fear-greed-postgres"
check_docker "fear-greed-redis"

# Vérifier les endpoints
echo ""
echo "📡 Vérification des endpoints..."

check_service "Backend Health" "http://localhost:8001/api/v1/health/ping"
check_service "Backend API" "http://localhost:8001/api/v1/index/latest"
check_service "Monitoring" "http://localhost:8001/api/v1/monitoring/health"

# Vérifier la base de données
echo ""
echo "🗄️  Vérification base de données..."

if docker ps | grep -q fear-greed-postgres; then
  TOTAL=$((TOTAL + 1))
  if docker exec fear-greed-postgres pg_isready -U fear_greed_user -d fear_greed_db &>/dev/null; then
    if [ "$VERBOSE" = true ]; then
      echo -e "${GREEN}✅ PostgreSQL ready${NC}"
    fi
    PASSED=$((PASSED + 1))
  else
    if [ "$VERBOSE" = true ]; then
      echo -e "${RED}❌ PostgreSQL not ready${NC}"
    fi
    FAILED=$((FAILED + 1))
  fi
fi

# Vérifier Redis
if docker ps | grep -q fear-greed-redis; then
  TOTAL=$((TOTAL + 1))
  if docker exec fear-greed-redis redis-cli ping &>/dev/null; then
    if [ "$VERBOSE" = true ]; then
      echo -e "${GREEN}✅ Redis ready${NC}"
    fi
    PASSED=$((PASSED + 1))
  else
    if [ "$VERBOSE" = true ]; then
      echo -e "${RED}❌ Redis not ready${NC}"
    fi
    FAILED=$((FAILED + 1))
  fi
fi

# Résumé
echo ""
echo "======================================"
echo "Résumé:"
echo "  Total: $TOTAL"
echo -e "  ${GREEN}✅ Réussis: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
  echo -e "  ${RED}❌ Échoués: $FAILED${NC}"
  exit 1
else
  echo -e "  ${GREEN}✅ Tous les checks passés !${NC}"
  exit 0
fi



