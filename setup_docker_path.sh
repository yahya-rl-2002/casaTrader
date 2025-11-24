#!/bin/bash

# Script pour configurer Docker depuis le SSD externe

SSD_PATH="/Volumes/YAHYA SSD"
DOCKER_APP="$SSD_PATH/Applications/Docker.app"

if [ ! -d "$DOCKER_APP" ]; then
    echo "❌ Docker.app non trouvé dans $SSD_PATH/Applications/"
    exit 1
fi

echo "✅ Docker trouvé sur le SSD externe"
echo ""

# Ajouter au PATH pour cette session
export PATH="$DOCKER_APP/Contents/Resources/bin:$PATH"

# Vérifier
if command -v docker &> /dev/null; then
    echo "✅ Docker accessible:"
    docker --version
    docker-compose --version
    echo ""
    echo "💡 Pour rendre permanent, ajoutez à ~/.zshrc:"
    echo "   export PATH=\"$DOCKER_APP/Contents/Resources/bin:\$PATH\""
else
    echo "⚠️  Docker non accessible dans le PATH"
fi
