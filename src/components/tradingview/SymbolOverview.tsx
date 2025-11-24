import TradingViewWidget from './TradingViewWidget'

interface Props {
  symbol: string
  theme?: 'light' | 'dark'
}

export function SymbolOverview({ symbol, theme = 'light' }: Props) {
  const config = {
    symbol,
    height: 420,
    autosize: true,
    colorTheme: theme,
    locale: 'fr',
    showChart: true,
    showFloatingTooltip: true,
    withDateRanges: true,
    range: '1M',
    details: true,
  }
  return (
    <div className="tradingview-widget-container">
      <TradingViewWidget
        scriptSrc="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js"
        config={config}
      />
    </div>
  )
}

export default SymbolOverview

