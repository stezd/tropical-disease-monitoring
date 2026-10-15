// Plain links only: no API, no data sent anywhere (AGENTS.md "Standalone").

const JKN_PACKAGE = "app.bpjs.mobile"
const PLAY_JKN = `https://play.google.com/store/apps/details?id=${JKN_PACKAGE}`

export const isAndroid = (userAgent = navigator.userAgent) =>
  /android/i.test(userAgent)

/** Mobile JKN. Android: ask for the app's launcher screen, with the Play Store
 * page as fallback. Others: Play Store.
 *
 * Mobile JKN 4.18.0 has no deep link (no URL scheme, no App Links), and Chrome
 * only opens apps that accept browser links. So in Chrome this usually lands on
 * the Play Store page, which shows "Buka" when the app is installed. Browsers
 * that allow launcher intents open the app directly. */
export function jknURL(userAgent = navigator.userAgent): string {
  if (isAndroid(userAgent)) {
    return (
      "intent:#Intent;action=android.intent.action.MAIN;" +
      "category=android.intent.category.LAUNCHER;" +
      `package=${JKN_PACKAGE};` +
      `S.browser_fallback_url=${encodeURIComponent(PLAY_JKN)};end`
    )
  }
  return PLAY_JKN
}

export const mapsURL = (q: string) =>
  `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`

/** Indonesian phone number in international form, e.g. "0812-3456-789" → "628123456789". */
const toIntl = (phone: string): string => {
  const digits = phone.replace(/\D/g, "")
  if (!digits) return ""
  if (digits.startsWith("62")) return digits
  if (digits.startsWith("0")) return `62${digits.slice(1)}`
  return digits
}

/** A wa.me number only when the phone looks like a mobile (08… / 628…).
 *
 * MSI's `telp` is often a landline (area codes like 021), which has no
 * WhatsApp. Returning null for those lets the UI fall back to a plain call
 * button instead of a dead WhatsApp link. */
export function whatsappNumber(phone?: string | null): string | null {
  if (!phone) return null
  const intl = toIntl(phone)
  if (!intl.startsWith("628")) return null
  return intl.length >= 10 && intl.length <= 15 ? intl : null
}

/** WhatsApp chat with a prefilled message. The patient opens it and presses
 * send themself; our server sends nothing. */
export const waURL = (number: string, text?: string) =>
  `https://wa.me/${number}${text ? `?text=${encodeURIComponent(text)}` : ""}`

export const telURL = (phone: string) => `tel:${toIntl(phone)}`

const ROMAN = /^[ivx]{1,4}$/

const titleCase = (name: string) =>
  name
    .toLowerCase()
    .split(" ")
    .map((w) =>
      ROMAN.test(w) ? w.toUpperCase() : w.replace(/^./, (c) => c.toUpperCase()),
    )
    .join(" ")

/** MSI names a Puskesmas by its village alone, in caps ("PASRUJAMBE"), so the
 * kind has to come from us — patients know what a "Puskesmas" is, not a bare
 * "PASRUJAMBE". 10.440 of 10.462 rows are all caps; "MASARAN I" needs the roman
 * numeral kept. */
export function facilityName(f: {
  name: string
  jenis_sarana_kode?: string | null
}): string {
  return f.jenis_sarana_kode === "102" && !/puskesmas/i.test(f.name)
    ? `Puskesmas ${titleCase(f.name)}`
    : f.name
}

/** Directions straight to one facility, by name. Shareable, no API key.
 *
 * Deliberately not an exact-coordinate pin: MSI coordinates are off by whole
 * kilometres (one Puskesmas was 3 km away; docs/SATUSEHAT.md §5), and Maps
 * resolves the name + city to the real place itself. The mirror's coordinates
 * are still fine for *ranking* by distance, which shrugs off that error. */
export function routeURL(f: {
  name: string
  city_name?: string | null
  jenis_sarana_kode?: string | null
}): string {
  const dest = [facilityName(f), f.city_name].filter(Boolean).join(", ")
  return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(dest)}&travelmode=driving`
}
