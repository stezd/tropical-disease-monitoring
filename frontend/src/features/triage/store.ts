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
}

const KEY = "tropicek_quiz"
const listeners = new Set<() => void>()

const fresh = (flowId = "infection"): QuizState => ({
  flowId,
  answers: blankAnswers(),
  step: 0,
  phase: "privacy",
  consented: false,
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
