#!/bin/bash

#############################################
# 🛑 ARRÊT COMPLET DU SAAS + FEAR & GREED
#############################################

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛑 Arrêt du SaaS CasaTrader + Fear & Greed Index"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

CURRENT_DIR="/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"

#############################################
# 1. ARRÊTER LE BACKEND (PORT 8001)
#############################################

echo "🔧 Arrêt du backend Fear & Greed (port 8001)..."

if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    BACKEND_PID=$(lsof -ti:8001)
    echo "   Arrêt du processus $BACKEND_PID..."
    kill -9 $BACKEND_PID 2>/dev/null || true
    echo "   ✅ Backend arrêté"
else
    echo "   ℹ️  Aucun backend en cours d'exécution"
fi

# Supprimer le fichier PID
rm -f "$CURRENT_DIR/logs/backend.pid"

echo ""

#############################################
# 2. ARRÊTER LE FRONTEND (PORT 8080)
#############################################

echo "🎨 Arrêt du frontend SaaS (port 8080)..."

if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    FRONTEND_PID=$(lsof -ti:8080)
    echo "   Arrêt du processus $FRONTEND_PID..."
    kill -9 $FRONTEND_PID 2>/dev/null || true
    echo "   ✅ Frontend arrêté"
else
    echo "   ℹ️  Aucun frontend en cours d'exécution"
fi

# Supprimer le fichier PID
rm -f "$CURRENT_DIR/logs/frontend.pid"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Tous les serveurs sont arrêtés !"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Pour redémarrer : ./start_all.sh"
echo ""

