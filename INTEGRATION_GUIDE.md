# 🚀 Guide d'Intégration du Fear & Greed Index dans votre SaaS

**Date** : 29 octobre 2025  
**Status** : ✅ Frontend SaaS en cours d'exécution (port 8080)

---

## 🎯 **SITUATION ACTUELLE**

Vous avez :
- ✅ **SaaS Frontend** : Vite + React + Shadcn UI (port 8080)
- ✅ **Fear & Greed Backend** : FastAPI copié dans `/backend`
- ⚠️ **Problème** : Incompatibilité Python 3.13 avec certaines dépendances

---

## 💡 **SOLUTION RECOMMANDÉE**

### **Option 1 : API Uniquement (RECOMMANDÉ)**

Utilisez le **backend déjà opérationnel** du projet original comme API externe :

```bash
# Terminal 1 : Backend Fear & Greed (ancien emplacement)
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 2 : Votre SaaS (déjà en cours)
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
npm run dev  # Port 8080
```

**Avantages** :
- ✅ Pas de problème de compatibilité
- ✅ Backend déjà installé et fonctionnel
- ✅ Séparer les préoccupations (microservices)

---

## 🔧 **INTÉGRATION DANS VOTRE SAAS**

### **Étape 1 : Créer un composant Fear & Greed**

Créez `/src/pages/FearGreedIndex.tsx` :

```tsx
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const API_BASE_URL = 'http://localhost:8001/api/v1';

export default function FearGreedIndex() {
  const [score, setScore] = useState<number>(50);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchScore() {
      try {
        const response = await fetch(`${API_BASE_URL}/index/latest`);
        const data = await response.json();
        setScore(data.score);
      } catch (error) {
        console.error('Failed to fetch score:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchScore();
    const interval = setInterval(fetchScore, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const getColor = (score: number) => {
    if (score >= 70) return 'bg-green-500';
    if (score >= 55) return 'bg-lime-500';
    if (score >= 45) return 'bg-amber-400';
    if (score >= 30) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getLabel = (score: number) => {
    if (score >= 70) return 'EXTREME GREED';
    if (score >= 55) return 'GREED';
    if (score >= 45) return 'NEUTRAL';
    if (score >= 30) return 'FEAR';
    return 'EXTREME FEAR';
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Fear & Greed Index</CardTitle>
          <CardDescription>Bourse de Casablanca</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className={`text-7xl font-bold ${getColor(score)} bg-clip-text text-transparent`}>
              {score.toFixed(2)}
            </div>
            <div className="text-2xl mt-4">{getLabel(score)}</div>
            
            {/* Barre gradient */}
            <div className="mt-8 relative w-full h-16 rounded-xl overflow-hidden"
                 style={{
                   background: 'linear-gradient(to right, #ef4444 0%, #f97316 25%, #fbbf24 50%, #84cc16 75%, #10b981 100%)'
                 }}>
              <div className="absolute inset-0 flex justify-between items-center px-6 text-sm font-bold text-white">
                <span>FEAR</span>
                <span>NEUTRAL</span>
                <span>GREED</span>
              </div>
              {/* Indicateur de position */}
              <div className="absolute top-0 bottom-0 w-1 bg-white shadow-2xl"
                   style={{ left: `${score}%` }}>
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-5 h-5 bg-white rounded-full shadow-xl border-4 border-gray-900"></div>
                <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-5 h-5 bg-white rounded-full shadow-xl border-4 border-gray-900"></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

### **Étape 2 : Ajouter la route**

Modifiez `/src/App.tsx` ou votre fichier de routes :

```tsx
import { Route } from 'react-router-dom';
import FearGreedIndex from './pages/FearGreedIndex';

