#!/bin/bash
echo "🔄 Redémarrage du backend..."
cd backend
source .venv/bin/activate
echo "✅ Environnement activé"
echo "🚀 Démarrage du backend sur le port 8001..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
