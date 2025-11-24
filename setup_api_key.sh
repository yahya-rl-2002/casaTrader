#!/bin/bash

# 🔑 Configuration Permanente de la Clé API OpenAI
# Ce script ajoute votre clé API à votre profil shell

echo "========================================================================"
echo "🔑 Configuration Permanente de la Clé API OpenAI"
echo "========================================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

OPENAI_KEY='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'

# Vérifier si la clé existe déjà dans .zshrc
if grep -q "OPENAI_API_KEY" ~/.zshrc 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Une clé OPENAI_API_KEY existe déjà dans ~/.zshrc${NC}"
    echo ""
    read -p "Voulez-vous la remplacer ? (o/n) : " replace
    
    if [ "$replace" = "o" ]; then
        # Supprimer l'ancienne ligne
        sed -i.bak '/OPENAI_API_KEY/d' ~/.zshrc
        echo -e "${GREEN}✅ Ancienne clé supprimée${NC}"
    else
        echo -e "${YELLOW}Configuration annulée${NC}"
        exit 0
    fi
fi

# Ajouter la nouvelle clé
echo "" >> ~/.zshrc
echo "# OpenAI API Key for Fear & Greed Index LLM Sentiment Analysis" >> ~/.zshrc
echo "export OPENAI_API_KEY='$OPENAI_KEY'" >> ~/.zshrc

echo -e "${GREEN}✅ Clé API ajoutée à ~/.zshrc${NC}"
echo ""

# Recharger le profil
source ~/.zshrc

# Vérifier que la clé est bien configurée
if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}✅ Clé API configurée avec succès !${NC}"
    echo "   Clé : ${OPENAI_API_KEY:0:20}..."
    echo ""
else
    echo -e "${RED}❌ Erreur : La clé n'a pas pu être chargée${NC}"
    echo ""
    echo "Rechargez manuellement votre profil :"
    echo "   source ~/.zshrc"
    exit 1
fi

echo "========================================================================"
echo "🎉 Configuration terminée !"
echo "========================================================================"
echo ""
echo "La clé API sera maintenant disponible dans tous vos terminaux."
echo ""
echo "Pour démarrer le système :"
echo "   cd '/Volumes/YAHYA SSD/Documents/fear and'"
echo "   ./start_with_llm.sh"
echo ""

