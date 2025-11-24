from __future__ import annotations

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import math

from app.core.logging import get_logger


logger = get_logger(__name__)


@dataclass(slots=True)
class SentimentResult:
    polarity: float  # -1.0 to 1.0
    confidence: float  # 0.0 to 1.0
    positive_words: List[str]
    negative_words: List[str]
    neutral_words: List[str]


class SentimentAnalyzer:
    """Simple sentiment analysis for French financial text"""
    
    def __init__(self):
        # French financial sentiment dictionaries
        self.positive_words = {
            'hausse', 'croissance', 'hausse', 'augmentation', 'progression', 'amélioration',
            'bénéfice', 'profit', 'gain', 'succès', 'performance', 'excellente', 'positive',
            'optimiste', 'confiance', 'investissement', 'opportunité', 'potentiel', 'forte',
            'soutenu', 'résilient', 'robuste', 'dynamique', 'prometteur', 'attractif',
            'rentable', 'lucratif', 'florissant', 'prospère', 'expansion', 'développement',
            'innovation', 'technologie', 'digital', 'transformation', 'modernisation',
            'efficacité', 'productivité', 'compétitivité', 'leadership', 'excellence',
            # Mots de résolution et contexte positif
            'résoudre', 'solution', 'résolution', 'résolu', 'régler', 'dépasser', 'surmonter',
            'historique', 'moment historique', 'tournant', 'progrès', 'avancée', 'réussite',
            'pacifier', 'apaiser', 'normaliser', 'stabiliser',
            # TERMES POSITIFS POUR LE MAROC (bénéfiques pour le pays)
            'reconnaissance', 'soutien', 'appui', 'solidarité', 'partenariat', 'coopération',
            'accord', 'entente', 'consensus', 'validation', 'approbation', 'endossement',
            'souveraineté', 'intégrité', 'territoriale', 'unité', 'cohésion', 'stabilité',
            'investissement', 'financement', 'projet', 'infrastructure', 'développement économique',
            'croissance économique', 'création emplois', 'création', 'emplois', 'emploi', 'embauche',
            'exportation', 'commerce', 'échange', 'partenariat économique', 'zone de libre échange',
            'réforme', 'modernisation', 'diversification', 'compétitivité', 'attractivité',
            'tourisme', 'visite', 'délégation', 'mission économique', 'foire', 'exposition',
            'récompense', 'prix', 'distinction', 'label', 'certification', 'qualification',
            'victoire', 'triomphe', 'succès diplomatique', 'diplomatie', 'relation bilatérale',
            'sahara marocain', 'sahara', 'province du sud', 'régions du sud', 'autonomie',
            'normalisation', 'relations diplomatiques', 'ambassade', 'consulat', 'reconnaissance internationale'
        }
        
        # Phrases complètes positives pour le Maroc
        self.positive_phrases = {
            'création emplois', 'création d\'emplois', 'création d\'emploi', 'création d emplois',
            'au maroc', 'du maroc', 'au marocain', 'pour le maroc', 'pour le marocain',
            'au sahara marocain', 'du sahara marocain', 'sahara marocain',
            'reconnaissance internationale', 'soutien international', 'appui international',
            'croissance économique', 'développement économique', 'investissement étranger'
        }
        
        self.negative_words = {
            'baisse', 'chute', 'déclin', 'récession', 'crise', 'difficulté', 'problème',
            'négative', 'pessimiste', 'inquiétude', 'risque', 'incertitude', 'volatilité',
            'instabilité', 'tension', 'conflit', 'déséquilibre', 'déficit', 'perte',
            'défaillance', 'faillite', 'chômage', 'inflation', 'dévaluation', 'dépression',
            'stagnation', 'ralentissement', 'affaiblissement', 'dégradation', 'détérioration',
            'menace', 'danger', 'alerte', 'préoccupation', 'anxiété', 'pessimisme',
            'décroissance', 'contraction', 'réduction', 'diminution', 'affaiblissement',
            # TERMES NÉGATIFS POUR LE MAROC (contre le pays)
            'contestation', 'remise en question', 'remise en cause', 'rejet', 'refus',
            'opposition', 'hostilité', 'condamnation', 'critique', 'attaque', 'accusation',
            'sanction', 'embargo', 'boycott', 'blocus', 'isolement', 'marginalisation',
            'désinvestissement', 'retrait', 'fermeture', 'licenciement', 'chômage',
            'perte emploi', 'suppression poste', 'restructuration', 'plan social',
            'fermeture usine', 'délocalisation', 'relocalisation', 'départ entreprise',
            'crise économique', 'récession', 'ralentissement économique', 'chute croissance',
            'dévaluation', 'inflation', 'hausse prix', 'augmentation coût vie',
            'instabilité politique', 'tension sociale', 'mouvement social', 'grève',
            'manifestation', 'protestation', 'émeute', 'violence', 'trouble',
            'corruption', 'scandale', 'affaire', 'enquête', 'procès', 'condamnation',
            'attentat', 'terrorisme', 'sécurité', 'menace sécuritaire', 'risque terroriste',
            'catastrophe', 'désastre', 'accident', 'tragédie', 'crise humanitaire',
            'sécheresse', 'inondation', 'tremblement terre', 'catastrophe naturelle',
            # Contexte géopolitique négatif pour le Maroc
            'non reconnaissance', 'retrait reconnaissance', 'gel relations', 'rupture',
            'tension diplomatique', 'crise diplomatique', 'conflit diplomatique',
            'ingérence', 'immixtion', 'séparatisme', 'sécession', 'indépendance province',
            'remise en question intégrité', 'contestation territoriale', 'revendication',
            'plan autonomie', 'référendum', 'séparatiste', 'polisario', 'rasd',
            'résolution onu', 'conseil sécurité', 'minurso', 'mission onu'
        }
        
        # Phrases complètes négatives pour le Maroc
        self.negative_phrases = {
            'sanctions contre', 'sanctions au', 'embargo contre', 'boycott contre',
            'contre le maroc', 'contre le marocain', 'contre maroc',
            'fermeture usine', 'fermeture d usine', 'licenciement', 'licenciements',
            'crise économique', 'crise au maroc', 'crise du maroc',
            'perte emploi', 'perte d emploi', 'perte d emplois', 'suppression poste'
        }
        
        # Financial context words that can modify sentiment
        self.intensifiers = {
            'très', 'extrêmement', 'fortement', 'considérablement', 'significativement',
            'substantiellement', 'drastiquement', 'radicalement', 'complètement',
            'totalement', 'absolument', 'parfaitement', 'exactement', 'précisément'
        }
        
        self.negators = {
            'pas', 'ne', 'non', 'aucun', 'jamais', 'rien', 'personne', 'nulle',
            'sans', 'ni', 'nullement', 'guère', 'peu', 'moins', 'déjà'
        }

    def analyze_text(self, text: str) -> SentimentResult:
        """Analyze sentiment of a text"""
        if not text or not text.strip():
            return SentimentResult(0.0, 0.0, [], [], [])
        
        # Clean and tokenize text
        cleaned_text = self._clean_text(text)
        words = self._tokenize(cleaned_text)
        
        if not words:
            return SentimentResult(0.0, 0.0, [], [], [])
        
        # Analyze sentiment
        positive_score, negative_score = self._calculate_sentiment_scores(words)
        
        # Calculate polarity (-1 to 1)
        total_score = positive_score + negative_score
        if total_score == 0:
            polarity = 0.0
        else:
            polarity = (positive_score - negative_score) / total_score
        
        # Calculate confidence based on word count and score magnitude
        word_count = len(words)
        confidence = min(1.0, (abs(positive_score - negative_score) / max(word_count, 1)) * 2)
        
        # Categorize words
        positive_words = self._extract_words_by_sentiment(words, 'positive')
        negative_words = self._extract_words_by_sentiment(words, 'negative')
        neutral_words = self._extract_words_by_sentiment(words, 'neutral')
        
        return SentimentResult(
            polarity=polarity,
            confidence=confidence,
            positive_words=positive_words,
            negative_words=negative_words,
            neutral_words=neutral_words
        )

    def analyze_articles(self, articles: List) -> List[SentimentResult]:
        """Analyze sentiment for multiple articles"""
        results = []
        for article in articles:
            # Combine title and summary for analysis
            text = f"{article.title} {article.summary}"
            result = self.analyze_text(text)
            results.append(result)
        return results

    def _clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep French accents
        text = re.sub(r'[^\w\sàâäéèêëïîôöùûüÿç]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words and phrases"""
        words = [word for word in text.split() if len(word) > 2]
        
        # Ajouter des phrases complètes pour mieux détecter les expressions composées
        phrases = []
        for i in range(len(words) - 1):
            # Bigrammes (2 mots consécutifs)
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)
        
        return words + phrases

    def _calculate_sentiment_scores(self, words: List[str]) -> tuple[float, float]:
        """Calculate positive and negative sentiment scores with Moroccan context"""
        positive_score = 0.0
        negative_score = 0.0
        
        # Mots positifs de résolution (annulent l'effet négatif de mots comme "conflit")
        resolution_words = {'résoudre', 'solution', 'régler', 'résolution', 'résout', 
                          'résolu', 'dépasser', 'surmonter', 'vaincre', 'terminer',
                          'finir', 'clôturer', 'apaiser', 'pacifier', 'normaliser',
                          'mettre fin', 'tourner la page', 'historique', 'moment historique'}
        
        # Mots clés marocains qui changent le contexte
        morocco_positive_context = {'maroc', 'marocain', 'marocaine', 'marocains', 'royaume',
                                  'masi', 'casablanca', 'rabat', 'marrakech', 'fes', 'tanger',
                                  'sahara marocain', 'province du sud', 'autonomie', 'régions du sud'}
        
        for i, word in enumerate(words):
            base_score = 1.0
            is_negated = False
            is_resolution_context = False
            is_morocco_context = False
            
            # Check for negation
            if i > 0 and words[i-1] in self.negators:
                is_negated = True
                base_score = -1.0
            
            # Check for resolution context (3 words before or after)
            context_window = 5  # Augmenté pour mieux capturer le contexte
            start_idx = max(0, i - context_window)
            end_idx = min(len(words), i + context_window + 1)
            context_words = words[start_idx:end_idx]
            context_text = ' '.join(context_words)
            
            # Si on trouve un mot de résolution dans le contexte, c'est un contexte positif
            for ctx_word in context_words:
                if ctx_word in resolution_words:
                    is_resolution_context = True
                    break
            
            # Vérifier le contexte marocain
            for morocco_word in morocco_positive_context:
                if morocco_word in context_text:
                    is_morocco_context = True
                    break
            
            # Check for intensifiers
            if i > 0 and words[i-1] in self.intensifiers:
                base_score *= 1.5
            
            # Bonus pour les mots positifs dans un contexte marocain
            if is_morocco_context:
                base_score *= 1.3  # Bonus de 30% pour le contexte marocain
            
            # Check word sentiment (mots simples et phrases)
            word_lower = word.lower()
            is_positive_phrase = word_lower in self.positive_phrases or any(phrase in word_lower for phrase in self.positive_phrases)
            is_negative_phrase = word_lower in self.negative_phrases or any(phrase in word_lower for phrase in self.negative_phrases)
            
            if word in self.positive_words or is_positive_phrase:
                if is_negated:
                    negative_score += base_score
                else:
                    positive_score += base_score
                    # Bonus si c'est dans un contexte marocain
                    if is_morocco_context:
                        positive_score += base_score * 0.2  # Bonus supplémentaire
                    # Bonus supplémentaire pour les phrases positives
                    if is_positive_phrase:
                        positive_score += base_score * 0.5  # Bonus pour les phrases complètes
            elif word in self.negative_words or is_negative_phrase:
                if is_negated:
                    positive_score += base_score
                elif is_resolution_context:
                    # Si on résout un conflit/problème, c'est positif !
                    positive_score += base_score * 1.5  # Bonus pour la résolution
                else:
                    negative_score += base_score
                    # Pénalité si c'est dans un contexte marocain négatif
                    if is_morocco_context and not is_resolution_context:
                        negative_score += base_score * 0.3  # Pénalité supplémentaire
        
        return positive_score, negative_score

    def _extract_words_by_sentiment(self, words: List[str], sentiment_type: str) -> List[str]:
        """Extract words by sentiment type"""
        if sentiment_type == 'positive':
            return [word for word in words if word in self.positive_words]
        elif sentiment_type == 'negative':
            return [word for word in words if word in self.negative_words]
        else:  # neutral
            return [word for word in words if word not in self.positive_words and word not in self.negative_words]

    def get_sentiment_label(self, polarity: float) -> str:
        """Get human-readable sentiment label"""
        if polarity >= 0.3:
            return "Positive"
        elif polarity <= -0.3:
            return "Negative"
        else:
            return "Neutral"

    def get_sentiment_color(self, polarity: float) -> str:
        """Get color code for sentiment"""
        if polarity >= 0.3:
            return "#10b981"  # Green
        elif polarity <= -0.3:
            return "#ef4444"  # Red
        else:
            return "#f59e0b"  # Yellow