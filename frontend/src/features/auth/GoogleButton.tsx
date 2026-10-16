// "Masuk dengan Google" via Google Identity Services. Google gives us an ID
// token; POST /login/google checks it and returns our own JWT, stored like a
// normal login. Hidden when VITE_GOOGLE_CLIENT_ID is empty (email + password
// still works). Plain sign-in, not an integration that needs an agreement.
import { useQueryClient } from "@tanstack/react-query"
import { useEffect, useRef, useState } from "react"

import { toast } from "sonner"

import { LoginService } from "@/client"
import { handleError } from "@/utils"
import { storeToken } from "./session"

const GSI_SRC = "https://accounts.google.com/gsi/client"
const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID?.trim() ?? ""

type CredentialResponse = { credential?: string }

type GoogleId = {
  initialize: (o: {
    client_id: string
    callback: (r: CredentialResponse) => void
    ux_mode?: "popup" | "redirect"
  }) => void
  renderButton: (el: HTMLElement, o: Record<string, unknown>) => void
}

declare global {
  interface Window {
    google?: { accounts?: { id?: GoogleId } }
  }
}

let script: Promise<GoogleId> | null = null

function loadGsi(): Promise<GoogleId> {
  script ??= new Promise<GoogleId>((resolve, reject) => {
    const ready = () => {
      const id = window.google?.accounts?.id
      if (id) resolve(id)
      else reject(new Error("Google Identity Services unavailable"))
    }
    if (window.google?.accounts?.id) return ready()
    const el = document.createElement("script")
    el.src = GSI_SRC
    el.async = true
    el.defer = true
    el.onload = ready
    el.onerror = () => {
      script = null
      reject(new Error("Google Identity Services failed to load"))
    }
    document.head.appendChild(el)
  })
  return script
}

const showError = (description: string) =>
  toast.error("Gagal masuk dengan Google", { description })

export function GoogleButton({
  onDone,
  text = "signin_with",
}: {
  /** Called after the token is stored. */
  onDone: () => void
  text?: "signin_with" | "signup_with" | "continue_with"
}) {
  const host = useRef<HTMLDivElement>(null)
  const queryClient = useQueryClient()
  const [failed, setFailed] = useState(false)
  // Keep the latest callback without re-rendering Google's button.
  const done = useRef(onDone)
  done.current = onDone

  useEffect(() => {
    if (!CLIENT_ID) return
    let alive = true
    loadGsi()
      .then((id) => {
        if (!alive || !host.current) return
        id.initialize({
          client_id: CLIENT_ID,
          ux_mode: "popup",
          callback: async (r) => {
            if (!r.credential) return
            try {
              const res = await LoginService.loginGoogle({
                body: { credential: r.credential },
              })
              storeToken(res.data.access_token)
              await queryClient.invalidateQueries({ queryKey: ["currentUser"] })
              done.current()
            } catch (e) {
              handleError.call(showError, e as Error)
            }
          },
        })
        id.renderButton(host.current, {
          type: "standard",
          theme: "outline",
          size: "large",
          shape: "pill",
          text,
          locale: "id",
          width: Math.min(360, host.current.clientWidth || 320),
        })
      })
      .catch(() => alive && setFailed(true))
    return () => {
      alive = false
    }
  }, [queryClient, text])

  if (!CLIENT_ID || failed) return null
  return (
    <>
      <div className="gbtn-wrap" ref={host} data-testid="google-button" />
      <div className="or-sep">atau</div>
    </>
  )
}
