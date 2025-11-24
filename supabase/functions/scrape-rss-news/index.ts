import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface Article {
  title: string;
  description?: string | null;
  content?: string | null;
  source: string;
  source_url: string;
  image_url?: string | null;
  published_at?: string | null;
  category?: string | null;
  tags?: string[] | null;
}

const RSS_FEEDS = [
  { name: 'Hespress', url: 'https://fr.hespress.com/rss', category: 'Économie' },
  { name: 'Medias24', url: 'https://www.medias24.com/rss', category: 'Économie' },
  { name: 'Le360', url: 'https://fr.le360.ma/rss', category: 'Économie' },
  { name: 'H24Info', url: 'https://www.h24info.ma/rss', category: 'Économie' },
  { name: "L'Opinion", url: 'https://www.lopinion.ma/xml/syndication.rss', category: 'Économie' },
  { name: 'TelQuel', url: 'https://telquel.ma/feed', category: 'Économie' },
];

function sanitiseHtmlToText(html: string): string {
  return html
    .replace(/<\/(script|style)[^>]*>/gi, '')
    .replace(/<br\s*\/?>(?=\s*<br)/gi, '<br/>')
    .replace(/<p[^>]*>/gi, '')
    .replace(/<\/(p|div)>/gi, '\n\n')
    .replace(/<[^>]+>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function parseRSS(rssText: string, sourceName: string, category: string): Article[] {
  const articles: Article[] = [];

  try {
    const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
    let match: RegExpExecArray | null;

    while ((match = itemRegex.exec(rssText)) !== null) {
      const itemContent = match[1];

      const titleMatch = itemContent.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>|<title>(.*?)<\/title>/i);
      const title = titleMatch ? (titleMatch[1] || titleMatch[2]) : null;

      const descMatch = itemContent.match(/<description><!\[CDATA\[(.*?)\]\]><\/description>|<description>(.*?)<\/description>/i);
      const description = descMatch ? (descMatch[1] || descMatch[2]) : null;

      const contentMatch = itemContent.match(/<content:encoded><!\[CDATA\[([\s\S]*?)\]\]><\/content:encoded>/i);
      let encodedHtml = contentMatch ? contentMatch[1] : null;
      if (encodedHtml) encodedHtml = encodedHtml.replace(/\r/g, '');

      const linkMatch = itemContent.match(/<link>(.*?)<\/link>/i);
      const link = linkMatch ? linkMatch[1] : null;

      const dateMatch = itemContent.match(/<pubDate>(.*?)<\/pubDate>/i);
      const pubDate = dateMatch ? new Date(dateMatch[1]).toISOString() : new Date().toISOString();

      const enclosureMatch = itemContent.match(/<enclosure[^>]+type="image[^\"]*"[^>]+url="([^"]+)"/i);
      let image: string | null = enclosureMatch ? enclosureMatch[1] : null;
      if (!image) {
        const mediaMatch = itemContent.match(/<media:(?:content|thumbnail)[^>]+url="([^"]+)"/i);
        if (mediaMatch?.[1]) image = mediaMatch[1];
      }
      if (!image && encodedHtml) {
        const encodedImage = encodedHtml.match(/<img[^>]+src="([^"]+)"/i);
        if (encodedImage?.[1]) image = encodedImage[1];
      }

      if (!title || !link) continue;

      let content: string | null = null;
      if (encodedHtml) {
        const text = sanitiseHtmlToText(encodedHtml);
        content = text.length ? text : null;
      }
      if (!content && description) content = description.trim();

      articles.push({
        title: title.trim(),
        description: description ? description.trim().substring(0, 500) : null,
        content,
        source: sourceName,
        source_url: link.trim(),
        image_url: image,
        published_at: pubDate,
        category,
        tags: ['rss', 'actualités', 'maroc'],
      });
    }
  } catch (error) {
    console.error('Erreur parsing RSS:', error);
  }

  return articles;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? Deno.env.get('PROJECT_URL') ?? '';
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? Deno.env.get('SERVICE_ROLE_KEY') ?? '';
    const anonKey = Deno.env.get('SUPABASE_ANON_KEY') ?? '';

    if (!supabaseUrl) {
      console.error('❌ SUPABASE_URL missing');
      return new Response(
        JSON.stringify({ success: false, error: 'SUPABASE_URL missing' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 },
      );
    }

    const keyToUse = serviceKey || anonKey;
    const supabaseClient = createClient(supabaseUrl, keyToUse, {
      global: { headers: { Authorization: req.headers.get('Authorization') ?? '' } },
    });

    console.log('🔄 Début du scraping RSS...');

    const allArticles: Article[] = [];

    for (const feed of RSS_FEEDS) {
      try {
        console.log(`📰 Scraping RSS: ${feed.name}`);
        const response = await fetch(feed.url, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (compatible; RSS Reader)',
            'Accept': 'application/rss+xml, application/xml, text/xml',
          },
        });

        if (!response.ok) {
          console.error(`❌ Erreur RSS ${feed.name}:`, response.status);
          continue;
        }

        const rssText = await response.text();
        const articles = parseRSS(rssText, feed.name, feed.category);
        console.log(`✅ ${articles.length} articles trouvés dans ${feed.name}`);
        allArticles.push(...articles.slice(0, 10));
      } catch (error) {
        console.error(`❌ Erreur scraping ${feed.name}:`, error);
      }
    }

    if (allArticles.length === 0) {
      console.log('📝 Aucun article trouvé via RSS');
    }

    let insertedCount = 0;
    if (allArticles.length > 0) {
      const { data, error } = await supabaseClient
        .from('articles')
        .upsert(allArticles, { onConflict: 'source_url', ignoreDuplicates: false })
        .select();

      if (error) {
        console.warn('⚠️ Insertion articles bloquée (RLS ou permissions). Retour fallback uniquement:', error.message);
      } else {
        insertedCount = data?.length || 0;
        console.log(`✅ ${insertedCount} articles insérés avec succès`);
      }
    }

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Scraping RSS terminé',
        articlesCount: insertedCount || allArticles.length,
        sources: RSS_FEEDS.map((f) => f.name),
        timestamp: new Date().toISOString(),
        articles: allArticles,
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 },
    );
  } catch (error) {
    console.error('❌ Erreur lors du scraping RSS:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        message: 'Erreur lors du scraping RSS',
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 },
    );
  }
});
