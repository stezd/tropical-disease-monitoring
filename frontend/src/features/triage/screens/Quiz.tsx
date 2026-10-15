import { useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { type ReactNode, type Ref, useMemo, useRef, useState } from "react"

import type { FlowPublic, ScoreResult } from "@/client"
import { previewKey, scoreAnswers } from "../api"
import { hop, Mascot, Sparkles } from "../components/Art"
import { BodyMap, PainScale } from "../components/Body"
import { Card, Modal, Options, Rich, StageMap, WarnBox } from "../components/Ui"
import { sfx, vibrate } from "../fx"
import {
  ageOf,
  asksPregnancy,
  bmiOf,
  cholesterolValid,
  companionQuestion,
  diaValid,
  GLUCOSE_HIGH_FROM,
  glucoseValid,
  hasRedFlag,
  type MultiKey,
  NONE,
  nowWithOffset,
  num,
  prune,
  type QuizAnswers,
  redFlagIds,
  STAGE_OF,
  type StepId,
  steps,
  sysValid,
  tempValid,
  toApi,
  uricValid,
  visible,
} from "../model"
import { quiz, useQuiz } from "../store"
import "@/styles/fe-extra.css"

type StepDef = {
  tab: string
  say: string
  valid: (a: QuizAnswers, flow: FlowPublic) => boolean
  nextLabel?: (a: QuizAnswers, flow: FlowPublic) => string
  nextCls?: (a: QuizAnswers, flow: FlowPublic) => string
}

type Vital = FlowPublic["vitals"][number]

/** Tile class: wide options span the row; "none" is tinted green. */
function tileCls(o: { id: string; wide?: boolean | null }) {
  return [o.wide && "wide", o.id === NONE && "safe"].filter(Boolean).join(" ")
}

/** A stand-in question was answered (at least one option, "none" included). */
function proxyAnswered(a: QuizAnswers, flow: FlowPublic, vital: Vital) {
  const opts = flow.vital_proxies?.[vital]
  if (!opts?.length) return true
  return opts.some((o) => a.vital_proxy.includes(o.id))
}

function vitalsValid(a: QuizAnswers, flow: FlowPublic) {
  const v = flow.vitals
  if (v.includes("temp")) {
    if (a.no_thermo ? !proxyAnswered(a, flow, "temp") : !tempValid(num(a.temp)))
      return false
  }
  if (v.includes("bp")) {
    if (a.no_bp) {
      if (!proxyAnswered(a, flow, "bp")) return false
    } else if (!sysValid(num(a.bp_sys)) || !diaValid(num(a.bp_dia))) {
      return false
    }
  }
  // Blood sugar is optional, but a typed value must make sense.
  if (v.includes("glucose") && a.glucose.trim()) {
    if (!glucoseValid(num(a.glucose))) return false
  }
  return true
}

/** Optional lab value: empty, or a number in range. */
const optionalValid = (v: string, ok: (n: number) => boolean) =>
  !v.trim() || ok(num(v))

const STEP_DEFS: Record<StepId, StepDef> = {
  who: {
    tab: "MULAI · DATA DIRI",
    say: "Halo, aku **Kak Tropi**! 👋 Kenalan dulu, yuk.",
    valid: (a, flow) => {
      const n = ageOf(a)
      return (
        !!a.who &&
        n >= 0 &&
        n <= 120 &&
        !!a.sex &&
        (!asksPregnancy(a, flow) || a.pregnant !== null)
      )
    },
  },
  q1: {
    tab: "TAHAP 1 · TANDA BAHAYA",
    say: "Cek **tanda bahaya** dulu, ya ❤️",
    valid: (a) => a.red_flags.length > 0,
    nextLabel: (a) =>
      hasRedFlag(a) ? "🚨 Lihat Tindakan Darurat" : "Lanjut ▶",
    nextCls: (a) => (hasRedFlag(a) ? "btn-danger" : "btn-primary"),
  },
  q2: {
    tab: "TAHAP 2 · KELUHAN UTAMA",
    say: "Aman! 😊 Apa **keluhan utamanya**?",
    valid: (a) => !!a.complaint,
  },
  q3: {
    tab: "TAHAP 3 · GEJALA",
    say: "Aku mulai punya **tebakan** 🔍",
    valid: (a) => !!a.pattern,
  },
  q4: {
    tab: "TAHAP 3 · GEJALA PENYERTA",
    say: "Ini membedakan penyakit yang **mirip** 🧩",
    valid: (a) => a.companion.length > 0,
    nextLabel: (a, flow) =>
      redFlagIds(a, flow).length ? "🚨 Lihat Tindakan Darurat" : "Lanjut ▶",
    nextCls: (a, flow) =>
      redFlagIds(a, flow).length ? "btn-danger" : "btn-primary",
  },
  q5: {
    tab: "TAHAP 4 · PETA EKOLOGI",
    say: "Lingkungan juga memberi **petunjuk** 🌴",
    valid: (a) => a.eco.length > 0,
  },
  q6: {
    tab: "TAHAP 4 · RIWAYAT OBAT",
    say: "Boleh dikosongkan kalau belum 💊",
    valid: () => true,
  },
  q7: {
    tab: "TAHAP 5 · TANDA VITAL",
    say: "Cek **suhu tubuh** 🌡️",
    valid: vitalsValid,
  },
  labs: {
    tab: "TAHAP 5 · PEMERIKSAAN OPSIONAL",
    say: "Punya hasil cek lab? **Boleh dilewati** 🧪",
    valid: (a) =>
      optionalValid(a.uric_acid, uricValid) &&
      optionalValid(a.cholesterol_total, cholesterolValid),
    nextLabel: (a) =>
      a.uric_acid.trim() || a.cholesterol_total.trim()
        ? "Lanjut ▶"
        : "Lewati ▶",
  },
  q8: {
    tab: "TAHAP 5 · KALKULATOR RISIKO",
    say: "Untuk hitung **risiko keparahan** ⚖️",
    valid: (a) => !!bmiOf(a) || !!a.nutrition_proxy,
  },
  q9: {
    tab: "TAHAP 5 · PETA NYERI",
    say: "Tunjukkan bagian yang **sakit** 👆",
    valid: (a) => !a.body.length || a.pain !== null,
    nextLabel: (a) =>
      a.body.length ? "Lanjut ▶" : "Tidak ada nyeri, lanjut ▶",
  },
}

const LAST_LABEL = "🔮 Lihat Tebakan Kak Tropi"

function noThermoNote(a: { complaint?: string | null }) {
  return a.complaint === "A"
    ? "Tak apa! Klasifikasi tetap memakai **pola demam** yang kamu pilih tadi."
    : "Tak apa! Klasifikasi tetap dihitung dari **jawaban lainnya**."
}

export function QuizScreen({ flow }: { flow: FlowPublic }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { answers: a, step } = useQuiz()
  const ids = steps(a, flow)
  const id = ids[Math.min(step, ids.length - 1)]
  const text = flow.step_text?.[id]
  const base = STEP_DEFS[id]
  const def: StepDef = {
    ...base,
    tab: text?.tab ?? base.tab,
    say: text?.say ?? base.say,
  }
  const valid = def.valid(a, flow)
  const isLast = ids.indexOf(id) === ids.length - 1
  const nextLabel = isLast
    ? LAST_LABEL
    : (def.nextLabel?.(a, flow) ?? "Lanjut ▶")
  const api = useMemo(() => toApi(a), [a])
  const mascot = useRef<SVGSVGElement>(null)
  const [modal, setModal] = useState<ReactNode>(null)
  const [busy, setBusy] = useState(false)

  const set = (patch: Partial<QuizAnswers>) =>
    quiz.answer((prev) => ({ ...prev, ...patch }))

  const pick = (
    key: MultiKey | "who" | "sex" | "complaint" | "pattern",
    id: string,
    multi: boolean,
  ) => {
    quiz.answer((prev) => {
      if (multi) {
        const k = key as MultiKey
        let arr = prev[k]
        if (id === NONE) arr = arr.includes(NONE) ? [] : [NONE]
        else {
          arr = arr.filter((x) => x !== NONE)
          arr = arr.includes(id) ? arr.filter((x) => x !== id) : [...arr, id]
        }
        return { ...prev, [k]: arr }
      }
      if (key === "complaint" && prev.complaint !== id) {
        return { ...prev, complaint: id, pattern: null, companion: [] }
      }
      if (key === "pattern" && prev.pattern !== id) {
        return prune({ ...prev, pattern: id, companion: [] }, flow)
      }
      if (key === "sex") return prune({ ...prev, sex: id as "L" | "P" }, flow)
      return { ...prev, [key]: id }
    })
    sfx.tap()
    vibrate()
    hop(mascot.current)
    if (key === "red_flags" && id !== NONE) vibrate([60, 40, 60])
  }

  const proceed = () => {
    const cur = quiz.get().answers
    if (id === "who") set(prune(cur, flow))
    if (
      (id === "q1" && hasRedFlag(cur)) ||
      (id === "q4" && redFlagIds(cur, flow).length)
    ) {
      quiz.set({ phase: "red" })
      return
    }
    const list = steps(quiz.get().answers, flow)
    if (step < list.length - 1) quiz.set({ step: step + 1 })
    else {
      set({ taken_at: nowWithOffset() })
      quiz.set({ phase: "thinking" })
    }
  }

  const next = async () => {
    if (!valid || busy) return
    sfx.tap()
    if (id === "q6") {
      // Drug warnings come from the server (advice.json). If it is down, carry on.
      // Rules only (preview): no model call mid-quiz, and its own query key so
      // it never stands in for the final result.
      setBusy(true)
      let r: ScoreResult | undefined
      try {
        r = await queryClient.fetchQuery({
          queryKey: previewKey(api, flow.id),
          queryFn: () => scoreAnswers(api, flow.id, true),
          staleTime: Number.POSITIVE_INFINITY,
        })
      } catch {
        r = undefined
      }
      setBusy(false)
      if (r?.drug_popups.length) {
        sfx.alert()
        vibrate([80, 60, 80])
        const red = r.drug_popups.some((p) => p.level === "r")
        setModal(
          <Modal
            tone={red ? "red" : "yellow"}
            tab="PERINGATAN OBAT"
            onClose={() => setModal(null)}
            actions={
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  setModal(null)
                  proceed()
                }}
              >
                Mengerti, lanjut ▶
              </button>
            }
          >
            <h3>Kak Tropi menemukan sesuatu! 🧐</h3>
            {r.drug_popups.map((w) => (
              <WarnBox key={w.text} {...w} />
            ))}
          </Modal>,
        )
        return
      }
    }
    proceed()
  }

  // The first question goes back to the privacy gate (which goes home).
  const back = () => {
    sfx.tap()
    if (step > 0) quiz.set({ step: step - 1 })
    else quiz.set({ phase: "privacy" })
  }

  const home = () => {
    sfx.tap()
    navigate({ to: "/" })
  }

  const body = (() => {
    switch (id) {
      case "who":
        return <StepWho flow={flow} a={a} pick={pick} set={set} />
      case "q1":
        return (
          <>
            <h2 className="qt">
              <span className="alertline">⚠️</span> Ada <u>salah satu</u> kondisi
              darurat ini?
            </h2>
            <p className="qh">Pilih semua yang dialami</p>
            <Options
              multi
              selected={a.red_flags}
              onPick={(i) => pick("red_flags", i, true)}
              options={[
                ...flow.red_flags
                  .filter((r) => r.listed !== false)
                  .map((r) => ({
                    id: r.id,
                    emoji: r.emoji,
                    text: r.text,
                    detail: r.detail,
                    cls: "danger",
                  })),
                {
                  id: NONE,
                  emoji: "✅",
                  text: "Tidak ada, saya aman",
                  cls: "safe",
                },
              ]}
            />
          </>
        )
      case "q2": {
        const box = (c: {
          id: string
          emoji: string
          name: string
          sub: string
        }) => (
          <button
            key={c.id}
            type="button"
            aria-pressed={a.complaint === c.id}
            className={`cbox c${c.id} ${a.complaint === c.id ? "on" : ""}`}
            onClick={() => pick("complaint", c.id, false)}
          >
            <span className="ce" aria-hidden="true">
              {c.emoji}
            </span>
            <span className="ct">
              <b>{c.name}</b>
              <span className="cs">{c.sub}</span>
            </span>
          </button>
        )
        return (
          <>
            <h2 className="qt">
              {text?.title ?? "Keluhan mana yang paling mengganggu?"}
            </h2>
            <p className="qh">{text?.hint ?? "Pilih satu"}</p>
            <div className={`cgrid ${flow.clusters.length % 2 ? "" : "even"}`}>
              {flow.clusters.map(box)}
            </div>
            {/* Outside the grid: a plain full-width row under the groups. */}
            {flow.allow_no_complaint &&
              box({
                id: NONE,
                emoji: "🙂",
                name: "Tidak ada keluhan",
                sub: "Cek risiko saja",
              })}
          </>
        )
      }
      case "q3": {
        const q = flow.patterns[a.complaint ?? ""]
        return (
          <>
            <h2 className="qt">{text?.title ?? q.title}</h2>
            <p className="qh">{text?.hint ?? "Pilih yang paling mirip"}</p>
            <Options
              selected={a.pattern ? [a.pattern] : []}
              onPick={(i) => pick("pattern", i, false)}
              options={q.options.filter((o) => visible(o, a, flow))}
            />
          </>
        )
      }
      case "q4": {
        const q = companionQuestion(a, flow)
        if (!q) return null
        return (
          <>
            <h2 className="qt">{q.title}</h2>
            <p className="qh">Pilih semua yang sesuai</p>
            <Options
              multi
              selected={a.companion}
              onPick={(i) => pick("companion", i, true)}
              options={q.options}
            />
          </>
        )
      }
      case "q5":
        return (
          <>
            <h2 className="qt">
              {text?.title ?? "Dalam 1–4 bulan terakhir, pernah…?"}
            </h2>
            <p className="qh">{text?.hint ?? "Pilih semua yang sesuai"}</p>
            <Options
              multi
              layout="tiles"
              selected={a.eco}
              onPick={(i) => pick("eco", i, true)}
              options={flow.eco
                .filter((o) => visible(o, a, flow))
                .map((o) => ({ ...o, cls: tileCls(o) }))}
            />
          </>
        )
      case "q6":
        return <StepDrugs flow={flow} a={a} set={set} />
      case "q7":
        return (
          <>
            {flow.vitals.includes("temp") && (
              <StepTemp
                flow={flow}
                a={a}
                set={set}
                pick={(i) => pick("vital_proxy", i, true)}
              />
            )}
            {flow.vitals.includes("bp") && (
              <StepBp
                flow={flow}
                a={a}
                set={set}
                pick={(i) => pick("vital_proxy", i, true)}
              />
            )}
          </>
        )
      case "labs":
        return (
          <StepLabs title={text?.title} hint={text?.hint} a={a} set={set} />
        )
      case "q8":
        return <StepBmi flow={flow} a={a} set={set} setModal={setModal} />
      case "q9":
        return <StepBody flow={flow} a={a} set={set} />
    }
  })()

  return (
    <QuizFrame
      flow={flow}
      stage={STAGE_OF[id]}
      say={def.say}
      mascotRef={mascot}
      onHome={home}
      overlay={modal}
      foot={
        <>
          <BackButton onClick={back} />
          <button
            type="button"
            className={`btn big ${def.nextCls?.(a, flow) ?? "btn-primary"}`}
            disabled={!valid || busy}
            onClick={next}
          >
            {busy ? "Sebentar…" : nextLabel}
          </button>
        </>
      }
    >
      <Card tab={def.tab} className="pop" key={id}>
        {body}
      </Card>
    </QuizFrame>
  )
}

