import { useEffect, useState } from 'react';
import { supabase } from '@/integrations/supabase/client';

export function useSession() {
  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState<import('@supabase/supabase-js').Session | null>(null);

  useEffect(() => {
    let mounted = true;
    supabase.auth.getSession().then(({ data }) => {
      if (!mounted) return;
      setSession(data.session);
      setLoading(false);
    });

    const { data } = supabase.auth.onAuthStateChange((_event, s) => {
      if (!mounted) return;
      setSession(s);
    });

    return () => {
      mounted = false;
      data.subscription.unsubscribe();
    };
  }, []);

  const user = session?.user ?? null;
  return { session, user, loading };
}

