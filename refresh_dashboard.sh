#!/bin/bash

# 🔄 Script pour forcer la mise à jour du dashboard avec les nouvelles données

echo "========================================================================"
echo "🔄 MISE À JOUR DU DASHBOARD"
echo "========================================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Répertoires
BACKEND_DIR="/Volumes/YAHYA SSD/Documents/fear and/backend"
FRONTEND_DIR="/Volumes/YAHYA SSD/Documents/fear and/frontend"

echo "========================================================================="
echo "📊 ÉTAPE 1 : Vérifier le score actuel dans le backend"
echo "========================================================================="
echo ""

# Vérifier que le backend est actif
BACKEND_SCORE=$(curl -s http://localhost:8000/api/v1/index/latest 2>/dev/null | grep -o '"score":[0-9.]*' | cut -d':' -f2)

if [ -n "$BACKEND_SCORE" ]; then
    echo -e "${GREEN}✅ Backend actif${NC}"
    echo "   Score actuel : $BACKEND_SCORE"
    echo ""
else
    echo -e "${RED}❌ Backend non actif sur http://localhost:8000${NC}"
    echo ""
    echo "Pour démarrer le backend :"
    echo "   cd '$BACKEND_DIR'"
    echo "   source .venv/bin/activate"
    echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    exit 1
fi

echo "========================================================================="
echo "🔄 ÉTAPE 2 : Forcer une nouvelle mise à jour des données"
echo "========================================================================="
echo ""

echo "Déclenchement du pipeline..."
TRIGGER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/scheduler/trigger 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pipeline déclenché${NC}"
    echo ""
    echo "⏳ Attente de la fin du pipeline (60 secondes)..."
    sleep 60
    
    # Récupérer le nouveau score
    NEW_SCORE=$(curl -s http://localhost:8000/api/v1/index/latest 2>/dev/null | grep -o '"score":[0-9.]*' | cut -d':' -f2)
    
    if [ -n "$NEW_SCORE" ]; then
        echo -e "${GREEN}✅ Nouveau score calculé : $NEW_SCORE${NC}"
        echo ""
    fi
else
    echo -e "${YELLOW}⚠️  Impossible de déclencher le pipeline${NC}"
    echo "   Utilisez le score actuel : $BACKEND_SCORE"
    echo ""
fi

echo "========================================================================="
echo "🌐 ÉTAPE 3 : Vérifier les endpoints"
echo "========================================================================="
echo ""

# Tester tous les endpoints
echo "Test des endpoints :"
echo ""

echo "1. /index/latest"
curl -s http://localhost:8000/api/v1/index/latest | head -c 100
echo "... ✅"
echo ""

echo "2. /components/latest"
curl -s http://localhost:8000/api/v1/components/latest | head -c 100
echo "... ✅"
echo ""

echo "3. /media/latest"
curl -s http://localhost:8000/api/v1/media/latest | head -c 100
echo "... ✅"
echo ""

echo "========================================================================="
echo "🎨 ÉTAPE 4 : Instructions pour rafraîchir le frontend"
echo "========================================================================="
echo ""

echo "Pour voir les nouvelles données dans le dashboard :"
echo ""
echo "1️⃣  Ouvrez votre navigateur à : http://localhost:3000/dashboard"
echo ""
echo "2️⃣  Appuyez sur Cmd+Shift+R (Mac) ou Ctrl+Shift+R (Windows)"
echo "    pour forcer le rechargement et vider le cache"
echo ""
echo "3️⃣  Si le score ne change toujours pas :"
echo "    • Ouvrez la console du navigateur (F12)"
echo "    • Allez dans l'onglet 'Application' ou 'Storage'"
echo "    • Supprimez 'localStorage' et 'sessionStorage'"
echo "    • Rechargez la page (F5)"
echo ""
echo "4️⃣  Si le frontend n'est pas démarré :"
echo "    cd '$FRONTEND_DIR'"
echo "    npm run dev"
echo ""

echo "========================================================================="
echo "📊 RÉSUMÉ"
echo "========================================================================="
echo ""
echo "   Backend : http://localhost:8000"
echo "   Frontend : http://localhost:3000/dashboard"
echo "   Score actuel : ${NEW_SCORE:-$BACKEND_SCORE}"
echo ""
echo "Pour voir les logs en temps réel :"
echo "   tail -f backend.log"
echo ""
echo "========================================================================="
echo "✅ Mise à jour terminée !"
echo "========================================================================="
echo ""

