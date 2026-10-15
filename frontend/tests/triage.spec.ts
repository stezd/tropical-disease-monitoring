import { expect, type Page, type Route, test } from "@playwright/test"

import { randomEmail, randomPassword } from "./utils/random"

test.use({ storageState: { cookies: [], origins: [] } })
// Scoring can take 10s+ when the whole suite runs in parallel.
test.setTimeout(60_000)

// Lanjut, not the "‹ Kembali" button next to it.
const next = (page: Page) => page.locator(".foot .btn:not(.btn-back)").click()

// Stub geolocation rather than granting it: CI serves the app over plain HTTP
// (http://backend:8000), and Chrome only exposes the real API on secure
// origins, so a granted permission would still fail there. Jakarta → the
// province lookup (public/data/provinsi.json) gives "DKI Jakarta".
async function stubGeo(page: Page, mode: "ok" | "denied" = "ok") {
  await page.addInitScript((m) => {
    const position = {
      coords: { latitude: -6.2, longitude: 106.8 },
      timestamp: 0,
    }
    const denied = { code: 1, PERMISSION_DENIED: 1, message: "denied" }
    Object.defineProperty(navigator, "geolocation", {
      configurable: true,
      value: {
        getCurrentPosition: (
          ok: (p: unknown) => void,
          fail: (e: unknown) => void,
        ) => (m === "ok" ? ok(position) : fail(denied)),
        watchPosition: () => 0,
        clearWatch: () => {},
      },
    })
  }, mode)
}

const facility = (
  id: string,
  name: string,
  dLat: number,
  phone: string | null,
  kode = "104",
) => ({
  satusehat_id: id,
  code: `P31000000${id}`,
  name,
  jenis_sarana_kode: kode,
  jenis_sarana_nama: kode === "102" ? "Puskesmas" : "Rumah Sakit",
  province_code: "31",
  province_name: "DKI Jakarta",
  city_name: "Jakarta Pusat",
  address: `Jl. Contoh No. ${id}`,
  phone,
  status_sarana: "verified",
  latitude: -6.2 - dLat,
  longitude: 106.8,
})

// Six facilities, listed out of order. Only NEARBY_LIMIT (5) show: WhatsApp
// holders first (nearest first), then the rest by distance. The farthest one,
// with no phone, drops out. MSI stores a Puskesmas by its village name alone,
// in caps: the card has to show "Puskesmas Pasrujambe".
const FACILITIES = [
  facility("4", "Faskes Jauh Sekali", 0.1, "081200000004"),
  facility("2", "Faskes Sedang", 0.02, "021-3456789"),
  facility("1", "Faskes Dekat", 0.001, "081234567890"),
  facility("3", "Faskes Agak Jauh", 0.05, null),
  facility("5", "PASRUJAMBE", 0.03, null, "102"),
  facility("6", "Faskes Terjauh", 0.2, null),
]

async function mockFacilities(page: Page) {
  await page.route("**/api/v1/facilities**", (route: Route) =>
    route.fulfill({ json: { data: FACILITIES, count: FACILITIES.length } }),
  )
}

/** Home → path → privacy gate (ticked) → first question. */
async function passGate(page: Page, path: RegExp | string) {
  await page.goto("/")
  await page.getByText(path).click()
  await expect(page.getByText("PRIVASI", { exact: true })).toBeVisible()
  await page.getByLabel(/Saya setuju/).check()
  await next(page)
}

async function startAs(page: Page, age: string) {
  await passGate(page, "Saya sedang sakit")
  await page.getByText("Saya sendiri").click()
  await page.getByPlaceholder("25").fill(age)
  await page.getByRole("button", { name: "Perempuan" }).click()
  await page.getByRole("button", { name: "Tidak hamil" }).click()
  await next(page)
}

