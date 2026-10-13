import { keepPreviousData, useQuery } from "@tanstack/react-query"
import { useEffect, useState } from "react"

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

export async function scoreAnswers(
  answers: Answers,
  flowId = FLOW_ID,
): Promise<ScoreResult> {
  return (
    await TriageService.scoreFlow({ path: { flow_id: flowId }, body: answers })
  ).data
}

export const scoreKey = (answers: Answers, flowId = FLOW_ID) => [
  "triage",
  "score",
  flowId,
  answers,
]

function useDebounced<T>(value: T, ms: number): T {
  const [v, setV] = useState(value)
  useEffect(() => {
    const t = setTimeout(() => setV(value), ms)
    return () => clearTimeout(t)
  }, [value, ms])
  return v
}

/** Live score for the mascot meter. Silent when the server is unreachable.
 * Only runs once a complaint is chosen and no red flag is picked. */
export function useLiveScore(answers: Answers) {
  const debounced = useDebounced(answers, 250)
  const enabled =
    !!debounced.complaint &&
    !(debounced.red_flags ?? []).some((x) => x !== "none")
  return useQuery({
    queryKey: scoreKey(debounced),
    queryFn: () => scoreAnswers(debounced),
    enabled,
    placeholderData: keepPreviousData,
    staleTime: Number.POSITIVE_INFINITY,
    retry: false,
  })
}
