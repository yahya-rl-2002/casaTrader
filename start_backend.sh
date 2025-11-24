#!/bin/bash

echo "🚀 Démarrage du Backend Fear & Greed Index"
echo "=========================================="

cd "/Volumes/YAHYA SSD/Documents/fear and/backend"

# Activer l'environnement virtuel
source .venv/bin/activate

# Vérifier si la DB existe, sinon l'initialiser
if [ ! -f "fear_greed.db" ]; then
    echo "📊 Initialisation de la base de données..."
    python init_db.py
fi

echo ""
echo "✅ Backend démarré sur http://localhost:8000"
echo "📚 Documentation API: http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

# Démarrer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000








