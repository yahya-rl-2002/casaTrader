#!/bin/bash

# 🛑 Script d'arrêt du système Fear & Greed Index

echo "================================================================================"
echo "  🛑 Arrêt du Système Fear & Greed Index"
echo "================================================================================"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_step() {
    echo -e "➜ $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

# Arrêter le backend
if [ -f /tmp/fear-greed-backend.pid ]; then
    BACKEND_PID=$(cat /tmp/fear-greed-backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        print_step "Arrêt du backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        sleep 1
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID 2>/dev/null
        fi
        print_success "Backend arrêté"
    else
        print_warning "Backend déjà arrêté"
    fi
    rm /tmp/fear-greed-backend.pid
else
    print_warning "Aucun PID backend trouvé"
fi

# Arrêter le frontend
if [ -f /tmp/fear-greed-frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/fear-greed-frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_step "Arrêt du frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        sleep 1
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
        print_success "Frontend arrêté"
    else
        print_warning "Frontend déjà arrêté"
    fi
    rm /tmp/fear-greed-frontend.pid
else
    print_warning "Aucun PID frontend trouvé"
fi

# Nettoyage des logs (optionnel)
if [ "$1" == "--clean" ]; then
    print_step "Nettoyage des logs..."
    rm -f /tmp/fear-greed-backend.log /tmp/fear-greed-frontend.log
    print_success "Logs supprimés"
fi

echo ""
echo "================================================================================"
echo "  ✅ Système Arrêté"
echo "================================================================================"
echo ""