/** "‹ Kembali" on the left of Lanjut in .foot. */
export function BackButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      type="button"
      className="btn btn-back"
      aria-label="Kembali"
      onClick={onClick}
    >
      <span className="bb-ico" aria-hidden="true">
        ‹
      </span>
      <span className="bb-txt">Kembali</span>
    </button>
  )
}

/** Quiz layout: HUD (home + stage map), mascot bubble, one card, footer. */
export function QuizFrame({
  flow,
  stage,
  say,
  mascotRef,
  onHome,
  foot,
  overlay,
  children,
}: {
  flow: FlowPublic
  stage: number
  say: string
  mascotRef?: Ref<SVGSVGElement>
  onHome: () => void
  foot: ReactNode
  overlay?: ReactNode
  children: ReactNode
}) {
  return (
    <div className="screen bg-quiz">
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
        <StageMap stages={flow.stages} current={stage} />
      </div>
      <div className="qlayout">
        <div className="mrow">
          <Mascot ref={mascotRef} className="m-sm" />
          <div className="bubble">
            <p>
              <Rich text={say} />
            </p>
          </div>
        </div>
        <div className="qmain">
          <div className="qwrap">{children}</div>
          <div className="foot">{foot}</div>
        </div>
      </div>
      {overlay}
    </div>
  )
}

