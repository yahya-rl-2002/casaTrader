import { useEffect, useRef } from 'react'

interface Props {
  theme?: 'light' | 'dark'
  locale?: 'fr' | 'en'
}

// Implémentation fidèle à votre snippet TradingView Heatmap
export function StockHeatmap({ theme = 'light', locale = 'fr' }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return
    containerRef.current.innerHTML = '<div class="tradingview-widget-container__widget" style="width:100%;height:100%"></div>'
    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js'
    script.type = 'text/javascript'
    script.async = true
    const config = {
      dataSource: 'CSEMAMASI',
      blockSize: 'market_cap_basic',
      blockColor: 'change',
      grouping: 'sector',
      locale,
      symbolUrl: '',
      colorTheme: theme,
      exchanges: [],
      hasTopBar: true,
      isDataSetEnabled: true,
      isZoomEnabled: true,
      hasSymbolTooltip: true,
      isMonoSize: true,
      width: '100%',
      height: '100%'
    }
    script.innerHTML = JSON.stringify(config)
    containerRef.current.appendChild(script)
    return () => { if (containerRef.current) containerRef.current.innerHTML = '' }
  }, [theme, locale])

  return (
    <div className="tradingview-widget-container" ref={containerRef} style={{ width: '100%', height: '100%' }}>
      <div className="tradingview-widget-copyright">
        <a href="https://fr.tradingview.com/heatmap/stock/" rel="noopener nofollow" target="_blank">
          <span className="blue-text">Track all markets on TradingView</span>
        </a>
      </div>
    </div>
  )
}

export default StockHeatmap
