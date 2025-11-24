-- Fonction simple pour nettoyer les doublons d'articles
CREATE OR REPLACE FUNCTION cleanup_duplicate_articles()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER := 0;
BEGIN
    -- Supprimer les doublons en gardant le plus récent
    WITH duplicates AS (
        SELECT id, 
               ROW_NUMBER() OVER (
                   PARTITION BY source_url 
                   ORDER BY created_at DESC
               ) as rn
        FROM articles
    )
    DELETE FROM articles 
    WHERE id IN (
        SELECT id FROM duplicates WHERE rn > 1
    );
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Index pour optimiser les requêtes de nettoyage
CREATE INDEX IF NOT EXISTS idx_articles_published_at_cleanup 
ON articles(published_at) 
WHERE published_at IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_articles_source_url_unique 
ON articles(source_url);