type Setter = (patch: Partial<QuizAnswers>) => void

function StepWho({
  flow,
  a,
  pick,
  set,
}: {
  flow: FlowPublic
  a: QuizAnswers
  pick: (key: "who" | "sex", id: string, multi: boolean) => void
  set: Setter
}) {
  return (
    <>
      <h2 className="qt">Siapa yang sedang sakit?</h2>
      <p className="qh">Pilih satu</p>
      <Options
        layout="tiles"
        selected={a.who ? [a.who] : []}
        onPick={(i) => pick("who", i, false)}
        options={flow.who}
      />
      <div className="frow">
        <label className="fld age">
          <span>Usia (tahun)</span>
          <div className="inp age">
            <input
              inputMode="numeric"
              maxLength={3}
              placeholder="25"
              value={a.age}
              onChange={(e) => {
                const age = e.target.value.replace(/\D/g, "").slice(0, 3)
                set(prune({ ...a, age }, flow))
              }}
            />
            <em>th</em>
          </div>
        </label>
        <div className="fld">
          <span id="sexLbl">Jenis kelamin</span>
          <fieldset className="seg" aria-labelledby="sexLbl">
            {flow.sex.map((o) => (
              <button
                key={o.id}
                type="button"
                aria-pressed={a.sex === o.id}
                className={a.sex === o.id ? "on" : ""}
                onClick={() => pick("sex", o.id, false)}
              >
                {o.text}
              </button>
            ))}
          </fieldset>
        </div>
      </div>
      {/* Max 3 fields at once: the pregnancy question appears only after who,
          age, and sex are filled. */}
      {!!a.who && asksPregnancy(a, flow) && (
        <div className="fld reveal-in mt-field">
          <span id="pregLbl">Sedang hamil?</span>
          <fieldset className="seg" aria-labelledby="pregLbl">
            {[
              { v: true, label: "Hamil" },
              { v: false, label: "Tidak hamil" },
            ].map((o) => (
              <button
                key={o.label}
                type="button"
                aria-pressed={a.pregnant === o.v}
                className={a.pregnant === o.v ? "on" : ""}
                onClick={() => {
                  set({ pregnant: o.v })
                  sfx.tap()
                }}
              >
                {o.label}
              </button>
            ))}
          </fieldset>
        </div>
      )}
    </>
  )
}

