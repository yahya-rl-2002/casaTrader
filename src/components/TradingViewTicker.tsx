import { useEffect, useRef } from 'react'

type SymbolItem = { proName: string; title?: string }

interface Props {
  symbols?: SymbolItem[]
  theme?: 'light' | 'dark'
  transparent?: boolean
  showAttribution?: boolean
}

// Default list provided by you (TradingView "CSEMA" symbols)
const DEFAULT_SYMBOLS: SymbolItem[] = [
  { proName: 'CSEMA:TGC', title: 'Travaux Généraux de Construction de Casablanca' },
  { proName: 'CSEMA:AKT', title: 'Akdital' },
  { proName: 'CSEMA:CMG', title: 'CMGP Group' },
  { proName: 'CSEMA:VCN', title: 'Vicenne' },
  { proName: 'CSEMA:MSA', title: 'Marsa Maroc SA' },
  { proName: 'CSEMA:STR', title: 'STROC Industrie SA' },
  { proName: 'CSEMA:ADI', title: 'Alliances Développement Immobilier' },
  { proName: 'CSEMA:ADH', title: 'Douja Promotion Groupe Addoha' },
  { proName: 'CSEMA:IAM', title: 'Maroc Telecom SA' },
  { proName: 'CSEMA:RDS', title: 'Résidences Dar Saada' },
  { proName: 'CSEMA:SNA', title: 'Stokvis Nord Afrique' },
  { proName: 'CSEMA:ATW', title: 'Attijariwafa Bank' },
  { proName: 'CSEMA:HPS', title: 'Hightech Payment Systems' },
  { proName: 'CSEMA:MUT', title: 'Mutandis' },
  { proName: 'CSEMA:JET', title: 'Jet Contractors' },
  { proName: 'CSEMA:CFG', title: 'CFG Bank' },
  { proName: 'CSEMA:BOA', title: 'Bank of Africa' },
  { proName: 'CSEMA:NKL', title: 'Ennakl' },
  { proName: 'CSEMA:DHO', title: 'Delta Holding' },
  { proName: 'CSEMA:TQM', title: 'TAQA Morocco' },
  { proName: 'CSEMA:FBR', title: 'Fenie Brossette' },
  { proName: 'CSEMA:CSR', title: 'COSUMAR' },
  { proName: 'CSEMA:IMO', title: 'Immorente Invest' },
  { proName: 'CSEMA:ARD', title: 'Aradei Capital' },
  { proName: 'CSEMA:CIH', title: 'CIH Bank' },
  { proName: 'CSEMA:SID', title: 'SONASID' },
  { proName: 'CSEMA:BCP', title: 'Banque Centrale Populaire' },
  { proName: 'CSEMA:COL', title: 'Colorado' },
  { proName: 'CSEMA:ATL', title: 'AtlantaSanad' },
  { proName: 'CSEMA:LHM', title: 'LafargeHolcim Maroc' },
  { proName: 'CSEMA:DYT', title: 'Disty Technologies' },
  { proName: 'CSEMA:MDP', title: 'Med Paper' },
  { proName: 'CSEMA:CDM', title: 'Crédit du Maroc' },
  { proName: 'CSEMA:CMA', title: 'Ciments du Maroc' },
  { proName: 'CSEMA:ATH', title: 'Auto Hall' },
  { proName: 'CSEMA:RIS', title: 'Risma' },
  { proName: 'CSEMA:CTM', title: 'CTM' },
  { proName: 'CSEMA:MNG', title: 'Managem' },
  { proName: 'CSEMA:SNP', title: 'NEOP' },
  { proName: 'CSEMA:CRS', title: 'Cartier Saada' },
  { proName: 'CSEMA:INV', title: 'Involys' },
  { proName: 'CSEMA:SOT', title: 'Sothema' },
  { proName: 'CSEMA:SMI', title: "Société Métallurgique d'Imiter" },
  { proName: 'CSEMA:AFI', title: 'Afric Industries' },
  { proName: 'CSEMA:GAZ', title: 'Afriquia Gaz' },
  { proName: 'CSEMA:S2M', title: 'S2M' },
  { proName: 'CSEMA:TMA', title: 'TotalEnergies Marketing Maroc' },
  { proName: 'CSEMA:DWY', title: 'Disway' },
  { proName: 'CSEMA:SAH', title: 'Sanlam Maroc' },
  { proName: 'CSEMA:M2M', title: 'M2M Group' },
  { proName: 'CSEMA:IBC', title: 'IBMaroc.com' },
  { proName: 'CSEMA:LBV', title: "Label'Vie" },
  { proName: 'CSEMA:SBM', title: 'Société des Boissons du Maroc' },
  { proName: 'CSEMA:MIC', title: 'Microdata' },
  { proName: 'CSEMA:CMT', title: 'Compagnie Minière de Touissit' },
  { proName: 'CSEMA:LES', title: 'Lesieur Cristal' },
  { proName: 'CSEMA:NEJ', title: 'Auto Nejma' },
  { proName: 'CSEMA:BCI', title: "BMCI" },
  { proName: 'CSEMA:AFM', title: 'AFMA' },
  { proName: 'CSEMA:WAA', title: 'Wafa Assurance' },
  { proName: 'CSEMA:MOX', title: 'Maghreb Oxygène' },
  { proName: 'CSEMA:ZDJ', title: 'Zellidja' },
  { proName: 'CSEMA:AGM', title: 'Agma' },
  { proName: 'CSEMA:PRO', title: 'Promopharm' },
  { proName: 'CSEMA:OUL', title: "Eaux Minérales d'Oulmès" },
  { proName: 'CSEMA:BAL', title: 'Balima' },
  { proName: 'CSEMA:MLE', title: 'Maroc Leasing' },
  { proName: 'CSEMA:SLF', title: 'Salafin' },
  { proName: 'CSEMA:DRI', title: 'DARI Couspate' },
  { proName: 'CSEMA:EQD', title: "Société d'Equipement Domestique et Ménager" },
  { proName: 'CSEMA:REB', title: 'Rebab Company' },
  { proName: 'CSEMA:DLM', title: 'Delattre Levivier Maroc' },
  { proName: 'CSEMA:MAB', title: 'Maghrebail' },
  { proName: 'CSEMA:SAM', title: "Maroc Industrie du Raffinage" },
  { proName: 'CSEMA:UMR', title: 'Unimer' },
  { proName: 'CSEMA:DIS', title: 'DIAC Salaf' },
]

export function TradingViewTicker({ symbols = DEFAULT_SYMBOLS, theme = 'light', transparent = true, showAttribution = true }: Props) {
  const container = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!container.current) return

    // Clear previous widget instance if any
    container.current.innerHTML = ''

    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js'
    script.type = 'text/javascript'
    script.async = true
    const config = {
      symbols,
      showSymbolLogo: true,
      colorTheme: theme,
      isTransparent: transparent,
      displayMode: 'adaptive',
      locale: 'fr',
    }
    script.innerHTML = JSON.stringify(config)
    container.current.appendChild(script)

    return () => {
      if (container.current) container.current.innerHTML = ''
    }
  }, [symbols, theme, transparent])

  return (
    <div className="w-full">
      <div className="tradingview-widget-container" ref={container} />
      {showAttribution && (
        <div className="tradingview-widget-copyright text-xs text-muted-foreground px-2 py-1">
          <a href="https://fr.tradingview.com/markets/" rel="noopener nofollow" target="_blank" className="text-primary">
            Track all markets on TradingView
          </a>
        </div>
      )}
    </div>
  )
}

export default TradingViewTicker
