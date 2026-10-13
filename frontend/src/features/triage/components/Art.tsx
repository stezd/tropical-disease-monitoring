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
          stroke="#6C4CE0"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <path
          d="M75 104Q80 120 74 128"
          stroke="#6C4CE0"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="56" cy="134" r="5.5" fill="#6C4CE0" />
        <circle cx="56" cy="134" r="2.4" fill="#CBB9FF" />
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
        <circle cx="33" cy="71" r="2.2" fill="#8B4DFF" />
        <circle cx="87" cy="71" r="2.2" fill="#8B4DFF" />
        <circle cx="60" cy="61" r="27" fill="#FFC99B" />
        <path
          d="M33 56Q36 35 60 34Q84 35 87 56Q75 44 62 47Q50 41 33 56Z"
          fill="#4B2B3F"
        />
        <path d="M41 37Q60 24 79 37L76 43Q60 35 44 43Z" fill="#fff" />
        <path d="M58 30h4v3h3v4h-3v3h-4v-3h-3v-4h3z" fill="#FF7E9A" />
        <g fill="none" stroke="#7B3FF2" strokeWidth="3">
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

function Palm({ x, y, s, c }: { x: number; y: number; s: number; c: string }) {
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`} fill={c}>
      <path
        d="M0 0Q-8 -45 6 -92"
        stroke={c}
        strokeWidth="7"
        fill="none"
        strokeLinecap="round"
      />
      <path d="M6 -92Q-22 -108 -52 -88Q-24 -96 6 -88Z" />
      <path d="M6 -92Q30 -112 62 -92Q34 -98 6 -88Z" />
      <path d="M6 -92Q-8 -120 -36 -122Q-12 -110 4 -88Z" />
      <path d="M6 -92Q24 -124 50 -120Q26 -110 8 -88Z" />
      <path d="M6 -92Q-26 -82 -40 -56Q-22 -80 4 -86Z" />
      <path d="M6 -92Q40 -84 50 -58Q32 -80 8 -86Z" />
    </g>
  )
}

/** Wavy hills left and right so the scene stays whole on wide screens. */
function SideHill({
  a,
  step,
  yL,
  yR,
  fill,
  op = 1,
}: {
  a: number
  step: number
  yL: number
  yR: number
  fill: string
  op?: number
}) {
  let L = `M-1300 ${yL} q${step / 2} ${-a} ${step} 0`
  let R = `M400 ${yR} q${step / 2} ${-a} ${step} 0`
  for (let i = 1; i < 1300 / step; i++) {
    L += ` t${step} 0`
    R += ` t${step} 0`
  }
  return (
    <>
      <path d={`${L} V820 H-1300Z`} fill={fill} opacity={op} />
      <path d={`${R} V820 H400Z`} fill={fill} opacity={op} />
    </>
  )
}

export function Scene() {
  return (
    <div className="scene">
      <svg
        viewBox="0 0 400 800"
        preserveAspectRatio="xMidYMax meet"
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
            <stop offset="0" stopColor="#5D52D9" />
            <stop offset=".3" stopColor="#9A62D8" />
            <stop offset=".52" stopColor="#F0839A" />
            <stop offset=".68" stopColor="#FFA97A" />
            <stop offset=".8" stopColor="#FFD08A" />
          </linearGradient>
          <radialGradient id="glow">
            <stop offset="0" stopColor="#FFF1B8" stopOpacity=".95" />
            <stop offset=".4" stopColor="#FFD27A" stopOpacity=".5" />
            <stop offset="1" stopColor="#FFB27A" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#FFB88A" />
            <stop offset="1" stopColor="#E77FA2" />
          </linearGradient>
        </defs>
        <rect x="-1300" y="-900" width="3000" height="1800" fill="url(#sky)" />
        <circle cx="200" cy="530" r="190" fill="url(#glow)" />
        <circle cx="200" cy="535" r="62" fill="#FFE9A6" />
        <g
          fill="none"
          stroke="#fff"
          strokeWidth="2.4"
          strokeLinecap="round"
          opacity=".55"
        >
          <path d="M80 300q7-7 14 0q7-7 14 0" />
          <path d="M118 330q5-5 10 0q5-5 10 0" />
          <path d="M290 270q6-6 12 0q6-6 12 0" />
          <path d="M-260 250q8-8 16 0q8-8 16 0" />
          <path d="M560 320q6-6 12 0q6-6 12 0" />
          <path d="M640 260q8-8 16 0q8-8 16 0" />
        </g>
        <g fill="#fff" opacity=".35">
          <ellipse cx="90" cy="420" rx="60" ry="12" />
          <ellipse cx="320" cy="390" rx="70" ry="13" />
          <ellipse cx="290" cy="440" rx="40" ry="8" />
          <ellipse cx="-180" cy="380" rx="90" ry="14" />
          <ellipse cx="-420" cy="450" rx="60" ry="10" />
          <ellipse cx="600" cy="420" rx="90" ry="14" />
          <ellipse cx="820" cy="370" rx="70" ry="12" />
        </g>
        <rect x="-1300" y="560" width="3000" height="70" fill="url(#sea)" />
        <g stroke="#FFE7B0" strokeWidth="3" strokeLinecap="round" opacity=".7">
          <path d="M150 578h40" />
          <path d="M210 592h50" />
          <path d="M170 606h30" />
          <path d="M-120 585h50" />
          <path d="M520 590h60" />
        </g>
        <SideHill a={30} step={130} yL={585} yR={548} fill="#C46FB0" op={0.9} />
        <path
          d="M0 585Q70 548 140 572T280 560T400 548V800H0Z"
          fill="#C46FB0"
          opacity=".9"
        />
        <SideHill a={34} step={260} yL={630} yR={612} fill="#9554BC" />
        <path d="M0 630Q110 590 220 628T400 612V800H0Z" fill="#9554BC" />
        <g transform="translate(262 560)">
          <rect x="0" y="22" width="78" height="44" rx="6" fill="#FFF1E4" />
          <path d="M-8 26L39 -4L86 26Z" fill="#F0778A" />
          <rect x="31" y="40" width="16" height="26" rx="3" fill="#8F5BD6" />
          <rect x="8" y="34" width="15" height="13" rx="3" fill="#FFD36E" />
          <rect x="55" y="34" width="15" height="13" rx="3" fill="#FFD36E" />
          <circle cx="39" cy="12" r="9" fill="#fff" />
          <path d="M37 6h4v4h4v4h-4v4h-4v-4h-4v-4h4z" fill="#26C4B1" />
        </g>
        <SideHill a={36} step={325} yL={690} yR={680} fill="#6E3DA6" />
        <path d="M0 690Q130 650 250 690T400 680V800H0Z" fill="#6E3DA6" />
        <Palm x={52} y={700} s={1.05} c="#4A2683" />
        <Palm x={368} y={690} s={0.85} c="#4A2683" />
        <Palm x={330} y={705} s={0.6} c="#5A3196" />
        <Palm x={-140} y={705} s={0.95} c="#4A2683" />
        <Palm x={-300} y={690} s={0.7} c="#5A3196" />
        <Palm x={-480} y={705} s={1.1} c="#4A2683" />
        <Palm x={560} y={705} s={1} c="#4A2683" />
        <Palm x={700} y={690} s={0.72} c="#5A3196" />
        <Palm x={880} y={705} s={1.1} c="#4A2683" />
        <SideHill a={22} step={260} yL={740} yR={742} fill="#4A2683" />
        <path d="M0 740Q140 712 400 742V800H0Z" fill="#4A2683" />
        <g fill="#3B1E6E">
          <path d="M90 742q8-30 14 0z" />
          <path d="M100 742q12-26 16 0z" />
          <path d="M300 744q6-24 12 0z" />
          <path d="M-220 744q8-28 14 0z" />
          <path d="M620 744q8-28 14 0z" />
        </g>
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
          <stop offset=".22" stopColor="#D6C8FF" />
          <stop offset=".65" stopColor="#8A55FF" />
          <stop offset="1" stopColor="#3A1C9E" />
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
