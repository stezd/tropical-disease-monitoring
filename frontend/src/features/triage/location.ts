// User location → province, in the browser (AGENTS.md "Data diri · Lokasi").
// Asked right after the privacy tick (screens/Consent.tsx), on both paths.
// The server passes the province to Gemma4 as the fact "Provinsi tempat
// tinggal" (backend/app/triage/Gemma4.py, docs/Format-Gemma4.md). No
// per-province weights.
//
// Coordinates stay on the device: nearest-facility picking ranks in the browser
// by default. The one exception is the opt-in server endpoint (see
// features/triage/nearby.ts and docs/SATUSEHAT.md §3), which sends the point
// only when VITE_FACILITIES_SERVER_NEAREST=true.
//
// Boundaries: public/data/provinsi.json, 38 provinces, packed from
// "Indonesia GeoJSON & TopoJSON Maps (38 Provinces)" (CC BY 4.0, see
// public/data/README.md). No map service is called.

export type Province = string

/** The 38 provinces, same names as public/data/provinsi.json. */
export const PROVINCES: Province[] = [
  "Aceh",
  "Bali",
  "Banten",
  "Bengkulu",
  "DKI Jakarta",
  "Daerah Istimewa Yogyakarta",
  "Gorontalo",
  "Jambi",
  "Jawa Barat",
  "Jawa Tengah",
  "Jawa Timur",
  "Kalimantan Barat",
  "Kalimantan Selatan",
  "Kalimantan Tengah",
  "Kalimantan Timur",
  "Kalimantan Utara",
  "Kepulauan Bangka Belitung",
  "Kepulauan Riau",
  "Lampung",
  "Maluku",
  "Maluku Utara",
  "Nusa Tenggara Barat",
  "Nusa Tenggara Timur",
  "Papua",
  "Papua Barat",
  "Papua Barat Daya",
  "Papua Pegunungan",
  "Papua Selatan",
  "Papua Tengah",
  "Riau",
  "Sulawesi Barat",
  "Sulawesi Selatan",
  "Sulawesi Tengah",
  "Sulawesi Tenggara",
  "Sulawesi Utara",
  "Sumatera Barat",
  "Sumatera Selatan",
  "Sumatera Utara",
]

// Each polygon is a list of rings (outer first, then holes); a ring is a flat
// [lon, lat, lon, lat, …] list.
type Shape = { n: Province; p: number[][][] }

// The boundaries are simplified, so coastal towns can fall just outside them.
// A point this close to a province's edge still counts as that province.
const NEAR_KM = 25

function inRing(x: number, y: number, r: number[]) {
  let inside = false
  for (let i = 0, j = r.length - 2; i < r.length; j = i, i += 2) {
    const [xi, yi, xj, yj] = [r[i], r[i + 1], r[j], r[j + 1]]
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) {
      inside = !inside
    }
  }
  return inside
}

/** Rough distance in km from a point to a ring's edge. */
function kmToRing(x: number, y: number, r: number[]) {
  const k = Math.cos((y * Math.PI) / 180)
  const px = x * k
  let best = Number.POSITIVE_INFINITY
  for (let i = 0, j = r.length - 2; i < r.length; j = i, i += 2) {
    const ax = r[j] * k
    const ay = r[j + 1]
    const dx = r[i] * k - ax
    const dy = r[i + 1] - ay
    const len = dx * dx + dy * dy
    const t = len
      ? Math.max(0, Math.min(1, ((px - ax) * dx + (y - ay) * dy) / len))
      : 0
    best = Math.min(best, Math.hypot(px - ax - t * dx, y - ay - t * dy))
  }
  return best * 111.32
}

export function provinceAt(
  shapes: Shape[],
  lat: number,
  lon: number,
): Province | null {
  let near: Province | null = null
  let nearKm = NEAR_KM
  for (const s of shapes) {
    for (const [outer, ...holes] of s.p) {
      if (inRing(lon, lat, outer) && !holes.some((h) => inRing(lon, lat, h))) {
        return s.n
      }
      const km = kmToRing(lon, lat, outer)
      if (km < nearKm) {
        near = s.n
        nearKm = km
      }
    }
  }
  return near
}

let shapes: Promise<Shape[]> | null = null

/** Returns the province for a coordinate, or null when outside Indonesia.
 * Throws when the boundary file cannot be loaded. */
export async function provinceFromCoords(
  lat: number,
  lon: number,
): Promise<Province | null> {
  shapes ??= fetch("/data/provinsi.json").then((r) => {
    if (!r.ok) throw new Error(`provinsi.json: ${r.status}`)
    return r.json() as Promise<Shape[]>
  })
  try {
    return provinceAt(await shapes, lat, lon)
  } catch (e) {
    shapes = null
    throw e
  }
}

export type Coords = { latitude: number; longitude: number }

export type LocateResult =
  | { ok: true; province: Province; latitude: number; longitude: number }
  | { ok: false; reason: "unsupported" | "denied" | "unavailable" | "outside" }

export type CoordsResult =
  | { ok: true; coords: Coords }
  | { ok: false; reason: "unsupported" | "denied" | "unavailable" }

// Granted this session, in memory only. Cleared when the tab closes: never in
// localStorage, never sent anywhere unless the opt-in endpoint is enabled.
let lastCoords: Coords | null = null

/** Coordinates already granted this session, if any (no prompt). */
export const cachedCoords = (): Coords | null => lastCoords

/** Ask for the browser location once, then reuse it for the session. */
export async function locateCoords(): Promise<CoordsResult> {
  if (lastCoords) return { ok: true, coords: lastCoords }
  if (!("geolocation" in navigator)) return { ok: false, reason: "unsupported" }
  const pos = await new Promise<GeolocationPosition | GeolocationPositionError>(
    (resolve) =>
      navigator.geolocation.getCurrentPosition(resolve, resolve, {
        maximumAge: 10 * 60 * 1000,
        timeout: 15_000,
      }),
  )
  if (!("coords" in pos)) {
    return {
      ok: false,
      reason: pos.code === pos.PERMISSION_DENIED ? "denied" : "unavailable",
    }
  }
  lastCoords = {
    latitude: pos.coords.latitude,
    longitude: pos.coords.longitude,
  }
  return { ok: true, coords: lastCoords }
}

/** Ask the browser for the location and turn it into a province. */
export async function askProvince(): Promise<LocateResult> {
  const r = await locateCoords()
  if (!r.ok) return { ok: false, reason: r.reason }
  let province: Province | null
  try {
    province = await provinceFromCoords(r.coords.latitude, r.coords.longitude)
  } catch {
    return { ok: false, reason: "unavailable" }
  }
  return province
    ? { ok: true, province, ...r.coords }
    : { ok: false, reason: "outside" }
}
