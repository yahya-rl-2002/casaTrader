import { useEffect, useRef } from 'react'

interface Props {
  symbol: string
  theme?: 'light' | 'dark'
  locale?: 'fr' | 'en'
}

// TradingView Company / Symbol Profile widget
export function SymbolProfile({ symbol, theme = 'light', locale = 'en' }: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current) return
    ref.current.innerHTML = '<div class="tradingview-widget-container__widget" style="width:100%;height:100%"></div>'
    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js'
    script.type = 'text/javascript'
    script.async = true
    const config = {
      symbol,
      colorTheme: theme,
      isTransparent: false,
      locale,
      width: '100%',
      height: '100%',
    }
    script.innerHTML = JSON.stringify(config)
    ref.current.appendChild(script)
    return () => { if (ref.current) ref.current.innerHTML = '' }
  }, [symbol, theme, locale])

  const linkSymbol = symbol.replace(':', '-')

  return (
    <div className="tradingview-widget-container" ref={ref}>
      <div className="tradingview-widget-copyright">
        <a href={`https://www.tradingview.com/symbols/${linkSymbol}/`} rel="noopener nofollow" target="_blank">
          <span className="blue-text">{linkSymbol.split('-')[1]} key facts</span>
        </a>
        <span className="trademark"> by TradingView</span>
      </div>
    </div>
  )
}

export default SymbolProfile

