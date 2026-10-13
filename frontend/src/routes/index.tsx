import { createFileRoute } from "@tanstack/react-router"

import { HomePage } from "@/features/triage/Shell"

export const Route = createFileRoute("/")({
  component: HomePage,
  head: () => ({ meta: [{ title: "TropiCek – Skrining Penyakit Tropis" }] }),
})
