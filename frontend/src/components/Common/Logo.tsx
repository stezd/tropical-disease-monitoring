import { Link } from "@tanstack/react-router"

import { cn } from "@/lib/utils"

interface LogoProps {
  variant?: "full" | "icon" | "responsive"
  className?: string
  asLink?: boolean
}

function Wordmark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "font-heading text-2xl font-bold tracking-wide text-[#0B524E]",
        className,
      )}
    >
      Tropi<span className="text-[#0F6B66]">Care</span>
    </span>
  )
}

function Icon({ className }: { className?: string }) {
  return (
    <img
      src="/favicon.svg"
      alt="TropiCare"
      className={cn("size-8", className)}
    />
  )
}

export function Logo({
  variant = "full",
  className,
  asLink = true,
}: LogoProps) {
  const content =
    variant === "responsive" ? (
      <>
        <Wordmark
          className={cn("group-data-[collapsible=icon]:hidden", className)}
        />
        <Icon
          className={cn(
            "hidden group-data-[collapsible=icon]:block",
            className,
          )}
        />
      </>
    ) : variant === "icon" ? (
      <Icon className={className} />
    ) : (
      <Wordmark className={className} />
    )

  if (!asLink) return content
  return <Link to="/">{content}</Link>
}
