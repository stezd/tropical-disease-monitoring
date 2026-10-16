// Inline SVG art from docs/TropiCek-Simulasi.html (mascot, home scene, orb, sparkles).
import { forwardRef, useMemo } from "react"

export const Mascot = forwardRef<SVGSVGElement, { className?: string }>(
  function Mascot({ className = "" }, ref) {
    return (
      <svg
        ref={ref}
        className={`mascot ${className}`}
        viewBox="0 0 120 152"
        aria-hidden="true"
      >
        <ellipse cx="60" cy="148" rx="34" ry="4" fill="#000" opacity=".16" />
        <path d="M24 148Q24 104 60 100Q96 104 96 148Z" fill="#35C9B8" />
        <path d="M24 148Q24 104 60 100Q40 110 38 148Z" fill="#2BB3A3" />
        <path d="M48 101L60 119L72 101Z" fill="#E9FFFB" />
        <rect x="53" y="88" width="14" height="15" rx="5" fill="#F6B183" />
        <path
          d="M45 104Q39 128 54 133"
          stroke="#0F6B66"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <path
          d="M75 104Q80 120 74 128"
          stroke="#0F6B66"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="56" cy="134" r="5.5" fill="#0F6B66" />
        <circle cx="56" cy="134" r="2.4" fill="#BFE6E0" />
        <rect
          x="78"
          y="118"
          width="11"
          height="9"
          rx="2"
          fill="#fff"
          opacity=".85"
        />
        <circle cx="60" cy="27" r="11" fill="#4B2B3F" />
        <path
          d="M30 63Q28 30 60 29Q92 30 90 63Q90 78 84 82L36 82Q30 78 30 63Z"
          fill="#4B2B3F"
        />
        <circle cx="33" cy="63" r="5" fill="#F6B183" />
        <circle cx="87" cy="63" r="5" fill="#F6B183" />
        <circle cx="33" cy="71" r="2.2" fill="#F06A6A" />
        <circle cx="87" cy="71" r="2.2" fill="#F06A6A" />
        <circle cx="60" cy="61" r="27" fill="#FFC99B" />
        <path
          d="M33 56Q36 35 60 34Q84 35 87 56Q75 44 62 47Q50 41 33 56Z"
          fill="#4B2B3F"
        />
        <path d="M41 37Q60 24 79 37L76 43Q60 35 44 43Z" fill="#fff" />
        <path d="M58 30h4v3h3v4h-3v3h-4v-3h-3v-4h3z" fill="#F06A6A" />
        <g fill="none" stroke="#0F6B66" strokeWidth="3">
          <circle cx="49" cy="61" r="9" />
          <circle cx="71" cy="61" r="9" />
          <path d="M58 60Q60 58 62 60" />
        </g>
        <g className="eyes" fill="#3A2340">
          <ellipse cx="49" cy="62" rx="2.7" ry="3.3" />
          <ellipse cx="71" cy="62" rx="2.7" ry="3.3" />
        </g>
        <circle cx="41" cy="74" r="4.5" fill="#FF8F9E" opacity=".6" />
        <circle cx="79" cy="74" r="4.5" fill="#FF8F9E" opacity=".6" />
        <path
          d="M52 75Q60 84 68 75Z"
          fill="#A23B54"
          stroke="#3A2340"
          strokeWidth="2.5"
          strokeLinejoin="round"
        />
        <g className="m-arm">
          <path
            d="M92 114Q106 100 104 84"
            stroke="#35C9B8"
            strokeWidth="11"
            strokeLinecap="round"
            fill="none"
          />
          <circle cx="104" cy="79" r="7.5" fill="#FFC99B" />
        </g>
      </svg>
    )
  },
)

/** Make the mascot hop once (after an answer). */
export function hop(el: SVGSVGElement | null) {
  if (!el) return
  el.classList.remove("hop")
  void el.getBoundingClientRect()
  el.classList.add("hop")
  setTimeout(() => el.classList.remove("hop"), 460)
}

