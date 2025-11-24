# 🚀 Comment Lancer le Système Fear & Greed Index

## ⚠️ IMPORTANT : Ne PAS lancer dans Cursor !

Le terminal de Cursor (sandbox) **NE PERMET PAS** de lancer des serveurs web.  
Vous DEVEZ utiliser votre **Terminal Mac** directement.

---

## ✅ Méthode Simple - 1 Commande

### Étape 1 : Ouvrir le Terminal Mac

**Pas le terminal Cursor** - Utilisez l'application **Terminal** de macOS :
- Appuyez sur `Cmd + Espace`
- Tapez "Terminal"
- Appuyez sur `Entrée`

### Étape 2 : Copier-Coller cette Commande

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and" && ./start_system.sh
```

### Étape 3 : Attendre le Démarrage

Vous verrez :
```
================================================================================
  ✅ Système Fear & Greed Index Démarré
================================================================================

  📊 Dashboard:       http://localhost:3000
  🔌 API Backend:     http://127.0.0.1:8000
  📚 Documentation:   http://127.0.0.1:8000/docs

  🔄 Automatisation:
     ✅ Mise à jour automatique toutes les 10 minutes
```

### Étape 4 : Ouvrir le Navigateur

Le système ouvrira automatiquement http://localhost:3000

**Vous devriez maintenant voir le score 33.73 au lieu de 50 !**

---

## 🛑 Pour Arrêter le Système

Dans le même terminal, appuyez sur `Ctrl+C`

Ou ouvrez un nouveau terminal et tapez :
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and" && ./stop_system.sh
```

---

## 🔧 Méthode Manuelle (2 Terminaux)

Si le script automatique ne fonctionne pas :

### Terminal 1 - Backend

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Attendez de voir :
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Scheduler started - Index will update every 10 minutes
```

### Terminal 2 - Frontend

Ouvrez un **NOUVEAU** Terminal Mac et tapez :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
npm run dev
```

Attendez de voir :
```
✓ Ready in 2.3s
○ Local:   http://localhost:3000
```

### Ouvrir le Navigateur

Allez sur : http://localhost:3000

---

## ✅ Vérification que ça Fonctionne

### 1. Tester l'API Backend

Ouvrez un nouveau terminal et testez :

```bash
curl http://localhost:8000/api/v1/index/latest
```

Vous devriez voir :
```json
{
  "as_of": "2025-10-25",
  "score": 33.73
}
```

Si vous voyez **50**, le backend n'est pas lancé correctement.

### 2. Ouvrir la Console du Navigateur