// Dans vos routes
<Route path="/fear-greed" element={<FearGreedIndex />} />
```

### **Étape 3 : Ajouter au menu de navigation**

Dans votre composant Navigation (`/src/components/Navigation.tsx`) :

```tsx
<Link to="/fear-greed">Fear & Greed Index</Link>
```

---

## 🔗 **ENDPOINTS DISPONIBLES**

Une fois le backend démarré sur le port 8001 :

```
GET  http://localhost:8001/api/v1/index/latest          # Score actuel
GET  http://localhost:8001/api/v1/index/history         # Historique
GET  http://localhost:8001/api/v1/components/latest     # Composants
GET  http://localhost:8001/api/v1/media/latest          # Articles
POST http://localhost:8001/api/v1/scheduler/trigger     # Actualiser
```

---

## 📊 **EXEMPLE DE DASHBOARD COMPLET**

Créez `/src/pages/MarketSentiment.tsx` :

```tsx
import { useEffect, useState } from 'react';
import { Card } from "@/components/ui/card";

interface IndexData {
  score: number;
  label: string;
  as_of: string;
}

interface Component {
  name: string;
  value: number;
  weight: number;
}

export default function MarketSentiment() {
  const [index, setIndex] = useState<IndexData | null>(null);
  const [components, setComponents] = useState<Component[]>([]);

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:8001/api/v1/index/latest').then(r => r.json()),
      fetch('http://localhost:8001/api/v1/components/latest').then(r => r.json())
    ]).then(([indexData, componentsData]) => {
      setIndex(indexData);
      setComponents([
        { name: 'Momentum', value: componentsData.momentum, weight: 20 },
        { name: 'Price Strength', value: componentsData.price_strength, weight: 15 },
        { name: 'Volume', value: componentsData.volume, weight: 15 },
        { name: 'Volatility', value: componentsData.volatility, weight: 20 },
        { name: 'Equity vs Bonds', value: componentsData.equity_vs_bonds, weight: 15 },
        { name: 'Media Sentiment', value: componentsData.media_sentiment, weight: 15 },
      ]);
    });
  }, []);

  if (!index) return <div>Loading...</div>;

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Score principal */}
      <Card className="p-6 text-center">
        <div className="text-7xl font-bold">{index.score.toFixed(2)}</div>
        <div className="text-2xl mt-4">{index.label}</div>
      </Card>

      {/* Composants */}
      <Card className="p-6">
        <h2 className="text-2xl font-bold mb-4">Breakdown des Composants</h2>
        <div className="space-y-4">
          {components.map(comp => (
            <div key={comp.name}>
              <div className="flex justify-between mb-1">
                <span>{comp.name}</span>
                <span>{comp.value.toFixed(2)} ({comp.weight}%)</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${comp.value}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
```

---

## 🚀 **COMMANDES DE DÉMARRAGE**

### **Terminal 1 : Backend Fear & Greed**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
export OPENAI_API_KEY='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'
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### **Terminal 2 : Votre SaaS (déjà en cours)**
```bash
# Déjà en cours sur le port 8080
# http://localhost:8080
```

---

## 🎨 **PERSONNALISATION**

Adaptez les couleurs à votre charte graphique dans Tailwind :

```tsx
// Au lieu de bg-red-500, bg-green-500, etc.
// Utilisez vos couleurs personnalisées :
className="bg-primary text-primary-foreground"
```

---

## 📱 **ACCÈS**

- **Votre SaaS** : http://localhost:8080
- **Fear & Greed API** : http://localhost:8001/docs
- **Fear & Greed Dashboard** : http://localhost:3000/dashboard

---

## ✅ **CHECKLIST D'INTÉGRATION**

- [ ] Backend Fear & Greed démarré (port 8001)
- [ ] Frontend SaaS démarré (port 8080)
- [ ] Composant `FearGreedIndex.tsx` créé
- [ ] Route ajoutée dans l'application
- [ ] Menu de navigation mis à jour
- [ ] Test de l'affichage du score
- [ ] Test de la mise à jour automatique

---

**Votre SaaS est prêt à afficher le Fear & Greed Index ! 🎉**

