-- Create financial_reports table
CREATE TABLE IF NOT EXISTS public.financial_reports (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  company_symbol TEXT NOT NULL,
  company_name TEXT NOT NULL,
  report_type TEXT NOT NULL CHECK (report_type IN ('rapport-annuel', 'resultats', 'communique', 'profit-warning', 'autre')),
  title TEXT NOT NULL,
  description TEXT,
  file_url TEXT,
  file_name TEXT,
  file_size BIGINT,
  file_type TEXT,
  published_at TIMESTAMP WITH TIME ZONE,
  period_start DATE,
  period_end DATE,
  tags TEXT[],
  featured BOOLEAN DEFAULT false,
  download_count INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  created_by UUID REFERENCES auth.users(id)
);

-- Enable Row Level Security
ALTER TABLE public.financial_reports ENABLE ROW LEVEL SECURITY;

-- Create policies for financial_reports
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'financial_reports' 
    AND policyname = 'Financial reports are viewable by everyone'
  ) THEN
    CREATE POLICY "Financial reports are viewable by everyone" 
    ON public.financial_reports 
    FOR SELECT 
    USING (true);
  END IF;
END $$;

DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'financial_reports' 
    AND policyname = 'Authenticated users can insert financial reports'
  ) THEN
    CREATE POLICY "Authenticated users can insert financial reports" 
    ON public.financial_reports 
    FOR INSERT 
    TO authenticated
    WITH CHECK (true);
  END IF;
END $$;

DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'financial_reports' 
    AND policyname = 'Users can update their own financial reports'
  ) THEN
    CREATE POLICY "Users can update their own financial reports" 
    ON public.financial_reports 
    FOR UPDATE 
    TO authenticated
    USING (auth.uid() = created_by);
  END IF;
END $$;

DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'financial_reports' 
    AND policyname = 'Users can delete their own financial reports'
  ) THEN
    CREATE POLICY "Users can delete their own financial reports" 
    ON public.financial_reports 
    FOR DELETE 
    TO authenticated
    USING (auth.uid() = created_by);
  END IF;
END $$;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_financial_reports_company_symbol ON public.financial_reports(company_symbol);
CREATE INDEX IF NOT EXISTS idx_financial_reports_report_type ON public.financial_reports(report_type);
CREATE INDEX IF NOT EXISTS idx_financial_reports_published_at ON public.financial_reports(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_financial_reports_featured ON public.financial_reports(featured);
CREATE INDEX IF NOT EXISTS idx_financial_reports_period ON public.financial_reports(period_start, period_end);

-- Create trigger for automatic timestamp updates
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger 
    WHERE tgname = 'update_financial_reports_updated_at'
  ) THEN
    CREATE TRIGGER update_financial_reports_updated_at
    BEFORE UPDATE ON public.financial_reports
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
  END IF;
END $$;

-- Create function to increment download count
CREATE OR REPLACE FUNCTION public.increment_download_count(report_id UUID)
RETURNS void AS $$
BEGIN
  UPDATE public.financial_reports 
  SET download_count = download_count + 1 
  WHERE id = report_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION public.increment_download_count(UUID) TO authenticated;


