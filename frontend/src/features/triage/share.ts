// Short screening summary for "Kirim rangkuman via WhatsApp" on a facility card.
// The patient opens WhatsApp and sends it themself (plain wa.me link); our server
// sends nothing. No name, NIK, or coordinates: the link is the same /ringkasan
// page as the QR (answers in the URL hash, see qr.ts).
//
// Patient-facing text: never "diagnosis" (AGENTS.md). Perlu OK DR.
import type { FlowPublic, ScoreResult } from "@/client"
import { NONE, type QuizAnswers, redFlagIds, toApi } from "./model"
import { summaryURL } from "./qr"

const INTRO = "Halo, saya mengirim rangkuman skrining dari aplikasi TropiCare."
const OUTRO = "Ini skrining awal, bukan pemeriksaan dokter."

function routeLine(flow: FlowPublic, route: string): string | null {
  const r = flow.routes[route]
  return r ? `• Rute: ${r.name} (${r.sub})` : null
}

function complaintLine(flow: FlowPublic, a: QuizAnswers): string | null {
  if (!a.complaint) return null
  const name =
    a.complaint === NONE
      ? "Tidak ada keluhan"
      : flow.clusters.find((c) => c.id === a.complaint)?.name
  return name ? `• Keluhan utama: ${name}` : null
}

function compose(lines: (string | null)[], link: string): string {
  return [
    INTRO,
    ...lines.filter(Boolean),
    `Rangkuman lengkap: ${link}`,
    OUTRO,
  ].join("\n")
}

/** Message for a finished screening (result page). */
export function resultShareText(
  flow: FlowPublic,
  r: ScoreResult,
  a: QuizAnswers,
): string {
  const top = r.unknown ? null : r.top
  return compose(
    [
      routeLine(flow, r.route),
      top
        ? `• Perkiraan utama: ${top.name}, kecocokan ${top.pct}%`
        : "• Perkiraan utama: belum dapat ditentukan",
      complaintLine(flow, a),
    ],
    summaryURL(toApi(a), flow.id),
  )
}

/** Message for the red route: the danger signs picked, no score. */
export function redShareText(flow: FlowPublic, a: QuizAnswers): string {
  const ids = redFlagIds(a, flow)
  const signs = flow.red_flags
    .filter((f) => ids.includes(f.id))
    .map((f) => f.condition)
    .join(", ")
  return compose(
    [routeLine(flow, "red"), signs ? `• Tanda bahaya: ${signs}` : null],
    summaryURL(toApi(a), flow.id),
  )
}
