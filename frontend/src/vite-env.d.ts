/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  /** "true" = rank nearest facilities on the server (coords leave the device).
   * Default/absent = rank in the browser. See docs/SATUSEHAT.md §3. */
  readonly VITE_FACILITIES_SERVER_NEAREST?: string
  /** OAuth Client ID (Web) for "Masuk dengan Google". Empty = button hidden.
   * Must match the backend's GOOGLE_CLIENT_ID. */
  readonly VITE_GOOGLE_CLIENT_ID?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
