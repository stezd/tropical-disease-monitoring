import { Link } from "@tanstack/react-router"

import { Logo } from "@/components/Common/Logo"
import { Mascot } from "@/features/triage/components/Art"

interface AuthLayoutProps {
  children: React.ReactNode
}

// Login, sign up, password reset in the TropiCare look: purple sky, white card.
export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-svh flex-col items-center bg-[linear-gradient(180deg,#4B44C4_0%,#6E4FDB_34%,#A85ED0_64%,#F07F9A_88%,#FFAE7E_100%)] px-4 py-6">
      <div className="flex w-full max-w-sm items-center justify-between">
        <Link
          to="/"
          className="grid size-10 place-items-center rounded-[13px] bg-white/20 text-2xl font-extrabold text-white"
          aria-label="Kembali ke beranda"
        >
          ‹
        </Link>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center gap-2 w-full max-w-sm">
        <div className="w-24">
          <Mascot />
        </div>
        <div className="w-full rounded-[26px] bg-white p-6 shadow-[0_8px_0_rgba(60,40,150,.22),0_22px_44px_rgba(30,15,90,.28)]">
          <div className="mb-4 flex justify-center">
            <Logo asLink={false} />
          </div>
          {children}
        </div>
        <p className="mt-2 text-center text-xs font-extrabold text-white">
          Masuk itu opsional. Skrining tetap bisa dipakai tanpa akun.
        </p>
      </div>
    </div>
  )
}
