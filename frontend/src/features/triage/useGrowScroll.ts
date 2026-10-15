// Scrolls a container down when its content grows after the user did something
// (a 4th field appears, a <details> opens), just enough to show the new part.
// Growth in the first moments after mount is ignored: that is the screen
// rendering, not the user acting. Returns a callback ref for the scroll element.
import { useCallback, useRef } from "react"

const SETTLE_MS = 400

export function useGrowScroll() {
  const cleanup = useRef<(() => void) | null>(null)

  return useCallback((el: HTMLElement | null) => {
    cleanup.current?.()
    cleanup.current = null
    if (!el) return

    const mountedAt = performance.now()
    let height = el.scrollHeight
    let frame = 0
    const check = () => {
      frame = 0
      const grown = el.scrollHeight > height
      height = el.scrollHeight
      if (!grown || performance.now() - mountedAt < SETTLE_MS) return
      if (el.scrollHeight - el.scrollTop - el.clientHeight <= 0) return
      const calm = matchMedia("(prefers-reduced-motion: reduce)").matches
      el.scrollTo({
        top: el.scrollHeight - el.clientHeight,
        behavior: calm ? "auto" : "smooth",
      })
    }
    const mo = new MutationObserver(() => {
      if (!frame) frame = requestAnimationFrame(check)
    })
    mo.observe(el, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["open", "class", "hidden"],
    })
    cleanup.current = () => {
      mo.disconnect()
      cancelAnimationFrame(frame)
    }
  }, [])
}
