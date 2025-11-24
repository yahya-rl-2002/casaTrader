#!/bin/bash

# 🚀 Script de démarrage du système Fear & Greed Index
# Bourse de Casablanca

echo "================================================================================"
echo "  🚀 Démarrage du Système Fear & Greed Index"
echo "  Bourse de Casablanca"
echo "================================================================================"
echo ""

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_step() {
    echo -e "${BLUE}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

# Vérifier que nous sommes dans le bon répertoire
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Répertoire projet non trouvé: $PROJECT_DIR"
    exit 1
fi

print_success "Répertoire projet trouvé"

# Vérifier les dépendances
print_step "Vérification des dépendances..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé"
    exit 1
fi
print_success "Python $(python3 --version) installé"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js n'est pas installé"
    exit 1
fi
print_success "Node.js $(node --version) installé"

# Démarrer le backend
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
print_step "Démarrage du Backend (FastAPI)..."
echo "───────────────────────────────────────────────────────────────────────────────"

cd "$PROJECT_DIR/backend" || exit 1

# Activer l'environnement virtuel
if [ ! -d ".venv" ]; then
    print_error "Environnement virtuel non trouvé. Créer avec: python3 -m venv .venv"
    exit 1
fi

source .venv/bin/activate
print_success "Environnement virtuel activé"

# Démarrer uvicorn en arrière-plan
print_step "Lancement de l'API sur http://127.0.0.1:8000"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > /tmp/fear-greed-backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > /tmp/fear-greed-backend.pid

sleep 3

# Vérifier que le backend démarre correctement
if ps -p $BACKEND_PID > /dev/null; then
    print_success "Backend démarré (PID: $BACKEND_PID)"
    print_success "API disponible sur: http://127.0.0.1:8000"
    print_success "Documentation: http://127.0.0.1:8000/docs"
else
    print_error "Échec du démarrage du backend"
    cat /tmp/fear-greed-backend.log
    exit 1
fi

# Démarrer le frontend
echo ""
echo "───────────────────────────────────────────────────────────────────────────────"
print_step "Démarrage du Frontend (Next.js)..."
echo "───────────────────────────────────────────────────────────────────────────────"

cd "$PROJECT_DIR/frontend" || exit 1

# Vérifier node_modules
if [ ! -d "node_modules" ]; then
    print_warning "node_modules non trouvé. Installation des dépendances..."
    npm install
fi

# Démarrer Next.js en arrière-plan
print_step "Lancement du dashboard sur http://localhost:3000"
npm run dev > /tmp/fear-greed-frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > /tmp/fear-greed-frontend.pid

sleep 5

# Vérifier que le frontend démarre correctement
if ps -p $FRONTEND_PID > /dev/null; then
    print_success "Frontend démarré (PID: $FRONTEND_PID)"
    print_success "Dashboard disponible sur: http://localhost:3000"
else
    print_error "Échec du démarrage du frontend"
    cat /tmp/fear-greed-frontend.log
    # Arrêter le backend
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Résumé final
echo ""
echo "================================================================================"
echo "  ✅ Système Fear & Greed Index Démarré"
echo "================================================================================"
echo ""
echo "  📊 Dashboard:       http://localhost:3000"
echo "  🔌 API Backend:     http://127.0.0.1:8000"
echo "  📚 Documentation:   http://127.0.0.1:8000/docs"
echo ""
echo "  🔄 Automatisation:"
echo "     ✅ Mise à jour automatique toutes les 10 minutes"
echo "     📡 Scheduler actif dès le démarrage"
echo "     🎛️  Contrôle: http://127.0.0.1:8000/api/v1/scheduler/status"
echo ""
echo "  📁 Logs:"
echo "     Backend:  /tmp/fear-greed-backend.log"
echo "     Frontend: /tmp/fear-greed-frontend.log"
echo ""
echo "  🛑 Pour arrêter le système:"
echo "     ./stop_system.sh"
echo "     ou:"
echo "     kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "================================================================================"
echo ""

# Ouvrir le dashboard dans le navigateur (optionnel)
if command -v open &> /dev/null; then
    sleep 2
    print_step "Ouverture du dashboard dans le navigateur..."
    open http://localhost:3000
fi

print_success "Système prêt ! Appuyez sur Ctrl+C pour arrêter"

# Garder le script actif et surveiller les processus
trap "echo ''; print_warning 'Arrêt du système...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm /tmp/fear-greed-*.pid 2>/dev/null; print_success 'Système arrêté'; exit 0" INT TERM

# Attendre que les processus se terminent
wait $BACKEND_PID $FRONTEND_PID

