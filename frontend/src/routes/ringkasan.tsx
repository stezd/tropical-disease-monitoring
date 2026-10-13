import { createFileRoute } from "@tanstack/react-router"

import { SummaryPage } from "@/features/triage/Shell"

export const Route = createFileRoute("/ringkasan")({
  component: SummaryPage,
  head: () => ({ meta: [{ title: "Rangkuman Pasien – TropiCek" }] }),
})