function StepDrugs({
  flow,
  a,
  set,
}: {
  flow: FlowPublic
  a: QuizAnswers
  set: Setter
}) {
  return (
    <>
      <h2 className="qt">Obat apa yang sudah diminum?</h2>
      <p className="qh">Opsional · ketuk atau ketik</p>
      <div className="inp">
        <textarea
          aria-label="Obat yang sudah diminum"
          placeholder="mis. Paracetamol, Loperamide…"
          maxLength={500}
          value={a.drugs}
          onChange={(e) => set({ drugs: e.target.value })}
        />
      </div>
      <div className="chips">
        {flow.drug_chips.map((d) => (
          <button
            key={d}
            type="button"
            className="chip"
            onClick={() => {
              const v = a.drugs.trim()
              set({ drugs: v ? `${v.replace(/[,\s]+$/, "")}, ${d}` : d })
              sfx.tap()
            }}
          >
            + {d}
          </button>
        ))}
      </div>
    </>
  )
}

function tempStatus(t: number): [string, string, string] {
  if (Number.isNaN(t)) return ["Masukkan suhu", "#EEE", "#555"]
  if (t < 34 || t > 43) return ["Angka tidak wajar", "#FFE3E6", "#C8102E"]
  if (t < 37.5) return ["😊 Normal", "#E2F9EE", "#15784F"]
  if (t < 38) return ["🙂 Subfebris", "#FFF6DB", "#8A5A00"]
  if (t < 39.5) return ["🤒 Demam", "#FFE8D6", "#A3410A"]
  return ["🥵 Demam tinggi", "#FFE3E6", "#C8102E"]
}

