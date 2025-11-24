-- Create articles table if it does not exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_name = 'articles'
  ) THEN
    CREATE TABLE public.articles (
      id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
      title text NOT NULL,
      description text,
      content text,
      source text NOT NULL,
      source_url text NOT NULL,
      image_url text,
      published_at timestamptz,
      category text,
      tags text[],
      created_at timestamptz NOT NULL DEFAULT now(),
      updated_at timestamptz NOT NULL DEFAULT now()
    );

    -- Enable RLS with public read access
    ALTER TABLE public.articles ENABLE ROW LEVEL SECURITY;
    DO $$ BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE schemaname='public' AND tablename='articles' AND policyname='Articles are publicly viewable'
      ) THEN
        CREATE POLICY "Articles are publicly viewable" ON public.articles FOR SELECT USING (true);
      END IF;
    END $$;
  END IF;
END $$;

-- Unique constraint for upsert by URL
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'articles_source_url_key'
  ) THEN
    ALTER TABLE public.articles ADD CONSTRAINT articles_source_url_key UNIQUE (source_url);
  END IF;
END $$;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON public.articles(published_at);
CREATE INDEX IF NOT EXISTS idx_articles_category ON public.articles(category);
CREATE INDEX IF NOT EXISTS idx_articles_source ON public.articles(source);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'trg_update_articles_updated_at'
  ) THEN
    CREATE TRIGGER trg_update_articles_updated_at
    BEFORE UPDATE ON public.articles
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
  END IF;
END $$;




















