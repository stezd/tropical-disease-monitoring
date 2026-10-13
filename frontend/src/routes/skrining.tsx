import { createFileRoute } from "@tanstack/react-router"

import { ScreeningPage } from "@/features/triage/Shell"

export const Route = createFileRoute("/skrining")({
  component: ScreeningPage,
  head: () => ({ meta: [{ title: "Skrining – TropiCare" }] }),
})
