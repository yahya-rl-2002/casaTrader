# 🚀 CasaTrader - Plateforme Complète d'Investissement Boursier

> **La plateforme tout-en-un pour les investisseurs de la Bourse de Casablanca**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🎯 Vue d'ensemble

**CasaTrader** est une plateforme SaaS complète conçue pour les investisseurs de la Bourse de Casablanca. Elle regroupe tous les outils essentiels pour analyser, suivre et gérer vos investissements en un seul endroit.

### ✨ Fonctionnalités Principales

#### 📊 **Analyse de Marché**
- **Fear & Greed Index** : Indice de sentiment du marché en temps réel
- **Vue d'ensemble du marché** : Suivi des principales valeurs et indices
- **Graphiques interactifs** : Analyse technique et historique
- **Heatmap de volume** : Visualisation du trading

#### 📰 **Actualités & Informations**
- **Flux d'actualités financières** : Agrégation depuis plusieurs sources marocaines
- **Analyse de sentiment** : IA pour analyser le sentiment des articles
- **Alertes personnalisées** : Notifications sur les événements importants

#### 📄 **Rapports Financiers**
- **Scraping automatique** : Téléchargement automatique des rapports de 55+ entreprises
- **Organisation par secteur** : Accès rapide aux documents par secteur d'activité
- **Recherche avancée** : Trouvez rapidement les rapports recherchés
- **Téléchargement direct** : Accès immédiat aux PDFs avec noms complets

#### 💼 **Gestion de Portefeuille**
- **Suivi de portefeuille** : Suivez vos positions en temps réel
- **Analyse de performance** : Statistiques détaillées sur vos investissements
- **Historique des transactions** : Journal complet de votre activité

#### 🔔 **Alertes & Notifications**
- **Alertes de prix** : Notifications quand une action atteint un seuil
- **Alertes d'actualités** : Soyez informé des nouvelles importantes
- **Alertes de rapports** : Notification lors de la publication de nouveaux rapports

---

## 🚀 Démarrage Rapide

### Prérequis

- **Python 3.10+** installé
- **Node.js 18+** installé
- **Poetry** (pour le backend)
- **NPM** (pour le frontend)
- **Compte Supabase** configuré

### Installation

#### 1. Cloner le dépôt

```bash
git clone https://github.com/yahya-rl-2002/casaTrader.git
cd casaTrader
```

#### 2. Configuration Backend

```bash
cd backend

# Installer les dépendances avec Poetry
poetry install

# OU avec pip
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API (Supabase, OpenAI, etc.)
```

#### 3. Configuration Frontend

```bash
cd ..

# Installer les dépendances
npm install

# Configurer les variables d'environnement
# Créer un fichier .env.local avec vos clés Supabase
```

#### 4. Démarrer les services

**Option 1 : Script automatique (Recommandé)**

```bash
./start_all.sh
```

**Option 2 : Démarrage manuel**

```bash
# Terminal 1 - Backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
npm run dev
```

### Accès aux services

- **Frontend** : http://localhost:8080
- **Backend API** : http://localhost:8001
- **Documentation API** : http://localhost:8001/docs

---

## 📁 Structure du Projet

```
casaTrader/
├── backend/                 # API FastAPI + Python
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── services/       # Services métier
│   │   │   └── financial_reports_scraper.py  # Scraping automatique
│   │   ├── pipelines/      # Traitement de données
│   │   ├── models/         # Modèles de données
│   │   └── tasks/          # Tâches planifiées
│   └── tests/              # Tests automatisés
│
├── frontend/               # Interface React + Vite
│   ├── src/
│   │   ├── pages/         # Pages principales
│   │   ├── components/    # Composants réutilisables
│   │   └── data/          # Données statiques
│   └── public/            # Assets publics
│
├── supabase/              # Configuration Supabase
│   ├── migrations/        # Migrations de base de données
│   └── functions/         # Edge Functions
│
├── docs/                  # Documentation
├── scripts/               # Scripts utilitaires
└── README.md             # Ce fichier
```

---

## 🔧 Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide
- **Python 3.10+** : Langage de programmation
- **Supabase** : Backend-as-a-Service (Base de données + Storage)
- **BeautifulSoup** : Scraping web
- **APScheduler** : Planification de tâches
- **OpenAI API** : Analyse de sentiment avec LLM

### Frontend
- **React 18** : Bibliothèque UI
- **TypeScript** : Typage statique
- **Vite** : Build tool rapide
- **Tailwind CSS** : Framework CSS
- **Shadcn UI** : Composants UI
- **React Router** : Routing
- **TanStack Query** : Gestion d'état serveur

### Infrastructure
- **Supabase** : Base de données PostgreSQL + Storage
- **Docker** : Containerisation (optionnel)
- **Nginx** : Reverse proxy (production)

---

## 📊 Fonctionnalités Détaillées

### Scraping Automatique des Rapports Financiers

La plateforme scrape automatiquement les rapports financiers de **55+ entreprises** cotées à la Bourse de Casablanca :

- ✅ Téléchargement automatique des PDFs
- ✅ Extraction des métadonnées (titre, date, entreprise)
- ✅ Stockage dans Supabase Storage
- ✅ Organisation par secteur et entreprise
- ✅ Mise à jour quotidienne automatique

**Entreprises configurées** : Akdital, Attijariwafa Bank, TGCC, Douja Prom Addoha, Afric Industries, Afriquia Gaz, Alliances, Aluminium Du Maroc, Aradei Capital, et 45+ autres...

### Fear & Greed Index

Indice de sentiment du marché calculé à partir de 6 composantes :

1. **Momentum** (20%) - Tendance des prix
2. **Price Strength** (15%) - Force des prix
3. **Volume** (15%) - Volume de trading
4. **Volatility** (20%) - Volatilité du marché
5. **Equity vs Bonds** (15%) - Performance relative
6. **Media Sentiment** (15%) - Sentiment des médias

**Mise à jour** : Automatique toutes les 10 minutes

---

## 🔐 Configuration

### Variables d'environnement Backend

Créer `backend/.env` :

```env
# Supabase
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_SERVICE_KEY=votre-service-key

# OpenAI (pour analyse de sentiment)
OPENAI_API_KEY=sk-...

# Base de données
DATABASE_URL=postgresql://...

# Configuration
ENVIRONMENT=development
```

### Variables d'environnement Frontend

Créer `.env.local` :

```env
VITE_SUPABASE_URL=https://votre-projet.supabase.co
VITE_SUPABASE_ANON_KEY=votre-anon-key
```

---

## 🧪 Tests

```bash
# Backend
cd backend
poetry run pytest

# Frontend
npm run test
```

---

## 📝 Documentation

- [Guide d'installation](./docs/INSTALLATION.md)
- [Documentation API](./docs/API.md)
- [Guide de développement](./docs/DEVELOPMENT.md)
- [Architecture](./docs/architecture.md)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👤 Auteur

**Yahya RL**
- GitHub: [@yahya-rl-2002](https://github.com/yahya-rl-2002)
- Dépôt: [casaTrader](https://github.com/yahya-rl-2002/casaTrader)

---

## 🙏 Remerciements

- **Supabase** pour l'infrastructure backend
- **TradingView** pour les widgets de graphiques
- Toutes les entreprises qui publient leurs rapports financiers en ligne

---

## 📞 Support

Pour toute question ou problème :
- Ouvrir une [issue](https://github.com/yahya-rl-2002/casaTrader/issues)
- Consulter la [documentation](./docs/)
- Contacter le support via l'application

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !**
