// Shared bits for login, sign-up, and "Masuk dengan Google".

/** Same key as hooks/useAuth (the API client reads it in main.tsx). */
export function storeToken(token: string) {
  localStorage.setItem("access_token", token)
}

/** `?redirect=` for /login and /signup: an in-app path only ("/skrining",
 * "/riwayat"), never another site ("//evil.example", "https://…"). */
function hasBadChar(v: string): boolean {
  for (let i = 0; i < v.length; i++) {
    if (v.charCodeAt(i) < 0x20 || v[i] === "\\") return true
  }
  return false
}

export function safeRedirect(v: unknown): string | undefined {
  if (typeof v !== "string") return undefined
  if (!v.startsWith("/") || v.startsWith("//") || hasBadChar(v)) {
    return undefined
  }
  return v.slice(0, 200)
}

export type RedirectSearch = { redirect?: string }

export const validateRedirectSearch = (
  search: Record<string, unknown>,
): RedirectSearch => {
  const redirect = safeRedirect(search.redirect)
  return redirect ? { redirect } : {}
}
