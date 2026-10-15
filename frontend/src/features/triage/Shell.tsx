import { useNavigate } from "@tanstack/react-router"
import { type ReactNode, useCallback, useEffect } from "react"

import type { FlowPublic } from "@/client"
import { useFlow } from "./api"
import { Mascot } from "./components/Art"
import { ToastHost } from "./components/Ui"
import { hasRedFlag, steps } from "./model"
import { ConsentScreen } from "./screens/Consent"
import { HistoryScreen } from "./screens/History"
import { HomeScreen } from "./screens/Home"
import { PrivacyScreen } from "./screens/Privacy"
import { QuizScreen } from "./screens/Quiz"
import { RedScreen } from "./screens/Red"
import { ResultScreen } from "./screens/Result"
import { SummaryScreen } from "./screens/Summary"
import { ThinkingScreen } from "./screens/Thinking"
import { quiz, useQuiz } from "./store"

/** Full-screen frame for every TropiCare screen (replaces the prototype's #phone). */
export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="tc-app">
      {children}
      <ToastHost />
    </div>
  )
}

export function Loading() {
  return (
    <div className="screen bg-quiz">
      <div className="loading" role="status" aria-live="polite">
        <Mascot className="m-load" />
        <p className="footdisc">Kak Tropi sedang bersiap…</p>
      </div>
    </div>
  )
}

function WithFlow({
  flowId,
  children,
}: {
  flowId: string
  children: (flow: FlowPublic) => ReactNode
}) {
  const { flow } = useFlow(flowId)
  if (!flow) return <Loading />
  return <>{children(flow)}</>
}

export function HomePage() {
  return (
    <Shell>
      <HomeScreen />
    </Shell>
  )
}

export function PrivacyPage() {
  return (
    <Shell>
      <PrivacyScreen />
    </Shell>
  )
}

export function HistoryPage() {
  return (
    <Shell>
      <HistoryScreen />
    </Shell>
  )
}

export function SummaryPage() {
  return (
    <Shell>
      <SummaryScreen />
    </Shell>
  )
}

/** The quiz for one flow: "infection" (/skrining) or "chronic" (/kronis). */
export function ScreeningPage({ flowId }: { flowId: string }) {
  const navigate = useNavigate()
  const { phase, answers, flowId: current } = useQuiz()
  // Answers from the other path must not leak into this one.
  useEffect(() => {
    if (current !== flowId) quiz.reset(flowId)
  }, [current, flowId])
  const restart = useCallback(() => {
    quiz.reset()
  }, [])
  const home = useCallback(() => navigate({ to: "/" }), [navigate])
  const toResult = useCallback(() => quiz.set({ phase: "result" }), [])
  const toQuiz = useCallback(() => quiz.set({ phase: "quiz" }), [])

  if (current !== flowId) {
    return (
      <Shell>
        <Loading />
      </Shell>
    )
  }

  return (
    <Shell>
      <WithFlow flowId={flowId}>
        {(flow) => {
          switch (phase) {
            case "red":
              // Back goes to the question that raised the danger sign: stage 1,
              // or the companion question (e.g. very yellow eyes with fever).
              // Looked up by id, so it stays right when the step list changes.
              return (
                <RedScreen
                  flow={flow}
                  answers={answers}
                  onBack={() => {
                    const list = steps(answers, flow)
                    const at = list.indexOf(hasRedFlag(answers) ? "q1" : "q4")
                    quiz.set({
                      phase: "quiz",
                      step: at >= 0 ? at : Math.max(0, list.indexOf("q1")),
                    })
                  }}
                  onRestart={restart}
                />
              )
            case "thinking":
              return (
                <ThinkingScreen
                  flow={flow}
                  answers={answers}
                  onDone={toResult}
                  onBack={toQuiz}
                />
              )
            case "result":
              return (
                <ResultScreen
                  flow={flow}
                  answers={answers}
                  onHome={home}
                  onRestart={restart}
                />
              )
            case "privacy":
              return <ConsentScreen flow={flow} />
            default:
              return <QuizScreen flow={flow} />
          }
        }}
      </WithFlow>
    </Shell>
  )
}
