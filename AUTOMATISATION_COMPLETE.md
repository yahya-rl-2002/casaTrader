# 🤖 Automatisation Complète du Système Fear & Greed Index

## 🎯 Objectif

Faire tourner le système **24h/24 et 7j/7** sans intervention manuelle :
- ✅ Démarrage automatique au boot du Mac
- ✅ Mise à jour automatique toutes les 10 minutes
- ✅ Redémarrage automatique en cas d'erreur
- ✅ Dashboard toujours accessible

---

## 🚀 **SOLUTION 1 : Démarrage Automatique avec LaunchAgent (Mac)**

### **Étape 1 : Créer le service LaunchAgent pour le Backend**

Créez le fichier de service :

```bash
nano ~/Library/LaunchAgents/com.feargreed.backend.plist
```

Puis copiez-collez ce contenu :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.feargreed.backend</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Volumes/YAHYA SSD/Documents/fear and/backend/.venv/bin/uvicorn</string>
        <string>app.main:app</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>8000</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Volumes/YAHYA SSD/Documents/fear and/backend</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>OPENAI_API_KEY</key>
        <string>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</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Volumes/YAHYA SSD/Documents/fear and/backend.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Volumes/YAHYA SSD/Documents/fear and/backend.error.log</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
</dict>
</plist>
```

Sauvegardez avec `Ctrl+O`, `Entrée`, `Ctrl+X`.

---

### **Étape 2 : Créer le service LaunchAgent pour le Frontend**

```bash
nano ~/Library/LaunchAgents/com.feargreed.frontend.plist
```

Contenu :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.feargreed.frontend</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/npm</string>
        <string>run</string>
        <string>dev</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Volumes/YAHYA SSD/Documents/fear and/frontend</string>
    
    <key>StandardOutPath</key>
    <string>/Volumes/YAHYA SSD/Documents/fear and/frontend.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Volumes/YAHYA SSD/Documents/fear and/frontend.error.log</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
</dict>
</plist>
```

---

### **Étape 3 : Activer les services**

```bash
# Charger le backend
launchctl load ~/Library/LaunchAgents/com.feargreed.backend.plist

# Charger le frontend
launchctl load ~/Library/LaunchAgents/com.feargreed.frontend.plist

# Vérifier qu'ils tournent
launchctl list | grep feargreed
```

---

### **Étape 4 : Gestion des services**

**Arrêter un service :**
```bash
launchctl unload ~/Library/LaunchAgents/com.feargreed.backend.plist
launchctl unload ~/Library/LaunchAgents/com.feargreed.frontend.plist
```

**Démarrer un service :**
```bash
launchctl load ~/Library/LaunchAgents/com.feargreed.backend.plist
launchctl load ~/Library/LaunchAgents/com.feargreed.frontend.plist
```

**Voir les logs :**
```bash
tail -f "/Volumes/YAHYA SSD/Documents/fear and/backend.log"
tail -f "/Volumes/YAHYA SSD/Documents/fear and/frontend.log"
```

---

## 🐳 **SOLUTION 2 : Docker (Recommandé pour Production)**

Pour un déploiement encore plus simple et portable :

### **Étape 1 : Vérifier que Docker est installé**

```bash
docker --version
```

Si pas installé : https://www.docker.com/products/docker-desktop

---

### **Étape 2 : Utiliser Docker Compose**

Le projet a déjà un `docker-compose.yml` ! Vérifiez-le :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"
cat docker-compose.yml
```

---

### **Étape 3 : Démarrer avec Docker**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"

# Créer un fichier .env pour la clé API
cat > .env << 'EOF'
OPENAI_API_KEY=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
EOF

# Démarrer tout le système
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter le système
docker-compose down
```

---

## ☁️ **SOLUTION 3 : Déploiement Cloud (Production)**

Pour un accès depuis n'importe où, déployez sur un serveur cloud :

### **Option A : Heroku (Gratuit/Payant)**

