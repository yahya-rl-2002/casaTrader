export interface CasablancaCompany {
  symbol: string;
  name: string;
  sector: string;
  marketCap?: string;
  description?: string;
  logo?: string;
}

export const CASABLANCA_COMPANIES: CasablancaCompany[] = [
  // Liste complète des entreprises cotées à la Bourse de Casablanca
  // Source officielle: https://www.casablanca-bourse.com/fr/listing-des-emetteurs
  
  // SECTEUR FINANCIER (BANQUES)
  { symbol: 'CSEMA:AFMA', name: 'AFMA', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:AGMA', name: 'AGMA', sector: 'Financials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:ADI', name: 'Alliances', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:ARD', name: 'Aradei Capital', sector: 'Financials', marketCap: 'Petite capitalisation' },
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
  { symbol: 'CSEMA:IMO', name: 'Immorente Invest', sector: 'Financials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:MAG', name: 'Maghrebail', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:MAR', name: 'Maroc Leasing', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:RES', name: 'Residences Dar Saada', sector: 'Financials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SAL', name: 'Salafin', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:SAH', name: 'Sanlam Maroc', sector: 'Financials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:WAA', name: 'Wafa Assurance', sector: 'Financials', marketCap: 'Moyenne capitalisation' },

  // SECTEUR INDUSTRIEL
  { symbol: 'CSEMA:AFI', name: 'Afric Industries', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:ALM', name: 'Aluminium Du Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:CIM', name: 'Ciments du Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:DEL', name: 'Delattre Levivier Maroc', sector: 'Industrials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:DEL', name: 'Delta Holding', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:FEN', name: 'Fenie Brossette', sector: 'Industrials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:HOL', name: 'Holcim (Maroc)', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:JET', name: 'Jet Contractors', sector: 'Industrials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:LAF', name: 'LafargeHolcim Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:MSA', name: 'Marsa Maroc', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:SRM', name: 'Realis. Mecaniques (SRM)', sector: 'Industrials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SNA', name: 'Stokvis Nord Afrique', sector: 'Industrials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:STR', name: 'Stroc Industrie', sector: 'Industrials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:TGCC', name: 'TGCC', sector: 'Industrials', marketCap: 'Moyenne capitalisation' },

  // SECTEUR OIL & GAS
  { symbol: 'CSEMA:AFR', name: 'Afriquia Gaz', sector: 'Oil & Gas', marketCap: 'Moyenne capitalisation', description: 'Distribution de carburants' },
  { symbol: 'CSEMA:SAM', name: 'Samir', sector: 'Oil & Gas', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:TMA', name: 'TotalEnergies Marketing Maroc', sector: 'Oil & Gas', marketCap: 'Moyenne capitalisation' },

  // SECTEUR TELECOM
  { symbol: 'CSEMA:IAM', name: 'Maroc Telecom', sector: 'Telecom', marketCap: 'Grande capitalisation', description: 'Opérateur télécom principal' },

  // SECTEUR HEALTH CARE
  { symbol: 'CSEMA:AKT', name: 'Akdital', sector: 'Health Care', marketCap: 'Moyenne capitalisation', logo: '/images/akdital-logo.svg' },
  { symbol: 'CSEMA:PRO', name: 'Promopharm S.A.', sector: 'Health Care', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SOT', name: 'Sothema', sector: 'Health Care', marketCap: 'Moyenne capitalisation' },

  // SECTEUR CONSUMER SERVICES
  { symbol: 'CSEMA:AUT', name: 'Auto Hall', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:ANE', name: 'Auto Nejma', sector: 'Consumer Services', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:CTM', name: 'CTM', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:ENN', name: 'Ennakl', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:LAB', name: 'Label Vie', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:RIS', name: 'Risma', sector: 'Consumer Services', marketCap: 'Moyenne capitalisation' },

  // SECTEUR CONSUMER GOODS
  { symbol: 'CSEMA:CAR', name: 'Cartier Saada', sector: 'Consumer Goods', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:CMG', name: 'CMGP Group', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:COS', name: 'Cosumar', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:DAR', name: 'Dari Couspate', sector: 'Consumer Goods', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:LES', name: 'Lesieur Cristal', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:MUT', name: 'Mutandis SCA', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:OUL', name: 'Oulmes', sector: 'Consumer Goods', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SBM', name: 'Société des Boissons du Maroc', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:UNI', name: 'Unimer', sector: 'Consumer Goods', marketCap: 'Moyenne capitalisation' },

  // SECTEUR BASIC MATERIALS
  { symbol: 'CSEMA:COL', name: 'Colorado', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:MAN', name: 'Managem', sector: 'Basic Materials', marketCap: 'Moyenne capitalisation', description: 'Compagnie minière' },
  { symbol: 'CSEMA:MOX', name: 'Maghreb Oxygene', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:MED', name: 'Med Paper', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:MIN', name: 'Miniere Touissit', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:REB', name: 'Rebab Company', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SMI', name: 'SMI', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SNP', name: 'SNEP', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SID', name: 'Sonasid', sector: 'Basic Materials', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:ZEL', name: 'Zellidja S.A', sector: 'Basic Materials', marketCap: 'Petite capitalisation' },

  // SECTEUR TECHNOLOGY
  { symbol: 'CSEMA:DIS', name: 'Disty Technologies', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:DIS', name: 'Disway', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:HPS', name: 'HPS', sector: 'Technology', marketCap: 'Moyenne capitalisation' },
  { symbol: 'CSEMA:IBM', name: 'IB Maroc.Com', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:INV', name: 'Involys', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:M2M', name: 'M2M Group', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:MIC', name: 'Microdata', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:S2M', name: 'S2M', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:SMM', name: 'S.M Monetique', sector: 'Technology', marketCap: 'Petite capitalisation' },
  { symbol: 'CSEMA:VCN', name: 'Vicenne', sector: 'Technology', marketCap: 'Petite capitalisation' },

  // SECTEUR UTILITIES
  { symbol: 'CSEMA:TQM', name: 'Taqa Morocco', sector: 'Utilities', marketCap: 'Moyenne capitalisation' }
];

// Statistiques par secteur (basées sur la liste officielle)
export const SECTOR_STATS = {
  'Financials': CASABLANCA_COMPANIES.filter(c => c.sector === 'Financials').length,
  'Industrials': CASABLANCA_COMPANIES.filter(c => c.sector === 'Industrials').length,
  'Oil & Gas': CASABLANCA_COMPANIES.filter(c => c.sector === 'Oil & Gas').length,
  'Telecom': CASABLANCA_COMPANIES.filter(c => c.sector === 'Telecom').length,
  'Health Care': CASABLANCA_COMPANIES.filter(c => c.sector === 'Health Care').length,
  'Consumer Services': CASABLANCA_COMPANIES.filter(c => c.sector === 'Consumer Services').length,
  'Consumer Goods': CASABLANCA_COMPANIES.filter(c => c.sector === 'Consumer Goods').length,
  'Basic Materials': CASABLANCA_COMPANIES.filter(c => c.sector === 'Basic Materials').length,
  'Technology': CASABLANCA_COMPANIES.filter(c => c.sector === 'Technology').length,
  'Utilities': CASABLANCA_COMPANIES.filter(c => c.sector === 'Utilities').length
};

// Fonction pour obtenir les entreprises par secteur
export const getCompaniesBySector = (sector: string) => {
  return CASABLANCA_COMPANIES.filter(company => company.sector === sector);
};

// Fonction pour obtenir les grandes capitalisations
export const getLargeCapCompanies = () => {
  return CASABLANCA_COMPANIES.filter(company => company.marketCap === 'Grande capitalisation');
};

// Fonction pour rechercher une entreprise
export const searchCompany = (query: string) => {
  const lowerQuery = query.toLowerCase();
  return CASABLANCA_COMPANIES.filter(company => 
    company.name.toLowerCase().includes(lowerQuery) ||
    company.symbol.toLowerCase().includes(lowerQuery) ||
    company.sector.toLowerCase().includes(lowerQuery)
  );
};
