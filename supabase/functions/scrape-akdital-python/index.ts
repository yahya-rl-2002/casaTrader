import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface ScrapedReport {
  company_symbol: string;
  company_name: string;
  report_type: string;
  title: string;
  description: string;
  file_url: string;
  file_name: string;
  file_size?: number;
  file_type: string;
  published_at: string;
  period_start?: string;
  period_end?: string;
  tags: string[];
  featured: boolean;
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Create Supabase client with service role key
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
      {
        auth: {
          autoRefreshToken: false,
          persistSession: false
        }
      }
    )

    console.log('Début du scraping Akdital avec logique Python...')
    
    // URLs à scraper (inspirées de votre script)
    const urlsToScrape = [
      'https://akdital.ma/financial-releases/',
      'https://akdital.ma/investors/',
      'https://akdital.ma/rapports-financiers/'
    ];

    const scrapedReports: ScrapedReport[] = [];
    let totalPdfsFound = 0;

    // Fonction pour scraper une URL et trouver les PDFs
    const scrapeUrl = async (url: string) => {
      try {
        console.log(`🔍 Scraping: ${url}`);
        
        const response = await fetch(url, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
          }
        });
        
        if (!response.ok) {
          console.log(`❌ Erreur HTTP ${response.status} pour ${url}`);
          return;
        }
        
        const html = await response.text();
        
        // Parser le HTML pour trouver les liens PDF
        const pdfLinks = html.match(/href="([^"]*\.pdf[^"]*)"/gi) || [];
        const relativePdfLinks = html.match(/href="([^"]*\.pdf[^"]*)"/gi) || [];
        
        console.log(`📄 ${pdfLinks.length} liens PDF trouvés sur ${url}`);
        totalPdfsFound += pdfLinks.length;
        
        // Traiter chaque lien PDF trouvé
        for (const linkMatch of pdfLinks) {
          const pdfUrl = linkMatch.replace(/href="|"/g, '');
          
          // Convertir les liens relatifs en absolus
          let fullPdfUrl = pdfUrl;
          if (!pdfUrl.startsWith('http')) {
            if (pdfUrl.startsWith('/')) {
              fullPdfUrl = 'https://akdital.ma' + pdfUrl;
            } else {
              fullPdfUrl = url + pdfUrl;
            }
          }
          
          // Extraire le nom du fichier
          const fileName = fullPdfUrl.split('/').pop() || 'rapport.pdf';
          
          // Déterminer le type de rapport et la société basé sur le nom du fichier
          const reportInfo = analyzeFileName(fileName, fullPdfUrl);
          
          const report: ScrapedReport = {
            company_symbol: 'CSEMA:AKDITAL',
            company_name: 'Akdital',
            report_type: reportInfo.type,
            title: `${reportInfo.title} - Akdital`,
            description: `Rapport financier officiel d'Akdital - ${reportInfo.company}`,
            file_url: fullPdfUrl,
            file_name: fileName,
            file_size: 0, // Sera mis à jour lors du téléchargement
            file_type: 'application/pdf',
            published_at: new Date().toISOString(),
            period_start: reportInfo.periodStart,
            period_end: reportInfo.periodEnd,
            tags: ['akdital', 'scraped', 'officiel', reportInfo.type, 'rapport-financier'],
            featured: reportInfo.featured
          };
          
          scrapedReports.push(report);
        }
        
      } catch (error) {
        console.error(`❌ Erreur scraping ${url}:`, error);
      }
    };

    // Fonction pour analyser le nom du fichier et déterminer les infos
    const analyzeFileName = (fileName: string, url: string) => {
      const lowerFileName = fileName.toLowerCase();
      
      // Pour Akdital, on utilise toujours "Akdital" comme société
      let symbol = 'CSEMA:AKDITAL';
      let company = 'Akdital';
      
      // Détecter la société basée sur le contenu du rapport
      if (lowerFileName.includes('atw') || lowerFileName.includes('attijari')) {
        symbol = 'CSEMA:AKDITAL';
        company = 'Akdital - Attijariwafa Bank';
      } else if (lowerFileName.includes('iam') || lowerFileName.includes('maroc') || lowerFileName.includes('telecom')) {
        symbol = 'CSEMA:AKDITAL';
        company = 'Akdital - Maroc Telecom';
      } else if (lowerFileName.includes('cih')) {
        symbol = 'CSEMA:AKDITAL';
        company = 'Akdital - CIH Bank';
      } else if (lowerFileName.includes('bcp') || lowerFileName.includes('centrale')) {
        symbol = 'CSEMA:AKDITAL';
        company = 'Akdital - BCP';
      } else if (lowerFileName.includes('cdm')) {
        symbol = 'CSEMA:AKDITAL';
        company = 'Akdital - CDM Capital';
      } else {
        // Par défaut, tous les rapports d'Akdital
        symbol = 'CSEMA:AKDITAL';
        company = 'Akdital';
      }
      
      // Détecter le type de rapport
      let type = 'autre';
      let title = fileName.replace('.pdf', '');
      
      if (lowerFileName.includes('annuel') || lowerFileName.includes('annual')) {
        type = 'rapport-annuel';
        title = `Rapport Annuel ${new Date().getFullYear()}`;
      } else if (lowerFileName.includes('trimestriel') || lowerFileName.includes('quarterly') || lowerFileName.includes('q1') || lowerFileName.includes('q2') || lowerFileName.includes('q3') || lowerFileName.includes('q4')) {
        type = 'resultats';
        title = `Résultats Trimestriels ${new Date().getFullYear()}`;
      } else if (lowerFileName.includes('semestriel') || lowerFileName.includes('semester')) {
        type = 'resultats';
        title = `Résultats Semestriels ${new Date().getFullYear()}`;
      } else if (lowerFileName.includes('communique') || lowerFileName.includes('press')) {
        type = 'communique';
        title = `Communiqué ${new Date().getFullYear()}`;
      }
      
      // Déterminer les périodes
      const currentYear = new Date().getFullYear();
      let periodStart = `${currentYear}-01-01`;
      let periodEnd = `${currentYear}-12-31`;
      
      if (lowerFileName.includes('q1')) {
        periodStart = `${currentYear}-01-01`;
        periodEnd = `${currentYear}-03-31`;
      } else if (lowerFileName.includes('q2')) {
        periodStart = `${currentYear}-04-01`;
        periodEnd = `${currentYear}-06-30`;
      } else if (lowerFileName.includes('q3')) {
        periodStart = `${currentYear}-07-01`;
        periodEnd = `${currentYear}-09-30`;
      } else if (lowerFileName.includes('q4')) {
        periodStart = `${currentYear}-10-01`;
        periodEnd = `${currentYear}-12-31`;
      }
      
      return {
        symbol,
        company,
        type,
        title,
        periodStart,
        periodEnd,
        featured: type === 'rapport-annuel' || lowerFileName.includes('important')
      };
    };

    // Scraper toutes les URLs
    for (const url of urlsToScrape) {
      await scrapeUrl(url);
      // Attendre un peu entre les requêtes
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    console.log(`📊 Total: ${scrapedReports.length} rapports trouvés`);

    // Insérer les rapports dans la base de données
    let totalInserted = 0;
    let totalUpdated = 0;

    for (const report of scrapedReports) {
      try {
        // Vérifier si le rapport existe déjà
        const { data: existing } = await supabaseClient
          .from('financial_reports')
          .select('id')
          .eq('company_symbol', report.company_symbol)
          .eq('file_url', report.file_url)
          .single()

        if (existing) {
          // Mettre à jour le rapport existant
          const { error: updateError } = await supabaseClient
            .from('financial_reports')
            .update({
              title: report.title,
              description: report.description,
              updated_at: new Date().toISOString()
            })
            .eq('id', existing.id)

          if (!updateError) {
            totalUpdated++
            console.log(`✅ Rapport mis à jour: ${report.title}`)
          }
        } else {
          // Insérer un nouveau rapport
          const { error: insertError } = await supabaseClient
            .from('financial_reports')
            .insert(report)

          if (!insertError) {
            totalInserted++
            console.log(`✅ Rapport inséré: ${report.title}`)
          } else {
            console.error(`❌ Erreur insertion: ${insertError.message}`)
          }
        }
      } catch (err) {
        console.error(`❌ Erreur traitement rapport ${report.title}:`, err)
      }
    }

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Scraping Akdital terminé avec succès',
        inserted: totalInserted,
        updated: totalUpdated,
        discovered: scrapedReports.length,
        totalPdfsFound,
        reports: scrapedReports.map(r => ({
          title: r.title,
          company: r.company_name,
          url: r.file_url,
          type: r.report_type
        }))
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )

  } catch (error) {
    console.error('Erreur scraping Akdital:', error)
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: 'Erreur lors du scraping Akdital' 
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )
  }
})