export function Sparkles({ n = 16 }: { n?: number }) {
  const dots = useMemo(
    () =>
      Array.from({ length: n }, () => ({
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 70}%`,
        animationDelay: `${(Math.random() * 3).toFixed(2)}s`,
        transform: `scale(${(0.5 + Math.random()).toFixed(2)})`,
      })),
    [n],
  )
  return (
    <div className="spk">
      {dots.map((style, i) => (
        <i key={i} style={style} />
      ))}
    </div>
  )
}

/** Dot grid for the hero (decoration only). */
function Dots({
  x,
  y,
  cols,
  rows,
}: {
  x: number
  y: number
  cols: number
  rows: number
}) {
  const out = []
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++)
      out.push(
        <circle key={`${r}-${c}`} cx={x + c * 14} cy={y + r * 14} r="2" />,
      )
  return (
    <g fill="#fff" opacity=".55">
      {out}
    </g>
  )
}

function Plus({ x, y, s = 1 }: { x: number; y: number; s?: number }) {
  return (
    <path
      transform={`translate(${x} ${y}) scale(${s})`}
      d="M-2.5 -9h5v6.5h6.5v5h-6.5v6.5h-5v-6.5h-6.5v-5h6.5z"
      fill="#fff"
      opacity=".6"
    />
  )
}

/** Calm teal hero: soft blobs, faint "+" marks and dot grids. */
export function Scene() {
  return (
    <div className="scene">
      <svg
        viewBox="0 0 400 800"
        preserveAspectRatio="xMidYMax slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient
            id="sky"
            gradientUnits="userSpaceOnUse"
            x1="0"
            y1="0"
            x2="0"
            y2="800"
          >
            <stop offset="0" stopColor="#E4F4F1" />
            <stop offset=".5" stopColor="#CDE8E3" />
            <stop offset="1" stopColor="#A9D7D0" />
          </linearGradient>
        </defs>
        <rect x="-1300" y="-900" width="3000" height="1800" fill="url(#sky)" />
        <circle cx="350" cy="110" r="150" fill="#A9D7D0" opacity=".45" />
        <circle cx="30" cy="330" r="120" fill="#E4F4F1" opacity=".7" />
        <circle cx="330" cy="470" r="90" fill="#A9D7D0" opacity=".35" />
        <circle cx="70" cy="60" r="60" fill="#fff" opacity=".35" />
        <Dots x={296} y={40} cols={5} rows={4} />
        <Dots x={22} y={420} cols={4} rows={3} />
        <Plus x={60} y={200} s={1.3} />
        <Plus x={340} y={290} />
        <Plus x={120} y={110} s={0.8} />
        <Plus x={370} y={400} s={0.8} />
        <Plus x={40} y={520} s={0.9} />
      </svg>
    </div>
  )
}

export function Orb() {
  return (
    <svg className="orb" viewBox="0 0 190 200" aria-hidden="true">
      <defs>
        <radialGradient id="og" cx=".35" cy=".3" r=".85">
          <stop offset="0" stopColor="#fff" />
          <stop offset=".22" stopColor="#CDE8E3" />
          <stop offset=".65" stopColor="#5FB3AA" />
          <stop offset="1" stopColor="#0B524E" />
        </radialGradient>
        <linearGradient id="ob" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#FFD36E" />
          <stop offset="1" stopColor="#E8901A" />
        </linearGradient>
      </defs>
      <path d="M45 172Q95 150 145 172L156 194H34Z" fill="url(#ob)" />
      <rect x="34" y="188" width="122" height="10" rx="5" fill="#C9700E" />
      <circle cx="95" cy="86" r="76" fill="url(#og)" />
      <g
        className="swirl"
        fill="none"
        stroke="#fff"
        strokeLinecap="round"
        opacity=".55"
      >
        <path d="M45 86Q60 40 110 48" strokeWidth="5" />
        <path d="M146 92Q132 140 84 130" strokeWidth="5" />
        <circle cx="140" cy="50" r="3" fill="#fff" />
        <circle cx="52" cy="128" r="2.5" fill="#fff" />
      </g>
      <ellipse
        cx="66"
        cy="50"
        rx="18"
        ry="10"
        fill="#fff"
        opacity=".55"
        transform="rotate(-30 66 50)"
      />
    </svg>
  )
}
