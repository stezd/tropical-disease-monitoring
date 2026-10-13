// "Rangkuman Pasien": the page staff see after scanning the QR on the result page.
// Answers come from the URL hash (never sent to the server as part of the URL);
// the page asks our own API to score them. Nothing is stored.
import { useQuery } from "@tanstack/react-query"
import { Link, useRouterState } from "@tanstack/react-router"
import { useMemo } from "react"

import { scoreAnswers, useFlow } from "../api"
import { Sparkles } from "../components/Art"
import { Card } from "../components/Ui"
import { readSummaryHash, unpackAnswers } from "../qr"
import { AdviceCards } from "./Result"

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
  })
  const r = score.data
  const route = r && flow ? flow.routes[r.route] : null

  return (
    <div className="screen bg-result">
      <Sparkles n={10} />
      <div className="hud">
        <Link className="icon-btn" to="/" aria-label="Beranda">
          ⌂
        </Link>
        <div className="htitle">Rangkuman Pasien</div>
      </div>
      <div className="rscroll">
        {!answers || score.isError ? (
          <Card tab="TIDAK BISA DIBACA" style={{ marginTop: 34 }}>
            <p className="saveinfo">
              {answers
                ? "Server TropiCare tidak bisa dihubungi. Coba muat ulang halaman ini."
                : "Kode QR ini tidak lengkap atau rusak. Minta pasien menampilkan QR dari halaman hasil sekali lagi."}
            </p>
          </Card>
        ) : !r || !route ? (
          <p className="footdisc">Memuat rangkuman…</p>
        ) : (
          <>
            <div
              className="banner"
              style={{
                background: `linear-gradient(${route.color_from},${route.color_to})`,
              }}
            >
              {route.emoji} {route.name}
            </div>
            <div className="rcols">
              <div className="rcol">
                <Card tab="KONDISI PASIEN" style={{ marginTop: 34 }}>
                  <pre className="scanpre">{r.summary}</pre>
                </Card>
              </div>
              <div className="rcol">
                <AdviceCards r={r} />
                <div className="btnrow">
                  <Link className="btn btn-teal" to="/">
                    Buka TropiCare
                  </Link>
                </div>
              </div>
            </div>
          </>
        )}
        <p className="footdisc">
          ⚠️ Ini hasil skrining awal dari jawaban pasien, bukan diagnosis dokter.
        </p>
      </div>
    </div>
  )
}
