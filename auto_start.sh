#!/bin/bash

# 🚀 Script de Démarrage Automatique du Système Fear & Greed Index
# Lance le backend et le frontend en arrière-plan

echo "========================================================================"
echo "🚀 DÉMARRAGE AUTOMATIQUE DU SYSTÈME"
echo "========================================================================"
echo ""

# Répertoires
ROOT_DIR="/Volumes/YAHYA SSD/Documents/fear and"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Clé API OpenAI
export OPENAI_API_KEY='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'

echo "📊 Démarrage du Backend..."
cd "$BACKEND_DIR"
source .venv/bin/activate

# Démarrer le backend en arrière-plan
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$ROOT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$ROOT_DIR/backend.pid"

echo "✅ Backend démarré (PID: $BACKEND_PID)"
echo "   URL : http://localhost:8000"
echo "   Logs : $ROOT_DIR/backend.log"
echo ""

# Attendre que le backend soit prêt
sleep 3

echo "🎨 Démarrage du Frontend..."
cd "$FRONTEND_DIR"

# Démarrer le frontend en arrière-plan
nohup npm run dev > "$ROOT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$ROOT_DIR/frontend.pid"

echo "✅ Frontend démarré (PID: $FRONTEND_PID)"
echo "   URL : http://localhost:3000"
echo "   Logs : $ROOT_DIR/frontend.log"
echo ""

echo "========================================================================"
echo "✅ SYSTÈME DÉMARRÉ AVEC SUCCÈS !"
echo "========================================================================"
echo ""
echo "📊 Dashboard : http://localhost:3000/dashboard"
echo "🔧 API : http://localhost:8000/docs"
echo ""
echo "📝 Logs :"
echo "   Backend : tail -f \"$ROOT_DIR/backend.log\""
echo "   Frontend : tail -f \"$ROOT_DIR/frontend.log\""
echo ""
echo "🛑 Pour arrêter le système :"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   # ou"
echo "   kill \$(cat \"$ROOT_DIR/backend.pid\" \"$ROOT_DIR/frontend.pid\")"
echo ""
echo "🔄 Le système se met à jour automatiquement toutes les 10 minutes"
echo ""
echo "🎉 Profitez de votre Fear & Greed Index !"
echo "========================================================================"

