// "Rangkuman Pasien": the page staff see after scanning the QR on the result page.
// Answers come from the URL hash (never sent to the server as part of the URL);
// the page asks our own API to score them. Nothing is stored.
//
// Order follows what staff need first: where the patient goes, danger signs, labs,
// the estimate, then the answers. Everything else is one tap away.
import { useQuery } from "@tanstack/react-query"
import { Link, useRouterState } from "@tanstack/react-router"
import { AxiosError } from "axios"
import { useMemo } from "react"

import type { ScoreResult, SummaryRow } from "@/client"
import { scoreAnswers, useFlow } from "../api"
import { Card, copyText, Rich, toast, WarnBox } from "../components/Ui"
import { readSummaryHash, unpackAnswers } from "../qr"

/** The API refused these answers (unknown flow, number out of range). */
const isBadCode = (e: unknown) =>
  e instanceof AxiosError && [404, 422].includes(e.response?.status ?? 0)

// Rows shown elsewhere on the page, not in "Data pasien".
const OWN_PLACE = new Set(["date", "lab", "estimate", "route"])
const EMPTY = new Set(["-", ""])
// "Tunjukkan QR ke petugas" is advice for the patient, not for the staff reading this.
const QR_TODO = /QR rangkuman/

export function SummaryScreen() {
  const hash = useRouterState({ select: (s) => s.location.hash })
  const packed = useMemo(() => {
    const code = readSummaryHash(hash)
    if (!code) return null
    try {
      return unpackAnswers(code)
    } catch {
      return null
    }
  }, [hash])
  const answers = packed?.answers ?? null
  const flowId = packed?.flowId ?? "infection"
  const { flow } = useFlow(flowId)
  const score = useQuery({
    queryKey: ["triage", "summary", flowId, answers],
    queryFn: () => scoreAnswers(answers!, flowId),
    enabled: !!answers,
    staleTime: Number.POSITIVE_INFINITY,
    retry: (n, e) => !isBadCode(e) && n < 2,
  })
  const r = score.data
  const route = r && flow ? flow.routes[r.route] : null

  return (
    <div className="screen bg-result">
      <div className="hud">
        <Link className="icon-btn" to="/" aria-label="Beranda">
          ⌂
        </Link>
        <div className="htitle">Rangkuman Pasien</div>
      </div>
      <div className="rscroll">
        {!answers || score.isError ? (
          <Card tab="TIDAK BISA DIBACA" className="card-solo">
            <p className="saveinfo">
              {answers
                ? isBadCode(score.error)
                  ? "Kode QR tidak valid. Minta pasien menampilkan QR dari halaman hasil sekali lagi."
                  : "Server TropiCare tidak bisa dihubungi. Coba muat ulang halaman ini."
                : "Kode QR ini tidak lengkap atau rusak. Minta pasien menampilkan QR dari halaman hasil sekali lagi."}
            </p>
          </Card>
        ) : !r || !route ? (
          <p className="footdisc">Memuat rangkuman…</p>
        ) : (
          <SummaryBody r={r} route={route} />
        )}
        <p className="footdisc">
          ⚠️ Ini hasil skrining awal dari jawaban pasien, bukan diagnosis dokter.
          Pastikan dengan pemeriksaan langsung.
        </p>
      </div>
    </div>
  )
}

function SummaryBody({
  r,
  route,
}: {
  r: ScoreResult
  route: { emoji: string; name: string; sub: string }
}) {
  const rows = new Map(r.summary_rows.map((x) => [x.key, x]))
  const value = (k: string) => rows.get(k)?.value ?? "-"
  const flags = value("red_flags")
  const hasFlags = !EMPTY.has(flags) && flags !== "tidak ada"
  const labs = EMPTY.has(value("lab")) ? [] : value("lab").split("; ")
  // Danger signs already have their own box when there are any.
  const facts = r.summary_rows.filter(
    (x) =>
      !OWN_PLACE.has(x.key) &&
      !EMPTY.has(x.value) &&
      !(x.key === "red_flags" && hasFlags),
  )
  const top = r.unknown ? null : r.top
  const todo = r.todo.filter((x) => !QR_TODO.test(x))

  const copy = async () => {
    toast(
      (await copyText(r.summary))
        ? "📋 Rangkuman tersalin!"
        : 'Gagal menyalin — buka "Teks lengkap".',
    )
  }

  return (
    <div className="rcols sumpage">
      <div className="rcol">
        <div className="card rcard">
          <div className={`rhead rt-${r.route}`}>
            <div className="re" aria-hidden="true">
              {route.emoji}
            </div>
            <h3>{route.name}</h3>
            <p>{route.sub}</p>
          </div>
          <div className="rbody">
            <div className="sum-place">
              <span>Arahkan ke</span>
              <b>{r.place}</b>
            </div>
            <div className="sum-meta">🕒 Diisi {value("date")}</div>
          </div>
        </div>

        {hasFlags && (
          <div className="warn r sum-flag">
            <span className="wi" aria-hidden="true">
              🚨
            </span>
            <span>
              <b>Tanda bahaya:</b> {flags}
            </span>
          </div>
        )}

        <Card tab="PERKIRAAN">
          {top ? (
            <div className="sum-top">
              <span className="sum-emo" aria-hidden="true">
                {top.emoji}
              </span>
              <span className="sum-name">{top.name}</span>
              <span className="sum-pct">{top.pct}%</span>
            </div>
          ) : (
            <div className="sum-top">
              <span className="sum-emo" aria-hidden="true">
                🩺
              </span>
              <span className="sum-name">Belum dapat ditentukan</span>
            </div>
          )}
          {r.others.length > 0 && (
            <ul className="sum-others" aria-label="Kemungkinan lain">
              {r.others.map((o) => (
                <li key={o.id}>
                  <span aria-hidden="true">{o.emoji}</span> {o.name}
                  <b>{o.pct}%</b>
                </li>
              ))}
            </ul>
          )}
        </Card>

        {labs.length > 0 && (
          <Card tab="LAB YANG MUNGKIN DIBUTUHKAN">
            <ul className="sum-labs">
              {labs.map((x) => (
                <li key={x}>🧪 {x}</li>
              ))}
            </ul>
          </Card>
        )}

        {r.warnings.length > 0 && (
          <Card tab="CATATAN PENTING">
            {r.warnings.map((w) => (
              <WarnBox key={w.text} {...w} />
            ))}
          </Card>
        )}
      </div>

      <div className="rcol">
        <Card tab="DATA PASIEN">
          <dl className="sum-facts">
            {facts.map((x) => (
              <Fact key={x.key} row={x} />
            ))}
          </dl>
        </Card>

        {top && r.reasons.length > 0 && (
          <Card tab="DASAR PERKIRAAN">
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

        <details className="sum sum-more">
          <summary>💬 Saran yang diterima pasien ({todo.length})</summary>
          <ul className="todo">
            {todo.map((x) => (
              <li key={x}>
                <Rich text={x} />
              </li>
            ))}
          </ul>
        </details>
        <details className="sum sum-more">
          <summary>📄 Teks lengkap</summary>
          <pre>{r.summary}</pre>
          <button type="button" className="btn btn-secondary" onClick={copy}>
            📋 Salin rangkuman
          </button>
        </details>
      </div>
    </div>
  )
}

function Fact({ row }: { row: SummaryRow }) {
  return (
    <div className={row.key === "patient" ? "sum-fact lead" : "sum-fact"}>
      <dt>{row.label}</dt>
      <dd>{row.value}</dd>
    </div>
  )
}