1. Créez un compte sur https://heroku.com
2. Installez Heroku CLI
3. Déployez :

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"
heroku create feargreed-index
heroku config:set OPENAI_API_KEY='sk-proj-...'
git push heroku main
```

---

### **Option B : DigitalOcean / AWS / Google Cloud**

1. Créez un serveur (VPS)
2. Installez Docker
3. Clonez le projet
4. Lancez avec `docker-compose up -d`

**Coût** : ~5-10$/mois pour un petit serveur

---

### **Option C : Render.com (Simple et Gratuit)**

1. Allez sur https://render.com
2. Connectez votre GitHub
3. Déployez le backend et frontend
4. Configurez les variables d'environnement

---

## 🔄 **Automatisation Déjà Intégrée**

Le système a **déjà** un scheduler automatique qui :

✅ **Scrape les articles** toutes les 10 minutes  
✅ **Analyse avec LLM** automatiquement  
✅ **Met à jour le score** en base de données  
✅ **Redémarre en cas d'erreur** (avec KeepAlive)  

**Vous n'avez rien à faire !** Le système tourne tout seul. 🎉

---

## 📊 **Monitoring et Logs**

### **Voir les logs en temps réel :**

```bash
# Backend
tail -f "/Volumes/YAHYA SSD/Documents/fear and/backend.log"

# Frontend
tail -f "/Volumes/YAHYA SSD/Documents/fear and/frontend.log"
```

---

### **Vérifier que tout fonctionne :**

```bash
# Backend actif ?
curl http://localhost:8000/api/v1/health

# Frontend actif ?
curl http://localhost:3000

# Scheduler actif ?
curl http://localhost:8000/api/v1/scheduler/status
```

---

## 💡 **Recommandations**

| Besoin | Solution Recommandée |
|--------|---------------------|
| **Mac toujours allumé** | LaunchAgent (Solution 1) |
| **Portabilité** | Docker (Solution 2) |
| **Accès depuis internet** | Cloud (Solution 3) |
| **Test local** | `./start_with_llm.sh` |

---

## 🎯 **Ma Recommandation : LaunchAgent (Solution 1)**

**Pourquoi ?**
- ✅ Gratuit
- ✅ Tourne sur votre Mac
- ✅ Démarre automatiquement au boot
- ✅ Redémarre automatiquement en cas d'erreur
- ✅ Logs facilement accessibles
- ✅ Pas besoin de serveur cloud

**Inconvénient :**
- ⚠️ Votre Mac doit rester allumé
- ⚠️ Accessible uniquement depuis votre réseau local

---

## 🚀 **BONUS : Script de Démarrage Simplifié**

J'ai créé un script `auto_start.sh` pour vous :

```bash
#!/bin/bash

# Script de démarrage automatique du système Fear & Greed Index

cd "/Volumes/YAHYA SSD/Documents/fear and"

# Configurer la clé API
export OPENAI_API_KEY='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'

# Démarrer le backend en arrière-plan
cd backend
source .venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
echo $! > ../backend.pid

# Démarrer le frontend en arrière-plan
cd ../frontend
nohup npm run dev > ../frontend.log 2>&1 &
echo $! > ../frontend.pid

echo "✅ Système démarré !"
echo "   Backend : http://localhost:8000"
echo "   Frontend : http://localhost:3000/dashboard"
echo ""
echo "Pour arrêter :"
echo "   kill \$(cat backend.pid frontend.pid)"
```

**Utilisation :**
```bash
chmod +x auto_start.sh
./auto_start.sh
```

---

## ✅ **Checklist Finale**

- [ ] Choisir une solution (LaunchAgent / Docker / Cloud)
- [ ] Configurer les services
- [ ] Tester le démarrage automatique
- [ ] Vérifier les logs
- [ ] Tester l'arrêt/redémarrage
- [ ] Configurer les sauvegardes (base de données)

---

## 🎉 **Résultat Final**

Une fois configuré :
- 🚀 Le système démarre **automatiquement** au boot
- 🔄 Les données se mettent à jour **toutes les 10 minutes**
- 🤖 Le LLM analyse **automatiquement** les nouveaux articles
- 📊 Le score est **toujours à jour**
- 🌐 Le dashboard est **toujours accessible**

**Vous n'avez plus rien à faire ! Le système tourne tout seul ! 🎊**

