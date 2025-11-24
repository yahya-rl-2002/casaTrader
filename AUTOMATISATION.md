# 🔄 Automatisation - Mise à Jour Toutes les 10 Minutes

## 🎯 Vue d'Ensemble

Le système Fear & Greed Index est maintenant configuré pour se mettre à jour **automatiquement toutes les 10 minutes** dès le démarrage du backend.

---

## ✅ Comment ça Fonctionne

### **1. Scheduler Intégré (APScheduler)**

Le scheduler démarre automatiquement avec le backend FastAPI et exécute le pipeline complet toutes les 10 minutes.

**Fichiers modifiés :**
- ✅ `backend/app/main.py` - Lifecycle avec scheduler
- ✅ `backend/app/services/scheduler.py` - Service scheduler amélioré
- ✅ `backend/app/tasks/jobs.py` - Job de mise à jour

---

## 🚀 Démarrage

### **Méthode Simple**

```bash
cd "/Volumes/YAHYA SSD/Documents/fear and"
./start_system.sh
```

Le scheduler démarre automatiquement et vous verrez dans les logs :

```
🚀 Starting Fear & Greed Index API
✅ Scheduler started - Index will update every 10 minutes
📊 Active jobs: 1
```

### **Vérifier le Statut**

Une fois le backend lancé, vérifiez le statut du scheduler :

```bash
curl http://localhost:8000/api/v1/scheduler/status | jq
```

**Réponse :**
```json
{
  "running": true,
  "jobs_count": 1,
  "jobs": [
    {
      "id": "index_update_10min",
      "name": "run_index_update_job",
      "next_run_time": "2025-10-25 15:20:00",
      "trigger": "interval[0:10:00]"
    }
  ]
}
```

---

## 🎛️ Contrôle du Scheduler via API

### **1. Statut du Scheduler**
```bash
GET http://localhost:8000/api/v1/scheduler/status
```

### **2. Déclencher Manuellement**
```bash
POST http://localhost:8000/api/v1/scheduler/trigger/index_update_10min
```

Force une mise à jour immédiate sans attendre les 10 minutes.

### **3. Pause le Scheduler**
```bash
POST http://localhost:8000/api/v1/scheduler/pause/index_update_10min
```

Suspend temporairement les mises à jour automatiques.

### **4. Reprendre le Scheduler**
```bash
POST http://localhost:8000/api/v1/scheduler/resume/index_update_10min
```

Réactive les mises à jour automatiques.

### **5. Changer l'Intervalle**
```bash
POST http://localhost:8000/api/v1/scheduler/configure
Content-Type: application/json

{
  "interval_minutes": 5
}
```

Change l'intervalle de mise à jour (ex: toutes les 5 minutes au lieu de 10).

---

## 📊 Monitoring

### **Logs en Temps Réel**

```bash
# Voir les mises à jour automatiques
tail -f /tmp/fear-greed-backend.log | grep "scheduled"
```

Vous verrez :
```
🔄 Starting scheduled index update (every 10 minutes)
✅ Scheduled update completed successfully - Score: 45.23
```

### **Dernière Mise à Jour**

Vérifier quand le dernier score a été calculé :

```bash
curl http://localhost:8000/api/v1/index/latest | jq '.as_of'
```

---

## 🔧 Configuration Avancée

### **Changer l'Intervalle par Défaut**

Éditer `backend/app/main.py` :

```python
# Ligne 29-33
scheduler_service.schedule_interval_job(
    job_callable=run_index_update_job,
    minutes=10,  # ← Changer ici (ex: 5, 15, 30)
    job_id="index_update_10min"
)
```

Puis redémarrer le backend :
```bash
./stop_system.sh
./start_system.sh
```

### **Désactiver l'Automatisation**

Si vous voulez désactiver les mises à jour automatiques, commentez dans `backend/app/main.py` :

```python
# scheduler_service.schedule_interval_job(
#     job_callable=run_index_update_job,
#     minutes=10,
#     job_id="index_update_10min"
# )
```

---

## ⏱️ Planification Personnalisée

### **Option 1 : Uniquement en Heures d'Ouverture**

Modifier `backend/app/services/scheduler.py` pour ajouter :

```python
from apscheduler.triggers.cron import CronTrigger

# Toutes les 10 min entre 9h et 16h30 (heures de bourse)
scheduler_service.scheduler.add_job(
    run_index_update_job,
    CronTrigger(
        day_of_week='mon-fri',  # Lundi à vendredi
        hour='9-16',             # 9h à 16h
        minute='*/10'            # Toutes les 10 min
    ),
    id='market_hours_update'
)
```

### **Option 2 : Différents Intervalles selon l'Heure**

```python
# Toutes les 5 min pendant les heures de trading
scheduler_service.scheduler.add_job(
    run_index_update_job,
    CronTrigger(hour='9-16', minute='*/5', day_of_week='mon-fri'),
    id='frequent_update'
)

# Toutes les 30 min hors trading
scheduler_service.scheduler.add_job(
    run_index_update_job,
    CronTrigger(hour='0-8,17-23', minute='*/30'),
    id='slow_update'
)
```

