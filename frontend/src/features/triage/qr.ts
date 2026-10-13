// QR summary. The QR holds the app URL + the answers in a compact code (no name,
// NIK, BPJS number, or photo). The answers sit after "#", which browsers never send
// to the server, so the staff's phone decodes them locally and only asks our own
// API to score them (nothing is stored).
import type { Answers } from "@/client"
import qrcode from "@/lib/qrcode-generator"

export const SUMMARY_PATH = "/ringkasan"
const HASH_KEY = "d="

const ARRAY_KEYS = [
  "red_flags",
  "companion",
  "eco",
  "body",
  "findings",
] as const
const STRING_KEYS = [
  "who",
  "complaint",
  "pattern",
  "drugs",
  "province",
  "taken_at",
] as const
const NUMBER_KEYS = ["age", "temp", "height_cm", "weight_kg", "pain"] as const

export function packAnswers(a: Answers): string {
  const o: Record<string, unknown> = {}
  for (const [k, v] of Object.entries(a)) {
    if (v === null || v === undefined || v === "" || v === false) continue
    if (Array.isArray(v) && !v.length) continue
    o[k] = v
  }
  let bin = ""
  for (const b of new TextEncoder().encode(JSON.stringify(o))) {
    bin += String.fromCharCode(b)
  }
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "")
}

/** Decode and sanitize. Throws on anything malformed. */
export function unpackAnswers(code: string): Answers {
  const bin = atob(code.replace(/-/g, "+").replace(/_/g, "/"))
  const o = JSON.parse(
    new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0))),
  )
  if (!o || typeof o !== "object") throw new Error("bad summary code")
  const a: Answers = {}
  for (const k of ARRAY_KEYS) {
    if (Array.isArray(o[k])) {
      a[k] = o[k].filter((x: unknown) => typeof x === "string").slice(0, 20)
    }
  }
  for (const k of STRING_KEYS) {
    if (typeof o[k] === "string") a[k] = o[k].slice(0, 200)
  }
  for (const k of NUMBER_KEYS) {
    if (typeof o[k] === "number" && Number.isFinite(o[k])) a[k] = o[k]
  }
  if (o.sex === "L" || o.sex === "P") a.sex = o.sex
  if (["longgar", "gemuk", "normal"].includes(o.nutrition_proxy)) {
    a.nutrition_proxy = o.nutrition_proxy
  }
  a.no_thermo = o.no_thermo === true
  return a
}

export function summaryURL(a: Answers, origin = window.location.origin) {
  return `${origin}${SUMMARY_PATH}#${HASH_KEY}${packAnswers(a)}`
}

export function readSummaryHash(hash = window.location.hash): string | null {
  const h = hash.replace(/^#/, "")
  return h.startsWith(HASH_KEY) ? h.slice(HASH_KEY.length) : null
}

/** Draw the QR on a canvas. Returns false when the text is too long for a QR. */
export function drawQR(canvas: HTMLCanvasElement, text: string): boolean {
  let qr: ReturnType<typeof qrcode>
  try {
    qr = qrcode(0, "L")
    qr.addData(text)
    qr.make()
  } catch {
    return false
  }
  const n = qr.getModuleCount()
  const quiet = 4
  const m = Math.max(2, Math.floor(460 / (n + 2 * quiet)))
  canvas.width = canvas.height = (n + 2 * quiet) * m
  const ctx = canvas.getContext("2d")
  if (!ctx) return false
  ctx.fillStyle = "#fff"
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  ctx.fillStyle = "#1C1250"
  for (let y = 0; y < n; y++) {
    for (let x = 0; x < n; x++) {
      if (qr.isDark(y, x)) ctx.fillRect((x + quiet) * m, (y + quiet) * m, m, m)
    }
  }
  return true
}