/** WhatsApp, Maps, and phone actions on the nearest-facility card. */
async function expectFacilityActions(page: Page) {
  await expect(page.locator(".nf-item b")).toHaveText(
    [
      "Faskes Dekat",
      "Faskes Jauh Sekali",
      "Faskes Sedang",
      "Puskesmas Pasrujambe",
      "Faskes Agak Jauh",
    ],
    { timeout: 10_000 },
  )
  const near = page.locator(".nf-item").first()
  await expect(
    near.getByRole("link", { name: /Cari di Google Maps/ }),
  ).toHaveAttribute(
    "href",
    /google\.com\/maps\/dir\/.*destination=Faskes%20Dekat%2C%20Jakarta%20Pusat/,
  )
  const wa = near.getByRole("link", { name: /Kirim rangkuman via WhatsApp/ })
  const href = (await wa.getAttribute("href")) ?? ""
  expect(href).toMatch(/^https:\/\/wa\.me\/6281234567890\?text=/)
  const text = decodeURIComponent(href.split("?text=")[1] ?? "")
  expect(text).toContain("rangkuman skrining")
  expect(text).toContain("/ringkasan#d=")
  expect(text).not.toMatch(/diagnosis/i)
  // Landline: a call, not WhatsApp.
  // (Maps links go by name, not coordinates: MSI's pins are off by km.)
  const landline = page.locator(".nf-item").nth(2)
  await expect(landline.getByRole("link", { name: /Telepon/ })).toHaveAttribute(
    "href",
    /^tel:62213456789$/,
  )
  await expect(landline.getByRole("link", { name: /WhatsApp/ })).toHaveCount(0)
}

test("Lanjut stays disabled until the privacy box is ticked", async ({
  page,
}) => {
  await stubGeo(page)
  await page.goto("/")
  await page.getByText("Saya sedang sakit").click()
  const lanjut = page.locator(".foot .btn:not(.btn-back)")
  await expect(lanjut).toBeDisabled()
  await page.getByLabel(/Saya setuju/).check()
  await expect(lanjut).toBeEnabled()
  await expect(page.locator(".loc-status.ok")).toContainText("DKI Jakarta")
})

test("Refused location shows the province picker", async ({ page }) => {
  await stubGeo(page, "denied")
  await page.goto("/")
  await page.getByText("Saya sedang sakit").click()
  await page.getByLabel(/Saya setuju/).check()
  await expect(page.locator(".loc-status.off")).toBeVisible()
  const province = page.getByLabel(/Provinsi \(opsional\)/)
  await expect(province).toBeVisible()
  await province.selectOption("Papua")
  await next(page)
  await expect(page.getByText("Siapa yang sedang sakit?")).toBeVisible()
})

test("Guest finishes the infection quiz and sees a route", async ({ page }) => {
  // Scoring can take ~45s when TRIAGE_SCORING_ENGINE=ai is set in .env (a model
  // scores the flow); CI runs the rules engine. test.slow() triples the budget.
  test.slow()
  await stubGeo(page)
  await mockFacilities(page)
  await startAs(page, "25")
  await page.getByText("Tidak ada, saya aman").click()
  await next(page)
  await page.getByText("Demam & Badan").click()
  await next(page)
  await page.getByText("Tinggi mendadak").click()
  await next(page)
  await page.getByText("Nyeri belakang mata").click()
  await next(page)
  await page.locator(".opt", { hasText: "Tidak ada" }).click()
  await next(page)
  await page.getByText("+ Ibuprofen").click()
  await next(page)
  await expect(page.getByText("PERINGATAN OBAT")).toBeVisible()
  await page.getByText("Mengerti, lanjut").click()
  await page.getByPlaceholder("37,0").fill("38,6")
  await next(page)
  await page.getByPlaceholder("160").fill("160")
  await page.getByPlaceholder("55").fill("52")
  await next(page)
  // Last step (pain map): no pain, straight to the result.
  await expect(page.locator(".foot .btn:not(.btn-back)")).toContainText(
    "Lihat Tebakan",
  )
  await next(page)

  await expect(page.getByText("SKRINING SELESAI")).toBeVisible({
    timeout: 60_000,
  })
  await expect(
    page.getByRole("heading", { name: "Demam Berdarah Dengue (DBD)" }),
  ).toBeVisible()
  await expect(page.locator(".rhead h3")).toContainText("KONDISI SEDANG")
  await expect(page.getByText(/bukan diagnosis dokter/)).toBeVisible()
  await expect(
    page.getByRole("img", { name: "QR rangkuman untuk petugas" }),
  ).toBeVisible()
  await expect(page.getByRole("link", { name: /Mobile JKN/ })).toHaveAttribute(
    "href",
    /app\.bpjs\.mobile/,
  )
  // Location was shared at the gate: the nearest facilities load on their own.
  await expectFacilityActions(page)
  // Guests are invited to make an account; there is no save button.
  await expect(page.getByRole("link", { name: /Buat akun/ })).toHaveAttribute(
    "href",
    /\/signup\?redirect=%2Fskrining/,
  )
  await expect(
    page.getByRole("button", { name: /Simpan ke riwayatku/ }),
  ).toHaveCount(0)
})

