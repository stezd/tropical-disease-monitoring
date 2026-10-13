// Quiz progress for the current tab. sessionStorage only, so a refresh keeps the
// answers but closing the tab clears them. Nothing goes to the server until the
// patient asks for a score or agrees to save.
import { useSyncExternalStore } from "react"

import { blankAnswers, type QuizAnswers } from "./model"

export type Phase = "quiz" | "red" | "thinking" | "result"

export type QuizState = {
  answers: QuizAnswers
  step: number
  phase: Phase
}

const KEY = "tropicek_quiz"
const listeners = new Set<() => void>()

const fresh = (): QuizState => ({
  answers: blankAnswers(),
  step: 0,
  phase: "quiz",
})

function read(): QuizState {
  try {
    const raw = sessionStorage.getItem(KEY)
    if (!raw) return fresh()
    const s = JSON.parse(raw) as QuizState
    return { ...fresh(), ...s, answers: { ...blankAnswers(), ...s.answers } }
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
  reset: () => write(fresh()),
}

export function useQuiz(): QuizState {
  return useSyncExternalStore((l) => {
    listeners.add(l)
    return () => listeners.delete(l)
  }, quiz.get)
}
