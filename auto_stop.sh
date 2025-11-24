#!/bin/bash

# 🛑 Script d'Arrêt du Système Fear & Greed Index

echo "========================================================================"
echo "🛑 ARRÊT DU SYSTÈME"
echo "========================================================================"
echo ""

ROOT_DIR="/Volumes/YAHYA SSD/Documents/fear and"

# Vérifier si les fichiers PID existent
if [ -f "$ROOT_DIR/backend.pid" ] || [ -f "$ROOT_DIR/frontend.pid" ]; then
    
    # Arrêter le backend
    if [ -f "$ROOT_DIR/backend.pid" ]; then
        BACKEND_PID=$(cat "$ROOT_DIR/backend.pid")
        echo "🛑 Arrêt du Backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null && echo "✅ Backend arrêté" || echo "⚠️  Backend déjà arrêté"
        rm "$ROOT_DIR/backend.pid"
    fi
    
    # Arrêter le frontend
    if [ -f "$ROOT_DIR/frontend.pid" ]; then
        FRONTEND_PID=$(cat "$ROOT_DIR/frontend.pid")
        echo "🛑 Arrêt du Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null && echo "✅ Frontend arrêté" || echo "⚠️  Frontend déjà arrêté"
        rm "$ROOT_DIR/frontend.pid"
    fi
    
    echo ""
    echo "========================================================================"
    echo "✅ SYSTÈME ARRÊTÉ"
    echo "========================================================================"
    
else
    echo "⚠️  Aucun processus en cours (fichiers PID introuvables)"
    echo ""
    echo "Voulez-vous tuer tous les processus sur les ports 8000 et 3000 ? (o/n)"
    read -r response
    
    if [ "$response" = "o" ]; then
        echo ""
        echo "🛑 Arrêt forcé..."
        
        # Tuer le processus sur le port 8000 (backend)
        if lsof -ti:8000 > /dev/null 2>&1; then
            kill -9 $(lsof -ti:8000) && echo "✅ Backend (port 8000) arrêté"
        fi
        
        # Tuer le processus sur le port 3000 (frontend)
        if lsof -ti:3000 > /dev/null 2>&1; then
            kill -9 $(lsof -ti:3000) && echo "✅ Frontend (port 3000) arrêté"
        fi
        
        echo ""
        echo "✅ Arrêt forcé terminé"
    fi
fi

echo ""

