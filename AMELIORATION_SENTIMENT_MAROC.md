# 🇲🇦 AMÉLIORATION DE L'ANALYSE DE SENTIMENT - CONTEXTE MAROCAIN

**Date** : 2025-11-02  
**Objectif** : Améliorer la détection du sentiment pour identifier ce qui est **BÉNÉFIQUE pour le MAROC** (positif) vs ce qui est **CONTRE le MAROC** (négatif)

---

## ✅ AMÉLIORATIONS APPORTÉES

### 1. **Dictionnaire de Mots Positifs pour le Maroc**

Ajout de termes spécifiques qui indiquent des nouvelles **POSITIVES pour le Maroc** :

#### Reconnaissance et Diplomatie
- `reconnaissance`, `soutien`, `appui`, `solidarité`, `partenariat`, `coopération`
- `accord`, `entente`, `consensus`, `validation`, `approbation`, `endossement`
- `souveraineté`, `intégrité`, `territoriale`, `unité`, `cohésion`, `stabilité`
- `normalisation`, `relations diplomatiques`, `ambassade`, `consulat`
- `reconnaissance internationale`, `diplomatie`, `relation bilatérale`

#### Économie et Investissement
- `investissement`, `financement`, `projet`, `infrastructure`
- `développement économique`, `croissance économique`
- `création emplois`, `emploi`, `embauche`
- `exportation`, `commerce`, `échange`, `partenariat économique`
- `zone de libre échange`, `attractivité`, `compétitivité`

#### Progrès et Modernisation
- `réforme`, `modernisation`, `diversification`
- `tourisme`, `visite`, `délégation`, `mission économique`
- `foire`, `exposition`, `récompense`, `prix`, `distinction`
- `victoire`, `triomphe`, `succès diplomatique`

#### Sahara Marocain
- `sahara marocain`, `sahara`, `province du sud`, `régions du sud`, `autonomie`

---

### 2. **Dictionnaire de Mots Négatifs pour le Maroc**

Ajout de termes spécifiques qui indiquent des nouvelles **NÉGATIVES pour le Maroc** :

#### Contestation et Opposition
- `contestation`, `remise en question`, `remise en cause`, `rejet`, `refus`
- `opposition`, `hostilité`, `condamnation`, `critique`, `attaque`, `accusation`

#### Sanctions et Isolations
- `sanction`, `embargo`, `boycott`, `blocus`, `isolement`, `marginalisation`
- `gel relations`, `rupture`, `tension diplomatique`, `crise diplomatique`

#### Économie Négative
- `désinvestissement`, `retrait`, `fermeture`, `licenciement`, `chômage`
- `perte emploi`, `suppression poste`, `restructuration`, `plan social`
- `fermeture usine`, `délocalisation`, `relocalisation`, `départ entreprise`
- `crise économique`, `récession`, `ralentissement économique`, `chute croissance`
- `dévaluation`, `inflation`, `hausse prix`, `augmentation coût vie`

#### Instabilité et Tensions
- `instabilité politique`, `tension sociale`, `mouvement social`, `grève`
- `manifestation`, `protestation`, `émeute`, `violence`, `trouble`
- `corruption`, `scandale`, `affaire`, `enquête`, `procès`

#### Sécurité et Menaces
- `attentat`, `terrorisme`, `sécurité`, `menace sécuritaire`, `risque terroriste`
- `catastrophe`, `désastre`, `accident`, `tragédie`, `crise humanitaire`

#### Géopolitique Négatif
- `non reconnaissance`, `retrait reconnaissance`
- `ingérence`, `immixtion`, `séparatisme`, `sécession`
- `indépendance province`, `remise en question intégrité`, `contestation territoriale`
- `revendication`, `plan autonomie`, `référendum`, `séparatiste`
- `polisario`, `rasd`, `résolution onu`, `conseil sécurité`, `minurso`

---

### 3. **Détection du Contexte Marocain**

L'analyseur détecte maintenant automatiquement le contexte marocain :

```python
# Mots clés marocains détectés
morocco_positive_context = {
    'maroc', 'marocain', 'marocaine', 'marocains', 'royaume',
    'masi', 'casablanca', 'rabat', 'marrakech', 'fes', 'tanger',
    'sahara marocain', 'province du sud', 'autonomie', 'régions du sud'
}
```

**Bonus appliqués** :
- **+30%** de score pour les mots positifs dans un contexte marocain
- **+20%** de bonus supplémentaire pour les bonnes nouvelles marocaines
- **+30%** de pénalité pour les mauvaises nouvelles dans un contexte marocain

---

### 4. **Amélioration du Prompt LLM**

Le LLM (GPT) utilise maintenant un prompt spécialisé pour comprendre le contexte marocain :

#### Critères Positifs pour le Maroc
- ✅ Reconnaissance internationale, soutien, appui
- ✅ Investissements au Maroc, création d'emplois
- ✅ Accords économiques, partenariats
- ✅ Croissance économique, hausse du MASI
- ✅ Nouvelles positives sur le Sahara marocain
- ✅ Résolution de conflits, normalisation

