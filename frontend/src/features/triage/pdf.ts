// "Unduh PDF" for the result page: the screening summary as a file the patient
// can keep or show to staff. Built in the browser (jsPDF is loaded on tap), so
// nothing is sent to the server. No name, NIK, or coordinates, same as the QR.
//
// The built-in PDF fonts only cover Latin text, so emoji are dropped.
// Patient-facing text: never "diagnosis" as a finding (AGENTS.md). Perlu OK DR.
import type { FlowPublic, ScoreResult } from "@/client"

const DISCLAIMER =
  "Ini adalah skrining awal, bukan diagnosis dokter. Jika kondisi memburuk, segera ke fasilitas kesehatan atau hubungi 119."

const MARGIN = 16
const LINE = 5.2

// Characters a standard PDF font can draw: Latin-1 plus bullet, dashes, ellipsis.
const EXTRA = new Set([0x2022, 0x2013, 0x2014, 0x2026])
const drawable = (ch: string) => {
  const c = ch.charCodeAt(0)
  return (
    c === 10 ||
    (c >= 0x20 && c <= 0x7e) ||
    (c >= 0xa0 && c <= 0xff) ||
    EXTRA.has(c)
  )
}

function clean(s: string): string {
  const text = s
    .replace(/\*\*/g, "")
    .replace(/≥/g, ">=")
    .replace(/≤/g, "<=")
    .replace(/→/g, "->")
  return Array.from(text)
    .filter(drawable)
    .join("")
    .replace(/ {2,}/g, " ")
    .trim()
}

export async function downloadSummaryPdf(flow: FlowPublic, r: ScoreResult) {
  const { jsPDF } = await import("jspdf")
  const doc = new jsPDF({ unit: "mm", format: "a4" })
  const width = doc.internal.pageSize.getWidth() - MARGIN * 2
  const bottom = doc.internal.pageSize.getHeight() - MARGIN
  let y = MARGIN

  const room = (h: number) => {
    if (y + h > bottom) {
      doc.addPage()
      y = MARGIN
    }
  }
  const text = (s: string, size = 10, bold = false, indent = 0) => {
    doc.setFont("helvetica", bold ? "bold" : "normal")
    doc.setFontSize(size)
    const lines = doc.splitTextToSize(clean(s), width - indent) as string[]
    for (const l of lines) {
      room(LINE)
      doc.text(l, MARGIN + indent, y)
      y += LINE
    }
  }
  const heading = (s: string) => {
    y += 3
    room(12)
    text(s.toUpperCase(), 9, true)
    doc.setDrawColor(180)
    doc.line(MARGIN, y - 3.5, MARGIN + width, y - 3.5)
    y += 0.5
  }
  const bullets = (items: string[]) => {
    for (const x of items) text(`• ${x}`, 10, false, 2)
  }

  const route = flow.routes[r.route]
  const top = r.unknown ? null : r.top
  const row = (k: string) => r.summary_rows.find((x) => x.key === k)?.value
  const labs = (row("lab") ?? "-") === "-" ? [] : row("lab")!.split("; ")
  const facts = r.summary_rows.filter(
    (x) =>
      !["date", "lab", "estimate", "route"].includes(x.key) &&
      x.value !== "-" &&
      x.value !== "",
  )

  text("TropiCare - Rangkuman Skrining", 16, true)
  y += 1
  if (row("date")) text(`Diisi ${row("date")}`, 9)

  heading("Rute")
  text(`${route.name} (${route.sub})`, 12, true)
  text(`Arahkan ke: ${r.place}`)

  heading("Perkiraan")
  if (top) text(`${top.name} - kecocokan ${top.pct}%`, 12, true)
  else text("Belum dapat ditentukan", 12, true)
  if (r.others.length) {
    text("Kemungkinan lain:", 10, true)
    bullets(r.others.map((o) => `${o.name} (${o.pct}%)`))
  }

  if (r.warnings.length) {
    heading("Catatan penting")
    bullets(r.warnings.map((w) => w.text))
  }
  if (labs.length) {
    heading("Lab yang mungkin dibutuhkan")
    bullets(labs)
  }
  if (facts.length) {
    heading("Data pasien")
    for (const f of facts) text(`${f.label}: ${f.value}`, 10, false, 2)
  }
  heading("Yang perlu dilakukan")
  bullets(r.todo)
  if (top && r.reasons.length) {
    heading("Dasar perkiraan")
    bullets(r.reasons)
  }

  y += 6
  room(14)
  doc.setTextColor(110)
  text(DISCLAIMER, 9)

  doc.save(`rangkuman-skrining-${new Date().toISOString().slice(0, 10)}.pdf`)
}
