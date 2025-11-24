-- Migration pour organiser les données Akdital
-- Focus sur Akdital uniquement pour bien structurer la base de données

-- 1. Mettre à jour tous les rapports pour qu'ils soient clairement identifiés comme Akdital
UPDATE financial_reports 
SET 
  company_name = 'Akdital',
  company_symbol = 'CSEMA:AKDITAL',
  description = COALESCE(description, 'Rapport financier officiel d''Akdital'),
  tags = ARRAY['akdital', 'officiel', 'rapport-financier', 'health-care', 'sante']
WHERE 
  company_name = 'Société Inconnue' 
  OR company_symbol = 'CSEMA:UNKNOWN'
  OR company_name = 'Akdital'
  OR company_symbol = 'CSEMA:AKDITAL'
  OR 'akdital' = ANY(COALESCE(tags, ARRAY[]::text[]));

-- 2. Ajouter une colonne sector si elle n'existe pas
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'financial_reports' 
    AND column_name = 'sector'
  ) THEN
    ALTER TABLE financial_reports ADD COLUMN sector VARCHAR(50);
  END IF;
END $$;

-- 3. Mettre à jour le secteur pour Akdital
UPDATE financial_reports 
SET sector = 'Health Care'
WHERE company_name = 'Akdital' 
   OR company_symbol = 'CSEMA:AKDITAL';

-- 4. Créer un index pour optimiser les requêtes Akdital
CREATE INDEX IF NOT EXISTS idx_financial_reports_akdital 
ON financial_reports(company_name, company_symbol) 
WHERE company_name = 'Akdital' OR company_symbol = 'CSEMA:AKDITAL';

-- 5. Créer un index pour le secteur Health Care
CREATE INDEX IF NOT EXISTS idx_financial_reports_health_care 
ON financial_reports(sector) 
WHERE sector = 'Health Care';

-- 6. Ajouter des contraintes pour s'assurer de la cohérence des données
ALTER TABLE financial_reports 
ADD CONSTRAINT check_akdital_consistency 
CHECK (
  (company_name = 'Akdital' AND company_symbol = 'CSEMA:AKDITAL') OR
  (company_name != 'Akdital' AND company_symbol != 'CSEMA:AKDITAL')
);

-- 7. Créer une vue spécialisée pour Akdital
CREATE OR REPLACE VIEW akdital_reports AS
SELECT 
  id,
  company_name,
  company_symbol,
  report_type,
  title,
  description,
  file_url,
  file_name,
  file_size,
  file_type,
  published_at,
  period_start,
  period_end,
  tags,
  featured,
  download_count,
  sector,
  created_at,
  updated_at,
  created_by
FROM financial_reports
WHERE company_name = 'Akdital' 
   OR company_symbol = 'CSEMA:AKDITAL'
   OR 'akdital' = ANY(COALESCE(tags, ARRAY[]::text[]));

-- 8. Créer une fonction pour obtenir les statistiques Akdital
CREATE OR REPLACE FUNCTION get_akdital_summary()
RETURNS TABLE (
  total_reports BIGINT,
  reports_with_files BIGINT,
  total_file_size BIGINT,
  average_file_size BIGINT,
  featured_reports BIGINT,
  total_downloads BIGINT,
  latest_report_date TIMESTAMP,
  oldest_report_date TIMESTAMP
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COUNT(*) as total_reports,
    COUNT(CASE WHEN file_url IS NOT NULL THEN 1 END) as reports_with_files,
    COALESCE(SUM(file_size), 0) as total_file_size,
    CASE 
      WHEN COUNT(CASE WHEN file_url IS NOT NULL THEN 1 END) > 0 
      THEN COALESCE(SUM(file_size), 0) / COUNT(CASE WHEN file_url IS NOT NULL THEN 1 END)
      ELSE 0 
    END as average_file_size,
    COUNT(CASE WHEN featured = true THEN 1 END) as featured_reports,
    COALESCE(SUM(download_count), 0) as total_downloads,
    MAX(published_at) as latest_report_date,
    MIN(published_at) as oldest_report_date
  FROM financial_reports
  WHERE company_name = 'Akdital' 
     OR company_symbol = 'CSEMA:AKDITAL'
     OR 'akdital' = ANY(COALESCE(tags, ARRAY[]::text[]));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 9. Créer une fonction pour nettoyer les données Akdital
CREATE OR REPLACE FUNCTION clean_akdital_data()
RETURNS void AS $$
BEGIN
  -- Supprimer les doublons basés sur le titre et la date
  DELETE FROM financial_reports 
  WHERE id IN (
    SELECT id FROM (
      SELECT id, 
             ROW_NUMBER() OVER (
               PARTITION BY title, published_at 
               ORDER BY created_at DESC
             ) as rn
      FROM financial_reports
      WHERE company_name = 'Akdital' 
         OR company_symbol = 'CSEMA:AKDITAL'
    ) t 
    WHERE rn > 1
  );
  
  -- Mettre à jour les tags pour être cohérents
  UPDATE financial_reports 
  SET tags = ARRAY['akdital', 'officiel', 'rapport-financier', 'health-care', 'sante']
  WHERE company_name = 'Akdital' 
     OR company_symbol = 'CSEMA:AKDITAL';
     
  -- S'assurer que tous les rapports Akdital ont le bon secteur
  UPDATE financial_reports 
  SET sector = 'Health Care'
  WHERE (company_name = 'Akdital' OR company_symbol = 'CSEMA:AKDITAL')
    AND (sector IS NULL OR sector != 'Health Care');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 10. Exécuter le nettoyage des données
SELECT clean_akdital_data();

-- 11. Créer une politique RLS pour Akdital (si nécessaire)
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'financial_reports' 
    AND policyname = 'Akdital reports are viewable by everyone'
  ) THEN
    CREATE POLICY "Akdital reports are viewable by everyone" 
    ON financial_reports 
    FOR SELECT 
    USING (
      company_name = 'Akdital' 
      OR company_symbol = 'CSEMA:AKDITAL'
      OR 'akdital' = ANY(COALESCE(tags, ARRAY[]::text[]))
    );
  END IF;
END $$;