/** Stand-in questions when there is no device (DR no. 1, Blueprint Q6). */
function ProxyQuestions({
  flow,
  vital,
  a,
  pick,
}: {
  flow: FlowPublic
  vital: Vital
  a: QuizAnswers
  pick: (id: string) => void
}) {
  const opts = flow.vital_proxies?.[vital]
  if (!opts?.length) return null
  return (
    <>
      <h3 className="subq">Kalau begitu, ada tanda ini?</h3>
      <Options multi selected={a.vital_proxy} onPick={pick} options={opts} />
    </>
  )
}

function StepTemp({
  flow,
  a,
  set,
  pick,
}: {
  flow: FlowPublic
  a: QuizAnswers
  set: Setter
  pick: (id: string) => void
}) {
  const t = num(a.temp)
  const pct = Number.isNaN(t)
    ? 30
    : Math.max(5, Math.min(100, ((t - 34) / 9) * 100))
  const [txt, bg, color] = tempStatus(t)
  const stepBy = (d: number) => {
    let v = num(a.temp)
    if (Number.isNaN(v)) v = 37
    v = Math.max(34, Math.min(43, Math.round((v + d) * 10) / 10))
    set({ temp: v.toFixed(1).replace(".", ",") })
    sfx.tap()
  }
  return (
    <>
      <h2 className="qt">Berapa suhu tubuhmu?</h2>
      <p className="qh">Dalam °C</p>
      <div className={`thermo ${a.no_thermo ? "is-off" : ""}`}>
        <div className="tbar" aria-hidden="true">
          <div className="tube">
            <div className="tfill" style={{ height: `${pct}%` }} />
          </div>
          <div className="bulb" />
        </div>
        <div className="tctl">
          <div className="tval">
            <button
              type="button"
              className="rbtn"
              onClick={() => stepBy(-0.1)}
              aria-label="Kurangi"
            >
              −
            </button>
            <div className="inp">
              <input
                inputMode="decimal"
                placeholder="37,0"
                aria-label="Suhu tubuh dalam derajat Celsius"
                value={a.temp}
                disabled={a.no_thermo}
                onChange={(e) => set({ temp: e.target.value.slice(0, 5) })}
              />
            </div>
            <button
              type="button"
              className="rbtn"
              onClick={() => stepBy(0.1)}
              aria-label="Tambah"
            >
              +
            </button>
          </div>
          <div className="stat-row">
            <span className="tstat" style={{ background: bg, color }}>
              {txt}
            </span>
          </div>
        </div>
      </div>
      <label className="chk">
        <input
          type="checkbox"
          checked={a.no_thermo}
          onChange={(e) => {
            set({ no_thermo: e.target.checked })
            sfx.tap()
          }}
        />{" "}
        Saya tidak punya termometer
      </label>
      {a.no_thermo && (
        <>
          <div className="note">
            <Rich text={noThermoNote(a)} />
          </div>
          <ProxyQuestions flow={flow} vital="temp" a={a} pick={pick} />
        </>
      )}
    </>
  )
}

