import { createFileRoute, redirect } from "@tanstack/react-router"

import { HistoryPage } from "@/features/triage/Shell"
import { isLoggedIn } from "@/hooks/useAuth"

export const Route = createFileRoute("/riwayat")({
  component: HistoryPage,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({ to: "/login", search: { redirect: "/riwayat" } })
    }
  },
  head: () => ({ meta: [{ title: "Riwayat Skrining – TropiCare" }] }),
})
