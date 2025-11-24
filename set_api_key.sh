#!/bin/bash

# 🔑 Configuration de la Clé API OpenAI pour cette session
# Script simple qui exporte la clé API

echo "========================================================================="
echo "🔑 Configuration de la Clé API OpenAI"
echo "========================================================================="
echo ""

export OPENAI_API_KEY='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'

if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ Clé API configurée avec succès !"
    echo "   Clé : ${OPENAI_API_KEY:0:20}..."
    echo ""
    echo "========================================================================="
    echo "🚀 Prêt à démarrer le système !"
    echo "========================================================================="
    echo ""
    echo "La clé API est maintenant active pour ce terminal."
    echo ""
    echo "Pour démarrer le système, exécutez :"
    echo "   ./start_with_llm.sh"
    echo ""
else
    echo "❌ Erreur : La clé n'a pas pu être configurée"
    exit 1
fi

