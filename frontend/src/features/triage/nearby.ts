// "Top N nearest facilities" for a result route.
//
// Default: rank in the browser from the province list, so the patient's
// coordinates never leave the device (docs/SATUSEHAT.md §3). Set
// VITE_FACILITIES_SERVER_NEAREST=true to use POST /facilities/nearest instead,
// which sends the coordinates to our own server for cross-province accuracy.
import { FacilitiesService, type FacilityPublic } from "@/client"
import { whatsappNumber } from "./links"
import { type Coords, provinceFromCoords } from "./location"

export const NEARBY_LIMIT = 5

// What to ask POST /facilities/nearest for, before re-ranking. 20 is that
// endpoint's cap; the extra room lets a WhatsApp-holder further out reach the top.
const FETCH_POOL = 20

export type Neighbour = FacilityPublic & {
  distance_km: number
  whatsapp: string | null
}

// Which facility kinds to try for a route, in order. MERAH needs a hospital
// (IGD); KUNING a Puskesmas; HIJAU a pharmacy when one is known, else a
// Puskesmas (apotek in MSI is mostly missing coordinates).
const KINDS_BY_ROUTE: Record<string, string[]> = {
  red: ["rs"],
  special: ["puskesmas", "rs"],
  yellow: ["puskesmas", "rs"],
  green: ["apotek", "puskesmas"],
}

export const facilityKinds = (route: string): string[] =>
  KINDS_BY_ROUTE[route] ?? ["puskesmas"]

// Two facilities closer than this are a tie, broken by data quality. Mirrors
// the backend adapter so both paths order the same way.
const TIE_KM = 0.5

function haversineKm(here: Coords, lat: number, lon: number): number {
  const r = 6371.0088
  const p1 = (here.latitude * Math.PI) / 180
  const p2 = (lat * Math.PI) / 180
  const dp = p2 - p1
  const dl = ((lon - here.longitude) * Math.PI) / 180
  const a =
    Math.sin(dp / 2) ** 2 + Math.cos(p1) * Math.cos(p2) * Math.sin(dl / 2) ** 2
  return 2 * r * Math.asin(Math.min(1, Math.sqrt(a)))
}

/** Contact-data completeness (0–4): phone matters most, then address, then MSI's
 * own verified/valid marker. Same rule as the backend adapter. */
function quality(f: FacilityPublic): number {
  const phone = f.phone ? 2 : 0
  const address = f.address ? 1 : 0
  const status = (f.status_sarana ?? "").toLowerCase()
  const verified = status === "verified" || status === "valid" ? 1 : 0
  return phone + address + verified
}

/** WhatsApp-holders first — those are the ones a patient can actually reach
 * from home — then distance, with data quality breaking near-ties. The distance
 * part mirrors the backend adapter so both paths order the same way. */
function compare(a: Neighbour, b: Neighbour): number {
  const wa = Number(!a.whatsapp) - Number(!b.whatsapp)
  if (wa !== 0) return wa
  const band =
    Math.floor(a.distance_km / TIE_KM) - Math.floor(b.distance_km / TIE_KM)
  if (band !== 0) return band
  const q = quality(b) - quality(a)
  return q !== 0 ? q : a.distance_km - b.distance_km
}

/** Nearest `limit` facilities to `here`. Facilities without coordinates cannot
 * be ranked and drop out. */
export function rankNearest(
  rows: FacilityPublic[],
  here: Coords,
  limit = NEARBY_LIMIT,
): Neighbour[] {
  const scored: Neighbour[] = []
  for (const f of rows) {
    if (f.latitude == null || f.longitude == null) continue
    scored.push({
      ...f,
      distance_km: haversineKm(here, f.latitude, f.longitude),
      // Curated number first; otherwise fall back to MSI's `telp`, which is
      // only accepted when it actually looks like a mobile.
      whatsapp: whatsappNumber(f.wa_number || f.phone),
    })
  }
  scored.sort(compare)
  return scored.slice(0, limit)
}

/** Opt-in: rank on our server (the coordinates leave the device). */
export const USE_SERVER =
  import.meta.env.VITE_FACILITIES_SERVER_NEAREST === "true"

const PAGE = 500
// Guard rail: no province needs more than a few thousand rows, and this keeps a
// bad `count` from looping forever.
const MAX_ROWS = 5000

/** Every operational facility of a kind in a province, paged. */
async function provinceFacilities(
  province: string,
  kind: string,
): Promise<FacilityPublic[]> {
  const out: FacilityPublic[] = []
  for (let skip = 0; skip < MAX_ROWS; skip += PAGE) {
    const res = await FacilitiesService.listFacilities({
      // with_coords drops the many coordinate-less rows (most Apotek) so the
      // paging stays small and only rankable facilities come back.
      query: { province, kind, limit: PAGE, skip, with_coords: true },
    })
    const rows = res.data?.data ?? []
    out.push(...rows)
    const total = res.data?.count ?? out.length
    if (rows.length < PAGE || out.length >= total) break
  }
  return out
}

async function serverNearest(
  here: Coords,
  route: string,
): Promise<Neighbour[]> {
  for (const kind of facilityKinds(route)) {
    const res = await FacilitiesService.nearestFacilities({
      body: {
        latitude: here.latitude,
        longitude: here.longitude,
        kind,
        // More than we show: a WhatsApp-holder that is not the closest still
        // has to be able to reach the top of the list.
        limit: FETCH_POOL,
      },
    })
    const rows = res.data?.data ?? []
    if (rows.length) {
      return rows
        .map((f) => ({
          ...f,
          whatsapp: whatsappNumber(f.wa_number || f.phone),
        }))
        .sort(compare)
        .slice(0, NEARBY_LIMIT)
    }
  }
  return []
}

/** Nearest facilities for a route, or an empty list when none can be found
 * (outside Indonesia, no mirror data, or a failed request). */
export async function fetchNearest(
  route: string,
  here: Coords,
): Promise<Neighbour[]> {
  if (USE_SERVER) return serverNearest(here, route)
  const province = await provinceFromCoords(here.latitude, here.longitude)
  if (!province) return []
  for (const kind of facilityKinds(route)) {
    const rows = await provinceFacilities(province, kind)
    const nearest = rankNearest(rows, here)
    if (nearest.length) return nearest
  }
  return []
}
