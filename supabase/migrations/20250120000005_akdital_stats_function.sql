-- Fonction pour obtenir les statistiques spécifiques à Akdital
CREATE OR REPLACE FUNCTION get_akdital_stats()
RETURNS TABLE (
  total_reports BIGINT,
  akdital_reports BIGINT,
  reports_with_files BIGINT,
  reports_without_files BIGINT,
  total_file_size BIGINT,
  average_file_size BIGINT,
  is_all_akdital BOOLEAN,
  companies_count BIGINT,
  file_types_count BIGINT
) AS $$
BEGIN
  RETURN QUERY
  WITH akdital_filter AS (
    SELECT * FROM financial_reports 
    WHERE company_name = 'Akdital' 
       OR company_name = 'Société Inconnue'
       OR company_symbol = 'CSEMA:AKDITAL'
       OR company_symbol = 'CSEMA:UNKNOWN'
       OR 'akdital' = ANY(COALESCE(tags, ARRAY[]::text[]))
  ),
  stats AS (
    SELECT 
      COUNT(*) as total_reports,
      COUNT(CASE WHEN file_url IS NOT NULL THEN 1 END) as reports_with_files,
      COUNT(CASE WHEN file_url IS NULL THEN 1 END) as reports_without_files,
      COALESCE(SUM(file_size), 0) as total_file_size,
      CASE 
        WHEN COUNT(CASE WHEN file_url IS NOT NULL THEN 1 END) > 0 
        THEN COALESCE(SUM(file_size), 0) / COUNT(CASE WHEN file_url IS NOT NULL THEN 1 END)
        ELSE 0 
      END as average_file_size,
      COUNT(DISTINCT company_name) as companies_count,
      COUNT(DISTINCT file_type) as file_types_count
    FROM akdital_filter
  )
  SELECT 
    s.total_reports,
    s.total_reports as akdital_reports, -- Tous sont Akdital
    s.reports_with_files,
    s.reports_without_files,
    s.total_file_size,
    s.average_file_size,
    true as is_all_akdital, -- Toujours true car on filtre pour Akdital
    s.companies_count,
    s.file_types_count
  FROM stats s;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour obtenir les rapports Akdital groupés par entreprise
CREATE OR REPLACE FUNCTION get_akdital_by_company()
RETURNS TABLE (
  company_name TEXT,
  company_symbol TEXT,
  reports_count BIGINT,
  total_size BIGINT,
  file_types TEXT[]
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    fr.company_name,
    fr.company_symbol,
    COUNT(*) as reports_count,
    COALESCE(SUM(fr.file_size), 0) as total_size,
    ARRAY_AGG(DISTINCT fr.file_type) FILTER (WHERE fr.file_type IS NOT NULL) as file_types
  FROM financial_reports fr
  WHERE fr.company_name = 'Akdital' 
     OR fr.company_name = 'Société Inconnue'
     OR fr.company_symbol = 'CSEMA:AKDITAL'
     OR fr.company_symbol = 'CSEMA:UNKNOWN'
     OR 'akdital' = ANY(COALESCE(fr.tags, ARRAY[]::text[]))
  GROUP BY fr.company_name, fr.company_symbol
  ORDER BY reports_count DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour obtenir les rapports Akdital groupés par type de fichier
CREATE OR REPLACE FUNCTION get_akdital_by_file_type()
RETURNS TABLE (
  file_type TEXT,
  reports_count BIGINT,
  total_size BIGINT,
  companies TEXT[]
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COALESCE(fr.file_type, 'inconnu') as file_type,
    COUNT(*) as reports_count,
    COALESCE(SUM(fr.file_size), 0) as total_size,
    ARRAY_AGG(DISTINCT fr.company_name) as companies
  FROM financial_reports fr
  WHERE fr.company_name = 'Akdital' 
     OR fr.company_name = 'Société Inconnue'
     OR fr.company_symbol = 'CSEMA:AKDITAL'
     OR fr.company_symbol = 'CSEMA:UNKNOWN'
     OR 'akdital' = ANY(COALESCE(fr.tags, ARRAY[]::text[]))
  GROUP BY fr.file_type
  ORDER BY reports_count DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;




















