-- Create documents bucket for financial reports
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'documents',
  'documents',
  true,
  52428800, -- 50MB limit
  ARRAY['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
)
ON CONFLICT (id) DO NOTHING;

-- Create policy to allow authenticated users to upload documents
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'objects' 
    AND policyname = 'Authenticated users can upload documents'
  ) THEN
    CREATE POLICY "Authenticated users can upload documents" 
    ON storage.objects 
    FOR INSERT 
    TO authenticated
    WITH CHECK (bucket_id = 'documents');
  END IF;
END $$;

-- Create policy to allow everyone to view documents
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'objects' 
    AND policyname = 'Documents are publicly viewable'
  ) THEN
    CREATE POLICY "Documents are publicly viewable" 
    ON storage.objects 
    FOR SELECT 
    USING (bucket_id = 'documents');
  END IF;
END $$;

-- Create policy to allow users to update their own documents
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'objects' 
    AND policyname = 'Users can update their own documents'
  ) THEN
    CREATE POLICY "Users can update their own documents" 
    ON storage.objects 
    FOR UPDATE 
    TO authenticated
    USING (bucket_id = 'documents');
  END IF;
END $$;

-- Create policy to allow users to delete their own documents
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'objects' 
    AND policyname = 'Users can delete their own documents'
  ) THEN
    CREATE POLICY "Users can delete their own documents" 
    ON storage.objects 
    FOR DELETE 
    TO authenticated
    USING (bucket_id = 'documents');
  END IF;
END $$;



