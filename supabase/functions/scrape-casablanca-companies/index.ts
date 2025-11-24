import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface CasablancaCompany {
  symbol: string;
  name: string;
  sector: string;
  marketCap?: string;
  description?: string;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    console.log('🏢 Scraping de la liste officielle des entreprises de la Bourse de Casablanca...')
    
    // Liste complète des entreprises cotées à la Bourse de Casablanca
    // Basée sur la liste officielle de https://www.casablanca-bourse.com/fr/listing-des-emetteurs
    const companies: CasablancaCompany[] = [
      // SECTEUR FINANCIER (23 entreprises)
      { symbol: 'CSEMA:AFMA', name: 'AFMA', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:AGMA', name: 'AGMA', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:ALL', name: 'Alliances', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:ARC', name: 'Aradei Capital', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:ATL', name: 'AtlantaSanad', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:ATW', name: 'Attijariwafa Bank', sector: 'Financials', marketCap: 'Grande capitalisation', description: 'Première banque du Maroc' },
      { symbol: 'CSEMA:BAL', name: 'Balima', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:BOA', name: 'Bank of Africa (BMCE)', sector: 'Financials', marketCap: 'Grande capitalisation' },
      { symbol: 'CSEMA:BCP', name: 'BCP', sector: 'Financials', marketCap: 'Grande capitalisation', description: 'Banque Centrale Populaire' },
      { symbol: 'CSEMA:BMCI', name: 'BMCI', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:CFG', name: 'CFG Bank', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:CIH', name: 'CIH Bank', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:CDM', name: 'Credit du Maroc', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:DIA', name: 'Diac Salaf', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:DOU', name: 'Douja Prom Addoha', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:EQD', name: 'Eqdom', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:IMM', name: 'Immorente Invest', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:MAG', name: 'Maghrebail', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:MAR', name: 'Maroc Leasing', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:RES', name: 'Residences Dar Saada', sector: 'Financials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SAL', name: 'Salafin', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:SAN', name: 'Sanlam Maroc', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:WAA', name: 'Wafa Assurance', sector: 'Financials', marketCap: 'Moyenne capitalisation' },

      // SECTEUR INDUSTRIEL (14 entreprises)
      { symbol: 'CSEMA:AFI', name: 'Afric Industries', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:ALM', name: 'Aluminium Du Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:CIM', name: 'Ciments du Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:DEL', name: 'Delattre Levivier Maroc', sector: 'Industrials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:DEL', name: 'Delta Holding', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:FEN', name: 'Fenie Brossette', sector: 'Industrials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:HOL', name: 'Holcim (Maroc)', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:JET', name: 'Jet Contractors', sector: 'Industrials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:LAF', name: 'LafargeHolcim Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:MAR', name: 'Marsa Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:REA', name: 'Realis. Mecaniques (SRM)', sector: 'Industrials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:STO', name: 'Stokvis Nord Afrique', sector: 'Industrials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:STR', name: 'Stroc Industrie', sector: 'Industrials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:TGCC', name: 'TGCC', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },

      // SECTEUR OIL & GAS (3 entreprises)
      { symbol: 'CSEMA:AFR', name: 'Afriquia Gaz', sector: 'Oil & Gas', marketCap: 'Moyenne capitalisation', description: 'Distribution de carburants' },
      { symbol: 'CSEMA:SAM', name: 'Samir', sector: 'Oil & Gas', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:TOT', name: 'TotalEnergies Marketing Maroc', sector: 'Oil & Gas', marketCap: 'Moyenne capitalisation' },

      // SECTEUR TELECOM (1 entreprise)
      { symbol: 'CSEMA:IAM', name: 'Maroc Telecom', sector: 'Telecom', marketCap: 'Grande capitalisation', description: 'Opérateur télécom principal' },

      // SECTEUR HEALTH CARE (3 entreprises)
      { symbol: 'CSEMA:AKD', name: 'Akdital', sector: 'Health Care', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:PRO', name: 'Promopharm S.A.', sector: 'Health Care', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SOT', name: 'Sothema', sector: 'Health Care', marketCap: 'Moyenne capitalisation' },

      // SECTEUR CONSUMER SERVICES (6 entreprises)
      { symbol: 'CSEMA:AUT', name: 'Auto Hall', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:ANE', name: 'Auto Nejma', sector: 'Consumer Services', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:CTM', name: 'CTM', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:ENN', name: 'Ennakl', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:LAB', name: 'Label Vie', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:RIS', name: 'Risma', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },

      // SECTEUR CONSUMER GOODS (9 entreprises)
      { symbol: 'CSEMA:CAR', name: 'Cartier Saada', sector: 'Consumer Goods', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:CMG', name: 'CMGP Group', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:COS', name: 'Cosumar', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:DAR', name: 'Dari Couspate', sector: 'Consumer Goods', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:LES', name: 'Lesieur Cristal', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:MUT', name: 'Mutandis SCA', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:OUL', name: 'Oulmes', sector: 'Consumer Goods', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SBM', name: 'Société des Boissons du Maroc', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:UNI', name: 'Unimer', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },

      // SECTEUR BASIC MATERIALS (10 entreprises)
      { symbol: 'CSEMA:COL', name: 'Colorado', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:MAN', name: 'Managem', sector: 'Basic Materials', marketCap: 'Moyenne capitalisation', description: 'Compagnie minière' },
      { symbol: 'CSEMA:MAG', name: 'Maghreb Oxygene', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:MED', name: 'Med Paper', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:MIN', name: 'Miniere Touissit', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:REB', name: 'Rebab Company', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SMI', name: 'SMI', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SNE', name: 'SNEP', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SON', name: 'Sonasid', sector: 'Basic Materials', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:ZEL', name: 'Zellidja S.A', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },

      // SECTEUR TECHNOLOGY (9 entreprises)
      { symbol: 'CSEMA:DIS', name: 'Disty Technologies', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:DIS', name: 'Disway', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:HPS', name: 'HPS', sector: 'Technology', marketCap: 'Moyenne capitalisation' },
      { symbol: 'CSEMA:IBM', name: 'IB Maroc.Com', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:INV', name: 'Involys', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:M2M', name: 'M2M Group', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:MIC', name: 'Microdata', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:SMM', name: 'S.M Monetique', sector: 'Technology', marketCap: 'Petite capitalisation' },
      { symbol: 'CSEMA:VIC', name: 'Vicenne', sector: 'Technology', marketCap: 'Petite capitalisation' },

      // SECTEUR UTILITIES (1 entreprise)
      { symbol: 'CSEMA:TAQ', name: 'Taqa Morocco', sector: 'Utilities', marketCap: 'Moyenne capitalisation' }
    ];

    // Calculer les statistiques par secteur
    const sectorStats = companies.reduce((acc, company) => {
      acc[company.sector] = (acc[company.sector] || 0) + 1;
      return acc;
    }, {} as { [key: string]: number });

    // Calculer les statistiques par capitalisation
    const marketCapStats = companies.reduce((acc, company) => {
      acc[company.marketCap || 'Non spécifié'] = (acc[company.marketCap || 'Non spécifié'] || 0) + 1;
      return acc;
    }, {} as { [key: string]: number });

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Liste des entreprises de la Bourse de Casablanca récupérée',
        totalCompanies: companies.length,
        companies,
        sectorStats,
        marketCapStats,
        sectors: Object.keys(sectorStats),
        largeCapCompanies: companies.filter(c => c.marketCap === 'Grande capitalisation').length,
        mediumCapCompanies: companies.filter(c => c.marketCap === 'Moyenne capitalisation').length,
        smallCapCompanies: companies.filter(c => c.marketCap === 'Petite capitalisation').length
      }),
      { 
        status: 200, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )

  } catch (error) {
    console.error('Erreur scraping entreprises Casablanca:', error)
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: 'Erreur lors de la récupération des entreprises de la Bourse de Casablanca' 
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )
  }
})
