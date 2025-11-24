# 🔄 Gestion des Migrations de Base de Données

## ✅ Implémentation Complète

Le système utilise maintenant **Alembic** pour gérer toutes les migrations de base de données de manière professionnelle et versionnée.

---

## 📋 Structure

```
backend/
├── alembic/
│   ├── env.py              # Configuration Alembic
│   ├── script.py.mako      # Template pour nouvelles migrations
│   └── versions/           # Migrations versionnées
│       └── *.py            # Fichiers de migration
├── alembic.ini              # Configuration Alembic
└── scripts/
    └── migrate.py          # Script helper pour migrations
```

---

## 🚀 Utilisation

### Commandes de Base

#### 1. Voir l'état actuel
```bash
cd backend
python scripts/migrate.py current
# ou directement
alembic current
```

#### 2. Appliquer toutes les migrations
```bash
python scripts/migrate.py upgrade
# ou
alembic upgrade head
```

#### 3. Appliquer jusqu'à une version spécifique
```bash
python scripts/migrate.py upgrade <revision>
# Exemple: alembic upgrade 9abb0d2fd4ad
```

#### 4. Annuler la dernière migration
```bash
python scripts/migrate.py downgrade
# ou
alembic downgrade -1
```

#### 5. Voir l'historique
```bash
python scripts/migrate.py history
# ou
alembic history
```

### Créer de Nouvelles Migrations

#### Migration Auto-générée (Recommandé)
```bash
# Alembic détecte automatiquement les changements dans les modèles
python scripts/migrate.py autogenerate "add new column to table"
# ou
alembic revision --autogenerate -m "add new column to table"
```

#### Migration Manuelle
```bash
# Créer une migration vide à éditer manuellement
python scripts/migrate.py create "custom migration"
# ou
alembic revision -m "custom migration"
```

---

## 📝 Workflow Recommandé

### 1. Modifier les Modèles

Éditer `backend/app/models/schemas.py` :
```python
class MediaArticle(Base):
    __tablename__ = "media_articles"
    # ... colonnes existantes ...
    new_column = Column(String, nullable=True)  # Nouvelle colonne
```

### 2. Générer la Migration

```bash
cd backend
python scripts/migrate.py autogenerate "add new_column to media_articles"
```

### 3. Vérifier la Migration

Éditer le fichier généré dans `alembic/versions/` pour vérifier/corriger si nécessaire.

### 4. Appliquer la Migration

```bash
python scripts/migrate.py upgrade
```

### 5. Vérifier

```bash
python scripts/migrate.py current
```

---

## 🔧 Configuration

### Fichier `alembic.ini`

La configuration utilise automatiquement `DATABASE_URL` depuis les settings :
- Développement : `sqlite:///./fear_greed.db`
- Production : `postgresql://user:pass@host:5432/dbname`

### Fichier `alembic/env.py`

Configuré pour :
- ✅ Charger automatiquement les modèles depuis `app.models.schemas`
- ✅ Utiliser la `database_url` depuis les settings
- ✅ Support SQLite et PostgreSQL
- ✅ Comparaison automatique des types et defaults

---

## 📊 Migrations Existantes

### Migration Initiale
- **Fichier**: `9abb0d2fd4ad_initial_migration_create_index_scores_.py`
- **Description**: Crée les tables `index_scores` et `media_articles` avec toutes les colonnes

### Colonnes Incluses

**Table `index_scores`**:
- id, as_of, score
- momentum, price_strength, volume, volatility
- equity_vs_bonds, media_sentiment
- created_at

**Table `media_articles`**:
- id, title, summary, content
- url, source, image_url
- published_at, sentiment_score, sentiment_label
- scraped_at, created_at

---

## 🔄 Migration depuis les Scripts Manuels

Les anciens scripts manuels (`add_content_column.py`, `add_image_url_column.py`) sont maintenant **obsolètes**.

**Si vous avez déjà exécuté ces scripts** :
- Les colonnes existent déjà dans votre DB
- Alembic détectera qu'elles existent et ne les recréera pas
- Vous pouvez continuer à utiliser Alembic pour les futures migrations

