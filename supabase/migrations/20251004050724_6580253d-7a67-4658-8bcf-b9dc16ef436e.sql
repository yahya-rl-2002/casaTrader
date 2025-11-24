-- Add unique constraint on source_url to enable upsert operations
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint 
    WHERE conname = 'articles_source_url_key'
  ) THEN
    ALTER TABLE public.articles 
    ADD CONSTRAINT articles_source_url_key UNIQUE (source_url);
  END IF;
END $$;