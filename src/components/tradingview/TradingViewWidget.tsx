import { useEffect, useRef } from 'react'

interface Props {
  scriptSrc: string
  config: Record<string, any>
  className?: string
}

export function TradingViewWidget({ scriptSrc, config, className }: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current) return
    ref.current.innerHTML = ''
    const script = document.createElement('script')
    script.src = scriptSrc
    script.type = 'text/javascript'
    script.async = true
    script.innerHTML = JSON.stringify(config)
    ref.current.appendChild(script)
    return () => {
      if (ref.current) ref.current.innerHTML = ''
    }
  }, [scriptSrc, JSON.stringify(config)])

  return <div className={className} ref={ref} />
}

export default TradingViewWidget

