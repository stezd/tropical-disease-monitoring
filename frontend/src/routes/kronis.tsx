import { createFileRoute } from "@tanstack/react-router"

import { ChronicPage } from "@/features/triage/Shell"

export const Route = createFileRoute("/kronis")({
  component: ChronicPage,
  head: () => ({ meta: [{ title: "Risiko Jangka Panjang – TropiCek" }] }),
})
