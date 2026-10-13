import { useQuery } from "@tanstack/react-query"
import { useEffect, useMemo, useRef, useState } from "react"

import { type FlowPublic, type ScoreResult, TriageService } from "@/client"
import { FLOW_ID, scoreAnswers, scoreKey } from "../api"
import { Sparkles } from "../components/Art"
import { Card, copyText, Rich, toast, WarnBox } from "../components/Ui"
import { confetti, sfx, vibrate } from "../fx"
import { jknURL, mapsURL } from "../links"
import { type QuizAnswers, toApi } from "../model"
import { drawQR, summaryURL } from "../qr"

export const DISCLAIMER =
  "⚠️ Ini adalah skrining awal, bukan diagnosis dokter. Jika kondisi memburuk, segera ke fasilitas kesehatan atau hubungi 119."

const QR_TODO = /QR rangkuman/

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
    queryKey: scoreKey(api),
    queryFn: () => scoreAnswers(api),
    staleTime: Number.POSITIVE_INFINITY,
  })
  const r = score.data
  const host = useRef<HTMLDivElement>(null)
  const [grow, setGrow] = useState(false)

  useEffect(() => {
    if (!r) return
    sfx.win()
    vibrate([30, 40, 30])
    confetti(host.current?.closest(".tc-app") as HTMLElement | null)
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
              className="btn btn-purple"
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
        <div className="banner" style={{ background: grad }}>
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
              <span className="rtag" style={{ background: grad }}>
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
                  {r.reasons.map((x) => (
                    <li key={x}>{x}</li>
                  ))}
                </ul>
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
                className="rhead"
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
                  className={`btn ${r.route === "green" ? "btn-teal" : "btn-purple"}`}
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
                  target="_blank"
                  rel="noopener"
                >
                  📅 Buat janji dokter (Mobile JKN)
                </a>
                {r.route !== "green" && <QrBox answers={api} />}
                <details className="sum">
                  <summary>📄 Lihat rangkuman lengkap</summary>
                  <pre>{r.summary}</pre>
                </details>
              </div>
            </div>

            {r.warnings.length > 0 && (
              <Card tab="CATATAN PENTING">
                {r.warnings.map((w) => (
                  <WarnBox key={w.text} {...w} />
                ))}
              </Card>
            )}

            <SaveCard answers={api} />

            <div className="btnrow">
              <button
                type="button"
                className="btn btn-teal"
                onClick={copySummary}
              >
                📋 Salin Rangkuman
              </button>
              <button
                type="button"
                className="btn btn-purple big"
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

function QrBox({ answers }: { answers: ReturnType<typeof toApi> }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [ok, setOk] = useState(true)
  useEffect(() => {
    if (canvas.current) setOk(drawQR(canvas.current, summaryURL(answers)))
  }, [answers])
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
      Tunjukkan ke petugas. Petugas yang memindai melihat rangkuman kondisimu
      dan saran penanganan. Jawabanmu ada di dalam QR ini dan tidak disimpan di
      server.
    </div>
  )
}

/** Save the anonymous result only after the patient says yes (AGENTS.md "Privacy"). */
function SaveCard({ answers }: { answers: ReturnType<typeof toApi> }) {
  const [state, setState] = useState<"idle" | "saving" | "saved" | "error">(
    "idle",
  )
  const save = async () => {
    setState("saving")
    try {
      await TriageService.createScreening({
        body: { flow_id: FLOW_ID, answers, consent: true },
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
            Boleh kami simpan jawabanmu <b>tanpa nama</b> untuk menguji dan
            memperbaiki TropiCare? Tidak ada nama, NIK, nomor BPJS, atau foto
            yang disimpan. Boleh dilewati.
          </p>
          {state === "error" && (
            <p className="saveinfo" style={{ color: "#B3122E" }}>
              Gagal menyimpan. Coba lagi nanti.
            </p>
          )}
          <button
            type="button"
            className="btn btn-purple"
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

export function AdviceCards({ r }: { r: ScoreResult }) {
  return (
    <>
      <Card tab="SARAN PENANGANAN">
        <ul className="todo">
          {r.todo
            .filter((x) => !QR_TODO.test(x))
            .map((x) => (
              <li key={x}>
                <Rich text={x} />
              </li>
            ))}
        </ul>
      </Card>
      {r.warnings.length > 0 && (
        <Card tab="CATATAN PENTING">
          {r.warnings.map((w) => (
            <WarnBox key={w.text} {...w} />
          ))}
        </Card>
      )}
    </>
  )
}
