import { useQuery } from "@tanstack/react-query"

import {
  type Answers,
  type FlowPublic,
  type ScoreResult,
  TriageService,
} from "@/client"
import snapshot from "./content.snapshot.json"

export const FLOW_ID = "infection"

// Offline copy written by scripts/generate-client.sh. Lets stage 1 and the red
// screen work even when the server is down.
const OFFLINE = snapshot as unknown as Record<string, FlowPublic>

export function useFlow(flowId = FLOW_ID) {
  const query = useQuery({
    queryKey: ["triage", "flow", flowId],
    queryFn: async () =>
      (await TriageService.readFlow({ path: { flow_id: flowId } })).data,
    staleTime: 60 * 60 * 1000,
    retry: 1,
  })
  const flow = query.data ?? (query.isError ? OFFLINE[flowId] : undefined)
  return { flow, offline: !query.data && query.isError, query }
}

/** Score answers. `preview` = rules only, never a model call: for mid-quiz
 * checks such as the drug pop-ups after step q6. The final result (Thinking,
 * Result) uses the server's configured engine. */
export async function scoreAnswers(
  answers: Answers,
  flowId: string,
  preview = false,
): Promise<ScoreResult> {
  return (
    await TriageService.scoreFlow({
      path: { flow_id: flowId },
      body: answers,
      ...(preview ? { query: { preview: true } } : {}),
    })
  ).data
}

/** Query key for the final result (shared by Thinking and Result). */
export const scoreKey = (answers: Answers, flowId: string) => [
  "triage",
  "score",
  flowId,
  answers,
]

/** Separate key for rule-only previews, so they never stand in for the result. */
export const previewKey = (answers: Answers, flowId: string) => [
  "triage",
  "preview",
  flowId,
  answers,
]
