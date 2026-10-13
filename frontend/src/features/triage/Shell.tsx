import { useNavigate } from "@tanstack/react-router"
import { type ReactNode, useCallback } from "react"

import type { FlowPublic } from "@/client"
import { useFlow } from "./api"
import { Mascot } from "./components/Art"
import { ToastHost } from "./components/Ui"
import { ChronicScreen } from "./screens/Chronic"
import { HomeScreen } from "./screens/Home"
import { QuizScreen } from "./screens/Quiz"
import { RedScreen } from "./screens/Red"
import { ResultScreen } from "./screens/Result"
import { SummaryScreen } from "./screens/Summary"
import { ThinkingScreen } from "./screens/Thinking"
import { quiz, useQuiz } from "./store"

/** Full-screen frame for every TropiCek screen (replaces the prototype's #phone). */
export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="tc-app">
      {children}
      <ToastHost />
    </div>
  )
}

function WithFlow({ children }: { children: (flow: FlowPublic) => ReactNode }) {
  const { flow } = useFlow()
  if (!flow) {
    return (
      <div className="screen bg-quiz">
        <div className="think" style={{ justifyContent: "center" }}>
          <Mascot className="m-think" />
          <p className="footdisc">Kak Tropi sedang bersiap…</p>
        </div>
      </div>
    )
  }
  return <>{children(flow)}</>
}

export function HomePage() {
  return (
    <Shell>
      <HomeScreen />
    </Shell>
  )
}

export function ChronicPage() {
  return (
    <Shell>
      <ChronicScreen />
    </Shell>
  )
}

export function SummaryPage() {
  return (
    <Shell>
      <WithFlow>{(flow) => <SummaryScreen flow={flow} />}</WithFlow>
    </Shell>
  )
}

export function ScreeningPage() {
  const navigate = useNavigate()
  const { phase, answers } = useQuiz()
  const restart = useCallback(() => {
    quiz.reset()
  }, [])
  const home = useCallback(() => navigate({ to: "/" }), [navigate])
  const toResult = useCallback(() => quiz.set({ phase: "result" }), [])
  const toQuiz = useCallback(() => quiz.set({ phase: "quiz" }), [])

  return (
    <Shell>
      <WithFlow>
        {(flow) => {
          switch (phase) {
            case "red":
              // Back goes to stage 1 (the red-flag question).
              return (
                <RedScreen
                  flow={flow}
                  answers={answers}
                  onBack={() => quiz.set({ phase: "quiz", step: 1 })}
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
            default:
              return <QuizScreen flow={flow} />
          }
        }}
      </WithFlow>
    </Shell>
  )
}
