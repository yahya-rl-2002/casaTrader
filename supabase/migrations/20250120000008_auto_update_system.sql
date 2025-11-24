-- Fonction pour nettoyer les doublons d'articles
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

-- Fonction pour nettoyer les anciens articles
CREATE OR REPLACE FUNCTION cleanup_old_articles(days_old INTEGER DEFAULT 7)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER := 0;
    cutoff_date TIMESTAMP;
BEGIN
    cutoff_date := NOW() - INTERVAL '1 day' * days_old;
    
    DELETE FROM articles 
    WHERE published_at < cutoff_date;
    
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

-- Vue pour les statistiques d'actualisation
CREATE OR REPLACE VIEW auto_update_stats AS
SELECT 
    COUNT(*) as total_articles,
    COUNT(DISTINCT source) as active_sources,
    COUNT(CASE WHEN published_at > NOW() - INTERVAL '1 hour' THEN 1 END) as articles_last_hour,
    COUNT(CASE WHEN published_at > NOW() - INTERVAL '24 hours' THEN 1 END) as articles_last_24h,
    MAX(published_at) as latest_article_date,
    MIN(published_at) as oldest_article_date
FROM articles;

-- Fonction pour obtenir les statistiques d'actualisation
CREATE OR REPLACE FUNCTION get_auto_update_stats()
RETURNS TABLE(
    total_articles BIGINT,
    active_sources BIGINT,
    articles_last_hour BIGINT,
    articles_last_24h BIGINT,
    latest_article_date TIMESTAMP,
    oldest_article_date TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM auto_update_stats;
END;
$$ LANGUAGE plpgsql;



















