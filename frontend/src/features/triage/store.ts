// Quiz progress for the current tab. sessionStorage only, so a refresh keeps the
// answers but closing the tab clears them. Nothing goes to the server until the
// patient asks for a score or (logged in) saves it to their history.
import { useSyncExternalStore } from "react"

import { blankAnswers, type QuizAnswers } from "./model"

// "privacy" is the consent gate shown before the first question.
export type Phase = "privacy" | "quiz" | "red" | "thinking" | "result"

export type QuizState = {
  // Which flow these answers belong to ("infection" or "chronic").
  flowId: string
  answers: QuizAnswers
  step: number
  phase: Phase
  // Ticked "Saya setuju" at the privacy gate (kept when going back to it).
  consented: boolean
  // Random id of this quiz run. Sent with the de-identified stats row so the
  // server counts one run once, even if the result page is opened twice.
  runId: string
}

// randomUUID needs a secure context (https or localhost); the server wants a UUID.
const newRunId = () =>
  typeof crypto.randomUUID === "function"
    ? crypto.randomUUID()
    : "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
        (
          Number(c) ^
          (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (Number(c) / 4)))
        ).toString(16),
      )

const KEY = "tropicek_quiz"
const listeners = new Set<() => void>()

const fresh = (flowId = "infection"): QuizState => ({
  flowId,
  answers: blankAnswers(),
  step: 0,
  phase: "privacy",
  consented: false,
  runId: newRunId(),
})

function read(): QuizState {
  try {
    const raw = sessionStorage.getItem(KEY)
    if (!raw) return fresh()
    const s = JSON.parse(raw) as QuizState
    const next = {
      ...fresh(),
      ...s,
      answers: { ...blankAnswers(), ...s.answers },
      // A session saved by an older version has no runId.
      runId: s.runId ?? newRunId(),
    }
    // No question before consent, even for a session saved by an older version.
    return next.consented ? next : { ...next, phase: "privacy" }
  } catch {
    return fresh()
  }
}

let state = read()

function write(next: QuizState) {
  state = next
  try {
    sessionStorage.setItem(KEY, JSON.stringify(next))
  } catch {
    // Private mode: keep in memory only.
  }
  for (const l of listeners) l()
}

export const quiz = {
  get: () => state,
  set: (patch: Partial<QuizState>) => write({ ...state, ...patch }),
  answer: (fn: (a: QuizAnswers) => QuizAnswers) =>
    write({ ...state, answers: fn(state.answers) }),
  reset: (flowId = state.flowId) => write(fresh(flowId)),
}

export function useQuiz(): QuizState {
  return useSyncExternalStore((l) => {
    listeners.add(l)
    return () => listeners.delete(l)
  }, quiz.get)
}