Dans le navigateur (http://localhost:3000) :
- Appuyez sur `F12` (ou `Cmd+Option+I` sur Mac)
- Allez dans l'onglet "Console"
- Cherchez les messages :

```
[DataLoader] Latest score: {score: 33.73, ...}
[DataLoader] Components: {momentum: 104, ...}
```

Si vous voyez des erreurs de connexion, le backend n'est pas démarré.

---

## 🐛 Résolution de Problèmes

### Problème 1 : "EPERM: operation not permitted"

**Cause :** Vous essayez de lancer dans le terminal Cursor

**Solution :** 
- ✅ Fermez le terminal Cursor (`Ctrl+C`)
- ✅ Ouvrez le **Terminal Mac** (app Terminal de macOS)
- ✅ Relancez avec `./start_system.sh`

---

### Problème 2 : "Port 8000 already in use"

**Cause :** Un autre processus utilise le port 8000

**Solution :**
```bash
# Trouver le processus
lsof -ti:8000

# Le tuer
lsof -ti:8000 | xargs kill -9

# Relancer
./start_system.sh
```

---

### Problème 3 : "Port 3000 already in use"

**Cause :** Un autre processus utilise le port 3000

**Solution :**
```bash
# Trouver le processus
lsof -ti:3000

# Le tuer
lsof -ti:3000 | xargs kill -9

# Relancer
./start_system.sh
```

---

### Problème 4 : Le Score est toujours 50

**Causes possibles :**

1. **Le backend n'est pas démarré**
   - Vérifiez : `curl http://localhost:8000/api/v1/index/latest`
   - Si erreur → Le backend n'est pas lancé

2. **Pas de données dans la DB**
   - Solution : Générer des données
   ```bash
   cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
   source .venv/bin/activate
   python test_complet_systeme.py
   ```

3. **Le frontend ne se connecte pas au backend**
   - Ouvrir F12 dans le navigateur
   - Vérifier les erreurs dans Console
   - Vérifier que les requêtes vers `localhost:8000` fonctionnent

---

### Problème 5 : "Module not found" dans le backend

**Solution :**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
pip install -r requirements.txt
# ou
poetry install
```

---

### Problème 6 : "Module not found" dans le frontend

**Solution :**
```bash
cd "/Volumes/YAHYA SSD/Documents/fear and/frontend"
npm install
```

---

## 📊 Ce que Vous Devriez Voir

### Dans le Dashboard (http://localhost:3000)

**Au lieu de 50, vous devriez voir :**

- 🎯 **Score : 33.73** (pas 50)
- 😟 **Niveau : FEAR** (pas NEUTRAL)
- 📈 **Momentum : 104.0** (pas 50)
- 📊 **Price Strength : 0.1** (pas 50)
- 📰 **Articles médias** : Liste d'articles réels
- 📐 **Formule simplifiée** : Calcul détaillé

### Dans le Terminal Backend

Vous devriez voir des messages comme :
```
INFO:     Uvicorn running on http://127.0.0.1:8000
🚀 Starting Fear & Greed Index API
✅ Scheduler started - Index will update every 10 minutes
📊 Active jobs: 1
```

Puis toutes les 10 minutes :
```
🔄 Starting scheduled index update (every 10 minutes)
✅ Scheduled update completed successfully - Score: 33.73
```

---

## 🎯 Checklist de Démarrage

- [ ] J'ai fermé le terminal Cursor
- [ ] J'ai ouvert le Terminal Mac (app Terminal de macOS)
- [ ] Je suis dans le bon répertoire : `/Volumes/YAHYA SSD/Documents/fear and`
- [ ] J'ai lancé `./start_system.sh`
- [ ] Le backend démarre sur port 8000
- [ ] Le frontend démarre sur port 3000
- [ ] Le navigateur s'ouvre automatiquement
- [ ] Je vois le score **33.73** (pas 50)
- [ ] Les composantes affichent les vraies valeurs

---

## 💡 Astuce : Créer un Alias

Pour démarrer encore plus rapidement, ajoutez à votre `~/.zshrc` :

```bash
alias fear-start='cd "/Volumes/YAHYA SSD/Documents/fear and" && ./start_system.sh'
alias fear-stop='cd "/Volumes/YAHYA SSD/Documents/fear and" && ./stop_system.sh'
```

Puis rechargez :
```bash
source ~/.zshrc
```

Maintenant vous pouvez juste taper :
```bash
fear-start  # Pour démarrer
fear-stop   # Pour arrêter
```

---

## 📞 Besoin d'Aide ?

Si ça ne fonctionne toujours pas :

1. **Vérifier les logs :**
   ```bash
   tail -f /tmp/fear-greed-backend.log
   tail -f /tmp/fear-greed-frontend.log
   ```

2. **Tester manuellement l'API :**
   ```bash
   curl http://localhost:8000/api/v1/index/latest | jq
   ```

3. **Vérifier les processus :**
   ```bash
   ps aux | grep uvicorn
   ps aux | grep next
   ```

---

## ✅ Résumé

**❌ NE PAS FAIRE :**
- Lancer dans le terminal Cursor
- Utiliser le terminal intégré de VSCode/Cursor pour les serveurs

**✅ À FAIRE :**
- Ouvrir le Terminal Mac (application Terminal de macOS)
- Lancer `./start_system.sh`
- Ouvrir http://localhost:3000

**Le score devrait être 33.73, pas 50 !** 🎯

---

**Créé le :** 25 octobre 2025  
**Version :** 1.0







