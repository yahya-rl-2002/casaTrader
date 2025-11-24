#!/bin/bash

# 🤖 Démarrage du système Fear & Greed Index avec LLM Sentiment Analysis
# Ce script démarre le backend avec le LLM activé et le frontend

echo "========================================================================"
echo "🤖 FEAR & GREED INDEX - Démarrage avec LLM"
echo "========================================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier la clé API OpenAI
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}❌ ERREUR : La variable OPENAI_API_KEY n'est pas définie !${NC}"
    echo ""
    echo "Pour utiliser le LLM, vous devez configurer votre clé API OpenAI :"
    echo ""
    echo -e "${YELLOW}   export OPENAI_API_KEY='sk-proj-...'${NC}"
    echo ""
    echo "Puis relancez ce script."
    echo ""
    echo "Pour obtenir une clé API :"
    echo "   https://platform.openai.com/api-keys"
    echo ""
    read -p "Voulez-vous continuer sans LLM (dictionnaire) ? (o/n) : " continue_without_llm
    if [ "$continue_without_llm" != "o" ]; then
        echo "Arrêt du script."
        exit 1
    fi
    echo ""
    echo -e "${YELLOW}⚠️  Démarrage sans LLM (dictionnaire uniquement)${NC}"
    echo ""
else
    echo -e "${GREEN}✅ Clé API OpenAI configurée${NC}"
    echo "   Clé : ${OPENAI_API_KEY:0:20}..."
    echo ""
fi

# Répertoires
BACKEND_DIR="/Volumes/YAHYA SSD/Documents/fear and/backend"
FRONTEND_DIR="/Volumes/YAHYA SSD/Documents/fear and/frontend"
ROOT_DIR="/Volumes/YAHYA SSD/Documents/fear and"
PID_FILE="$ROOT_DIR/.system_pids"

# Créer le fichier de PIDs
touch "$PID_FILE"

echo "========================================================================="
echo "📦 ÉTAPE 1 : Démarrage du Backend (FastAPI + LLM)"
echo "========================================================================="
echo ""

# Vérifier que le backend existe
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}❌ ERREUR : Le répertoire backend n'existe pas !${NC}"
    exit 1
fi

cd "$BACKEND_DIR"

# Vérifier l'environnement virtuel
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé, création...${NC}"
    poetry install
fi

# Activer l'environnement virtuel et démarrer le backend
echo -e "${BLUE}🚀 Démarrage du serveur backend sur http://localhost:8000${NC}"
echo ""

source .venv/bin/activate

# Démarrer le backend en arrière-plan
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > "$ROOT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "backend:$BACKEND_PID" > "$PID_FILE"

echo -e "${GREEN}✅ Backend démarré (PID: $BACKEND_PID)${NC}"
echo "   URL : http://localhost:8000"
echo "   Docs : http://localhost:8000/docs"
echo "   Logs : $ROOT_DIR/backend.log"
echo ""

# Attendre que le backend soit prêt
echo "⏳ Attente du backend (max 30s)..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend prêt !${NC}"
        break
    fi
    sleep 1
done
echo ""

echo "========================================================================="
echo "🎨 ÉTAPE 2 : Démarrage du Frontend (Next.js)"
echo "========================================================================="
echo ""

# Vérifier que le frontend existe
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ ERREUR : Le répertoire frontend n'existe pas !${NC}"
    exit 1
fi

cd "$FRONTEND_DIR"

# Vérifier node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules non trouvé, installation...${NC}"
    npm install
fi

# Démarrer le frontend en arrière-plan
echo -e "${BLUE}🚀 Démarrage du serveur frontend sur http://localhost:3000${NC}"
echo ""

npm run dev > "$ROOT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "frontend:$FRONTEND_PID" >> "$PID_FILE"

echo -e "${GREEN}✅ Frontend démarré (PID: $FRONTEND_PID)${NC}"
echo "   URL : http://localhost:3000"
echo "   Logs : $ROOT_DIR/frontend.log"
echo ""

# Attendre que le frontend soit prêt
echo "⏳ Attente du frontend (max 30s)..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend prêt !${NC}"
        break
    fi
    sleep 1
done
echo ""

echo "========================================================================="
echo "🤖 ÉTAPE 3 : Configuration du LLM Sentiment Analysis"
echo "========================================================================="
echo ""

if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  LLM non configuré${NC}"
    echo "   Le système utilisera l'analyse de sentiment par dictionnaire"
    echo ""
    echo "   Pour activer le LLM :"
    echo "   1. Obtenez une clé API sur https://platform.openai.com/api-keys"
    echo "   2. Exécutez : export OPENAI_API_KEY='sk-proj-...'"
    echo "   3. Relancez ce script"
    echo ""
else
    echo -e "${GREEN}✅ LLM Sentiment Analysis activé${NC}"
    echo "   Modèle : gpt-4o-mini"
    echo "   Coût estimé : ~$0.20/mois"
    echo ""
    echo "   Le système analysera automatiquement les articles avec l'IA"
    echo "   pour un sentiment plus précis et contextuel."
    echo ""
fi

echo "========================================================================="
echo "⏰ ÉTAPE 4 : Scheduler automatique"
echo "========================================================================="
echo ""

echo -e "${GREEN}✅ Scheduler actif${NC}"
echo "   Fréquence : Toutes les 10 minutes"
echo "   Prochain update : Dans 10 minutes"
echo ""
echo "   Le système mettra à jour automatiquement :"
echo "   - Les données du marché (MASI)"
echo "   - Les articles de presse (4 sources)"
if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "   - L'analyse de sentiment avec GPT 🤖"
else
    echo "   - L'analyse de sentiment (dictionnaire) 📚"
fi
echo "   - Le score Fear & Greed Index"
echo ""

echo "========================================================================="
echo "🎉 SYSTÈME DÉMARRÉ AVEC SUCCÈS !"
echo "========================================================================="
echo ""
echo "📊 Dashboard : http://localhost:3000/dashboard"
echo "🔧 API Backend : http://localhost:8000/docs"
echo ""
echo "Pour arrêter le système :"
echo "   ./stop_system.sh"
echo ""
echo "Pour surveiller les logs :"
echo "   tail -f $ROOT_DIR/backend.log"
echo "   tail -f $ROOT_DIR/frontend.log"
echo ""

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}🤖 LLM Sentiment Analysis : ACTIF${NC}"
    echo ""
    echo "Pour tester le LLM manuellement :"
    echo "   cd \"$BACKEND_DIR\""
    echo "   source .venv/bin/activate"
    echo "   python test_llm_sentiment.py"
    echo ""
fi

echo "Pour lancer une mise à jour manuelle maintenant :"
echo "   curl -X POST http://localhost:8000/api/v1/scheduler/trigger"
echo ""

# Ouvrir le navigateur (optionnel)
sleep 3
if command -v open &> /dev/null; then
    echo "🌐 Ouverture du navigateur..."
    open http://localhost:3000/dashboard
fi

echo "========================================================================="
echo "Système en cours d'exécution. Appuyez sur Ctrl+C pour arrêter."
echo "========================================================================="

# Garder le script en vie
wait

