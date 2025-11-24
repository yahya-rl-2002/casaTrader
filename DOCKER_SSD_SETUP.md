# 🐳 Configuration Docker depuis SSD Externe

## ✅ Docker Installé

Docker est installé sur votre SSD externe :
- **Emplacement** : `/Volumes/YAHYA SSD/Applications/Docker.app`
- **Version** : Docker 28.5.1

---

## 🔧 Configuration

### Option 1 : Script automatique (Recommandé)

```bash
source scripts/setup-docker-ssd.sh
```

### Option 2 : Ajout manuel au PATH

Ajoutez à `~/.zshrc` ou `~/.bash_profile` :

```bash
export PATH="/Volumes/YAHYA SSD/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

Puis rechargez :
```bash
source ~/.zshrc
```

### Option 3 : Alias (temporaire)

```bash
alias docker='/Volumes/YAHYA SSD/Applications/Docker.app/Contents/Resources/bin/docker'
alias docker-compose='/Volumes/YAHYA SSD/Applications/Docker.app/Contents/Resources/bin/docker-compose'
```

---

## 🚀 Utilisation

### Lancer Docker Desktop

```bash
open "/Volumes/YAHYA SSD/Applications/Docker.app"
```

### Vérifier l'installation

```bash
docker --version
docker-compose --version
docker info
```

### Utiliser avec le projet

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down

# Déploiement production
./scripts/deploy-production.sh
```

---

## ⚠️ Notes

1. **Docker Desktop doit être lancé** avant d'utiliser les commandes docker
2. Le PATH a été ajouté à `~/.zshrc` automatiquement
3. Si vous changez de terminal, rechargez : `source ~/.zshrc`

---

## 🔍 Dépannage

### Docker non trouvé

```bash
# Vérifier le PATH
echo $PATH | grep Docker

# Ajouter manuellement
export PATH="/Volumes/YAHYA SSD/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

### Docker Desktop ne démarre pas

```bash
# Vérifier que le SSD est monté
ls "/Volumes/YAHYA SSD/Applications/Docker.app"

# Lancer manuellement
open "/Volumes/YAHYA SSD/Applications/Docker.app"
```

---

**✅ Configuration terminée ! Docker est prêt à être utilisé.**
