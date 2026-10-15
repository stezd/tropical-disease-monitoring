import { useQuery } from "@tanstack/react-query"
import { Link, useRouterState } from "@tanstack/react-router"
import { useEffect, useMemo, useRef, useState } from "react"

import { type FlowPublic, TriageService } from "@/client"
import { isLoggedIn } from "@/hooks/useAuth"
import { scoreAnswers, scoreKey } from "../api"
import { Sparkles } from "../components/Art"
import { NearestFacilities } from "../components/Nearby"
import { QrCard } from "../components/QrCard"
import { Card, copyText, Rich, toast, WarnBox } from "../components/Ui"
import { confetti, sfx, vibrate } from "../fx"
import { isAndroid, jknURL, mapsURL } from "../links"
import { type QuizAnswers, toApi } from "../model"
import { resultShareText } from "../share"
import "@/styles/result.css"

const DISCLAIMER =
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
  const top = r.unknown ? null : r.top
  const pct = top?.pct ?? 0

  const copySummary = async () => {
    if (await copyText(r.summary)) {
      sfx.ding()
      toast("📋 Rangkuman tersalin!")
    } else toast('Gagal menyalin — buka "Lihat rangkuman lengkap".')
  }

  // Phones read top to bottom: hero (route + estimate), what to do, nearest
  // facilities, notes, QR, other possibilities, why, save, summary, restart. From 640px the
  // hero spans the width; below it "what to do" sits left and "QR + why"
  // right. The last group (save, summary, restart) goes under whichever column
  // is likely shorter. Rough heights in ~150px units; only a layout hint.
  const leftH = 2.3 + r.todo.length * 0.35 + r.warnings.length * 0.5
  const rightH =
    (r.route !== "green" ? 2.7 : 0) +
    (r.others.length ? 1.3 : 0) +
    (top ? 2.1 : 0)
  const endRight = rightH < leftH
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
        <div className="banner">✨ SKRINING SELESAI! ✨</div>
        <div className={`rcols res ${endRight ? "end-right" : ""}`}>
          <section className="card rhero" aria-label="Hasil skrining">
            <div className={`rhead rt-${r.route}`}>
              <span className="re" aria-hidden="true">
                {route.emoji}
              </span>
              <div>
                <h3>{route.name}</h3>
                <p>{route.sub}</p>
              </div>
            </div>
            {top ? (
              <div className="est">
                <div className="bigemo" aria-hidden="true">
                  {top.emoji}
                </div>
                <div className="est-txt">
                  <p className="lead">Aku menebak kamu mungkin mengalami…</p>
                  <h2>{top.name}</h2>
                </div>
                <div
                  className="score"
                  role="img"
                  aria-label={`Klasifikasi kecocokan ${pct} persen`}
                >
                  <div
                    className="score-ring"
                    style={{ ["--p" as string]: pct }}
                  >
                    <div>{pct}%</div>
                  </div>
                  <small>klasifikasi kecocokan</small>
                </div>
              </div>
            ) : (
              <div className="est">
                <div className="bigemo" aria-hidden="true">
                  🩺
                </div>
                <div className="est-txt">
                  <h2>Belum dapat ditentukan</h2>
                  <p className="lead">
                    Gejalamu belum cocok dengan satu pola. Lebih aman diperiksa
                    langsung, ya!
                  </p>
                </div>
              </div>
            )}
          </section>

          <div className="rgrp rg-act">
            <Card tab="YANG PERLU DILAKUKAN">
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
              <div className="ractions">
                <a
                  className="btn btn-primary big"
                  href={mapsURL(r.maps_query)}
                  target="_blank"
                  rel="noopener"
                >
                  🧭 Navigasi ke {r.nav_label} Terdekat
                </a>
                <a
                  className="btn btn-jkn"
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
              </div>
            </Card>

            <NearestFacilities
              route={r.route}
              mapsQuery={r.maps_query}
              shareText={resultShareText(flow, r, answers)}
            />

            {r.warnings.length > 0 && (
              <Card tab="CATATAN PENTING" className="rnotes">
                {r.warnings.map((w) => (
                  <WarnBox key={w.text} {...w} />
                ))}
              </Card>
            )}
          </div>

          <div className="rgrp rg-info">
            {r.route !== "green" && <QrCard answers={api} flowId={flow.id} />}

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

          <div className="rgrp rg-end">
            <SaveCard answers={api} flowId={flow.id} />

            <Card tab="RANGKUMAN" className="rsum">
              <details className="sum">
                <summary>📄 Lihat rangkuman lengkap</summary>
                <pre>{r.summary}</pre>
              </details>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={copySummary}
              >
                📋 Salin Rangkuman
              </button>
            </Card>

            <button
              type="button"
              className="btn btn-secondary rrestart"
              onClick={onRestart}
            >
              ↻ Ulangi Skrining
            </button>
          </div>
        </div>
        <p className="footdisc">{DISCLAIMER}</p>
      </div>
    </div>
  )
}