**Si vous partez de zéro** :
- Exécutez simplement `alembic upgrade head`
- Toutes les tables et colonnes seront créées automatiquement

---

## 🛠️ Commandes Utiles

### Voir les Différences (sans créer de migration)
```bash
alembic check
```

### Créer une Migration Vide
```bash
alembic revision -m "description"
```

### Marquer la DB comme étant à une version spécifique (sans appliquer)
```bash
alembic stamp <revision>
```

### Voir le SQL qui sera exécuté (sans l'appliquer)
```bash
alembic upgrade head --sql
```

---

## ⚠️ Bonnes Pratiques

### 1. Toujours Vérifier les Migrations Auto-générées

Alembic peut parfois manquer certains changements ou proposer des modifications incorrectes. **Toujours vérifier** le fichier de migration avant de l'appliquer.

### 2. Tester en Développement d'Abord

```bash
# 1. Tester la migration
alembic upgrade head

# 2. Vérifier que tout fonctionne
python -m pytest

# 3. Si problème, annuler
alembic downgrade -1
```

### 3. Backup Avant Migration en Production

```bash
# PostgreSQL
pg_dump -U user -d dbname > backup_before_migration.sql

# SQLite
cp fear_greed.db fear_greed.db.backup
```

### 4. Migrations Irréversibles

Certaines migrations (comme supprimer une colonne) sont difficiles à annuler. Créer une migration de rollback si nécessaire.

---

## 🐛 Dépannage

### Erreur: "Target database is not up to date"

**Solution**:
```bash
# Voir l'état actuel
alembic current

# Appliquer les migrations manquantes
alembic upgrade head
```

### Erreur: "Can't locate revision identified by 'xxxxx'"

**Solution**:
```bash
# Voir l'historique
alembic history

# Marquer la DB à la bonne version
alembic stamp head
```

### Migration Échoue

**Solution**:
```bash
# Annuler la migration
alembic downgrade -1

# Corriger le fichier de migration
# Puis réessayer
alembic upgrade head
```

### SQLite et ALTER TABLE

SQLite a des limitations sur `ALTER TABLE`. Alembic gère automatiquement ces cas en créant une nouvelle table et en copiant les données.

---

## 📈 Exemples de Migrations

### Ajouter une Colonne

**1. Modifier le modèle**:
```python
class MediaArticle(Base):
    # ... colonnes existantes ...
    new_field = Column(String, nullable=True)
```

**2. Générer la migration**:
```bash
alembic revision --autogenerate -m "add new_field to media_articles"
```

**3. Appliquer**:
```bash
alembic upgrade head
```

### Modifier une Colonne

**1. Modifier le modèle**:
```python
class MediaArticle(Base):
    # Avant: title = Column(String, nullable=False)
    title = Column(String(500), nullable=False)  # Limite de longueur
```

**2. Générer et appliquer** (comme ci-dessus)

### Supprimer une Colonne

**1. Retirer du modèle**:
```python
class MediaArticle(Base):
    # Retirer: old_field = Column(String, nullable=True)
    pass
```

**2. Générer la migration** (Alembic détectera la suppression)

**3. ⚠️ Vérifier la migration** - peut nécessiter une copie de données

---

## 🔐 Migration en Production

### Checklist

- [ ] Backup de la base de données
- [ ] Tester la migration en staging
- [ ] Vérifier le fichier de migration généré
- [ ] Planifier une fenêtre de maintenance si nécessaire
- [ ] Documenter les changements
- [ ] Prévoir un plan de rollback

### Commandes Production

```bash
# 1. Backup
pg_dump -U user -d dbname > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Voir les migrations à appliquer
alembic current
alembic history

# 3. Voir le SQL (sans appliquer)
alembic upgrade head --sql

# 4. Appliquer
alembic upgrade head

# 5. Vérifier
alembic current
```

---

## 📚 Ressources

- [Documentation Alembic](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Migrations](https://docs.sqlalchemy.org/en/20/core/metadata.html)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

**Date**: 2025-11-13  
**Version**: 1.0.0  
**Statut**: ✅ Implémenté et Opérationnel