test("Back button returns to the previous question", async ({ page }) => {
  await stubGeo(page)
  await startAs(page, "25")
  await expect(page.getByText("Tidak ada, saya aman")).toBeVisible()
  await page.getByRole("button", { name: "Kembali" }).click()
  await expect(page.getByText("Siapa yang sedang sakit?")).toBeVisible()
  await page.getByRole("button", { name: "Kembali" }).click()
  await expect(page.getByText("PRIVASI", { exact: true })).toBeVisible()
})

test("Red flag opens the red route without the server", async ({ page }) => {
  await stubGeo(page, "denied")
  await startAs(page, "40")
  // Emergency check runs in the browser: block the API from here on.
  await page.route("**/api/v1/**", (route) => route.abort())
  await page.getByText("Sesak napas sangat berat").click()
  await next(page)
  await expect(
    page.getByRole("heading", { name: "KONDISI DARURAT" }),
  ).toBeVisible()
  await expect(page.getByRole("link", { name: /Telepon 119/ })).toHaveAttribute(
    "href",
    "tel:119",
  )
  await expect(page.locator(".numcard b")).toHaveText(["119", "112"])
  await expect(page.locator(".conf")).toHaveCount(0)
  // The IGD Maps search is there right away, without waiting for location.
  await expect(
    page.getByRole("link", { name: /Navigasi ke IGD Terdekat/ }),
  ).toHaveAttribute("href", /google\.com\/maps\/search/)
})

test("Red route lists the nearest hospitals with actions", async ({ page }) => {
  await stubGeo(page)
  await mockFacilities(page)
  await startAs(page, "40")
  await page.getByText("Sesak napas sangat berat").click()
  await next(page)
  await expect(
    page.getByRole("heading", { name: "KONDISI DARURAT" }),
  ).toBeVisible()
  await expectFacilityActions(page)
})

test("Guest finishes the chronic risk check", async ({ page }) => {
  // Same as the infection quiz: a model-scored flow takes ~45s locally.
  test.slow()
  await stubGeo(page)
  await mockFacilities(page)
  await passGate(page, "Cek risiko penyakit jangka panjang")
  await page.getByText("Saya sendiri").click()
  await page.getByPlaceholder("25").fill("55")
  await page.getByRole("button", { name: "Laki-laki" }).click()
  await next(page)
  // PTM danger signs come first; their details stay hidden until asked.
  await expect(page.locator(".opt").first()).toContainText("Nyeri dada kiri")
  await expect(page.locator(".opt .od")).toHaveCount(0)
  await page.getByRole("button", { name: /Lihat ciri-ciri/ }).click()
  await expect(page.locator(".opt .od").first()).toBeVisible()
  await page.getByText("Tidak ada, saya aman").click()
  await next(page)
  await page.locator(".cbox", { hasText: "Sendi mendadak" }).click()
  await next(page)
  await page.getByText(/jempol kaki/).click()
  await next(page)
  await page.locator(".opt", { hasText: "Tidak ada" }).click()
  await next(page)
  await next(page) // no drugs
  await page.getByPlaceholder("120").fill("130")
  await page.getByPlaceholder("80").fill("85")
  await expect(page.locator(".tstat")).toHaveText("Meningkat")
  await next(page)
  await expect(
    page.getByRole("heading", { name: "Pemeriksaan opsional" }),
  ).toBeVisible()
  await next(page) // skip labs
  await page.getByPlaceholder("160").fill("168")
  await page.getByPlaceholder("55").fill("80")
  await next(page)
  await next(page) // no pain

  await expect(page.getByText("SKRINING SELESAI")).toBeVisible({
    timeout: 60_000,
  })
  await expect(
    page.getByRole("heading", { name: "Gout Arthritis (Asam Urat)" }),
  ).toBeVisible()
  await expect(page.getByText(/BERPUASA/)).toBeVisible()
  await expect(page.getByText(/bukan diagnosis dokter/)).toBeVisible()
})

