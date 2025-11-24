# 🚀 Comment Démarrer Votre SaaS avec Fear & Greed Index

---

## ⚠️ IMPORTANT : REDÉMARRAGE REQUIS

Le proxy Vite a été configuré, mais nécessite un **redémarrage complet** de Vite pour fonctionner.

---

## 🎯 ÉTAPES À SUIVRE

### **1. Arrêter le Frontend Actuel**

Dans le terminal où Vite tourne, appuyez sur **Ctrl+C** ou :

```bash
lsof -ti:8080 | xargs kill -9
```

### **2. Utiliser le Script de Démarrage Automatique**

```bash
cd "/Volumes/YAHYA SSD/Téléchargements/casablanca-stock"
./start_all.sh
```

**Ce script va :**
1. ✅ Vérifier si le backend est en cours (port 8001)
2. ✅ Démarrer le backend si nécessaire
3. ✅ Vérifier si le frontend est en cours (port 8080)
4. ✅ Démarrer le frontend avec le proxy configuré
5. ✅ Afficher toutes les URLs d'accès

---

## 🌐 URLs d'Accès

Après le démarrage, vous pourrez accéder à :

| Page | URL |
|------|-----|
| **SaaS Principal** | http://localhost:8080 |
| **Fear & Greed** | http://localhost:8080/fear-greed |
| **Dashboard Complet** | http://localhost:8080/fear-greed-dashboard |

**Toutes les API passent maintenant par le port 8080 !**

---

## 🔍 Vérifier que Tout Fonctionne

### **Test 1 : Vérifier les Ports**

```bash
lsof -i :8001,8080
```

Vous devriez voir 2 processus (backend + frontend).

### **Test 2 : Tester l'API via le Proxy**

```bash
curl http://localhost:8080/api/v1/index/latest
```

Devrait retourner le score JSON.

### **Test 3 : Ouvrir dans le Navigateur**

1. Allez sur : http://localhost:8080/fear-greed
2. Vous devriez voir la carte avec le score **52.30**
3. Cliquez dessus → Redirige vers le dashboard

---

## 🎉 C'EST TOUT !

**Commande unique pour tout démarrer :**

```bash
./start_all.sh
```

**Commande unique pour tout arrêter :**

```bash
./stop_all.sh
```

---

## 📊 Architecture

```
Port 8080 (Frontend) ──┬─→ Pages React du SaaS
                       │
                       └─→ Proxy /api/v1/* ──→ Port 8001 (Backend)
```

**Pas de CORS, tout sur le même port ! 🚀**