// Remembers (per tab) that this exact result was saved, so a remount or refresh
// cannot offer a second save of the same screening.
const savedKey = (flowId: string, answers: unknown) => {
  const s = JSON.stringify([flowId, answers])
  let h = 0
  for (let i = 0; i < s.length; i++)
    h = (Math.imul(h, 31) + s.charCodeAt(i)) | 0
  return `tropicek_saved_${h}`
}
const wasSaved = (key: string) => {
  try {
    return sessionStorage.getItem(key) === "1"
  } catch {
    return false
  }
}

/** Guests are invited to make an account; only logged-in users can save, and
 * only after pressing the button (AGENTS.md "Privacy"). Answers stay in
 * sessionStorage, so after logging in the patient comes back to this result. */
function SaveCard({
  answers,
  flowId,
}: {
  answers: ReturnType<typeof toApi>
  flowId: string
}) {
  const here = useRouterState({ select: (s) => s.location.pathname })
  const key = savedKey(flowId, answers)
  const [state, setState] = useState<"idle" | "saving" | "saved" | "error">(
    () => (wasSaved(key) ? "saved" : "idle"),
  )
  if (!isLoggedIn()) {
    return (
      <Card tab="SIMPAN RIWAYAT">
        <p className="saveinfo">
          Mau menyimpan hasil ini dan melihatnya lagi nanti? Buat akun atau
          masuk dulu. Tanpa akun, hasil tidak disimpan.
        </p>
        <div className="save-btns">
          <Link
            className="btn btn-primary"
            to="/signup"
            search={{ redirect: here }}
          >
            ✨ Buat akun
          </Link>
          <Link
            className="btn btn-secondary"
            to="/login"
            search={{ redirect: here }}
          >
            Masuk
          </Link>
        </div>
      </Card>
    )
  }

  const save = async () => {
    setState("saving")
    try {
      await TriageService.createScreening({
        body: { flow_id: flowId, answers, consent: true },
      })
      try {
        sessionStorage.setItem(key, "1")
      } catch {
        // Private mode: the flag lives in memory only.
      }
      setState("saved")
      sfx.ding()
    } catch {
      setState("error")
    }
  }
  return (
    <Card tab="SIMPAN RIWAYAT">
      {state === "saved" ? (
        <>
          <p className="saveinfo">✔ Tersimpan di riwayat akunmu.</p>
          <div className="save-btns">
            <Link className="btn btn-secondary" to="/riwayat">
              📜 Lihat riwayat
            </Link>
          </div>
        </>
      ) : (
        <>
          <p className="saveinfo">
            Simpan hasil ini ke akunmu? Kamu bisa menghapusnya kapan saja di
            Riwayat skrining.
          </p>
          {state === "error" && (
            <p className="saveinfo err" role="alert">
              Gagal menyimpan. Coba lagi nanti.
            </p>
          )}
          <div className="save-btns">
            <button
              type="button"
              className="btn btn-primary"
              disabled={state === "saving"}
              onClick={save}
            >
              {state === "saving" ? "Menyimpan…" : "💾 Simpan ke riwayatku"}
            </button>
            <Link className="btn btn-secondary" to="/riwayat">
              📜 Lihat riwayat
            </Link>
          </div>
        </>
      )}
    </Card>
  )
}
