import { expect, type Page, test } from "@playwright/test"

test.use({ storageState: { cookies: [], origins: [] } })

const next = (page: Page) => page.locator(".foot .btn").click()

async function startAs(page: Page, age: string) {
  await page.goto("/")
  await page.getByText("Saya sedang sakit").click()
  await page.getByText("Saya sendiri").click()
  await page.getByPlaceholder("25").fill(age)
  await page.getByRole("button", { name: "Perempuan" }).click()
  await page.getByRole("button", { name: "Tidak hamil" }).click()
  await next(page)
}

test("Guest finishes the infection quiz and sees a route", async ({ page }) => {
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
  await next(page) // no pain
  await next(page) // no photo

  await expect(page.getByText("SKRINING SELESAI")).toBeVisible({
    timeout: 20_000,
  })
  await expect(
    page.getByRole("heading", { name: "Demam Berdarah Dengue (DBD)" }),
  ).toBeVisible()
  await expect(page.locator(".rtag")).toContainText("KONDISI SEDANG")
  await expect(page.getByText(/bukan diagnosis dokter/)).toBeVisible()
  await expect(page.locator(".qrbox canvas")).toBeVisible()
  await expect(page.getByRole("link", { name: /Mobile JKN/ })).toHaveAttribute(
    "href",
    /app\.bpjs\.mobile/,
  )
})

test("Red flag opens the red route without the server", async ({ page }) => {
  await startAs(page, "40")
  // Emergency check runs in the browser: block the API from here on.
  await page.route("**/api/v1/**", (route) => route.abort())
  await page.getByText("Sesak napas sangat berat").click()
  await next(page)
  await expect(page.getByText("KONDISI DARURAT")).toBeVisible()
  await expect(page.getByRole("link", { name: /Telepon 119/ })).toHaveAttribute(
    "href",
    "tel:119",
  )
  await expect(page.locator(".numcard b")).toHaveText(["119", "112"])
  await expect(page.locator(".conf")).toHaveCount(0)
})

test("Guest finishes the chronic risk check", async ({ page }) => {
  await page.goto("/")
  await page.getByText("Cek risiko penyakit jangka panjang").click()
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
  await next(page)
  await page.getByPlaceholder("160").fill("168")
  await page.getByPlaceholder("55").fill("80")
  await next(page)
  await next(page) // no photo

  await expect(page.getByText("SKRINING SELESAI")).toBeVisible({
    timeout: 20_000,
  })
  await expect(
    page.getByRole("heading", { name: "Gout Arthritis (Asam Urat)" }),
  ).toBeVisible()
  await expect(page.getByText(/BERPUASA/)).toBeVisible()
  await expect(page.getByText(/bukan diagnosis dokter/)).toBeVisible()
})

test("Broken summary QR shows a clear message", async ({ page }) => {
  await page.goto("/ringkasan#d=not-a-real-code")
  await expect(page.getByText("TIDAK BISA DIBACA")).toBeVisible()
})
