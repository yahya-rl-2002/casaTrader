# 🐳 Installation de Docker

## ❌ État Actuel

Docker n'est **pas installé** sur votre système.

---

## 📥 Installation pour macOS

### Option 1 : Docker Desktop (Recommandé)

1. **Télécharger Docker Desktop**
   - Allez sur : https://www.docker.com/products/docker-desktop
   - Téléchargez la version pour Mac (Intel ou Apple Silicon)

2. **Installer**
   - Ouvrez le fichier `.dmg` téléchargé
   - Glissez Docker dans le dossier Applications
   - Lancez Docker Desktop depuis Applications

3. **Vérifier l'installation**
   ```bash
   docker --version
   docker-compose --version
   ```

### Option 2 : Homebrew

```bash
# Installer Docker Desktop via Homebrew
brew install --cask docker

# Lancer Docker Desktop
open /Applications/Docker.app
```

---

## ✅ Vérification

Après l'installation, vérifiez que Docker fonctionne :

```bash
# Vérifier la version
docker --version
docker-compose --version

# Vérifier que Docker est en cours d'exécution
docker info

# Tester avec un conteneur
docker run hello-world
```

---

## 🚀 Utilisation avec le Projet

Une fois Docker installé, vous pouvez utiliser :

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Déploiement production
./scripts/deploy-production.sh
```

---

## ⚠️ Notes Importantes

1. **Docker Desktop** nécessite :
   - macOS 10.15 (Catalina) ou plus récent
   - Au moins 4 GB de RAM
   - VirtualBox doit être désinstallé (conflit)

2. **Premier démarrage** :
   - Docker Desktop peut prendre quelques minutes au premier lancement
   - Acceptez les permissions système si demandées

3. **Ressources** :
   - Par défaut, Docker Desktop utilise 2 CPU et 2 GB RAM
   - Vous pouvez ajuster dans Docker Desktop > Settings > Resources

---

## 🔧 Dépannage

### Docker ne démarre pas

```bash
# Vérifier les permissions
sudo chown -R $(whoami) ~/.docker

# Redémarrer Docker Desktop
killall Docker && open /Applications/Docker.app
```

### Erreur de permissions

```bash
# Ajouter votre utilisateur au groupe docker (Linux)
sudo usermod -aG docker $USER
# Puis reconnectez-vous
```

---

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Docker Desktop pour Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Guide Docker Compose](https://docs.docker.com/compose/)

---

**💡 Astuce** : Si vous n'avez pas besoin de Docker pour le moment, vous pouvez utiliser les scripts de démarrage manuel (`./start_all.sh`) qui fonctionnent sans Docker.



