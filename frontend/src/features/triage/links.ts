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
