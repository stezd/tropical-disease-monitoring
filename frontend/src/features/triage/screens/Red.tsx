// Red route. Runs fully in the browser: no server call, so it works offline.
// Calm and serious: no confetti, no game sounds, no mascot (AGENTS.md "Must not break").
import { useEffect } from "react"

import type { FlowPublic } from "@/client"
import { NearestFacilities } from "../components/Nearby"
import { Card, copyText, RED_TAB, toast } from "../components/Ui"
import { vibrate } from "../fx"
import { mapsURL } from "../links"
import { type QuizAnswers, redFlagIds } from "../model"

export function RedScreen({
  flow,
  answers,
  onBack,
  onRestart,
}: {
  flow: FlowPublic
  answers: QuizAnswers
  onBack: () => void
  onRestart: () => void
}) {
  const ids = redFlagIds(answers, flow)
  const flags = flow.red_flags.filter((r) => ids.includes(r.id))
  const onlyRabies = flags.length === 1 && flags[0].id === "rabies"
  const q = onlyRabies
    ? flow.red_maps.rabies
    : flags.some((f) => f.id === "ginjal")
      ? flow.red_maps.ginjal
      : flow.red_maps.default
  const facilities = [...new Set(flags.map((f) => f.facility))]

  useEffect(() => {
    vibrate([220, 100, 220, 100, 220])
  }, [])

  const copy = async (n: string) => {
    toast((await copyText(n)) ? `Nomor ${n} tersalin` : `Nomor darurat: ${n}`)
  }

  return (
    <div className="screen bg-red">
      <div className="hud">
        <button
          type="button"
          className="icon-btn"
          onClick={onBack}
          aria-label="Kembali"
        >
          ‹
        </button>
        <div className="htitle">KONDISI DARURAT</div>
      </div>
      <div className="rscroll">
        <div className="redcols">
          <div className="redcol">
            <div className="siren" aria-hidden="true">
              🚨
            </div>
            <h1 className="redh">KONDISI DARURAT</h1>
            <p className="redp">
              Kuesioner dihentikan. Segera ke <b>IGD Rumah Sakit</b> sekarang —
              jangan menunggu.
            </p>
            <a className="btn btn-danger big" href="tel:119">
              📞 Telepon 119 · Ambulans
            </a>
            <Card
              tab="NOMOR DARURAT"
              tabStyle={RED_TAB}
              style={{ marginTop: "var(--card-gap)" }}
            >
              <div className="nums">
                <div className="numcard">
                  <b>119</b>
                  <span>Gawat darurat medis / ambulans</span>
                  <button type="button" onClick={() => copy("119")}>
                    Salin
                  </button>
                </div>
                <div className="numcard">
                  <b>112</b>
                  <span>Nomor darurat umum</span>
                  <button type="button" onClick={() => copy("112")}>
                    Salin
                  </button>
                </div>
              </div>
            </Card>
            <a
              className="btn btn-secondary"
              style={{ marginTop: "var(--sp-4)" }}
              href={mapsURL(q)}
              target="_blank"
              rel="noopener"
            >
              🧭 Navigasi ke {onlyRabies ? "Rabies Center" : "IGD"} Terdekat
            </a>
            {flags.some((f) => f.id === "rabies") && !onlyRabies && (
              <a
                className="btn btn-secondary"
                style={{ marginTop: "var(--sp-4)" }}
                href={mapsURL(flow.red_maps.rabies)}
                target="_blank"
                rel="noopener"
              >
                💉 Cari Rabies Center (VAR)
              </a>
            )}
            <NearestFacilities route="red" tone="red" />
          </div>
          <div className="redcol">
            <Card
              tab="TERDETEKSI"
              tabStyle={RED_TAB}
              style={{ marginTop: "var(--card-gap)" }}
            >
              {flags.map((f) => (
                <div className="rflag" key={f.id}>
                  <span className="oe" aria-hidden="true">
                    {f.emoji}
                  </span>
                  <div>
                    <b>{f.condition}</b>
                    {f.first_aid && <em>🩹 Sambil menuju RS: {f.first_aid}</em>}
                    {f.dont && <em className="dont">🚫 Jangan: {f.dont}</em>}
                  </div>
                </div>
              ))}
            </Card>
            <Card tab="FASILITAS YANG DICARI" tabStyle={RED_TAB}>
              <p className="saveinfo">
                Jangan ke klinik biasa. Cari rumah sakit yang punya:
              </p>
              <div className="fac">
                {facilities.map((f) => (
                  <span key={f}>✔ {f}</span>
                ))}
              </div>
            </Card>
            <div className="btnrow">
              <button type="button" className="btn btn-ghost" onClick={onBack}>
                ‹ Salah pilih? Ubah jawaban
              </button>
              <button
                type="button"
                className="btn btn-ghost"
                onClick={onRestart}
              >
                ↻ Ulangi Skrining
              </button>
            </div>
          </div>
        </div>
        <p className="footdisc">
          ⚠️ Ini skrining awal, bukan diagnosis dokter. Pada keadaan darurat,
          hubungi 119 atau datang ke IGD terdekat.
        </p>
      </div>
    </div>
  )
}
