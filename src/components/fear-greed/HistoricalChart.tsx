import * as React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export default function HistoricalChart() {
  const [historicalData, setHistoricalData] = React.useState<any[]>([]);
  const [mounted, setMounted] = React.useState(false);
  const [isRealData, setIsRealData] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
    
    // Charger uniquement les données réelles depuis localStorage
    if (typeof window !== 'undefined') {
      const storedData = window.localStorage.getItem('fear_greed_history');
      if (storedData) {
        try {
          const parsedData = JSON.parse(storedData);
          // Transformer les données pour Recharts
          const formattedData = parsedData.map((item: any) => ({
            date: new Date(item.as_of).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' }),
            score: item.score,
          })).reverse(); // Inverser pour avoir les plus récents à droite
          
          if (formattedData.length > 0) {
            setHistoricalData(formattedData);
            setIsRealData(true);
            console.log('✅ Données historiques réelles chargées:', formattedData.length, 'points');
            return;
          }
        } catch (e) {
          console.error('Erreur parsing données historiques:', e);
        }
      }
    }
    
    // Pas de données - afficher message
    console.warn('⚠️ Aucune donnée historique disponible. Veuillez attendre le chargement initial.');
    setHistoricalData([]);
    setIsRealData(false);
  }, []);

  if (!mounted || historicalData.length === 0) {
    return null; // Rendu silencieux pendant l'hydration
  }

  return (
    <div className="bg-gray-800 rounded-2xl p-8 shadow-xl border border-gray-700">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">
          Tendance Historique ({historicalData.length} jours)
        </h2>
        <span className={`text-xs px-3 py-1 rounded-full font-semibold ${
          isRealData 
            ? 'bg-green-100 text-green-700' 
            : 'bg-yellow-100 text-yellow-700'
        }`}>
          {isRealData ? '✓ Données Réelles' : '⚠ Données Démo'}
        </span>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={historicalData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(200,200,200,0.3)" />
          <XAxis 
            dataKey="date" 
            stroke="rgba(100,100,100,0.7)"
            tick={{ fill: 'rgba(100,100,100,0.7)', fontSize: 12 }}
            interval="preserveStartEnd"
          />
          <YAxis 
            domain={[0, 100]}
            stroke="rgba(100,100,100,0.7)"
            tick={{ fill: 'rgba(100,100,100,0.7)' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid rgba(200,200,200,0.5)',
              borderRadius: '8px',
              color: '#333',
            }}
          />
          <ReferenceLine y={50} stroke="rgba(150,150,150,0.4)" strokeDasharray="3 3" />
          <Line 
            type="monotone" 
            dataKey="score" 
            stroke="#8b5cf6" 
            strokeWidth={3}
            dot={{ fill: '#8b5cf6', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div className="mt-4 text-center text-sm text-gray-400">
        Évolution du sentiment du marché au fil du temps
      </div>
    </div>
  );
}

