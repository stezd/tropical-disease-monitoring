// "Kak Tropi sedang menebak…" — Akinator-style pause before the result.
// The score comes from the server; the steps shown are ScoreResult.analysis_steps.
import { useQuery } from "@tanstack/react-query"
import { useEffect, useMemo, useState } from "react"

import type { FlowPublic } from "@/client"
import { scoreAnswers, scoreKey } from "../api"
import { Mascot, Orb, Sparkles } from "../components/Art"
import { Card } from "../components/Ui"
import { reducedMotion, sfx } from "../fx"
import { mapsURL } from "../links"
import { type QuizAnswers, toApi } from "../model"

const SAYINGS = [
  "Hmm… biar aku pikirkan baik-baik… 🤔",
  "Aku mencocokkan pola gejalamu…",
  "Ooh, petunjuknya mulai jelas! 💡",
  "Sebentar lagi… hampir ketemu! ✨",
]
const STEP_MS = 620

export function ThinkingScreen({
  flow,
  answers,
  onDone,
  onBack,
}: {
  flow: FlowPublic
  answers: QuizAnswers
  onDone: () => void
  onBack: () => void
}) {
  const api = useMemo(() => toApi(answers), [answers])
  const score = useQuery({
    queryKey: scoreKey(api, flow.id),
    queryFn: () => scoreAnswers(api, flow.id),
    staleTime: Number.POSITIVE_INFINITY,
    retry: 1,
  })
  const r = score.data
  const steps = r?.analysis_steps ?? []
  const [done, setDone] = useState(0)
  const [emoji, setEmoji] = useState("❓")
  const pool = useMemo(
    () => Object.values(flow.diseases).map((d) => d.emoji),
    [flow],
  )
  const final = r?.meter_candidates ?? 1
  const fast = reducedMotion()

  // Spin disease emojis in the orb until the result is in.
  useEffect(() => {
    if (r && done >= steps.length) return
    const t = setInterval(
      () => setEmoji(pool[Math.floor(Math.random() * pool.length)]),
      140,
    )
    return () => clearInterval(t)
  }, [r, done, steps.length, pool])

  // Tick through the analysis steps, then show the result.
  useEffect(() => {
    if (!r) return
    const ms = fast ? 150 : STEP_MS
    if (done < steps.length) {
      const t = setTimeout(() => {
        sfx.think()
        setDone((d) => d + 1)
      }, ms)
      return () => clearTimeout(t)
    }
    setEmoji(r.top && !r.unknown ? r.top.emoji : "🩺")
    const t = setTimeout(onDone, fast ? 300 : 1200)
    return () => clearTimeout(t)
  }, [r, done, steps.length, fast, onDone])

  const left = steps.length
    ? Math.round(20 - (20 - final) * (done / steps.length))
    : 20
  const saying =
    r && done >= steps.length
      ? null
      : SAYINGS[
          Math.min(
            SAYINGS.length - 1,
            Math.floor((done / Math.max(1, steps.length)) * SAYINGS.length),
          )
        ]

  if (score.isError) {
    return (
      <div className="screen bg-think">
        <div className="hud">
          <button
            type="button"
            className="icon-btn"
            onClick={onBack}
            aria-label="Kembali"
          >
            ‹
          </button>
          <div className="htitle">Koneksi terputus</div>
        </div>
        <div className="think">
          <Card
            tab="BELUM BISA MENEBAK"
            style={{ marginTop: 34, width: "100%" }}
          >
            <p className="saveinfo">
              Kak Tropi tidak bisa menghubungi server. Jawabanmu masih aman di
              perangkat ini. Coba lagi sebentar lagi.
            </p>
            <p className="saveinfo">
              Kalau tetap gagal dan kamu merasa sakit, datang ke Puskesmas
              terdekat untuk diperiksa langsung.
            </p>
            <div className="mbtns">
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => score.refetch()}
              >
                ↻ Coba lagi
              </button>
              <a
                className="btn btn-secondary"
                href={mapsURL("puskesmas terdekat")}
                target="_blank"
                rel="noopener"
              >
                🧭 Puskesmas terdekat
              </a>
            </div>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="screen bg-think">
      <Sparkles n={26} />
      <div className="hud">
        <div className="htitle">🤖 Kak Tropi sedang menebak…</div>
      </div>
      <div className="think">
        <div className="orbbox">
          <Orb />
          <div
            className="orbEmo"
            aria-hidden="true"
            style={{
              transform: done >= steps.length && r ? "scale(1.25)" : undefined,
            }}
          >
            {emoji}
          </div>
          <Mascot className="m-think" />
        </div>
        <div className="bubble" aria-live="polite">
          <p>{saying ?? <b>Aku tahu! 🎉</b>}</p>
        </div>
        <ul className="tsteps">
          {steps.map((s, i) => (
            <li key={s} className={i < done ? "ok" : i === done ? "run" : ""}>
              <span className="dot" />
              <span>{s}</span>
            </li>
          ))}
        </ul>
        <div className="candBig">
          🔮 Kemungkinan tersisa: <b>{left}</b>
        </div>
      </div>
    </div>
  )
}
