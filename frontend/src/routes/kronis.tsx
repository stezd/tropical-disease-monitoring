import { createFileRoute } from "@tanstack/react-router"

import { ScreeningPage } from "@/features/triage/Shell"

export const Route = createFileRoute("/kronis")({
  component: () => <ScreeningPage flowId="chronic" />,
  head: () => ({ meta: [{ title: "Risiko Jangka Panjang – TropiCare" }] }),
})
