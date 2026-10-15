// Building blocks in the prototype's look (DESIGN.md "Components").
import {
  type CSSProperties,
  type ReactNode,
  useEffect,
  useRef,
  useState,
  useSyncExternalStore,
} from "react"

/** Render "**bold**" from content JSON without raw HTML. */
export function Rich({ text }: { text: string }) {
  const parts = text.split("**")
  return <>{parts.map((p, i) => (i % 2 ? <b key={i}>{p}</b> : p))}</>
}

export function Card({
  tab,
  tabStyle,
  className = "",
  style,
  children,
}: {
  tab?: string
  tabStyle?: CSSProperties
  className?: string
  style?: CSSProperties
  children: ReactNode
}) {
  return (
    <div className={`card ${className}`} style={style}>
      {tab && (
        <div className="tab" style={tabStyle}>
          {tab}
        </div>
      )}
      {children}
    </div>
  )
}

export const RED_TAB: CSSProperties = {
  background: "#FFD6DA",
  color: "#C8102E",
}

type Choice = {
  id: string
  emoji: string
  text: string
  detail?: string | null
  cls?: string
}

export function Options({
  options,
  selected,
  multi = false,
  layout = "",
  onPick,
}: {
  options: Choice[]
  selected: string[]
  multi?: boolean
  layout?: "" | "tiles" | "tiles tiles3"
  onPick: (id: string) => void
}) {
  // Details stay one tap away so the list is quick to scan. They show for picked
  // options (to confirm the choice) and for everyone after "Lihat ciri-ciri".
  // Screen readers always get them.
  const [showAll, setShowAll] = useState(false)
  const hasDetail = options.some((o) => o.detail)
  return (
    <>
      {hasDetail && (
        <button
          type="button"
          className="dtoggle"
          aria-expanded={showAll}
          onClick={() => setShowAll((v) => !v)}
        >
          {showAll ? "Sembunyikan ciri-ciri ▲" : "ⓘ Lihat ciri-ciri ▼"}
        </button>
      )}
      <div className={`opts ${layout}`}>
        {options.map((o) => {
          const on = selected.includes(o.id)
          return (
            <button
              key={o.id}
              type="button"
              className={`opt ${o.cls ?? ""} ${on ? "on" : ""} ${multi ? "multi" : ""}`}
              aria-pressed={on}
              onClick={() => onPick(o.id)}
            >
              <span className="oe" aria-hidden="true">
                {o.emoji}
              </span>
              <span className="ot">
                {o.text}
                {o.detail && (
                  <span className={showAll || on ? "od" : "sr-only"}>
                    {o.detail}
                  </span>
                )}
              </span>
              <span className="ck" />
            </button>
          )
        })}
      </div>
    </>
  )
}

export function StageMap({
  stages,
  current,
}: {
  stages: { emoji: string; name: string }[]
  current: number
}) {
  return (
    <div
      className="stages"
      role="img"
      aria-label={`Tahap ${current + 1} dari ${stages.length}: ${stages[current]?.name ?? ""}`}
    >
      {stages.map((s, i) => (
        <span key={s.name} style={{ display: "contents" }}>
          {i > 0 && <span className={`sl ${i <= current ? "done" : ""}`} />}
          <span
            className={`st ${i < current ? "done" : i === current ? "cur" : ""}`}
            title={s.name}
          >
            {i < current ? "★" : s.emoji}
          </span>
        </span>
      ))}
    </div>
  )
}

export function WarnBox({
  level,
  icon,
  text,
}: {
  level: "y" | "r" | "b"
  icon: string
  text: string
}) {
  return (
    <div className={`warn ${level}`}>
      <span className="wi" aria-hidden="true">
        {icon}
      </span>
      <span>
        <Rich text={text} />
      </span>
    </div>
  )
}

export function Modal({
  tone = "",
  tab,
  onClose,
  children,
  actions,
}: {
  tone?: "" | "yellow" | "red"
  tab?: string
  onClose?: () => void
  children: ReactNode
  actions?: ReactNode
}) {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null
    ref.current?.focus()
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose?.()
    }
    window.addEventListener("keydown", onKey)
    return () => {
      window.removeEventListener("keydown", onKey)
      prev?.focus?.()
    }
  }, [onClose])
  return (
    // biome-ignore lint/a11y/noStaticElementInteractions: backdrop click closes; Escape is handled above
    <div
      className="ov"
      onClick={(e) => e.target === e.currentTarget && onClose?.()}
      role="presentation"
    >
      <div
        ref={ref}
        className={`card ${tone}`}
        role="dialog"
        aria-modal="true"
        aria-label={tab}
        tabIndex={-1}
      >
        {tab && <div className="tab">{tab}</div>}
        {onClose && (
          <button
            type="button"
            className="xbtn"
            onClick={onClose}
            aria-label="Tutup"
          >
            ✕
          </button>
        )}
        <div className="mbody">{children}</div>
        {actions && <div className="mbtns">{actions}</div>}
      </div>
    </div>
  )
}

// Toast: dark pill at the bottom (prototype #toast).
let toastMsg = ""
let toastShow = false
let toastTimer: ReturnType<typeof setTimeout> | undefined
const toastListeners = new Set<() => void>()
const emit = () => {
  for (const l of toastListeners) l()
}

export function toast(msg: string) {
  toastMsg = msg
  toastShow = true
  emit()
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastShow = false
    emit()
  }, 2400)
}

export function ToastHost() {
  const snap = useSyncExternalStore(
    (l) => {
      toastListeners.add(l)
      return () => toastListeners.delete(l)
    },
    () => (toastShow ? `1${toastMsg}` : `0${toastMsg}`),
  )
  return (
    <div className={`tc-toast ${snap[0] === "1" ? "show" : ""}`} role="status">
      {snap.slice(1)}
    </div>
  )
}

export async function copyText(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    }
  } catch {
    // fall through
  }
  const ta = document.createElement("textarea")
  ta.value = text
  ta.style.position = "fixed"
  ta.style.opacity = "0"
  document.body.appendChild(ta)
  ta.select()
  try {
    return document.execCommand("copy")
  } catch {
    return false
  } finally {
    ta.remove()
  }
}
