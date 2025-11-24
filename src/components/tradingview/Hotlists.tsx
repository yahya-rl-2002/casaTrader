import { useEffect, useRef } from 'react'

interface Props {
  theme?: 'light' | 'dark'
  locale?: 'fr' | 'en'
}

// TradingView Hotlists widget (config selon ton snippet)
export function Hotlists({ theme = 'light', locale = 'fr' }: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current) return
    ref.current.innerHTML = '<div class="tradingview-widget-container__widget"></div>'
    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-hotlists.js'
    script.type = 'text/javascript'
    script.async = true
    const config = {
      exchange: 'CSEMA',
      colorTheme: theme,
      dateRange: '12M',
      showChart: true,
      locale,
      largeChartUrl: '',
      isTransparent: false,
      showSymbolLogo: true,
      showFloatingTooltip: false,
      plotLineColorGrowing: 'rgba(76, 175, 80, 1)',
      plotLineColorFalling: 'rgba(233, 30, 99, 1)',
      gridLineColor: 'rgba(240, 243, 250, 0)',
      scaleFontColor: '#0F0F0F',
      belowLineFillColorGrowing: 'rgba(41, 98, 255, 0.12)',
      belowLineFillColorFalling: 'rgba(41, 98, 255, 0.12)',
      belowLineFillColorGrowingBottom: 'rgba(41, 98, 255, 0)',
      belowLineFillColorFallingBottom: 'rgba(41, 98, 255, 0)',
      symbolActiveColor: 'rgba(41, 98, 255, 0.12)',
      width: '100%',
      height: 550,
    }
    script.innerHTML = JSON.stringify(config)
    ref.current.appendChild(script)
    return () => { if (ref.current) ref.current.innerHTML = '' }
  }, [theme, locale])

  return (
    <div className="tradingview-widget-container" ref={ref}>
      <div className="tradingview-widget-copyright">
        <a href="https://fr.tradingview.com/markets/stocks-usa/" rel="noopener nofollow" target="_blank">
          <span className="blue-text">Track all markets on TradingView</span>
        </a>
      </div>
    </div>
  )
}

export default Hotlists