/** Blood pressure label. Same cut-offs as backend/app/domain/vitals.py
 * bp_category (DR 2026-10-15): Normal (sys ≤ 120) · Meningkat (120 < sys < 140
 * and dia < 90) · Tinggi (sys ≥ 140 or dia ≥ 90) · Sangat tinggi (sys > 160). */
function bpStatus(sys: number, dia: number): [string, string, string] {
  if (Number.isNaN(sys) || Number.isNaN(dia))
    return ["Masukkan tensi", "#EEE", "#555"]
  if (!sysValid(sys) || !diaValid(dia))
    return ["Angka tidak wajar", "#FFE3E6", "#C8102E"]
  if (sys > 160) return ["Sangat tinggi", "#FFE3E6", "#C8102E"]
  if (sys >= 140 || dia >= 90) return ["Tinggi", "#FFE8D6", "#A3410A"]
  if (sys > 120) return ["Meningkat", "#FFF6DB", "#8A5A00"]
  return ["Normal", "#E2F9EE", "#15784F"]
}

function StepBp({
  flow,
  a,
  set,
  pick,
}: {
  flow: FlowPublic
  a: QuizAnswers
  set: Setter
  pick: (id: string) => void
}) {
  const [txt, bg, color] = bpStatus(num(a.bp_sys), num(a.bp_dia))
  const g = num(a.glucose)
  // Max 3 fields per page: the blood-sugar field appears once BP is done.
  const bpDone = a.no_bp || (sysValid(num(a.bp_sys)) && diaValid(num(a.bp_dia)))
  const digits = (v: string) => v.replace(/\D/g, "").slice(0, 3)
  return (
    <>
      <h2 className="qt">Berapa tensi darahmu?</h2>
      <p className="qh">Dalam mmHg, mis. 120/80</p>
      {!a.no_bp && (
        <div>
          <div className="two">
            <label className="fld">
              <span>Sistolik (atas)</span>
              <div className="inp">
                <input
                  inputMode="numeric"
                  placeholder="120"
                  maxLength={3}
                  value={a.bp_sys}
                  disabled={a.no_bp}
                  onChange={(e) => set({ bp_sys: digits(e.target.value) })}
                />
                <em>mmHg</em>
              </div>
            </label>
            <label className="fld">
              <span>Diastolik (bawah)</span>
              <div className="inp">
                <input
                  inputMode="numeric"
                  placeholder="80"
                  maxLength={3}
                  value={a.bp_dia}
                  disabled={a.no_bp}
                  onChange={(e) => set({ bp_dia: digits(e.target.value) })}
                />
                <em>mmHg</em>
              </div>
            </label>
          </div>
          <div className="stat-row">
            <span className="tstat" style={{ background: bg, color }}>
              {txt}
            </span>
          </div>
        </div>
      )}
      <label className="chk">
        <input
          type="checkbox"
          checked={a.no_bp}
          onChange={(e) => {
            set({ no_bp: e.target.checked })
            sfx.tap()
          }}
        />{" "}
        Saya tidak punya alat tensi
      </label>
      {a.no_bp && <ProxyQuestions flow={flow} vital="bp" a={a} pick={pick} />}
      {flow.vitals.includes("glucose") && bpDone && (
        <label className="fld reveal-in mt-field">
          <span>Gula darah sewaktu (opsional)</span>
          <small className="fhint">diukur kapan saja, tidak perlu puasa</small>
          <div className="inp">
            <input
              inputMode="decimal"
              placeholder="mis. 110"
              maxLength={4}
              value={a.glucose}
              onChange={(e) =>
                set({ glucose: e.target.value.replace(/[^\d.,]/g, "") })
              }
            />
            <em>mg/dL</em>
          </div>
          {a.glucose.trim() && !glucoseValid(g) && (
            <div className="note">Angka gula darah tidak wajar.</div>
          )}
          {glucoseValid(g) && g >= GLUCOSE_HIGH_FROM && (
            <div className="stat-row">
              <span
                className="tstat"
                style={{ background: "#FFE8D6", color: "#A3410A" }}
              >
                Tinggi
              </span>
            </div>
          )}
        </label>
      )}
    </>
  )
}

