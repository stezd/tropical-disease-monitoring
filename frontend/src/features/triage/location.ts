// Skeleton: user location → province, in the browser (AGENTS.md "Tahap 4 · Lokasi").
// Status ⏳: endemic provinces and weights wait for DR + ST (question no. 10).
//
// Plan:
// 1. Bundle simplified province boundaries (GeoJSON, ~200 KB) in public/, no map service.
// 2. Ask permission with navigator.geolocation.getCurrentPosition.
// 3. Point-in-polygon → province name. Keep only the name; drop the coordinates.
// 4. If permission is denied, let the patient pick a province or skip.
// 5. Send it as `Answers.province`; scoring adds `weights.province[<name>]`.

export type Province = string

/** Returns the province for a coordinate, or null. Not implemented yet. */
export async function provinceFromCoords(
  _lat: number,
  _lon: number,
): Promise<Province | null> {
  return null
}

export async function askProvince(): Promise<Province | null> {
  if (!("geolocation" in navigator)) return null
  const pos = await new Promise<GeolocationPosition | null>((resolve) =>
    navigator.geolocation.getCurrentPosition(resolve, () => resolve(null), {
      maximumAge: 10 * 60 * 1000,
      timeout: 10_000,
    }),
  )
  if (!pos) return null
  return provinceFromCoords(pos.coords.latitude, pos.coords.longitude)
}
