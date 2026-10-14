// Body map and 0–10 face pain scale, copied from the prototype's bodySVG() and painScale().
import type { JSX } from "react"

import type { BodyRegion, PainFace } from "@/client"

// Shapes per region id (ids and names come from flow.json body_regions).
const SHAPES: Record<string, JSX.Element> = {
  head: <circle cx="100" cy="36" r="24" />,
  chest: <rect x="64" y="70" width="72" height="50" rx="16" />,
  ruq: <rect x="64" y="122" width="35" height="34" rx="8" />,
  luq: <rect x="101" y="122" width="35" height="34" rx="8" />,
  low: <path d="M64 158H136V184Q136 200 120 200H80Q64 200 64 184Z" />,
  arm_r: <rect x="38" y="74" width="22" height="84" rx="11" />,
  arm_l: <rect x="140" y="74" width="22" height="84" rx="11" />,
  wrist_r: <rect x="39" y="160" width="20" height="16" rx="8" />,
  wrist_l: <rect x="141" y="160" width="20" height="16" rx="8" />,
  thigh_r: <rect x="66" y="204" width="31" height="62" rx="13" />,
  thigh_l: <rect x="103" y="204" width="31" height="62" rx="13" />,
  calf_r: <rect x="68" y="270" width="27" height="50" rx="12" />,
  calf_l: <rect x="105" y="270" width="27" height="50" rx="12" />,
  ankle_r: <rect x="69" y="323" width="25" height="15" rx="7" />,
  ankle_l: <rect x="106" y="323" width="25" height="15" rx="7" />,
}

const SKIN = { fill: "#FFE0C7", stroke: "#F0A97A", strokeWidth: 2 }

export function BodyMap({
  regions,
  selected,
  onToggle,
}: {
  regions: BodyRegion[]
  selected: string[]
  onToggle: (id: string) => void
}) {
  return (
    <svg viewBox="0 0 200 362" aria-label="Peta tubuh">
      <rect x="92" y="58" width="16" height="14" rx="4" {...SKIN} />
      <circle cx="49" cy="188" r="9" {...SKIN} />
      <circle cx="151" cy="188" r="9" {...SKIN} />
      <ellipse cx="80" cy="348" rx="15" ry="7" {...SKIN} />
      <ellipse cx="120" cy="348" rx="15" ry="7" {...SKIN} />
      {regions.map((r) =>
        SHAPES[r.id] ? (
          // biome-ignore lint/a11y/useSemanticElements: SVG shapes cannot be <button>
          <g
            key={r.id}
            className={`bp ${selected.includes(r.id) ? "on" : ""}`}
            role="checkbox"
            aria-checked={selected.includes(r.id)}
            aria-label={r.name}
            tabIndex={0}
            onClick={() => onToggle(r.id)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault()
                onToggle(r.id)
              }
            }}
          >
            <title>{r.name}</title>
            {SHAPES[r.id]}
          </g>
        ) : null,
      )}
      <g pointerEvents="none" fill="#7A4B3A">
        <circle cx="92" cy="34" r="2.5" />
        <circle cx="108" cy="34" r="2.5" />
        <path
          d="M93 44q7 6 14 0"
          stroke="#7A4B3A"
          strokeWidth="2.2"
          fill="none"
          strokeLinecap="round"
        />
      </g>
      <g
        pointerEvents="none"
        fontFamily="Nunito,sans-serif"
        fontWeight="900"
        fontSize="10"
        fill="#fff"
        opacity=".9"
      >
        <text x="18" y="20">
          KANAN
        </text>
        <text x="152" y="20">
          KIRI
        </text>
      </g>
    </svg>
  )
}

const PAIN_COLORS = [
  "#3BB54A",
  "#8DC63F",
  "#F2D21B",
  "#F7B733",
  "#F4A340",
  "#F08A2E",
  "#EC7B2C",
  "#E8622C",
  "#D0392A",
  "#C9302A",
  "#C22424",
]

/** Vertical 0–10 scale (0 on top). No starting value. Saved as 0–10. */
export function PainScale({
  faces,
  value,
  onPick,
}: {
  faces: PainFace[]
  value: number | null
  onPick: (v: number) => void
}) {
  const face = value == null ? null : Math.ceil(value / 2) * 2
  const label = (n: number) => faces.find((f) => f.value === n)?.label
  return (
    <fieldset
      className="fscale"
      aria-label="Skala nyeri 0 sampai 10, dari tidak sakit sampai sakit sekali"
    >
      {PAIN_COLORS.map((c, n) => (
        <button
          key={`n${n}`}
          type="button"
          className={`fnum ${n < 8 ? "dk" : ""} ${value === n ? "on" : ""}`}
          style={{ gridRow: n + 1, ["--fc" as string]: c }}
          aria-pressed={value === n}
          aria-label={`${n} dari 10${label(n) ? `, ${label(n)}` : ""}`}
          onClick={() => onPick(n)}
        >
          {n}
        </button>
      ))}
      {faces.map((f) => (
        <span key={`f${f.value}`} style={{ display: "contents" }}>
          <span className="flab" style={{ gridRow: f.value + 1 }}>
            {f.label}
          </span>
          <button
            type="button"
            className={`fface ${face === f.value ? "on" : ""}`}
            style={{
              gridRow: f.value + 1,
              ["--fc" as string]: PAIN_COLORS[f.value],
            }}
            tabIndex={-1}
            aria-hidden="true"
            onClick={() => onPick(f.value)}
          >
            {f.emoji}
          </button>
        </span>
      ))}
    </fieldset>
  )
}
