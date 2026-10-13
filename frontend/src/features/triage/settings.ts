// Per-device preferences (Pengaturan). Stored in localStorage; no health data here.
import { useSyncExternalStore } from "react"

export type Settings = { sound: boolean; vibrate: boolean }

const KEY = "tropicek_settings"
const DEFAULTS: Settings = { sound: true, vibrate: true }
const listeners = new Set<() => void>()

function read(): Settings {
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(KEY) ?? "{}") }
  } catch {
    return DEFAULTS
  }
}

let current = read()

export const getSettings = () => current

export function setSettings(patch: Partial<Settings>) {
  current = { ...current, ...patch }
  try {
    localStorage.setItem(KEY, JSON.stringify(current))
  } catch {
    // Private mode: keep in memory only.
  }
  for (const l of listeners) l()
}

export function useSettings(): Settings {
  return useSyncExternalStore((l) => {
    listeners.add(l)
    return () => listeners.delete(l)
  }, getSettings)
}
