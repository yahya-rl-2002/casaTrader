#!/bin/bash

# Wrapper pour docker-compose qui utilise docker compose (plugin) si disponible

# Ajouter Docker au PATH si sur SSD externe
if [ -d "/Volumes/YAHYA SSD/Applications/Docker.app" ]; then
    export PATH="/Volumes/YAHYA SSD/Applications/Docker.app/Contents/Resources/bin:$PATH"
fi

# Essayer docker compose (plugin) d'abord
if docker compose version &>/dev/null; then
    docker compose "$@"
# Sinon essayer docker-compose (standalone)
elif command -v docker-compose &>/dev/null; then
    docker-compose "$@"
else
    echo "❌ docker-compose non trouvé"
    exit 1
fi
