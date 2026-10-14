import { createFileRoute } from "@tanstack/react-router"

import { PrivacyPage } from "@/features/triage/Shell"

export const Route = createFileRoute("/privasi")({
  component: PrivacyPage,
  head: () => ({ meta: [{ title: "Privasi – TropiCare" }] }),
})
