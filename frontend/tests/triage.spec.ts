import { expect, type Page, test } from "@playwright/test"

test.use({ storageState: { cookies: [], origins: [] } })

const next = (page: Page) => page.locator(".foot .btn").click()

async function startAs(page: Page, age: string) {
  await page.goto("/")
  await page.getByText("Saya sedang sakit").click()
  await page.getByText("Saya sendiri").click()
  await page.getByPlaceholder("25").fill(age)
  await page.getByRole("button", { name: "Perempuan" }).click()
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
  await expect(page.locator(".rtag")).toContainText("RUTE KUNING")
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

test("Broken summary QR shows a clear message", async ({ page }) => {
  await page.goto("/ringkasan#d=not-a-real-code")
  await expect(page.getByText("TIDAK BISA DIBACA")).toBeVisible()
})
