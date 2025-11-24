-- Fonction pour incrémenter le compteur de téléchargements
CREATE OR REPLACE FUNCTION increment_download_count(report_id UUID)
RETURNS void AS $$
BEGIN
  UPDATE financial_reports 
  SET download_count = COALESCE(download_count, 0) + 1,
      updated_at = NOW()
  WHERE id = report_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;



