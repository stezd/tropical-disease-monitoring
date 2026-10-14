import { keepPreviousData, useQuery } from "@tanstack/react-query"
import { useEffect, useMemo, useRef, useState } from "react"

import { type FlowPublic, TriageService } from "@/client"
import { scoreAnswers, scoreKey } from "../api"
import { Sparkles } from "../components/Art"
import { PhotoCard } from "../components/PhotoCard"
import { Card, copyText, Rich, toast, WarnBox } from "../components/Ui"
import { confetti, sfx, vibrate } from "../fx"
import { isAndroid, jknURL, mapsURL } from "../links"
import { type QuizAnswers, toApi } from "../model"
import { drawQR, summaryURL } from "../qr"

export const DISCLAIMER =
  "⚠️ Ini adalah skrining awal, bukan diagnosis dokter. Jika kondisi memburuk, segera ke fasilitas kesehatan atau hubungi 119."

// "Kenapa aku menebak ini?": the first reasons (complaint, pattern, companion
// symptoms) stay visible; the rest are one tap away.
const WHY_SHOWN = 3

export function ResultScreen({
  flow,
  answers,
  onHome,
  onRestart,
}: {
  flow: FlowPublic
  answers: QuizAnswers
  onHome: () => void
  onRestart: () => void
}) {
  const api = useMemo(() => toApi(answers), [answers])
  const score = useQuery({
    queryKey: scoreKey(api, flow.id),
    queryFn: () => scoreAnswers(api, flow.id),
    staleTime: Number.POSITIVE_INFINITY,
    // A photo added on this page changes the answers: keep showing the old
    // result while the new one loads instead of the loading screen.
    placeholderData: keepPreviousData,
  })
  const r = score.data
  const host = useRef<HTMLDivElement>(null)
  const [grow, setGrow] = useState(false)

  // Celebrate the first result only, not each re-score.
  const celebrated = useRef(false)
  useEffect(() => {
    if (!r) return
    if (!celebrated.current) {
      celebrated.current = true
      sfx.win()
      vibrate([30, 40, 30])
      confetti(host.current?.closest(".tc-app") as HTMLElement | null)
    }
    const t = setTimeout(() => setGrow(true), 60)
    return () => clearTimeout(t)
  }, [r])

  if (!r) {
    return (
      <div className="screen bg-result">
        <div className="think">
          <p className="footdisc">
            {score.isError ? "Gagal memuat hasil." : "Memuat hasil…"}
          </p>
          {score.isError && (
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => score.refetch()}
            >
              ↻ Coba lagi
            </button>
          )}
        </div>
      </div>
    )
  }

  const route = flow.routes[r.route]
  const grad = `linear-gradient(${route.color_from},${route.color_to})`
  const top = r.unknown ? null : r.top
  const pct = top?.pct ?? 0

  const copySummary = async () => {
    if (await copyText(r.summary)) {
      sfx.ding()
      toast("📋 Rangkuman tersalin!")
    } else toast('Gagal menyalin — buka "Lihat rangkuman lengkap".')
  }

  return (
    <div className="screen bg-result" ref={host}>
      <Sparkles n={18} />
      <div className="hud">
        <button
          type="button"
          className="icon-btn"
          onClick={onHome}
          aria-label="Beranda"
        >
          ⌂
        </button>
        <div className="htitle">Hasil Skrining</div>
      </div>
      <div className="rscroll">
        <div className={`banner rt-${r.route}`} style={{ background: grad }}>
          ✨ SKRINING SELESAI! ✨
        </div>
        <div className="rcols">
          <div className="rcol">
            <Card
              tab="TEBAKAN KAK TROPI"
              className="reveal"
              style={{ marginTop: 34 }}
            >
              {top ? (
                <>
                  <div className="lead">
                    Aku menebak kamu mungkin mengalami…
                  </div>
                  <div className="bigemo" aria-hidden="true">
                    {top.emoji}
                  </div>
                  <h2>{top.name}</h2>
                  <div
                    className="score-ring"
                    style={{ ["--p" as string]: pct }}
                    role="img"
                    aria-label={`Klasifikasi kecocokan ${pct} persen`}
                  >
                    <div>
                      {pct}%<small>klasifikasi kecocokan</small>
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <div className="bigemo" aria-hidden="true">
                    🩺
                  </div>
                  <h2>Belum dapat ditentukan</h2>
                  <p className="lead">
                    Gejalamu belum cocok dengan satu pola. Lebih aman diperiksa
                    langsung, ya!
                  </p>
                </>
              )}
              <span
                className={`rtag rt-${r.route}`}
                style={{ background: grad }}
              >
                {route.emoji} {route.name}
              </span>
            </Card>

            {r.others.length > 0 && (
              <Card tab="KEMUNGKINAN LAIN">
                <div className="bars">
                  {r.others.map((o) => (
                    <div className="bar" key={o.id}>
                      <span className="be" aria-hidden="true">
                        {o.emoji}
                      </span>
                      <span className="bn">
                        {o.name}
                        <div className="bt">
                          <i style={{ width: grow ? `${o.pct}%` : 0 }} />
                        </div>
                      </span>
                      <span className="bp2">{o.pct}%</span>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {top && (
              <Card tab="KENAPA AKU MENEBAK INI?">
                <ul className="why">
                  {r.reasons.slice(0, WHY_SHOWN).map((x) => (
                    <li key={x}>{x}</li>
                  ))}
                </ul>
                {r.reasons.length > WHY_SHOWN && (
                  <details className="sum">
                    <summary>
                      Lihat {r.reasons.length - WHY_SHOWN} alasan lain
                    </summary>
                    <ul className="why">
                      {r.reasons.slice(WHY_SHOWN).map((x) => (
                        <li key={x}>{x}</li>
                      ))}
                    </ul>
                  </details>
                )}
                {r.cross_checks.length > 0 && (
                  <div className="xval">
                    {r.cross_checks.map((x) => (
                      <div key={x}>
                        ⚖️ <Rich text={x} />
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            )}
          </div>

          <div className="rcol">
            <div className="card rcard">
              <div
                className={`rhead rt-${r.route}`}
                style={{
                  background: `linear-gradient(160deg,${route.color_from},${route.color_to})`,
                }}
              >
                <div className="re" aria-hidden="true">
                  {route.emoji}
                </div>
                <h3>{route.name}</h3>
                <p>{route.sub}</p>
              </div>
              <div className="rbody">
                <h4>Yang perlu dilakukan</h4>
                <ul className="todo">
                  {r.todo.map((x) => (
                    <li key={x}>
                      <Rich text={x} />
                    </li>
                  ))}
                </ul>
                <div className="place">
                  <span className="pe" aria-hidden="true">
                    📍
                  </span>
                  <div>
                    {r.place}
                    <small>Dibuka di Google Maps</small>
                  </div>
                </div>
                <a
                  className="btn btn-primary"
                  href={mapsURL(r.maps_query)}
                  target="_blank"
                  rel="noopener"
                >
                  🧭 Navigasi ke {r.nav_label} Terdekat
                </a>
                <a
                  className="btn btn-jkn"
                  style={{ marginTop: 14 }}
                  href={jknURL()}
                  // An intent link hands off to Android; a new tab would stay blank.
                  target={isAndroid() ? undefined : "_blank"}
                  rel="noopener"
                >
                  📅 Buat janji dokter (Mobile JKN)
                </a>
                {isAndroid() && (
                  <p className="jkn-hint">
                    Kalau yang terbuka Play Store, ketuk <b>Buka</b>.
                  </p>
                )}
                {r.route !== "green" && (
                  <QrBox answers={api} flowId={flow.id} />
                )}
                <details className="sum">
                  <summary>📄 Lihat rangkuman lengkap</summary>
                  <pre>{r.summary}</pre>
                </details>
              </div>
            </div>

            <PhotoCard flow={flow} route={r.route} />

            {r.warnings.length > 0 && (
              <Card tab="CATATAN PENTING">
                {r.warnings.map((w) => (
                  <WarnBox key={w.text} {...w} />
                ))}
              </Card>
            )}

            <SaveCard answers={api} flowId={flow.id} />

            <div className="btnrow">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={copySummary}
              >
                📋 Salin Rangkuman
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={onRestart}
              >
                ↻ Ulangi Skrining
              </button>
            </div>
          </div>
        </div>
        <p className="footdisc">{DISCLAIMER}</p>
      </div>
    </div>
  )
}

function QrBox({
  answers,
  flowId,
}: {
  answers: ReturnType<typeof toApi>
  flowId: string
}) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [ok, setOk] = useState(true)
  useEffect(() => {
    if (canvas.current) {
      setOk(drawQR(canvas.current, summaryURL(answers, flowId)))
    }
  }, [answers, flowId])
  if (!ok) return null
  return (
    <div className="qrbox">
      <canvas
        ref={canvas}
        width={232}
        height={232}
        aria-label="QR rangkuman untuk petugas"
      />
      <b>QR Rangkuman</b>
      Tunjukkan ke petugas agar tidak perlu ditanya ulang. Tidak disimpan di
      server.
    </div>
  )
}

/** Save the anonymous result only after the patient says yes (AGENTS.md "Privacy"). */
function SaveCard({
  answers,
  flowId,
}: {
  answers: ReturnType<typeof toApi>
  flowId: string
}) {
  const [state, setState] = useState<"idle" | "saving" | "saved" | "error">(
    "idle",
  )
  const save = async () => {
    setState("saving")
    try {
      await TriageService.createScreening({
        body: { flow_id: flowId, answers, consent: true },
      })
      setState("saved")
      sfx.ding()
    } catch {
      setState("error")
    }
  }
  return (
    <Card tab="BANTU TROPICARE">
      {state === "saved" ? (
        <p className="saveinfo">
          ✔ Jawaban tersimpan tanpa nama. Terima kasih!
        </p>
      ) : (
        <>
          <p className="saveinfo">
            Boleh simpan jawabanmu <b>tanpa nama</b> untuk memperbaiki
            TropiCare? Tanpa nama atau foto. Boleh dilewati.
          </p>
          {state === "error" && (
            <p className="saveinfo" style={{ color: "#B3122E" }}>
              Gagal menyimpan. Coba lagi nanti.
            </p>
          )}
          <button
            type="button"
            className="btn btn-secondary"
            disabled={state === "saving"}
            onClick={save}
          >
            {state === "saving" ? "Menyimpan…" : "Ya, simpan tanpa nama"}
          </button>
        </>
      )}
    </Card>
  )
}
