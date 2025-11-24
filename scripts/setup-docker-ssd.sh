#!/bin/bash

# Script pour configurer Docker depuis le SSD externe
# Usage: source scripts/setup-docker-ssd.sh

SSD_PATH="/Volumes/YAHYA SSD"
DOCKER_APP="$SSD_PATH/Applications/Docker.app"
DOCKER_BIN="$DOCKER_APP/Contents/Resources/bin"

echo "🐳 Configuration Docker depuis SSD externe"
echo "=========================================="
echo ""

# Vérifier que Docker existe
if [ ! -d "$DOCKER_APP" ]; then
    echo "❌ Docker.app non trouvé dans $SSD_PATH/Applications/"
    exit 1
fi

echo "✅ Docker trouvé: $DOCKER_APP"
echo ""

# Ajouter au PATH pour cette session
export PATH="$DOCKER_BIN:$PATH"

# Vérifier les versions
echo "📋 Versions:"
if command -v docker &> /dev/null; then
    docker --version
else
    echo "❌ docker non trouvé"
fi

if command -v docker-compose &> /dev/null; then
    docker-compose --version
elif docker compose version &>/dev/null; then
    docker compose version
else
    echo "❌ docker-compose non trouvé"
fi

echo ""

# Vérifier si Docker est en cours d'exécution
if docker info &>/dev/null; then
    echo "✅ Docker est en cours d'exécution"
else
    echo "⚠️  Docker Desktop n'est pas lancé"
    echo "🚀 Lancement de Docker Desktop..."
    open "$DOCKER_APP"
    echo "⏳ Attendez que Docker démarre (icône dans la barre de menu)"
    echo ""
    echo "Vérifiez avec: docker info"
fi

echo ""
echo "💡 Pour rendre permanent, ajoutez à ~/.zshrc:"
echo "   export PATH=\"$DOCKER_BIN:\$PATH\""
echo ""
echo "   Ou sourcez ce script:"
echo "   source scripts/setup-docker-ssd.sh"



