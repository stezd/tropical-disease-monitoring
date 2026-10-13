// Quiz answers as the UI holds them, and how they map to the API.
// Option IDs come from backend/app/triage/content (shared with BE and scoring).
import type { Answers, FlowPublic, Option } from "@/client"

export const NONE = "none"

export type QuizAnswers = {
  who: string | null
  age: string
  sex: "L" | "P" | null
  red_flags: string[]
  complaint: string | null
  pattern: string | null
  companion: string[]
  eco: string[]
  drugs: string
  temp: string
  no_thermo: boolean
  height: string
  weight: string
  nutrition_proxy: "longgar" | "gemuk" | "normal" | null
  body: string[]
  pain: number | null
  findings: string[]
  taken_at: string | null
}

export type MultiKey = "red_flags" | "companion" | "eco" | "findings"

export const blankAnswers = (): QuizAnswers => ({
  who: null,
  age: "",
  sex: null,
  red_flags: [],
  complaint: null,
  pattern: null,
  companion: [],
  eco: [],
  drugs: "",
  temp: "",
  no_thermo: false,
  height: "",
  weight: "",
  nutrition_proxy: null,
  body: [],
  pain: null,
  findings: [],
  taken_at: null,
})

/** Parse "37,5" or "37.5". NaN when empty or invalid. */
export const num = (v: string) => {
  const n = Number.parseFloat(String(v).replace(",", "."))
  return Number.isFinite(n) ? n : Number.NaN
}

export const ageOf = (a: QuizAnswers) => {
  const n = Number.parseInt(a.age.trim(), 10)
  return Number.isFinite(n) ? n : Number.NaN
}

export const isChild = (a: QuizAnswers, flow: FlowPublic) =>
  ageOf(a) < flow.child_age_limit

/** Options with `child_only` show only when the patient is a child. */
export const visible = (o: Option, a: QuizAnswers, flow: FlowPublic) =>
  !o.child_only || isChild(a, flow)

export const tempValid = (t: number) => t >= 34 && t <= 43

export function bmiOf(a: QuizAnswers): number | null {
  const h = num(a.height)
  const w = num(a.weight)
  if (!(h >= 50 && h <= 230 && w >= 3 && w <= 250)) return null
  return w / (h / 100) ** 2
}

export const hasRedFlag = (a: QuizAnswers) =>
  a.red_flags.some((x) => x !== NONE)

/** Age changes which options show. Drop answers that are no longer visible. */
export function pruneByAge(a: QuizAnswers, flow: FlowPublic): QuizAnswers {
  const pattern = flow.patterns[a.complaint ?? ""]?.options.find(
    (o) => o.id === a.pattern,
  )
  return {
    ...a,
    pattern: pattern && !visible(pattern, a, flow) ? null : a.pattern,
    eco: a.eco.filter((id) => {
      const o = flow.eco.find((e) => e.id === id)
      return !o || visible(o, a, flow)
    }),
  }
}

export type StepId =
  | "who"
  | "q1"
  | "q2"
  | "q3"
  | "q4"
  | "q5"
  | "q6"
  | "q7"
  | "q8"
  | "q9"
  | "q10"

export function steps(a: QuizAnswers, flow: FlowPublic): StepId[] {
  const f: StepId[] = ["who", "q1", "q2", "q3"]
  if (a.complaint && flow.companions[a.complaint]) f.push("q4")
  return [...f, "q5", "q6", "q7", "q8", "q9", "q10"]
}

/** Index in the stage map (flow.stages) for each step. */
export const STAGE_OF: Record<StepId, number> = {
  who: 0,
  q1: 0,
  q2: 1,
  q3: 2,
  q4: 2,
  q5: 3,
  q6: 3,
  q7: 4,
  q8: 4,
  q9: 4,
  q10: 4,
}

/** Number within the API's accepted range, else null (the API would reject it). */
const optNum = (v: string, max: number) => {
  const n = num(v)
  return Number.isFinite(n) && n >= 0 && n <= max ? n : null
}

export function toApi(a: QuizAnswers): Answers {
  const age = ageOf(a)
  const t = num(a.temp)
  return {
    who: a.who,
    age: Number.isFinite(age) ? age : null,
    sex: a.sex,
    red_flags: a.red_flags,
    complaint: a.complaint,
    pattern: a.pattern,
    companion: a.companion,
    eco: a.eco,
    drugs: a.drugs.slice(0, 500),
    temp: !a.no_thermo && tempValid(t) ? Math.round(t * 10) / 10 : null,
    no_thermo: a.no_thermo,
    height_cm: optNum(a.height, 300),
    weight_kg: optNum(a.weight, 500),
    nutrition_proxy: a.nutrition_proxy,
    body: a.body,
    pain: a.body.length ? a.pain : null,
    findings: a.findings,
    taken_at: a.taken_at,
  }
}

/** Current time as ISO 8601 with the device's UTC offset, e.g. 2026-10-13T15:04:00+08:00. */
export function nowWithOffset(d = new Date()): string {
  const pad = (n: number) => String(Math.floor(Math.abs(n))).padStart(2, "0")
  const off = -d.getTimezoneOffset()
  const sign = off >= 0 ? "+" : "-"
  return (
    `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
    `T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}` +
    `${sign}${pad(off / 60)}:${pad(off % 60)}`
  )
}
