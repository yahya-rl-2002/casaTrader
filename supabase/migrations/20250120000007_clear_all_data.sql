-- Clear all data from tables
TRUNCATE TABLE public.articles CASCADE;
TRUNCATE TABLE public.financial_reports CASCADE;
TRUNCATE TABLE public.financial_docs CASCADE;

-- Reset sequences if they exist
DO $$
BEGIN
    -- Reset articles sequence
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE sequencename = 'articles_id_seq') THEN
        ALTER SEQUENCE articles_id_seq RESTART WITH 1;
    END IF;
    
    -- Reset financial_reports sequence  
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE sequencename = 'financial_reports_id_seq') THEN
        ALTER SEQUENCE financial_reports_id_seq RESTART WITH 1;
    END IF;
    
    -- Reset financial_docs sequence
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE sequencename = 'financial_docs_id_seq') THEN
        ALTER SEQUENCE financial_docs_id_seq RESTART WITH 1;
    END IF;
END $$;



















