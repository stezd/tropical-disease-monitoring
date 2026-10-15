// Privacy gate: the first card after choosing a path (both paths). Lanjut stays
// disabled until "Saya setuju" is ticked. Ticking it asks for the browser
// location: the coordinates stay in memory on this device (location.ts) for the
// nearest-facility list, and only the province name goes into the answers.
// If location is refused, the patient may pick a province or skip it.
import { useNavigate } from "@tanstack/react-router"
import { useState } from "react"

import type { FlowPublic } from "@/client"
import { PrivacyText } from "../components/Privacy"
import { Card } from "../components/Ui"
import { sfx } from "../fx"
import { askProvince, PROVINCES } from "../location"
import { quiz, useQuiz } from "../store"
import { BackButton, QuizFrame } from "./Quiz"

type Loc =
  | { s: "idle" }
  | { s: "locating" }
  | { s: "ok" }
  | { s: "off"; reason: string }

const OFF_TEXT: Record<string, string> = {
  denied: "Lokasi tidak diizinkan.",
  unsupported: "Perangkat ini tidak bisa membagikan lokasi.",
  unavailable: "Lokasi belum bisa diambil.",
  outside: "Lokasimu sepertinya di luar Indonesia.",
  none: "Lokasi belum ada.",
}

export function ConsentScreen({ flow }: { flow: FlowPublic }) {
  const navigate = useNavigate()
  const { answers: a, consented } = useQuiz()
  const [agreed, setAgreed] = useState(consented)
  // Back from the first question: show what was found the first time.
  const [loc, setLoc] = useState<Loc>(() => {
    if (!consented) return { s: "idle" }
    return a.province ? { s: "ok" } : { s: "off", reason: "none" }
  })
  // "Ubah provinsi": lets the patient correct a detected province.
  const [editing, setEditing] = useState(false)

  const locate = async () => {
    setLoc({ s: "locating" })
    const r = await askProvince()
    if (r.ok) {
      quiz.answer((prev) => ({ ...prev, province: r.province }))
      setLoc({ s: "ok" })
    } else {
      setLoc({ s: "off", reason: r.reason })
    }
  }

  const tick = (checked: boolean) => {
    sfx.tap()
    setAgreed(checked)
    if (!checked) quiz.set({ consented: false })
    if (checked && loc.s === "idle") void locate()
  }

  const next = () => {
    if (!agreed) return
    sfx.tap()
    quiz.set({ phase: "quiz", step: 0, consented: true })
  }

  const home = () => {
    sfx.tap()
    navigate({ to: "/" })
  }

  return (
    <QuizFrame
      flow={flow}
      stage={0}
      say="Sebelum mulai, ini cara aku **menjaga datamu** 🔒"
      onHome={home}
      foot={
        <>
          <BackButton onClick={home} />
          <button
            type="button"
            className="btn big btn-primary"
            disabled={!agreed}
            onClick={next}
          >
            Lanjut ▶
          </button>
        </>
      }
    >
      <Card tab="PRIVASI" className="pop consent-gate">
        <h2 className="qt">Baca dulu, ya</h2>
        <p className="qh">Centang setuju untuk mulai. Lokasi boleh ditolak.</p>
        {/* Scrollable: focusable so keyboard users can scroll it. */}
        <section
          className="consent-text"
          // biome-ignore lint/a11y/noNoninteractiveTabindex: scrollable region must be keyboard-scrollable
          tabIndex={0}
          aria-label="Kebijakan privasi"
        >
          <PrivacyText />
        </section>
        <label className="chk">
          <input
            type="checkbox"
            checked={agreed}
            onChange={(e) => tick(e.target.checked)}
          />
          <span>
            Saya setuju dengan kebijakan privasi di atas, termasuk izin lokasi
            untuk mencari faskes terdekat.
          </span>
        </label>
        <div aria-live="polite">
          {loc.s === "locating" && (
            <p className="loc-status">📍 Mencari lokasi…</p>
          )}
          {loc.s === "ok" && a.province && (
            <p className="loc-status ok">
              📍 Lokasi: {a.province}{" "}
              <button
                type="button"
                className="linkbtn"
                aria-expanded={editing}
                onClick={() => setEditing((v) => !v)}
              >
                Ubah provinsi
              </button>
            </p>
          )}
          {loc.s === "off" && (
            <p className="loc-status off">
              📍 {OFF_TEXT[loc.reason] ?? OFF_TEXT.unavailable} Pilih provinsi
              supaya perkiraan lebih tepat.
            </p>
          )}
        </div>
        {(loc.s === "off" || editing) && (
          <label className="fld reveal-in mt-field">
            <span>Provinsi (opsional)</span>
            <div className="inp">
              <select
                value={a.province ?? ""}
                onChange={(e) => {
                  const province = e.target.value || null
                  quiz.answer((prev) => ({ ...prev, province }))
                }}
              >
                <option value="">Pilih provinsi (boleh dilewati)</option>
                {PROVINCES.map((p) => (
                  <option key={p} value={p}>
                    {p}
                  </option>
                ))}
              </select>
            </div>
          </label>
        )}
      </Card>
    </QuizFrame>
  )
}
