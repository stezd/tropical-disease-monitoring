import { Link } from "@tanstack/react-router"

import { Logo } from "@/components/Common/Logo"
import { Mascot } from "@/features/triage/components/Art"

interface AuthLayoutProps {
  children: React.ReactNode
}

// Login, sign up, password reset in the TropiCare look: teal backdrop, white card.
export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-svh flex-col items-center bg-[radial-gradient(ellipse_at_50%_0%,#E4F4F1_0,#CDE8E3_62%)] px-4 py-6">
      <div className="flex w-full max-w-sm items-center justify-between">
        <Link
          to="/"
          className="grid size-10 place-items-center rounded-full border border-[#E1EDEA] bg-white text-2xl font-semibold text-[#0F6B66] shadow-[0_6px_20px_rgba(15,107,102,.08)]"
          aria-label="Kembali ke beranda"
        >
          ‹
        </Link>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center gap-2 w-full max-w-sm">
        <div className="w-24">
          <Mascot />
        </div>
        <div className="w-full rounded-[26px] border border-[#E1EDEA] bg-white p-6 shadow-[0_6px_20px_rgba(15,107,102,.08)]">
          <div className="mb-4 flex justify-center">
            <Logo asLink={false} />
          </div>
          {children}
        </div>
        <p className="mt-2 text-center text-xs font-semibold text-[#15323A]">
          Masuk itu opsional. Skrining tetap bisa dipakai tanpa akun.
        </p>
      </div>
    </div>
  )
}
