import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.3';
import { JSDOM } from 'npm:jsdom@22.1.0';
import { Readability } from 'npm:@mozilla/readability@0.5.0';

// CORS headers for Supabase Functions
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

// Shape of an article record in DB
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

// Minimal scraped page coming from Firecrawl API
interface ScrapedPage {
  url: string;
  markdown?: string;
  html?: string;
  metadata?: {
    title?: string;
    description?: string;
    ogImage?: string;
  };
}

// Site configuration for discovery and article selection
type SiteConfig = {
  url: string;        // listing/section URL
  source: string;     // source label
  category: string;   // category label
  domain: string;     // expected domain used to filter links
  articlePatterns: RegExp[]; // url patterns that likely indicate an article page
  excludePatterns?: RegExp[]; // url patterns to ignore
};

const SITES: SiteConfig[] = [
  {
    url: 'https://medias24.com',
    source: 'Medias24',
    category: 'Économie',
    domain: 'medias24.com',
    articlePatterns: [/\/\d{4}\/\d{2}\/\d{2}\//i, /\/article\//i, /\/economie\//i, /\/categorie\/economie\//i],
    excludePatterns: [/\/tag\//i, /\/auteur\//i, /\/category\//i],
  },
  {
    url: 'https://www.lesiteinfo.com/economie',
    source: 'Le Site Info',
    category: 'Économie',
    domain: 'lesiteinfo.com',
    articlePatterns: [/\/\d{4}\/\d{2}\/\d{2}\//i, /\/economie\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i],
  },
  {
    url: 'https://www.leconomiste.com',
    source: "L'Économiste",
    category: 'Économie',
    domain: 'leconomiste.com',
    articlePatterns: [/\/article\//i, /\/\d{4}-\d{2}-\d{2}\//i],
    excludePatterns: [/\/node\//i, /\/edition\//i],
  },
  // Challenge — Bourse & Finance Maroc
  {
    url: 'https://www.challenge.ma/bourse/',
    source: 'Challenge',
    category: 'Économie',
    domain: 'challenge.ma',
    articlePatterns: [/\/bourse\//i, /\/\d{4}\/\d{2}\/\d{2}\//i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/auteur\//i, /\/category\//i, /\/video\//i],
  },
  {
    url: 'https://www.challenge.ma/actualite-finance-maroc/',
    source: 'Challenge',
    category: 'Économie',
    domain: 'challenge.ma',
    articlePatterns: [/\/actualite-finance-maroc\//i, /\/finance\//i, /\/\d{4}\/\d{2}\/\d{2}\//i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/auteur\//i, /\/category\//i, /\/video\//i],
  },
  {
    url: 'https://fr.hespress.com/economie',
    source: 'Hespress',
    category: 'Économie',
    domain: 'hespress.com',
    // Hespress (FR) a des articles sous /economie, souvent en .html
    articlePatterns: [/\/economie\//i, /\.html$/i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/sujet\//i, /\/category\//i],
  },
  // Ajouts
  {
    url: 'https://boursenews.ma',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    // Boursenews utilise /article/, /news/, et des rubriques liées au marché
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/macro\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://boursenews.ma/espace-investisseurs',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://boursenews.ma/news',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/macro\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://boursenews.ma/actualite',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/macro\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://boursenews.ma/analyses',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/macro\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://boursenews.ma/marche',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/macro\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://boursenews.ma/bourse',
    source: 'Boursenews',
    category: 'Économie',
    domain: 'boursenews.ma',
    articlePatterns: [
      /\/article\//i,
      /\/news\//i,
      /\/actualite\//i,
      /\/analyses?\//i,
      /\/macro\//i,
      /\/marche\//i,
      /\/\d{4}\/\d{2}\/\d{2}/i,
    ],
    excludePatterns: [/\/tag/i, /\/category/i, /\/auteur/i, /\/video/i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://www.lopinion.ma/Economie_r3.html',
    source: "L'Opinion",
    category: 'Économie',
    domain: 'lopinion.ma',
    articlePatterns: [
      /\/[^\/]+_a\d+\.html/i,
    ],
    excludePatterns: [/\/tag/i, /\/video/i, /\/contact/i],
  },
  {
    url: 'https://www.lopinion.ma/Politique_r2.html',
    source: "L'Opinion",
    category: 'Politique',
    domain: 'lopinion.ma',
    articlePatterns: [
      /\/[^\/]+_a\d+\.html/i,
    ],
    excludePatterns: [/\/tag/i, /\/video/i, /\/contact/i],
  },
  {
    url: 'https://www.h24info.ma/economie',
    source: 'H24Info',
    category: 'Économie',
    domain: 'h24info.ma',
    articlePatterns: [/\/economie\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/category\//i],
  },
  {
    url: 'https://fr.le360.ma/economie',
    source: 'Le360',
    category: 'Économie',
    domain: 'le360.ma',
    articlePatterns: [/\/economie\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i, /\/video\//i],
  },
  {
    url: 'https://leseco.ma/business',
    source: 'LesEco',
    category: 'Économie',
    domain: 'leseco.ma',
    articlePatterns: [/\/business\//i, /\/\d{4}\/\d{2}\/\d{2}\//i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i],
  },
  // Politique — mêmes médias, sections politique
  {
    url: 'https://fr.hespress.com/politique',
    source: 'Hespress',
    category: 'Politique',
    domain: 'hespress.com',
    articlePatterns: [/\/politique\//i, /\.html$/i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/sujet\//i, /\/category\//i],
  },
  {
    url: 'https://fr.le360.ma/politique/',
    source: 'Le360',
    category: 'Politique',
    domain: 'le360.ma',
    articlePatterns: [/\/politique\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i, /\/video\//i],
  },
  {
    url: 'https://www.h24info.ma/politique',
    source: 'H24Info',
    category: 'Politique',
    domain: 'h24info.ma',
    articlePatterns: [/\/politique\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/category\//i],
  },
  {
    url: 'https://www.lesiteinfo.com/politique',
    source: 'Le Site Info',
    category: 'Politique',
    domain: 'lesiteinfo.com',
    articlePatterns: [/\/politique\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i],
  },
  {
    url: 'https://leseco.ma/politique',
    source: 'LesEco',
    category: 'Politique',
    domain: 'leseco.ma',
    articlePatterns: [/\/politique\//i, /\/\d{4}\/\d{2}\/\d{2}\//i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i],
  },
  // Le Matin — Économie & Politique
  {
    url: 'https://lematin.ma/economie',
    source: 'Le Matin',
    category: 'Économie',
    domain: 'lematin.ma',
    articlePatterns: [/\/economie\//i, /\/article\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/(contact|apropos|privacy)/i],
  },
  {
    url: 'https://lematin.ma/politique',
    source: 'Le Matin',
    category: 'Politique',
    domain: 'lematin.ma',
    articlePatterns: [/\/politique\//i, /\/article\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/(contact|apropos|privacy)/i],
  },
  // TelQuel — Économie & Politique
  {
    url: 'https://telquel.ma/categorie/economie',
    source: 'TelQuel',
    category: 'Économie',
    domain: 'telquel.ma',
    articlePatterns: [
      /\/\d{4}\/\d{2}\/\d{2}\/[^_]+_\d+\/?$/i,
      /\/instant-t\//i,
    ],
    excludePatterns: [/\/tag\//i, /\/auteur\//i, /\/video\//i, /\/contact/i],
  },
  // EcoActu — Économie/Finance
  {
    url: 'https://ecoactu.ma',
    source: 'EcoActu',
    category: 'Économie',
    domain: 'ecoactu.ma',
    articlePatterns: [/\/economie\//i, /\/finance\//i, /\/bourse\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i, /\/video\//i],
  },
  // Aujourd'hui Le Maroc — Économie & Politique
  {
    url: 'https://aujourdhui.ma/economie',
    source: "Aujourd'hui Le Maroc",
    category: 'Économie',
    domain: 'aujourdhui.ma',
    articlePatterns: [/\/economie\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/category\//i],
  },
  {
    url: 'https://aujourdhui.ma/actualite/politique',
    source: "Aujourd'hui Le Maroc",
    category: 'Politique',
    domain: 'aujourdhui.ma',
    articlePatterns: [/\/politique\//i, /\/\d{4}\/\d{2}\/\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/category\//i],
  },
  {
    url: 'https://lematin.ma/economie',
    source: 'Le Matin',
    category: 'Économie',
    domain: 'lematin.ma',
    articlePatterns: [/\/economie\//i, /\/article\//i, /\/\d{4}-\d{2}-\d{2}\//i],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/category\//i],
  },
  {
    url: 'https://www.lavieeco.com/economie/',
    source: 'La Vie Eco',
    category: 'Économie',
    domain: 'lavieeco.com',
    articlePatterns: [/\/economie\//i, /\/\d{4}\/\d{2}\/\d{2}\//i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i],
  },
  {
    url: 'https://aujourdhui.ma/economie',
    source: "Aujourd'hui le Maroc",
    category: 'Économie',
    domain: 'aujourdhui.ma',
    articlePatterns: [/\/economie\//i, /\/\d{4}\/\d{2}\/\d{2}\//i, /\/actualite\//i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i, /\/video\//i],
  },
  {
    url: 'https://ecoactu.ma/category/economie/',
    source: 'EcoActu',
    category: 'Économie',
    domain: 'ecoactu.ma',
    articlePatterns: [/\/economie\//i, /\/\d{4}\/(\d{2})?\/(\d{2})?/i, /\/article\//i],
    excludePatterns: [/\/tag\//i, /\/category\//i],
  },
  {
    url: 'https://www.financesnews.com/',
    source: 'Finances News',
    category: 'Économie',
    domain: 'financesnews.com',
    articlePatterns: [/\/economie/i, /\/bourse/i, /\/finance/i, /\/article/i, /\/\d{4}\//i],
    excludePatterns: [/\/tag/i, /\/video/i, /\/category/i],
  },
  {
    url: 'https://telquel.ma/categorie/maroc/politique',
    source: 'TelQuel',
    category: 'Politique',
    domain: 'telquel.ma',
    articlePatterns: [
      /\/\d{4}\/\d{2}\/\d{2}\/[^_]+_\d+\/?$/i,
      /\/instant-t\//i,
    ],
    excludePatterns: [/\/tag\//i, /\/video\//i, /\/contact/i],
  },
  {
    url: 'https://www.yabiladi.com',
    source: 'Yabiladi',
    category: 'Économie',
    domain: 'yabiladi.com',
    articlePatterns: [/\/economie/i, /\/article/i, /\/\d{4}-\d{2}-\d{2}/i],
    excludePatterns: [/\/tag/i, /\/video/i],
  },
];

// Util: safe string trimming
function clean(v?: string | null): string | null {
  if (!v) return null;
  const t = v.toString().trim();
  return t.length ? t : null;
}

// Remove social share/boilerplate lines from markdown/text content
function stripBoilerplate(text: string): string {
  const patterns: RegExp[] = [
    // Social sharing patterns
    /\bPartager\s+sur\b/i,
    /facebook\.com\/sharer/i,
    /twitter\.com\/intent/i,
    /linkedin\.com\/shareArticle/i,
    /api\.whatsapp\.com\/send/i,
    /telegram\.me\/share|t\.me\/share/i,
    /Copier\s+lien/i,
    /Lien\s+imprimable/i,
    
    // Advertisement patterns
    /Publicité/i,
    /Advertisement/i,
    /Sponsored/i,
    /Promoted/i,
    
    // Navigation patterns
    /Retour\s+à\s+la\s+liste/i,
    /Voir\s+plus\s+d'articles/i,
    /Articles\s+similaires/i,
    /Lire\s+aussi/i,
    
    // Footer patterns
    /©\s+\d{4}/i,
    /Tous\s+droits\s+réservés/i,
    /All\s+rights\s+reserved/i,
    
    // Cookie/legal patterns
    /Acceptez\s+les\s+cookies/i,
    /Cookie\s+policy/i,
    /Mentions\s+légales/i,
    /Terms\s+of\s+service/i,
    
    // Newsletter patterns
    /Newsletter/i,
    /Abonnez-vous/i,
    /Subscribe/i,
    
    // Comment patterns
    /Commentaires/i,
    /Comments/i,
    /Laisser\s+un\s+commentaire/i,
  ];
  
  const lines = text.split(/\n+/);
  const filtered = lines.filter((l) => {
    const trimmed = l.trim();
    // Keep lines that are substantial content
    if (trimmed.length < 20) return false;
    // Remove lines matching boilerplate patterns
    if (patterns.some((re) => re.test(trimmed))) return false;
    // Remove lines that are mostly punctuation or numbers
    if (/^[^\w\s]*$/.test(trimmed)) return false;
    return true;
  });
  
  return filtered.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

// Enhanced content extraction for better article quality
function extractFullArticleContent(html: string, markdown?: string, pageUrl?: string): string | null {
  const cleanedMarkdown = markdown?.trim();
  if (cleanedMarkdown && cleanedMarkdown.length >= 300) {
    const mdParagraphs = cleanedMarkdown
      .split(/\n{2,}/)
      .map((p) => p.trim())
      .filter((p) => p.length >= 60 && !/^#/.test(p) && !p.startsWith('*') && !p.startsWith('-'))
      .slice(0, 40);
    if (mdParagraphs.length >= 3) {
      const mdContent = stripBoilerplate(mdParagraphs.join('\n\n'));
      if (mdContent && mdContent.length >= 400) {
        return mdContent;
      }
    }
  }

  if (html) {
    try {
      const dom = new JSDOM(html, {
        url: pageUrl || 'https://placeholder.local',
      });

      try {
        const reader = new Readability(dom.window.document, {
          keepClasses: false,
          charThreshold: 280,
        });

        const article = reader.parse();
        if (article?.content) {
          const articleDom = new JSDOM(`<body>${article.content}</body>`, {
            url: pageUrl || 'https://placeholder.local',
          });

          try {
            const doc = articleDom.window.document;
            const textSegments: string[] = [];

            const paragraphs = Array.from(doc.querySelectorAll('p'))
              .map((node) => node.textContent?.replace(/\s+/g, ' ').trim() ?? '')
              .filter((text) => text.length >= 60 && !/Publicité|Advertisement|Partager|Share/i.test(text));

            const listSegments = Array.from(doc.querySelectorAll('ul, ol'))
              .map((list) => {
                const items = Array.from(list.querySelectorAll('li'))
                  .map((item) => item.textContent?.replace(/\s+/g, ' ').trim() ?? '')
                  .filter((text) => text.length >= 40);
                if (!items.length) return null;
                return `LISTE:\n- ${items.join('\n- ')}`;
              })
              .filter((segment): segment is string => Boolean(segment));

            textSegments.push(...paragraphs.slice(0, 50));
            textSegments.push(...listSegments.slice(0, 8));

            const readabilityContent = stripBoilerplate(textSegments.join('\n\n'));
            if (readabilityContent && readabilityContent.length >= 450) {
              return readabilityContent;
            }
          } finally {
            articleDom.window.close();
          }
        }

        if (article?.textContent) {
          const textSegments = article.textContent
            .split(/\n+/)
            .map((line) => line.trim())
            .filter((line) => line.length >= 60);
          const fallbackReadability = stripBoilerplate(textSegments.slice(0, 60).join('\n\n'));
          if (fallbackReadability && fallbackReadability.length >= 400) {
            return fallbackReadability;
          }
        }
      } finally {
        dom.window.close();
      }
    } catch (error) {
      console.error('Readability extraction error:', error);
    }
  }

  const allBlocks = Array.from(html.matchAll(/<(p|li)[^>]*>(.*?)<\/\1>/gis))
    .map((match) => match[2]
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim())
    .filter((text) => text.length >= 60 && !/Publicité|Advertisement|Partager|Share/i.test(text));

  if (allBlocks.length > 0) {
    const content = stripBoilerplate(allBlocks.slice(0, 40).join('\n\n'));
    if (content && content.length >= 350) {
      return content;
    }
  }

  return null;
}

// Extract structured content including tables and sections
function extractStructuredContent(html: string): string | null {
  const contentParts: string[] = [];
  
  // Extract tables
  const tables = Array.from(html.matchAll(/<table[^>]*>(.*?)<\/table>/gis));
  tables.forEach(table => {
    const tableContent = table[1]
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (tableContent.length > 50) {
      contentParts.push(`TABLEAU: ${tableContent}`);
    }
  });
  
  // Extract sections with headers
  const sections = Array.from(html.matchAll(/<(h[1-6]|div[^>]*class=["'][^"']*section[^"']*["'])[^>]*>(.*?)<\/(h[1-6]|div)>/gis));
  sections.forEach(section => {
    const sectionContent = section[2]
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (sectionContent.length > 30) {
      contentParts.push(`SECTION: ${sectionContent}`);
    }
  });
  
  // Extract lists
  const lists = Array.from(html.matchAll(/<(ul|ol)[^>]*>(.*?)<\/(ul|ol)>/gis));
  lists.forEach(list => {
    const listContent = list[2]
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (listContent.length > 50) {
      contentParts.push(`LISTE: ${listContent}`);
    }
  });
  
  if (contentParts.length > 0) {
    return contentParts.join('\n\n');
  }
  
  return null;
}

// AI-enhanced content extraction for optimal article quality
async function extractContentWithAI(html: string, pageUrl?: string, markdown?: string): Promise<ContentExtractionResult> {
  const openAiKey = Deno.env.get('OPENAI_API_KEY');
  if (!openAiKey) {
    console.warn('OPENAI_API_KEY not set, using deterministic extraction only.');
    const fallbackContent = extractFullArticleContent(html, markdown, pageUrl);
    return { content: fallbackContent, summary: null, keyData: [] };
  }

  const plainText = Array.from(html.matchAll(/<(p|li|h[1-4])[^>]*>(.*?)<\/\1>/gis))
    .map((match) => match[0]
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<br\s*\/?>(\s|\n)*/gi, '\n')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim())
    .filter(Boolean)
    .join('\n');

  if (!plainText || plainText.length < 300) {
    const fallbackContent = extractFullArticleContent(html, markdown, pageUrl);
    return { content: fallbackContent, summary: null, keyData: [] };
  }

  const truncatedText = plainText.slice(0, 6000);

  try {
    const response = await fetch('https://api.openai.com/v1/responses', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${openAiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        input: `Tu es un assistant de rédaction senior spécialisé dans la presse économique marocaine.
À partir du texte HTML donné, reconstruis l'article complet en français, en respectant les consignes suivantes :
- Inclure uniquement le texte éditorial (pas de menus, commentaires, publicités, popups ou widgets).
- Préserver l'ordre des paragraphes, des citations, des listes et des chiffres clés.
- Conserver les titres de section importants si présents.
- Ajouter une synthèse finale de 2 phrases maximum qui résume l'information principale.
- Extraire jusqu'à 5 données clés chiffrées (montants, pourcentages, dates, etc.), en reprenant exactement les valeurs du texte.

Retourne le résultat UNIQUEMENT au format JSON suivant :
{
  "content": "...",
  "summary": "...",
  "keyData": ["..."]
}

URL de l'article : ${pageUrl ?? 'inconnue'}
Texte :
${truncatedText}`,
        max_output_tokens: 1200,
        temperature: 0.2,
        response_format: {
          type: 'json_schema',
          json_schema: {
            name: 'article_extraction',
            schema: {
              type: 'object',
              required: ['content'],
              properties: {
                content: { type: 'string', minLength: 300 },
                summary: { type: 'string' },
                keyData: {
                  type: 'array',
                  maxItems: 8,
                  items: { type: 'string' }
                }
              }
            }
          }
        }
      })
    });

    if (!response.ok) {
      console.error('OpenAI extraction failed:', response.status, await response.text());
      const fallbackContent = extractFullArticleContent(html, markdown, pageUrl);
      return { content: fallbackContent, summary: null, keyData: [] };
    }

    const payload = await response.json();
    const aiOutput: string | undefined = payload?.output?.[0]?.content?.[0]?.text;

    if (!aiOutput) {
      console.warn('OpenAI content empty, using fallback.');
      const fallbackContent = extractFullArticleContent(html, markdown, pageUrl);
      return { content: fallbackContent, summary: null, keyData: [] };
    }

    let parsed: ArticleExtraction | null = null;
    try {
      parsed = JSON.parse(aiOutput) as ArticleExtraction;
    } catch (parseError) {
      console.error('OpenAI JSON parse error:', parseError);
      const fallbackContent = extractFullArticleContent(html, markdown, pageUrl);
      return { content: fallbackContent, summary: null, keyData: [] };
    }

    const cleanedContent = parsed.content ? stripBoilerplate(parsed.content) : null;
    const finalContent = cleanedContent && cleanedContent.length >= 350
      ? cleanedContent
      : extractFullArticleContent(html, markdown, pageUrl);

    return {
      content: finalContent,
      summary: parsed.summary || null,
      keyData: parsed.keyData?.filter(Boolean) || []
    };
  } catch (error) {
    console.error('OpenAI extraction error:', error);
    const fallbackContent = extractFullArticleContent(html, markdown, pageUrl);
    return { content: fallbackContent, summary: null, keyData: [] };
  }
}

function resolveImageUrl(src?: string | null, baseUrl?: string): string | null {
  if (!src) return null;
  const trimmed = src.trim().replace(/^['"]|['"]$/g, '');
  if (!trimmed || trimmed === '#' || /^data:/i.test(trimmed)) return null;
  try {
    const resolved = baseUrl ? new URL(trimmed, baseUrl).toString() : new URL(trimmed).toString();
    return resolved;
  } catch {
    if (baseUrl) {
      try {
        return new URL(trimmed, baseUrl).toString();
      } catch {
        return null;
      }
    }
    return null;
  }
}

function extractHeroImage(html?: string, metadata?: ScrapedPage['metadata'], pageUrl?: string): string | null {
  const candidates: string[] = [];
  const addCandidate = (value?: string | null) => {
    const resolved = resolveImageUrl(value, pageUrl);
    if (resolved && !candidates.includes(resolved)) {
      candidates.push(resolved);
    }
  };

  if (metadata?.ogImage) addCandidate(metadata.ogImage);

  if (html) {
    try {
      const dom = new JSDOM(html, { url: pageUrl || 'https://placeholder.local' });
      const document = dom.window.document;

      const metaSelectors = [
        'meta[property="og:image"]',
        'meta[property="og:image:secure_url"]',
        'meta[property="og:image:url"]',
        'meta[name="twitter:image"]',
        'meta[name="twitter:image:src"]',
        'meta[name="image"]',
        'meta[itemprop="image"]'
      ];
      metaSelectors.forEach((selector) => {
        const element = document.querySelector(selector);
        if (element) {
          addCandidate(element.getAttribute('content'));
        }
      });

      const imgSelectors = [
        'article img',
        'main img',
        'header img',
        '.post img',
        '.entry img',
        '.content img',
        '.article img',
        '.hero img',
        '.single img'
      ];
      for (const selector of imgSelectors) {
        const images = Array.from(document.querySelectorAll<HTMLImageElement>(selector));
        for (const img of images) {
          const attributes = ['data-src', 'data-lazy-src', 'data-original', 'data-actualsrc', 'src', 'data-href'];
          for (const attr of attributes) {
            const value = img.getAttribute(attr);
            if (value) addCandidate(value);
          }
        }
        if (candidates.length) break;
      }

      const picture = document.querySelector('picture source[srcset]');
      if (picture) {
        const srcset = picture.getAttribute('srcset');
        if (srcset) {
          const firstSrc = srcset.split(',')[0]?.trim().split(' ')[0];
          addCandidate(firstSrc);
        }
      }

      dom.window.close();
    } catch (error) {
      console.error('extractHeroImage error:', error);
    }
  }

  const filtered = candidates.filter((url) => !/logo|placeholder|avatar|default/i.test(url));
  return filtered[0] || candidates[0] || null;
}

// Attempt to find first <img src> in HTML
function parseFirstImage(html?: string, baseUrl?: string): string | null {
  if (!html) return null;
  const match = html.match(/<img[^>]+src=["']([^"'>]+)["'][^>]*>/i);
  if (!match?.[1]) return null;
  return resolveImageUrl(match[1], baseUrl);
}

// Global URL patterns to exclude (videos/media files)
const GLOBAL_EXCLUDE_URL_PATTERNS = [
  /\/video(\/|$)/i,
  /\/videos(\/|$)/i,
  /[?&]video=/i,
  /\.(mp4|mov|avi|mkv)(\?|$)/i,
  /\.(css|js|mjs|json|png|jpe?g|gif|svg|ico|webp)(\?|$)/i,
];

// Call Firecrawl to scrape a single page with AI-enhanced content extraction
// If onlyMainContent=false, we fetch full HTML to preserve links (useful for listings)
async function scrapePage(url: string, onlyMainContent: boolean = true): Promise<ScrapedPage | null> {
  // Utiliser directement le fallback HTML brut (plus fiable sans Firecrawl)
  console.log(`🔍 Scraping ${url} with raw HTML...`);
  
  try {
    const html = await fetchRawHtml(url);
    if (!html) {
      console.log(`❌ No HTML content for ${url}`);
      return null;
    }
    
    console.log(`✅ Raw HTML success for ${url}`);
    
    return {
      url,
      html,
      markdown: '', // Pas de markdown avec HTML brut
      metadata: {}
    };
    
  } catch (error) {
    console.error('Raw HTML scrape error:', error);
    return null;
  }
}

// Extract absolute links from HTML matching domain + patterns
function extractLinks(html: string, baseUrl: string, domain: string, include: RegExp[], exclude: RegExp[] = []): string[] {
  const hrefs = new Set<string>();
  const re = /href\s*=\s*("([^"]+)"|'([^']+)')/gi; // handles " and '
  let m: RegExpExecArray | null;
  while ((m = re.exec(html)) !== null) {
    const raw = (m[2] || m[3]);
    try {
      const abs = new URL(raw, baseUrl).toString();
      const u = new URL(abs);
      if (u.hostname.includes(domain)) {
        const urlStr = u.toString();
        const hasInclude = include.some((r) => r.test(urlStr));
        const hasExclude = exclude.some((r) => r.test(urlStr));
        if (hasInclude && !hasExclude) {
          hrefs.add(urlStr.replace(/(#.*)$/, ''));
        }
      }
    } catch { /* ignore invalid URLs */ }
  }
  return Array.from(hrefs);
}

// Extract <meta> or <time> based publication date
function extractPublishedAt(html?: string, metadata?: Record<string, unknown>): string | null {
  const candidates: (string | null | undefined)[] = [];

  // Attempt from metadata if Firecrawl passed through some fields
  if (metadata) {
    const md = metadata as Record<string, unknown>;
    const tryKeys = ['publishedTime', 'date', 'article:published_time', 'pubDate'];
    for (const k of tryKeys) {
      const v = md[k] as string | undefined;
      if (v) candidates.push(v);
    }
  }

  // HTML-based extraction
  if (html) {
    const patterns = [
      /<meta[^>]+property=["']article:published_time["'][^>]+content=["']([^"']+)["'][^>]*>/i,
      /<meta[^>]+name=["']pubdate["'][^>]+content=["']([^"']+)["'][^>]*>/i,
      /<meta[^>]+name=["']date["'][^>]+content=["']([^"']+)["'][^>]*>/i,
      /<meta[^>]+itemprop=["']datePublished["'][^>]+content=["']([^"']+)["'][^>]*>/i,
      /<time[^>]+datetime=["']([^"']+)["'][^>]*>/i,
      // Patterns spécifiques pour les sites marocains
      /<span[^>]*class=["'][^"']*date[^"']*["'][^>]*>([^<]+)<\/span>/i,
      /<div[^>]*class=["'][^"']*date[^"']*["'][^>]*>([^<]+)<\/div>/i,
      /<p[^>]*class=["'][^"']*date[^"']*["'][^>]*>([^<]+)<\/p>/i,
      // Patterns pour les dates françaises
      /(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})/i,
      /(\d{1,2})\/(\d{1,2})\/(\d{4})/i,
      /(\d{4})-(\d{1,2})-(\d{1,2})/i,
    ];
    for (const p of patterns) {
      const m = html.match(p);
      if (m?.[1]) candidates.push(m[1]);
    }
  }

  for (const c of candidates) {
    if (!c) continue;
    const d = new Date(c);
    if (!isNaN(d.getTime())) {
      // Vérifier que la date n'est pas dans le futur (plus de 1 jour)
      const now = new Date();
      const oneDayFromNow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
      if (d.getTime() <= oneDayFromNow.getTime()) {
        return d.toISOString();
      }
    }
  }
  return null;
}

// Extract canonical URL from HTML
function extractCanonicalUrl(html?: string, fallback?: string): string | undefined {
  if (html) {
    const m = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["'][^>]*>/i);
    if (m?.[1]) return m[1];
    const og = html.match(/<meta[^>]+property=["']og:url["'][^>]+content=["']([^"']+)["'][^>]*>/i);
    if (og?.[1]) return og[1];
  }
  return fallback;
}

function normalizeUrl(u: string): string {
  try {
    const x = new URL(u);
    x.hash = '';
    x.search = '';
    return x.toString();
  } catch {
    return u.split('?')[0];
  }
}

// Extract OG image or similar
function extractOgImage(html?: string, metadata?: ScrapedPage['metadata']): string | null {
  if (metadata?.ogImage) return metadata.ogImage;
  if (html) {
    const m = html.match(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["'][^>]*>/i);
    if (m?.[1]) return m[1];
  }
  return null;
}

// Extract meta keywords if available
function extractMetaKeywords(html?: string): string[] {
  if (!html) return [];
  const m = html.match(/<meta[^>]+name=["']keywords["'][^>]+content=["']([^"']+)["'][^>]*>/i);
  if (!m?.[1]) return [];
  return m[1]
    .split(',')
    .map((k) => k.trim())
    .filter((k) => k.length > 0);
}

// Heuristic tags from textual content
function inferTags(text: string): string[] {
  const t = text.toLowerCase();
  const tags = new Set<string>();
  const add = (s: string) => tags.add(s);
  if (/(\b|_)masi(\b|_)/.test(t)) add('masi');
  if (/(\b|_)banque|bank|bancaire/.test(t)) add('banque');
  if (/bourse|boursier|boursière/.test(t)) add('bourse');
  if (/maroc|marocaine|marocain/.test(t)) add('maroc');
  if (/dividende|dividendes/.test(t)) add('dividendes');
  if (/obligation|obligataire/.test(t)) add('obligations');
  if (/inflation|taux d'?intérêt|taux directeur/.test(t)) add('macro');
  // tickers courants (heuristique simple)
  const tickers = ['ATW', 'BCP', 'BMCE', 'CIH', 'IAM', 'OCP', 'HPS', 'COSUMAR', 'LES', 'CMT', 'TAQA'];
  for (const tk of tickers) {
    if (new RegExp(`\\b${tk.toLowerCase()}\\b`).test(t)) add(tk);
  }
  return Array.from(tags);
}

function isTelquelUrl(url: string): boolean {
  return /telquel\.ma/i.test(url);
}

function convertRinaMarkdownToHtml(raw: string): string | null {
  if (!raw) return null;
  const marker = 'Markdown Content:';
  let md = raw;
  const idx = md.indexOf(marker);
  if (idx !== -1) md = md.slice(idx + marker.length).trim();
  md = md.replace(/\r/g, '');
  md = md.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_m, alt, src) => `<img src="${src}" alt="${alt}" />`);
  md = md.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, text, href) => `<a href="${href}">${text}</a>`);
  const paragraphs = md
    .split(/\n{2,}/)
    .map((p) => p.replace(/\n+/g, ' ').trim())
    .filter((p) => p.length > 0)
    .map((p) => `<p>${p}</p>`);
  if (!paragraphs.length) return null;
  return `<html><body>${paragraphs.join('\n')}</body></html>`;
}

function isCloudflareBlock(text: string): boolean {
  return /__cf_chl|Just a moment|cf-chl/i.test(text);
}

function extractContentFromTextDivs(html?: string): string | null {
  if (!html) return null;
  
  // Try multiple content selectors for better coverage
  const contentSelectors = [
    /<div[^>]+class=["'][^"']*texte[^"']*["'][^>]*>(.*?)<\/div>/gis,
    /<div[^>]+class=["'][^"']*content[^"']*["'][^>]*>(.*?)<\/div>/gis,
    /<div[^>]+class=["'][^"']*article[^"']*["'][^>]*>(.*?)<\/div>/gis,
    /<div[^>]+class=["'][^"']*post[^"']*["'][^>]*>(.*?)<\/div>/gis,
    /<article[^>]*>(.*?)<\/article>/gis,
    /<main[^>]*>(.*?)<\/main>/gis
  ];
  
  let allBlocks: string[] = [];
  
  for (const selector of contentSelectors) {
    const matches = Array.from(html.matchAll(selector));
    if (matches.length > 0) {
      const blocks = matches
        .map((m) => m[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim())
        .filter((t) => t.length > 50 && !t.includes('Publicité') && !t.includes('Advertisement'));
      allBlocks = allBlocks.concat(blocks);
    }
  }
  
  if (!allBlocks.length) return null;
  
  // Take more content blocks for better quality (up to 8 blocks)
  const combined = allBlocks.slice(0, 8).join('\n\n');
  const cleaned = stripBoilerplate(combined);
  return cleaned && cleaned.length >= 150 ? cleaned : null;
}

function extractImageFromContentBlocks(html: string, pageUrl?: string): string | null {
  try {
    const dom = new JSDOM(html, { url: pageUrl || 'https://placeholder.local' });
    const document = dom.window.document;
    const selectors = [
      'article img',
      'main img',
      '.featured img',
      '.post img',
      '.entry img',
      '.article img',
      '.content img',
      '.single img',
      '.news img',
      'figure img'
    ];

    for (const selector of selectors) {
      const img = document.querySelector<HTMLImageElement>(selector);
      if (!img) continue;

      const attributes = ['data-src', 'data-lazy-src', 'data-original', 'data-actualsrc', 'srcset', 'src'];
      for (const attr of attributes) {
        const val = img.getAttribute(attr);
        if (!val) continue;

        if (attr === 'srcset') {
          const first = val.split(',')[0]?.trim().split(' ')[0];
          const resolved = resolveImageUrl(first, pageUrl);
          if (resolved && !/logo|placeholder|avatar|default/i.test(resolved)) {
            dom.window.close();
            return resolved;
          }
        } else {
          const resolved = resolveImageUrl(val, pageUrl);
          if (resolved && !/logo|placeholder|avatar|default/i.test(resolved)) {
            dom.window.close();
            return resolved;
          }
        }
      }
    }

    dom.window.close();
  } catch (error) {
    console.error('extractImageFromContentBlocks error:', error);
  }
  return null;
}

// Build an Article from a scraped article page
async function buildArticleFromPage(page: ScrapedPage, source: string, category: string): Promise<Article | null> {
  if (!page.markdown && !page.html) return null;
  const title = clean(page.metadata?.title) || null;
  if (title && /404|page non trouvée|not found/i.test(title)) return null;
  let description = clean(page.metadata?.description) || null;
  let image_url = extractHeroImage(page.html, page.metadata, page.url);
  if (!image_url) {
    image_url = resolveImageUrl(parseFirstImage(page.html, page.url), page.url) ?? null;
  }
  const extractedDate = extractPublishedAt(page.html, page.metadata);
  const published_at = extractedDate || null;
  const canonical = normalizeUrl(extractCanonicalUrl(page.html, page.url) || page.url);

  let content: string | null = null;
  let summaryFromAI: string | null = null;
  let keyData: string[] = [];

  if (page.html) {
    const aiResult = await extractContentWithAI(page.html, page.url, page.markdown);
    if (aiResult.content && aiResult.content.length >= 300) {
      content = aiResult.content;
    }
    summaryFromAI = aiResult.summary;
    keyData = Array.isArray(aiResult.keyData) ? aiResult.keyData.filter(Boolean) : [];
    if (!description && summaryFromAI) {
      description = clean(summaryFromAI);
    }
  }

  if (!content || content.length < 300) {
    const fallback = extractFullArticleContent(page.html || '', page.markdown, page.url);
    if (fallback && fallback.length >= 300) {
      content = fallback;
    }
  }

  if (content && page.html) {
    const structuredContent = extractStructuredContent(page.html);
    if (structuredContent) {
      content = `${content}\n\n${structuredContent}`;
    }
  } else if (!content && page.html) {
    const structuredContent = extractStructuredContent(page.html);
    if (structuredContent) {
      content = structuredContent;
    }
  }

  if (!image_url && page.html) {
    const imageFromStructured = extractImageFromContentBlocks(page.html, page.url);
    if (imageFromStructured) {
      image_url = imageFromStructured;
    }
  }

  if ((!content || content.length < 200) && page.html) {
    if (/<video|youtube|youtu\.be|vimeo|jwplayer/i.test(page.html)) {
      return null;
    }
    const divContent = extractContentFromTextDivs(page.html);
    if (divContent) content = divContent;
  }

  if (keyData.length && content) {
    const formatted = keyData.map((item) => `- ${item.trim()}`).join('\n');
    if (formatted && !/POINTS CLÉS/i.test(content)) {
      content = `${content}\n\nPOINTS CLÉS :\n${formatted}`;
    }
  }

  const textForTags = `${title ?? ''} ${description ?? ''} ${content ?? ''}`;
  const inferred = inferTags(textForTags);
  const metaKeywords = extractMetaKeywords(page.html);
  const tags = Array.from(new Set([...(metaKeywords || []), ...inferred]));

  if (!title || !content) return null;

  const article: Article = {
    title,
    description,
    content,
    source,
    source_url: canonical,
    image_url: image_url ?? null,
    published_at,
    category,
    tags: tags.length ? tags : null,
  };

  return article;
}

// Fetch raw HTML fallback helpers
async function fetchRawHtml(url: string, retries = 2): Promise<string | null> {
  const headers: Record<string, string> = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3'
  };
  try {
    const res = await fetch(url, { headers });
    if (res.ok) {
      const text = await res.text();
      if (!isTelquelUrl(url) || !isCloudflareBlock(text)) {
        return text;
      }
    } else if (retries > 0 && (res.status === 429 || res.status >= 500)) {
      await delay(600 * (3 - retries));
      return fetchRawHtml(url, retries - 1);
    } else if (!isTelquelUrl(url) || res.status !== 403) {
      console.error('raw fetch error', res.status, url);
      return null;
    }
  } catch (e) {
    if (retries > 0) {
      await delay(600 * (3 - retries));
      return fetchRawHtml(url, retries - 1);
    }
    console.error('raw fetch exception', url, e);
    return null;
  }

  if (isTelquelUrl(url)) {
    try {
      const proxied = await fetch(`https://r.jina.ai/${url}`);
      if (proxied.ok) {
        const proxyText = await proxied.text();
        const html = convertRinaMarkdownToHtml(proxyText);
        if (html) return html;
      }
    } catch (proxErr) {
      console.error('telquel proxy fetch error', url, proxErr);
    }
  }

  if (retries > 0) {
    await delay(600 * (3 - retries));
    return fetchRawHtml(url, retries - 1);
  }
  return null;
}

async function buildArticleFromHtml(url: string, html: string, source: string, category: string): Promise<Article | null> {
  const getMeta = (name: string, prop = 'name') => html.match(new RegExp(`<meta[^>]+${prop}=["']${name}["'][^>]+content=["']([^"']+)["'][^>]*>`, 'i'))?.[1] || null;
  const ogTitle = getMeta('og:title', 'property');
  const titleTag = html.match(/<title[^>]*>([^<]+)<\/title>/i)?.[1] || null;
  const title = clean(ogTitle || titleTag);
  if (title && /404|page non trouvée|not found/i.test(title)) return null;
  let description = clean(getMeta('description'));
  let image_url = extractHeroImage(html, undefined, url);
  if (!image_url) image_url = clean(parseFirstImage(html, url));
  const extractedDate = extractPublishedAt(html, undefined);
  const published_at = extractedDate || null;
  const canonical = normalizeUrl(extractCanonicalUrl(html, url) || url);

  const aiResult = await extractContentWithAI(html, url, undefined);
  let content = aiResult.content;
  let summaryFromAI = aiResult.summary;
  let keyData = aiResult.keyData;

  if (!content || content.length < 300) {
    const fallback = extractFullArticleContent(html, undefined, url);
    if (fallback && fallback.length >= 300) {
      content = fallback;
    }
  }

  const structuredContent = extractStructuredContent(html);
  if (structuredContent) {
    content = content ? `${content}\n\n${structuredContent}` : structuredContent;
  }

  if (!image_url) {
    const imageFromStructured = extractImageFromContentBlocks(html, url);
    if (imageFromStructured) {
      image_url = imageFromStructured;
    }
  }

  if ((!content || content.length < 200) && /<video|youtube|youtu\.be|vimeo|jwplayer/i.test(html)) {
    return null;
  }

  if ((!description || description.length < 40) && summaryFromAI) {
    description = clean(summaryFromAI);
  }

  if (keyData.length && content) {
    const formatted = keyData.map((item) => `- ${item.trim()}`).join('\n');
    if (formatted && !/POINTS CLÉS/i.test(content)) {
      content = `${content}\n\nPOINTS CLÉS :\n${formatted}`;
    }
  }

  if ((!content || content.length < 200)) {
    const divContent = extractContentFromTextDivs(html);
    if (divContent) content = divContent;
  }

  if (!title || !content) return null;

  const metaKeywords = extractMetaKeywords(html);
  const tags = inferTags(`${title} ${description ?? ''} ${content ?? ''}`);
  const combinedTags = Array.from(new Set([...(metaKeywords || []), ...tags]));

  const article: Article = {
    title,
    description,
    content,
    source,
    source_url: canonical,
    image_url: image_url ?? null,
    published_at,
    category,
    tags: combinedTags.length ? combinedTags : null,
  };

  return article;
}

// Discover and scrape articles for a given site
async function scrapeSite(site: SiteConfig, maxArticles: number): Promise<Article[]> {
  console.log(`Discovering links on ${site.url} ...`);
  
  // Utiliser directement le HTML brut (plus fiable)
  const listingHtml = await fetchRawHtml(site.url);
  
  if (!listingHtml) {
    console.log(`❌ No HTML content for ${site.source}`);
    return [];
  }

  let links = extractLinks(listingHtml, site.url, site.domain, site.articlePatterns, site.excludePatterns);
  // Apply global video/media exclusions
  links = links.filter((u) => !GLOBAL_EXCLUDE_URL_PATTERNS.some((re) => re.test(u)));
  console.log(`Found ${links.length} candidate links on ${site.source}`);
  const unique = Array.from(new Set(links)).slice(0, maxArticles);

  const results: Article[] = [];
  for (const url of unique) {
    // Utiliser directement le HTML brut pour chaque article
    const raw = await fetchRawHtml(url);
    if (raw) {
      const art = await buildArticleFromHtml(url, raw, site.source, site.category);
      if (art) {
        results.push(art);
        console.log(`✅ Raw HTML success for ${url}`);
        console.log(`📰 Article added: ${art.title}`);
      }
    } else {
      console.log(`❌ No article extracted from ${url}`);
    }
    
    await delay(700);
  }
  
  console.log(`🎉 Scraped ${results.length} articles from ${site.source}`);
  return results;
}

function delay(ms: number) { return new Promise((r) => setTimeout(r, ms)); }

interface ContentExtractionResult {
  content: string | null;
  summary: string | null;
  keyData: string[];
}

interface ArticleExtraction {
  content: string | null;
  summary: string | null;
  keyData: string[];
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? Deno.env.get('PROJECT_URL');
    const supabaseKey = Deno.env.get('SERVICE_ROLE_KEY') ?? Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
    if (!supabaseUrl || !supabaseKey) throw new Error('Supabase credentials not set');
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Optional payload to control scraping
    let maxPerSite = 6;
    let sitesFilter: string[] | undefined;
    let offset = 0;
    let limitSites: number | undefined;
    let pathContains: string[] | undefined;
    let rescrapeUrls: string[] = [];
    try {
      if (req.method === 'POST') {
        const body = await req.json().catch(() => ({}));
        if (typeof body.maxPerSite === 'number' && body.maxPerSite > 0 && body.maxPerSite <= 50) {
          maxPerSite = body.maxPerSite;
        }
        if (Array.isArray(body.sites)) {
          sitesFilter = body.sites.filter((s: unknown) => typeof s === 'string') as string[];
        }
        if (typeof body.offset === 'number' && body.offset >= 0) {
          offset = body.offset;
        }
        if (typeof body.limitSites === 'number' && body.limitSites > 0) {
          limitSites = body.limitSites;
        }
        if (Array.isArray(body.pathContains)) {
          pathContains = body.pathContains.filter((s: unknown) => typeof s === 'string') as string[];
        }
        if (Array.isArray(body.rescrapeUrls)) {
          rescrapeUrls = body.rescrapeUrls.filter((u: unknown) => typeof u === 'string') as string[];
        }
      }
    } catch (parseErr) {
      console.error('Failed to parse body', parseErr);
      return new Response(JSON.stringify({ success: false, error: 'Invalid JSON body' }), { headers: corsHeaders, status: 400 });
    }

    const sites = sitesFilter ? SITES.filter((s) => sitesFilter.includes(s.source)) : SITES;
    const sliced = limitSites ? sites.slice(offset, offset + limitSites) : sites.slice(offset);

    const allTargets = sliced.filter((s) =>
      (!pathContains || pathContains.some((frag) => s.url.toLowerCase().includes(frag)))
      || (rescrapeUrls.length > 0)
    );
    const start = Math.min(offset, allTargets.length);
    const end = limitSites ? Math.min(start + limitSites, allTargets.length) : allTargets.length;
    const targets = allTargets.slice(start, end);
    console.log('Scraping targets:', targets.map((t) => t.source).join(', '), `offset=${start} limit=${limitSites ?? 'all'}`);

    // Scrape with small concurrency to keep things fluid
    const concurrency = 2;
    const queue = [...targets];
    const collected: Article[] = [];
    const rescrapeCollected: Article[] = [];
    const errors: { source: string; error: string }[] = [];

    async function worker() {
      while (queue.length) {
        const site = queue.shift()!;
        try {
          const articles = await scrapeSite(site, maxPerSite);
          console.log(`Scraped ${articles.length} from ${site.source}`);
          collected.push(...articles);
          if (rescrapeUrls.length) {
            const inSelection = articles.filter((article) => rescrapeUrls.includes(article.source_url));
            if (inSelection.length) {
              rescrapeCollected.push(...inSelection);
            }
          }
        } catch (e) {
          console.error('Site scrape error', site.source, e);
          errors.push({ source: site.source, error: e instanceof Error ? e.message : 'unknown' });
        }
        await delay(500);
      }
    }

    await Promise.all(Array.from({ length: Math.min(concurrency, targets.length) }, () => worker()));

    // Deduplicate by source_url to avoid ON CONFLICT touching same row twice
    const byUrl = new Map<string, Article>();
    for (const a of collected) {
      if (!byUrl.has(a.source_url)) byUrl.set(a.source_url, a);
    }
    if (rescrapeCollected.length) {
      const resMap = new Map<string, Article>();
      for (const a of rescrapeCollected) {
        resMap.set(a.source_url, a);
      }
      rescrapeCollected.length = 0;
      rescrapeCollected.push(...resMap.values());
    }
    const unique = Array.from(byUrl.values());

    let inserted = 0;

    if (rescrapeUrls.length && rescrapeCollected.length) {
      const { error: deleteError } = await supabase
        .from('articles')
        .delete()
        .in('source_url', rescrapeUrls);

      if (deleteError) {
        console.error('Rescrape delete error:', deleteError);
        return new Response(
          JSON.stringify({ success: false, error: deleteError.message }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 },
        );
      }

      const { data, error: insertError } = await supabase
        .from('articles')
        .insert(rescrapeCollected)
        .select();

      if (insertError) {
        console.error('Rescrape insert error:', insertError);
        return new Response(
          JSON.stringify({ success: false, error: insertError.message }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 },
        );
      }
      inserted = data?.length || rescrapeCollected.length;
    } else if (unique.length) {
      const { data, error } = await supabase
        .from('articles')
        .upsert(unique, { onConflict: 'source_url', ignoreDuplicates: false })
        .select();
      if (error) {
        console.error('DB upsert error:', error);
        return new Response(
          JSON.stringify({ success: false, error: error.message, inserted }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 },
        );
      }
      inserted = data?.length || 0;
    }

    const nextOffset = end < allTargets.length ? end : null;
    return new Response(
      JSON.stringify({ success: true, articlesCount: inserted, errors, processed: targets.map(t => t.source), totalTargets: allTargets.length, nextOffset }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 },
    );
  } catch (error) {
    console.error('scrape-news error:', error);
    return new Response(
      JSON.stringify({ success: false, error: error instanceof Error ? error.message : 'Unknown error' }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 },
    );
  }
});
