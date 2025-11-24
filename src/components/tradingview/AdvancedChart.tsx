import { useEffect, useRef } from 'react'

interface Props {
  symbol: string
  theme?: 'light' | 'dark'
  interval?: '1' | '5' | '15' | '30' | '60' | '240' | 'D' | 'W' | 'M'
  allowSymbolChange?: boolean
  hideSideToolbar?: boolean
  hideTopToolbar?: boolean
  hideLegend?: boolean
  hideVolume?: boolean
}

export function AdvancedChart({
  symbol,
  theme = 'light',
  interval = 'D',
  allowSymbolChange = true,
  hideSideToolbar = true,
  hideTopToolbar = false,
  hideLegend = false,
  hideVolume = false,
}: Props) {
  const backgroundColor = theme === 'dark' ? '#0b0b0b' : '#ffffff'
  const gridColor = theme === 'dark' ? 'rgba(200, 200, 200, 0.06)' : 'rgba(46, 46, 46, 0.06)'

  const config = {
    allow_symbol_change: allowSymbolChange,
    calendar: false,
    details: false,
    hide_side_toolbar: hideSideToolbar,
    hide_top_toolbar: hideTopToolbar,
    hide_legend: hideLegend,
    hide_volume: hideVolume,
    hotlist: false,
    interval,
    locale: 'fr',
    save_image: true,
    style: '1',
    symbol,
    theme,
    timezone: 'Etc/UTC',
    backgroundColor,
    gridColor,
    watchlist: [],
    withdateranges: false,
    compareSymbols: [],
    studies: [],
    autosize: true,
  }

  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return
    containerRef.current.innerHTML =
      '<div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>'
    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js'
    script.type = 'text/javascript'
    script.async = true
    script.innerHTML = JSON.stringify(config)
    containerRef.current.appendChild(script)
    return () => {
      if (containerRef.current) containerRef.current.innerHTML = ''
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbol, theme, interval, allowSymbolChange, hideSideToolbar, hideTopToolbar, hideLegend, hideVolume])

  return (
    <div className="tradingview-widget-container" ref={containerRef} style={{ height: '100%', width: '100%' }} />
  )
}

export default AdvancedChart