/** Optional lab results (chronic path): uric acid and total cholesterol.
 * Recorded only; thresholds need DR, weights need ST (both 0 for now). */
function StepLabs({
  title,
  hint,
  a,
  set,
}: {
  title?: string | null
  hint?: string | null
  a: QuizAnswers
  set: Setter
}) {
  const clean = (v: string) => v.replace(/[^\d.,]/g, "").slice(0, 5)
  const uric = num(a.uric_acid)
  const chol = num(a.cholesterol_total)
  return (
    <>
      <h2 className="qt">{title ?? "Pemeriksaan opsional"}</h2>
      <p className="qh">
        {hint ?? "Isi dari hasil cek terakhir. Kosongkan kalau tidak ada."}
      </p>
      <label className="fld">
        <span>Asam urat (opsional)</span>
        <div className="inp">
          <input
            inputMode="decimal"
            placeholder="mis. 6,5"
            value={a.uric_acid}
            onChange={(e) => set({ uric_acid: clean(e.target.value) })}
          />
          <em>mg/dL</em>
        </div>
        {a.uric_acid.trim() && !uricValid(uric) && (
          <div className="note">Angka asam urat tidak wajar (1–30 mg/dL).</div>
        )}
      </label>
      <label className="fld mt-field">
        <span>Kolesterol total (opsional)</span>
        <div className="inp">
          <input
            inputMode="decimal"
            placeholder="mis. 190"
            value={a.cholesterol_total}
            onChange={(e) => set({ cholesterol_total: clean(e.target.value) })}
          />
          <em>mg/dL</em>
        </div>
        {a.cholesterol_total.trim() && !cholesterolValid(chol) && (
          <div className="note">
            Angka kolesterol tidak wajar (50–600 mg/dL).
          </div>
        )}
      </label>
    </>
  )
}

