// Scrolls a container down only when a new element appears or a <details> opens
// and that makes the content taller (a 4th field appears), just enough to show
// the new part. Height changes with no new element never scroll.
// Growth in the first moments after mount is ignored: that is the screen
// rendering, not the user acting. Returns a callback ref for the scroll element.
import { useCallback, useRef } from "react"

const SETTLE_MS = 400

export function useGrowScroll(enabled = true) {
  const cleanup = useRef<(() => void) | null>(null)

  return useCallback(
    (el: HTMLElement | null) => {
      cleanup.current?.()
      cleanup.current = null
      if (!el || !enabled) return

      const mountedAt = performance.now()
      let height = el.scrollHeight
      let frame = 0
      let added = false
      const check = () => {
        frame = 0
        const grown = added && el.scrollHeight > height
        added = false
        height = el.scrollHeight
        if (!grown || performance.now() - mountedAt < SETTLE_MS) return
        if (el.scrollHeight - el.scrollTop - el.clientHeight <= 0) return
        const calm = matchMedia("(prefers-reduced-motion: reduce)").matches
        el.scrollTo({
          top: el.scrollHeight - el.clientHeight,
          behavior: calm ? "auto" : "smooth",
        })
      }
      const mo = new MutationObserver((records) => {
        for (const r of records) {
          if (
            r.type === "attributes" ||
            [...r.addedNodes].some((n) => n.nodeType === 1)
          )
            added = true
        }
        if (!frame) frame = requestAnimationFrame(check)
      })
      mo.observe(el, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["open", "hidden"],
      })
      cleanup.current = () => {
        mo.disconnect()
        cancelAnimationFrame(frame)
      }
    },
    [enabled],
  )
}