test("History page sends a signed-out visitor to /login", async ({ page }) => {
  await page.goto("/riwayat")
  await page.waitForURL(/\/login/)
  await expect(page.getByTestId("email-input")).toBeVisible()
})

test("Loading screen shows the mascot without a scrollbar", async ({
  page,
}) => {
  await stubGeo(page)
  let release: () => void = () => {}
  const gate = new Promise<void>((r) => {
    release = r
  })
  await page.route("**/api/v1/triage/flows/*", async (route) => {
    await gate
    await route.continue()
  })
  await page.goto("/skrining")
  const loading = page.locator(".loading")
  await expect(loading).toBeVisible()
  await expect(loading.locator(".m-load")).toBeVisible()
  const overflow = await page.evaluate(
    () =>
      document.documentElement.scrollHeight -
      document.documentElement.clientHeight,
  )
  expect(overflow).toBeLessThanOrEqual(0)
  release()
})

test("Broken summary QR shows a clear message", async ({ page }) => {
  await page.goto("/ringkasan#d=not-a-real-code")
  await expect(page.getByText("TIDAK BISA DIBACA")).toBeVisible()
})

// Guest → "Buat akun" on the result → sign up → log in → back to the same
// result (answers stay in sessionStorage) → save → history → delete.
test("Account from the result page saves to the history", async ({ page }) => {
  const email = randomEmail()
  const password = randomPassword()
  await stubGeo(page, "denied")
  await passGate(page, "Saya sedang sakit")
  await page.getByText("Saya sendiri").click()
  await page.getByPlaceholder("25").fill("30")
  await page.getByRole("button", { name: "Laki-laki" }).click()
  await next(page)
  await page.getByText("Tidak ada, saya aman").click()
  await next(page)
  await page.getByText("Demam & Badan").click()
  await next(page)
  await page.getByText("Tinggi mendadak").click()
  await next(page)
  await page.getByText("Nyeri belakang mata").click()
  await next(page)
  await page.locator(".opt", { hasText: "Tidak ada" }).click()
  await next(page)
  await next(page) // no drugs
  await page.getByPlaceholder("37,0").fill("38,6")
  await next(page)
  await page.getByPlaceholder("160").fill("170")
  await page.getByPlaceholder("55").fill("65")
  await next(page)
  await next(page) // no pain
  await expect(page.getByText("SKRINING SELESAI")).toBeVisible({
    timeout: 20_000,
  })

  await page.getByRole("link", { name: /Buat akun/ }).click()
  await page.getByTestId("full-name-input").fill("Pasien Uji")
  await page.getByTestId("email-input").fill(email)
  await page.getByTestId("password-input").fill(password)
  await page.getByTestId("confirm-password-input").fill(password)
  await page.getByRole("button", { name: "Sign Up" }).click()
  await page.waitForURL(/\/login\?redirect=%2Fskrining/)
  await page.getByTestId("email-input").fill(email)
  await page.getByTestId("password-input").fill(password)
  await page.getByRole("button", { name: "Log In" }).click()
  await page.waitForURL("/skrining")

  await expect(page.getByText("SKRINING SELESAI")).toBeVisible({
    timeout: 20_000,
  })
  await expect(page.getByRole("link", { name: /Buat akun/ })).toHaveCount(0)
  await page.getByRole("button", { name: /Simpan ke riwayatku/ }).click()
  await expect(page.getByText(/Tersimpan di riwayat akunmu/)).toBeVisible()

  await page.getByRole("link", { name: /Lihat riwayat/ }).click()
  await expect(
    page.getByText("RIWAYAT SKRINING", { exact: true }),
  ).toBeVisible()
  await expect(page.locator(".hist-item")).toHaveCount(1)
  await expect(page.locator(".hist-badge")).toContainText("KONDISI")
  await page.getByRole("button", { name: /Hapus/ }).click()
  await page.getByRole("button", { name: "Ya, hapus" }).click()
  await expect(page.locator(".hist-item")).toHaveCount(0)
  await expect(page.locator(".hist-empty")).toBeVisible()
})