function StepBmi({
  flow,
  a,
  set,
  setModal,
}: {
  flow: FlowPublic
  a: QuizAnswers
  set: Setter
  setModal: (m: ReactNode) => void
}) {
  const b = bmiOf(a)
  const proxy = flow.nutrition_proxies.find((p) => p.id === a.nutrition_proxy)
  const openProxy = () => {
    sfx.tap()
    const close = () => setModal(null)
    setModal(
      <Modal tone="yellow" tab="PROKSI GIZI" onClose={close}>
        <h3>
          Tidak apa-apa! 😊
          <br />
          Secara fisik, apakah Anda merasa:
        </h3>
        <Options
          selected={a.nutrition_proxy ? [a.nutrition_proxy] : []}
          options={flow.nutrition_proxies}
          onPick={(id) => {
            set({ nutrition_proxy: id as QuizAnswers["nutrition_proxy"] })
            sfx.tap()
            close()
          }}
        />
      </Modal>,
    )
  }
  return (
    <>
      <h2 className="qt">Tinggi & berat badanmu?</h2>
      <p className="qh">Dipakai untuk memperkirakan status gizi</p>
      <div className="two">
        <label className="fld">
          <span>Tinggi Badan</span>
          <div className="inp">
            <input
              inputMode="decimal"
              placeholder="160"
              maxLength={5}
              value={a.height}
              onChange={(e) => set({ height: e.target.value })}
            />
            <em>cm</em>
          </div>
        </label>
        <label className="fld">
          <span>Berat Badan</span>
          <div className="inp">
            <input
              inputMode="decimal"
              placeholder="55"
              maxLength={5}
              value={a.weight}
              onChange={(e) => set({ weight: e.target.value })}
            />
            <em>kg</em>
          </div>
        </label>
      </div>
      {flow.measure_waist && (
        <label className="fld mt-tight">
          <span>Lingkar perut / pinggang (opsional)</span>
          <div className="inp">
            <input
              inputMode="decimal"
              placeholder="85"
              maxLength={5}
              value={a.waist}
              onChange={(e) => set({ waist: e.target.value })}
            />
            <em>cm</em>
          </div>
        </label>
      )}
      <button
        type="button"
        className={`opt mt-tight ${a.nutrition_proxy && !b ? "on" : ""}`}
        onClick={openProxy}
      >
        <span className="oe" aria-hidden="true">
          🤷
        </span>
        <span className="ot">
          {flow.measure_waist
            ? "Tidak tahu / tak punya timbangan atau meteran"
            : "Tidak tahu / tak punya timbangan"}
          {proxy && (
            <span className="od">Jawaban pengganti: {proxy.text} · ubah</span>
          )}
        </span>
        <span className="ck" />
      </button>
    </>
  )
}

function StepBody({
  flow,
  a,
  set,
}: {
  flow: FlowPublic
  a: QuizAnswers
  set: Setter
}) {
  const sel = flow.body_regions.filter((b) => a.body.includes(b.id))
  return (
    <>
      <h2 className="qt">Ketuk bagian yang sakit/bengkak</h2>
      <p className="qh">Boleh lebih dari satu</p>
      <div className="bodywrap">
        <div className="bodysvg">
          <BodyMap
            regions={flow.body_regions}
            selected={a.body}
            onToggle={(id) => {
              const body = a.body.includes(id)
                ? a.body.filter((x) => x !== id)
                : [...a.body, id]
              set({ body, pain: body.length ? a.pain : null })
              sfx.tap()
              vibrate()
            }}
          />
        </div>
        <div className="bside">
          <div className="sel-list">
            {sel.length ? (
              sel.map((b) => <span key={b.id}>{b.name}</span>)
            ) : (
              <div className="empty">
                Belum ada. Tidak ada yang sakit? Langsung lanjut.
              </div>
            )}
          </div>
          {sel.length > 0 && (
            <div className="pain">
              <p className="pq">Seberapa nyeri? Ketuk angka atau wajah</p>
              <PainScale
                faces={flow.pain_faces}
                value={a.pain}
                onPick={(v) => {
                  set({ pain: v })
                  sfx.tap()
                  vibrate()
                }}
              />
            </div>
          )}
        </div>
      </div>
    </>
  )
}
