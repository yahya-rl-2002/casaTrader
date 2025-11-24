"use client";

import { useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export default function RefreshButton() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info', text: string } | null>(null);
  const [progress, setProgress] = useState(0);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    setMessage({ type: 'info', text: '🔄 Lancement du pipeline...' });
    setProgress(0);

    try {
      // Étape 1 : Déclencher le pipeline
      setMessage({ type: 'info', text: '📰 Scraping des articles de presse...' });
      setProgress(20);

      const response = await fetch(`${API_BASE_URL}/scheduler/trigger`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }

      const result = await response.json();
      
      setProgress(50);
      setMessage({ type: 'info', text: '🤖 Analyse de sentiment avec LLM...' });

      // Attendre un peu pour que le pipeline se termine
      await new Promise(resolve => setTimeout(resolve, 3000));

      setProgress(80);
      setMessage({ type: 'info', text: '📊 Calcul du nouveau score...' });

      // Attendre encore un peu
      await new Promise(resolve => setTimeout(resolve, 2000));

      setProgress(100);
      setMessage({ type: 'success', text: '✅ Score mis à jour ! Rechargement...' });

      // Recharger la page après un court délai
      setTimeout(() => {
        window.location.reload();
      }, 1500);

    } catch (error) {
      console.error('Erreur lors du rafraîchissement:', error);
      setMessage({ 
        type: 'error', 
        text: `❌ Erreur: ${error instanceof Error ? error.message : 'Erreur inconnue'}` 
      });
      setIsRefreshing(false);
      setProgress(0);

      // Effacer le message d'erreur après 5 secondes
      setTimeout(() => {
        setMessage(null);
      }, 5000);
    }
  };

  return (
    <div className="flex items-center gap-3">
      {/* Bouton de rafraîchissement */}
      <button
        onClick={handleRefresh}
        disabled={isRefreshing}
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-sm
          transition-all duration-200 shadow-lg
          ${isRefreshing 
            ? 'bg-gray-600 text-gray-300 cursor-not-allowed' 
            : 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white hover:shadow-xl transform hover:scale-105'
          }
        `}
      >
        {isRefreshing ? (
          <>
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Actualisation...</span>
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Actualiser le Score</span>
          </>
        )}
      </button>

      {/* Message de statut */}
      {message && (
        <div className={`
          px-4 py-2 rounded-lg text-sm font-medium animate-fade-in
          ${message.type === 'success' ? 'bg-green-500/20 text-green-300 border border-green-500/30' : ''}
          ${message.type === 'error' ? 'bg-red-500/20 text-red-300 border border-red-500/30' : ''}
          ${message.type === 'info' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' : ''}
        `}>
          {message.text}
        </div>
      )}

      {/* Barre de progression */}
      {isRefreshing && progress > 0 && (
        <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}

