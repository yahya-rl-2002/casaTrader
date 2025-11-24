import TradingViewWidget from './TradingViewWidget'

interface Props {
  theme?: 'light' | 'dark'
}

// Watchlist/Quotes: utilise le widget "Market Quotes"
export function MarketQuotes({ theme = 'light' }: Props) {
  const groups = [
    {
      name: 'Banques',
      symbols: [
        { name: 'CSEMA:ATW' },
        { name: 'CSEMA:BCP' },
        { name: 'CSEMA:CIH' },
        { name: 'CSEMA:CFG' },
        { name: 'CSEMA:BOA' },
      ],
    },
    {
      name: 'Télécom & Tech',
      symbols: [
        { name: 'CSEMA:IAM' },
        { name: 'CSEMA:HPS' },
        { name: 'CSEMA:M2M' },
        { name: 'CSEMA:MIC' },
      ],
    },
    {
      name: 'Énergie & Matériaux',
      symbols: [
        { name: 'CSEMA:TQM' },
        { name: 'CSEMA:GAZ' },
        { name: 'CSEMA:CMA' },
        { name: 'CSEMA:LHM' },
      ],
    },
  ]

  const config = {
    width: '100%',
    height: 420,
    colorTheme: theme,
    locale: 'fr',
    showSymbolLogo: true,
    isTransparent: true,
    symbolsGroups: groups,
  }

  return (
    <div className="tradingview-widget-container">
      <TradingViewWidget
        scriptSrc="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js"
        config={config}
      />
    </div>
  )
}

export default MarketQuotes

