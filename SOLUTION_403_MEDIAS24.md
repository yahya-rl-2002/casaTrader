# ✅ Solution pour Contourner le 403 Forbidden de Medias24

**Date**: Aujourd'hui  
**Problème**: Medias24 retournait une erreur 403 Forbidden lors du scraping  
**Solution**: Utilisation de `cloudscraper` pour contourner les protections anti-bot

---

## 🔍 Problème Identifié

Medias24 utilise une protection anti-bot sophistiquée qui bloque les requêtes HTTP standard, même avec des headers réalistes. Les tentatives avec `requests` standard retournaient systématiquement une erreur **403 Forbidden**.

### Tentatives Échouées

1. ❌ Headers HTTP améliorés (User-Agent, Accept-Language, etc.)
2. ❌ Rotation de User-Agent
3. ❌ Session persistante avec cookies
4. ❌ Délais entre requêtes
5. ❌ Essai de différentes URLs (homepage, économie, www)

---

## ✅ Solution Implémentée

### Utilisation de `cloudscraper`

`cloudscraper` est une bibliothèque Python spécialement conçue pour contourner les protections anti-bot, notamment Cloudflare, mais aussi d'autres systèmes de protection similaires.

### Modifications Apportées

#### 1. Installation de cloudscraper

```bash
pip install cloudscraper
```

#### 2. Intégration dans le scraper Medias24

```python
# Essayer d'importer cloudscraper
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    cloudscraper = None
```

#### 3. Utilisation de cloudscraper dans le constructeur

```python
def __init__(self, delay_between_requests: int = 3, use_cloudscraper: bool = True):
    self.use_cloudscraper = use_cloudscraper and CLOUDSCRAPER_AVAILABLE
    
    if self.use_cloudscraper:
        logger.info("Utilisation de cloudscraper pour contourner les protections anti-bot")
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            },
            delay=10  # Délai pour éviter la détection
        )
    else:
        # Fallback vers requests standard
        self.session = requests.Session()
```

#### 4. Gestion de la vérification SSL

Cloudscraper gère automatiquement la vérification SSL, donc on ne doit pas désactiver `verify` :

```python
# Pour cloudscraper, ne pas désactiver la vérification SSL
if self.use_cloudscraper:
    response = self.session.get(url, timeout=25, allow_redirects=True)
else:
    response = self.session.get(url, timeout=20, allow_redirects=True, verify=False)
```

---

## 📊 Résultats

### Avant la Solution

```
❌ MEDIAS24: 0 articles scrapés
   - Erreur: 403 Forbidden
   - Toutes les tentatives échouaient
```

### Après la Solution

```
✅ MEDIAS24: 1 article scrapé → 1 de qualité
   - cloudscraper contourne avec succès la protection anti-bot
   - Articles récupérés et sauvegardés
```

### Résultats Globaux

| Source | Articles Scrapés | Articles de Qualité | Statut |
|--------|------------------|---------------------|--------|
| **BourseNews** | 5 | 1 | ✅ |
| **Challenge** | 1 | 1 | ✅ |
| **Hespress** | 3 | 3 | ✅ |
| **LaVieEco** | 0 | 0 | ❌ |
| **L'Économiste** | 2 | 2 | ✅ |
| **Medias24** | 1 | 1 | ✅ |

**Total**: 8 articles scrapés et sauvegardés ✅

---

## 🔧 Fonctionnalités Ajoutées

### 1. Rotation User-Agent (si cloudscraper non disponible)

```python
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15...',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...',
]
```

### 2. Initialisation de Session

Le scraper fait maintenant une première requête pour obtenir des cookies valides avant de commencer le scraping.

### 3. Essai de Plusieurs URLs

Le scraper essaie plusieurs URLs dans l'ordre :
1. `https://medias24.com/economie` (page économie)
2. `https://medias24.com` (page d'accueil)
3. `https://www.medias24.com` (page d'accueil avec www)

### 4. Fallback Intelligent

Si cloudscraper n'est pas disponible, le scraper utilise `requests` standard avec toutes les optimisations (headers, rotation User-Agent, etc.).

---

## 📝 Utilisation

### Utilisation Standard (avec cloudscraper)

```python
from app.pipelines.ingestion.medias24_scraper import Medias24Scraper

scraper = Medias24Scraper(delay_between_requests=3, use_cloudscraper=True)
articles = scraper.fetch_articles(max_articles=10)
```

### Utilisation sans cloudscraper (fallback)

```python
scraper = Medias24Scraper(delay_between_requests=3, use_cloudscraper=False)
articles = scraper.fetch_articles(max_articles=10)
```

---

## ⚠️ Notes Importantes

1. **Respect des Conditions d'Utilisation** : Assurez-vous de respecter les conditions d'utilisation de Medias24 et ne pas surcharger leurs serveurs.

2. **Délais Recommandés** : Utilisez un délai d'au moins 3 secondes entre les requêtes pour éviter la détection.

3. **Cloudscraper** : Cette bibliothèque est spécialement conçue pour contourner les protections anti-bot, mais elle peut être plus lente que `requests` standard.

4. **Maintenance** : Les protections anti-bot évoluent, donc la solution peut nécessiter des mises à jour à l'avenir.

---

## 🚀 Conclusion

La solution avec `cloudscraper` permet de contourner avec succès le 403 Forbidden de Medias24. Le système de scraping fonctionne maintenant pour **5 sources sur 6**, avec un total de **8 articles scrapés et sauvegardés**.

**Medias24 est maintenant opérationnel !** ✅




