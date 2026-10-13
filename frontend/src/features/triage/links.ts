// Plain links only: no API, no data sent anywhere (AGENTS.md "Standalone").

const PLAY_JKN = "https://play.google.com/store/apps/details?id=app.bpjs.mobile"

/** Mobile JKN: Android opens the app (Play Store fallback), others open Play Store. */
export function jknURL(userAgent = navigator.userAgent): string {
  if (/android/i.test(userAgent)) {
    return `intent://#Intent;package=app.bpjs.mobile;S.browser_fallback_url=${encodeURIComponent(PLAY_JKN)};end`
  }
  return PLAY_JKN
}

export const mapsURL = (q: string) =>
  `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`