---

## 🐳 Alternative : Cron System (Production)

Pour un déploiement en production, vous pouvez utiliser un cron job système :

### **1. Créer un Script de Mise à Jour**

`/usr/local/bin/update_fear_greed.sh` :

```bash
#!/bin/bash
cd "/Volumes/YAHYA SSD/Documents/fear and/backend"
source .venv/bin/activate
python -c "import asyncio; from app.services.pipeline_service import PipelineService; asyncio.run(PipelineService().run_full_pipeline())" >> /var/log/fear-greed-cron.log 2>&1
```

### **2. Configurer Cron**

```bash
# Ouvrir crontab
crontab -e

# Ajouter la ligne (toutes les 10 minutes)
*/10 * * * * /usr/local/bin/update_fear_greed.sh
```

### **3. Vérifier les Logs Cron**

```bash
tail -f /var/log/fear-greed-cron.log
```

---

## 🔄 Systemd Service (Linux Production)

Pour un serveur Linux en production :

### **1. Créer le Service**

`/etc/systemd/system/fear-greed-scheduler.service` :

```ini
[Unit]
Description=Fear & Greed Index Scheduler
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/fear-and
ExecStart=/path/to/.venv/bin/python -m app.tasks.workers
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **2. Activer et Démarrer**

```bash
sudo systemctl daemon-reload
sudo systemctl enable fear-greed-scheduler
sudo systemctl start fear-greed-scheduler
sudo systemctl status fear-greed-scheduler
```

### **3. Logs**

```bash
journalctl -u fear-greed-scheduler -f
```

---

## 📈 Performances

### **Temps d'Exécution Typique**

| Opération | Durée |
|-----------|-------|
| Scraping marché | 5-10s |
| Scraping médias (4 sources) | 30-60s |
| Sentiment analysis | 10-20s |
| Calcul composantes | 1-2s |
| Sauvegarde DB | <1s |
| **TOTAL** | **~2-3 minutes** |

### **Charge Système**

- CPU : ~20-30% pendant le scraping
- RAM : ~200-300 MB
- Réseau : ~2-5 MB par mise à jour

**→ Compatible avec mises à jour toutes les 10 minutes sans problème !**

---

## ⚠️ Gestion des Erreurs

Le scheduler intègre plusieurs mécanismes de résilience :

### **1. Retries Automatiques**
- 3 tentatives avec backoff exponentiel
- Délai : 5s, 10s, 20s

### **2. Prévention des Overlaps**
```python
max_instances=1  # Empêche les exécutions simultanées
```

### **3. Logging Détaillé**
Chaque mise à jour est loggée avec :
- ✅ Timestamp
- ✅ Score calculé
- ✅ Nombre d'articles
- ✅ Durée d'exécution
- ❌ Erreurs éventuelles

---

## 🎯 Recommandations

### **Environnement de Développement**
- ✅ **10 minutes** - Bon équilibre entre fraîcheur et charge

### **Environnement de Production**
- ✅ **5 minutes** pendant heures de trading (9h-16h30)
- ✅ **30 minutes** hors trading
- ✅ Pause le week-end (optionnel)

### **Tests / Debug**
- ⚠️ **1 minute** pour tests rapides (attention à la charge sur les sources)
- ✅ Utiliser `POST /scheduler/trigger/...` pour tests manuels

---

## 📞 Dépannage

### **Le Scheduler ne Démarre Pas**

**Symptôme** : Aucune mise à jour automatique

**Solution** :
```bash
# Vérifier les logs
tail -f /tmp/fear-greed-backend.log | grep -i scheduler

# Vérifier le statut via API
curl http://localhost:8000/api/v1/scheduler/status
```

### **Mises à Jour Trop Lentes**

**Symptôme** : Mises à jour prennent >5 minutes

**Solution** :
- Réduire `max_articles_per_source` dans le scraper
- Augmenter l'intervalle à 15-20 minutes
- Vérifier la connexion réseau

### **Erreurs Répétées**

**Symptôme** : Logs montrent des échecs répétés

**Solution** :
```bash
# Pause le scheduler
curl -X POST http://localhost:8000/api/v1/scheduler/pause/index_update_10min

# Tester manuellement
cd backend
python test_complet_systeme.py

# Si OK, reprendre
curl -X POST http://localhost:8000/api/v1/scheduler/resume/index_update_10min
```

---

## 📊 Dashboard - Indicateur d'Automatisation

Le frontend affiche automatiquement :
- 🟢 Système actif (scheduler en cours)
- 🕐 Dernière mise à jour (auto-refresh 5 min)

---

## ✅ Résumé

**Le système est maintenant 100% automatisé !**

- 🔄 Mise à jour **toutes les 10 minutes**
- 🚀 Démarre **automatiquement** avec le backend
- 🎛️ **Contrôlable** via API
- 📊 **Monitorable** via logs et status
- ⚡ **Performant** (~2-3 min par mise à jour)
- 🛡️ **Résilient** avec retries et gestion d'erreurs

**Lancez `./start_system.sh` et profitez des mises à jour automatiques ! 🎉**







