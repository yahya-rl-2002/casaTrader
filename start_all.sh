#!/bin/bash

#############################################
# 🚀 DÉMARRAGE COMPLET DU SAAS + FEAR & GREED
#############################################

set -e  # Arrêter en cas d'erreur

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Démarrage du SaaS CasaTrader + Fear & Greed Index"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Répertoire actuel
CURRENT_DIR="/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
BACKEND_DIR="$CURRENT_DIR/backend"

# Fichiers de logs
FRONTEND_LOG="$CURRENT_DIR/logs/frontend.log"
BACKEND_LOG="$CURRENT_DIR/logs/backend.log"

# Créer le dossier de logs
mkdir -p "$CURRENT_DIR/logs"

# Nettoyer les anciens logs
> "$FRONTEND_LOG"
> "$BACKEND_LOG"

echo "📁 Répertoire SaaS    : $CURRENT_DIR"
echo "📁 Répertoire Backend : $BACKEND_DIR"
echo ""

#############################################
# 1. DÉMARRER LE BACKEND FEAR & GREED (PORT 8001)
#############################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 ÉTAPE 1/2 : Démarrage du Backend Fear & Greed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Vérifier si le backend est déjà en cours
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Le port 8001 est déjà utilisé"
    echo "   🔫 Arrêt du processus existant sur le port 8001..."
    lsof -ti:8001 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

echo "🐍 Activation de l'environnement virtuel Python..."
cd "$BACKEND_DIR"

if [ ! -d ".venv" ]; then
    echo "❌ ERREUR : L'environnement virtuel .venv n'existe pas"
    echo "   Veuillez d'abord installer les dépendances :"
    echo "   cd \"$BACKEND_DIR\" && poetry install"
    exit 1
fi

source .venv/bin/activate

echo "🔑 Configuration de la clé API OpenAI..."
# ⚠️  SÉCURITÉ : La clé API doit être dans .env, pas ici !
if [ -z "$OPENAI_API_KEY" ]; then
    if [ -f "$BACKEND_DIR/.env" ]; then
        # Charger depuis .env si disponible
        export $(grep -v '^#' "$BACKEND_DIR/.env" | xargs)
    else
        echo "⚠️  WARNING: OPENAI_API_KEY non définie. Créez un fichier .env dans backend/"
        echo "   Exemple: echo 'OPENAI_API_KEY=sk-proj-...' > $BACKEND_DIR/.env"
    fi
fi

echo "🚀 Lancement du serveur backend sur http://0.0.0.0:8001 ..."
uvicorn app.main:app --host 0.0.0.0 --port 8001 >> "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!

echo "   PID: $BACKEND_PID"
echo "   Logs: $BACKEND_LOG"

# Attendre que le backend soit prêt
echo "   ⏳ Attente du démarrage du backend..."
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo "   ✅ Backend démarré avec succès !"
else
    echo "   ❌ ERREUR : Le backend n'a pas démarré correctement"
    echo "   Consultez les logs : tail -f $BACKEND_LOG"
    exit 1
fi

echo ""

#############################################
# 2. DÉMARRER LE FRONTEND SAAS (PORT 8080)
#############################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎨 ÉTAPE 2/2 : Démarrage du Frontend SaaS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$CURRENT_DIR"

# Vérifier si le frontend est déjà en cours
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Le port 8080 est déjà utilisé"
    echo "   🔫 Arrêt du processus existant sur le port 8080..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

echo "🎨 Lancement du serveur frontend sur http://localhost:8080 ..."
npm run dev >> "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!

echo "   PID: $FRONTEND_PID"
echo "   Logs: $FRONTEND_LOG"

# Attendre que le frontend soit prêt
echo "   ⏳ Attente du démarrage du frontend..."
sleep 4

if ps -p $FRONTEND_PID > /dev/null; then
    echo "   ✅ Frontend démarré avec succès !"
else
    echo "   ❌ ERREUR : Le frontend n'a pas démarré correctement"
    echo "   Consultez les logs : tail -f $FRONTEND_LOG"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TOUS LES SERVEURS SONT DÉMARRÉS !"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Accès aux services :"
echo ""
echo "   📊 SaaS CasaTrader       : http://localhost:8080"
echo "   📈 Fear & Greed Index    : http://localhost:8080/fear-greed"
echo "   📉 Fear & Greed Dashboard: http://localhost:8080/fear-greed-dashboard"
echo "   🔌 API Backend           : http://localhost:8001/api/v1"
echo ""
echo "📋 PIDs des processus :"
echo "   Backend  : $BACKEND_PID"
echo "   Frontend : $FRONTEND_PID"
echo ""
echo "📝 Logs en temps réel :"
echo "   Backend  : tail -f $BACKEND_LOG"
echo "   Frontend : tail -f $FRONTEND_LOG"
echo ""
echo "🛑 Pour arrêter tous les serveurs :"
echo "   ./stop_all.sh"
echo "   OU"
echo "   lsof -ti:8001,8080 | xargs kill -9"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Prêt à l'emploi ! Ouvrez http://localhost:8080 dans votre navigateur !"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Sauvegarder les PIDs pour stop_all.sh
echo "$BACKEND_PID" > "$CURRENT_DIR/logs/backend.pid"
echo "$FRONTEND_PID" > "$CURRENT_DIR/logs/frontend.pid"

