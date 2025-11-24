#!/bin/bash

# 🚀 Script de démarrage rapide pour le Fear & Greed Index
# Pour intégration dans votre SaaS

clear

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   FEAR & GREED INDEX - Bourse de Casablanca                    ║"
echo "║   Démarrage rapide pour intégration SaaS                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"

echo -e "${BLUE}📍 Répertoire du projet : ${PROJECT_DIR}${NC}"
echo ""

# Menu interactif
echo "Que voulez-vous faire ?"
echo ""
echo "1. 🚀 Démarrer le système complet (Backend + Frontend)"
echo "2. 🔧 Démarrer uniquement le Backend (API)"
echo "3. 🎨 Démarrer uniquement le Frontend"
echo "4. 📦 Installer les dépendances"
echo "5. 🧪 Tester le LLM"
echo "6. 📊 Voir le dernier score"
echo "7. 📚 Ouvrir la documentation"
echo "8. ❌ Quitter"
echo ""

read -p "Votre choix (1-8) : " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 Démarrage du système complet...${NC}"
        echo ""
        
        # Vérifier la clé API
        if [ -z "$OPENAI_API_KEY" ]; then
            echo -e "${YELLOW}⚠️  Clé API OpenAI non configurée${NC}"
            read -p "Voulez-vous configurer la clé API maintenant ? (o/n) : " configure_key
            
            if [ "$configure_key" = "o" ]; then
                source "$PROJECT_DIR/set_api_key.sh"
            else
                echo -e "${YELLOW}⚠️  Le système démarrera sans LLM (dictionnaire uniquement)${NC}"
                echo ""
            fi
        fi
        
        cd "$PROJECT_DIR"
        ./start_with_llm.sh
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}🔧 Démarrage du Backend uniquement...${NC}"
        echo ""
        
        cd "$PROJECT_DIR/backend"
        
        # Vérifier l'environnement virtuel
        if [ ! -d ".venv" ]; then
            echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé. Installation...${NC}"
            poetry install || (python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
        fi
        
        source .venv/bin/activate
        
        # Configurer la clé API si nécessaire
        if [ -z "$OPENAI_API_KEY" ]; then
            export OPENAI_API_KEY='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'
        fi
        
        echo -e "${GREEN}✅ Backend démarré sur http://localhost:8000${NC}"
        echo -e "${BLUE}📖 Documentation API : http://localhost:8000/docs${NC}"
        echo ""
        
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
        
    3)
        echo ""
        echo -e "${GREEN}🎨 Démarrage du Frontend uniquement...${NC}"
        echo ""
        
        cd "$PROJECT_DIR/frontend"
        
        # Vérifier node_modules
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}⚠️  node_modules non trouvé. Installation...${NC}"
            npm install
        fi
        
        echo -e "${GREEN}✅ Frontend démarré sur http://localhost:3000${NC}"
        echo ""
        
        npm run dev
        ;;
        
    4)
        echo ""
        echo -e "${GREEN}📦 Installation des dépendances...${NC}"
        echo ""
        
        # Backend
        echo -e "${BLUE}🔧 Installation Backend...${NC}"
        cd "$PROJECT_DIR/backend"
        
        if command -v poetry &> /dev/null; then
            poetry install
        else
            python3 -m venv .venv
            source .venv/bin/activate
            pip install -r requirements.txt
        fi
        
        echo -e "${GREEN}✅ Backend installé${NC}"
        echo ""
        
        # Frontend
        echo -e "${BLUE}🎨 Installation Frontend...${NC}"
        cd "$PROJECT_DIR/frontend"
        npm install
        
        echo -e "${GREEN}✅ Frontend installé${NC}"
        echo ""
        echo -e "${GREEN}🎉 Installation terminée !${NC}"
        echo ""
        echo "Vous pouvez maintenant :"
        echo "  - Lancer le système complet : ./DEMARRER_ICI.sh (option 1)"
        echo "  - Tester le LLM : ./DEMARRER_ICI.sh (option 5)"
        ;;
        
    5)
        echo ""
        echo -e "${GREEN}🧪 Test du LLM Sentiment Analyzer...${NC}"
        echo ""
        
        cd "$PROJECT_DIR/backend"
        source .venv/bin/activate
        
        # Configurer la clé API
        export OPENAI_API_KEY='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'
        
        python test_llm_sentiment.py
        ;;
        
    6)
        echo ""
        echo -e "${GREEN}📊 Récupération du dernier score...${NC}"
        echo ""
        
        cd "$PROJECT_DIR/backend"
        source .venv/bin/activate
        
        python -c "
from app.models.database import SessionLocal
from app.models.schemas import IndexScore
from sqlalchemy import desc

db = SessionLocal()
latest = db.query(IndexScore).order_by(desc(IndexScore.created_at)).first()

if latest:
    print('╔════════════════════════════════════════╗')
    print(f'║   Score actuel : {latest.score:.2f}/100           ║')
    print(f'║   Date : {latest.as_of}               ║')
    print('╚════════════════════════════════════════╝')
else:
    print('⚠️  Aucun score trouvé. Lancez le système d abord.')

db.close()
"
        echo ""
        ;;
        
    7)
        echo ""
        echo -e "${GREEN}📚 Documentation disponible :${NC}"
        echo ""
        echo "📄 INTEGRATION_SAAS.md - Guide d'intégration dans votre SaaS"
        echo "📄 README.md - Vue d'ensemble du projet"
        echo "📄 CALCUL_DU_SCORE.md - Explication de la formule"
        echo "📄 INTEGRATION_LLM_COMPLETE.md - Détails sur le LLM"
        echo ""
        
        read -p "Ouvrir INTEGRATION_SAAS.md ? (o/n) : " open_doc
        
        if [ "$open_doc" = "o" ]; then
            if command -v open &> /dev/null; then
                open "$PROJECT_DIR/INTEGRATION_SAAS.md"
            else
                cat "$PROJECT_DIR/INTEGRATION_SAAS.md"
            fi
        fi
        ;;
        
    8)
        echo ""
        echo -e "${GREEN}👋 Au revoir !${NC}"
        echo ""
        exit 0
        ;;
        
    *)
        echo ""
        echo -e "${RED}❌ Choix invalide${NC}"
        echo ""
        exit 1
        ;;
esac

