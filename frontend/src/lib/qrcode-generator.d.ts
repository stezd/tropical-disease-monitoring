// Types for the vendored qrcode-generator (only what TropiCek uses).
interface QRCode {
  addData(data: string, mode?: string): void
  make(): void
  getModuleCount(): number
  isDark(row: number, col: number): boolean
}
declare function qrcode(
  typeNumber: number,
  errorCorrectionLevel: "L" | "M" | "Q" | "H",
): QRCode
export default qrcode