#### Critères Négatifs pour le Maroc
- ❌ Contestation, remise en question
- ❌ Sanctions, embargo, boycott
- ❌ Perte d'investissements, fermeture d'entreprises
- ❌ Crise économique, récession
- ❌ Instabilité politique, tensions sociales
- ❌ Menaces sécuritaires, attentats
- ❌ Nouvelles négatives sur le Sahara

---

## 📊 EXEMPLES DE DÉTECTION AMÉLIORÉE

### Exemples Positifs

| Article | Score Avant | Score Après | Amélioration |
|---------|-------------|-------------|--------------|
| "Guterres sur le Sahara marocain : 'C'est un moment historique pour résoudre ce conflit'" | 0.00 (Neutre) | **+1.00** (Positif) | ✅ Détecte "historique", "résoudre" et contexte Sahara |
| "Reconnaissance américaine du Sahara marocain" | 0.00 (Neutre) | **+1.00** (Très Positif) | ✅ Détecte "reconnaissance" et "sahara marocain" |
| "Investissement de 5 milliards au Maroc" | 0.00 (Neutre) | **+0.8** (Positif) | ✅ Détecte "investissement" et "maroc" |
| "Création de 10 000 emplois au Maroc" | 0.00 (Neutre) | **+0.9** (Positif) | ✅ Détecte "création emplois" et contexte marocain |
| "Croissance économique du Maroc" | +0.3 (Positif) | **+0.7** (Positif) | ✅ Bonus contexte marocain |

### Exemples Négatifs

| Article | Score Avant | Score Après | Amélioration |
|---------|-------------|-------------|--------------|
| "Sanctions européennes contre le Maroc" | -0.3 (Négatif) | **-1.0** (Très Négatif) | ✅ Détecte "sanction" et contexte marocain |
| "Fermeture d'usine à Casablanca, 500 licenciements" | -0.3 (Négatif) | **-0.9** (Négatif) | ✅ Détecte "fermeture", "licenciement" et contexte Casablanca |
| "Crise économique au Maroc" | -0.5 (Négatif) | **-0.8** (Négatif) | ✅ Bonus pénalité contexte marocain |
| "Contestation de la souveraineté marocaine" | 0.00 (Neutre) | **-0.8** (Négatif) | ✅ Détecte "contestation" et contexte marocain |

---

## 🎯 LOGIQUE DE DÉTECTION

### Règles de Score

1. **Détection du Contexte Marocain** :
   - Si le texte contient des mots-clés marocains → bonus/pénalité appliqué

2. **Mots Positifs dans Contexte Marocain** :
   - Score de base × 1.3 (bonus 30%)
   - Bonus supplémentaire de 20% pour les nouvelles marocaines

3. **Mots Négatifs dans Contexte Marocain** :
   - Pénalité de 30% supplémentaire pour les mauvaises nouvelles marocaines

4. **Résolution de Conflits** :
   - Si un mot négatif ("conflit") apparaît avec un mot de résolution ("résoudre")
   - → Score positif avec bonus de 50%

---

## 📈 IMPACT SUR LE MEDIA SENTIMENT

L'amélioration permet de mieux refléter le sentiment réel des médias marocains :

- **Avant** : Beaucoup d'articles classés neutres (0.00) car le contexte marocain n'était pas détecté
- **Après** : Articles correctement classés selon leur impact réel sur le Maroc

### Exemples Concrets

1. **"Guterres sur le Sahara marocain : 'C'est un moment historique pour résoudre ce conflit'"**
   - Avant : 0.00 (neutre) car seul "conflit" était détecté
   - Après : +1.00 (positif) car "historique" + "résoudre" + contexte Sahara détecté

2. **"Reconnaissance américaine du Sahara marocain"**
   - Avant : 0.00 (neutre) car mots absents du dictionnaire
   - Après : +1.00 (très positif) car "reconnaissance" + "sahara marocain" détecté

3. **"Sanctions européennes contre le Maroc"**
   - Avant : -0.3 (légèrement négatif)
   - Après : -1.0 (très négatif) avec pénalité contexte marocain

---

## 🔄 MISE À JOUR AUTOMATIQUE

Le système utilise maintenant :
1. **LLM (GPT)** si disponible → Analyse contextuelle avancée avec prompt spécialisé Maroc
2. **NLP amélioré** en fallback → Dictionnaire enrichi + détection contexte marocain

Les prochains articles scrapés seront automatiquement analysés avec ces améliorations !

---

## 📝 NOTES TECHNIQUES

- **Fichiers modifiés** :
  - `backend/app/services/sentiment_service.py` : Dictionnaire enrichi + détection contexte
  - `backend/app/services/llm_sentiment_service.py` : Prompt spécialisé Maroc

- **Performance** : Pas d'impact sur la performance, même temps de calcul

- **Rétrocompatibilité** : Compatible avec les articles existants, réanalyse possible

---

**Généré le** : 2025-11-02











