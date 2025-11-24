import { useEffect, useRef } from 'react'

interface Props {
  theme?: 'light' | 'dark'
}

// Implémentation conforme à ton snippet Screener TradingView
export function Screener({ theme = 'light' }: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current) return
    ref.current.innerHTML = '<div class="tradingview-widget-container__widget"></div>'
    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-screener.js'
    script.type = 'text/javascript'
    script.async = true
    const config = {
      market: 'morocco',
      showToolbar: true,
      defaultColumn: 'overview',
      defaultScreen: 'most_capitalized',
      isTransparent: false,
      locale: 'fr',
      colorTheme: theme,
      width: '100%',
      height: 550,
    }
    script.innerHTML = JSON.stringify(config)
    ref.current.appendChild(script)
    return () => { if (ref.current) ref.current.innerHTML = '' }
  }, [theme])

  return (
    <div className="tradingview-widget-container" ref={ref}>
      <div className="tradingview-widget-copyright">
        <a href="https://fr.tradingview.com/screener/" rel="noopener nofollow" target="_blank">
          <span className="blue-text">Track all markets on TradingView</span>
        </a>
      </div>
    </div>
  )
}

export default Screener
