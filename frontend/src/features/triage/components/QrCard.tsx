// Result page: QR for the health worker, plus "Salin QR" (image to clipboard)
// and "Simpan QR" (PNG download). The QR content comes from qr.ts unchanged
// (app URL + compact answers; no name, NIK, or photo). The exported image adds
// a short caption so a forwarded picture still says what it is.
import { useEffect, useRef, useState } from "react"

import type { Answers } from "@/client"
import { sfx } from "../fx"
import { drawQR, summaryURL } from "../qr"
import { Card, toast } from "./Ui"

const CAPTION = "TropiCare · Rangkuman untuk petugas"
const CAPTION_SUB = "Pindai dengan kamera HP"
const FILE_NAME = "tropicare-qr-rangkuman.png"

/** Image clipboard: Chromium 76+, Safari 13.1+, Firefox 127+. Needs HTTPS. */
export function canCopyImage(): boolean {
  if (!window.isSecureContext || typeof ClipboardItem === "undefined") {
    return false
  }
  if (!navigator.clipboard?.write) return false
  // ClipboardItem.supports() exists in newer browsers only; assume yes otherwise.
  const supports = (
    ClipboardItem as unknown as { supports?: (t: string) => boolean }
  ).supports
  return supports ? supports("image/png") : true
}

/** The on-screen QR plus a white margin and the caption, as a PNG blob. */
function qrImage(qr: HTMLCanvasElement): Promise<Blob> {
  const pad = 32
  const size = qr.width
  const out = document.createElement("canvas")
  out.width = size + pad * 2
  out.height = size + pad * 2 + 76
  const ctx = out.getContext("2d")
  if (!ctx) return Promise.reject(new Error("no 2d context"))
  ctx.fillStyle = "#fff"
  ctx.fillRect(0, 0, out.width, out.height)
  ctx.imageSmoothingEnabled = false
  ctx.drawImage(qr, pad, pad)
  ctx.textAlign = "center"
  ctx.fillStyle = "#3a2e6e"
  ctx.font = '600 26px Fredoka, Nunito, "Segoe UI", sans-serif'
  ctx.fillText(CAPTION, out.width / 2, size + pad + 34, out.width - pad)
  ctx.fillStyle = "#5e5890"
  ctx.font = '700 19px Nunito, "Segoe UI", sans-serif'
  ctx.fillText(CAPTION_SUB, out.width / 2, size + pad + 64, out.width - pad)
  return new Promise((resolve, reject) =>
    out.toBlob(
      (b) => (b ? resolve(b) : reject(new Error("toBlob failed"))),
      "image/png",
    ),
  )
}

function download(blob: Blob) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = FILE_NAME
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 10_000)
}

export function QrCard({
  answers,
  flowId,
}: {
  answers: Answers
  flowId: string
}) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [ok, setOk] = useState(true)
  const [canCopy] = useState(canCopyImage)
  useEffect(() => {
    if (canvas.current) {
      setOk(drawQR(canvas.current, summaryURL(answers, flowId)))
    }
  }, [answers, flowId])
  if (!ok) return null

  const save = async () => {
    if (!canvas.current) return
    try {
      download(await qrImage(canvas.current))
      toast("💾 QR disimpan sebagai gambar.")
    } catch {
      toast("Gagal menyimpan QR. Tunjukkan layar ini ke petugas.")
    }
  }

  const copy = async () => {
    if (!canvas.current) return
    try {
      // Pass the blob as a promise: Safari only allows clipboard writes that
      // start inside the tap, before any await.
      await navigator.clipboard.write([
        new ClipboardItem({ "image/png": qrImage(canvas.current) }),
      ])
      sfx.ding()
      toast("📋 QR tersalin! Tempel di chat untuk dikirim.")
    } catch {
      // Permission denied or image type refused: save the file instead.
      await save()
    }
  }

  return (
    <Card tab="QR UNTUK PETUGAS" className="qrcard">
      <canvas
        ref={canvas}
        width={232}
        height={232}
        role="img"
        aria-label="QR rangkuman untuk petugas"
      />
      <p className="qrcap">
        <b>QR Rangkuman</b>
        Tunjukkan ke petugas agar tidak perlu ditanya ulang. Tidak disimpan di
        server.
      </p>
      <div className="qrbtns">
        {canCopy && (
          <button type="button" className="btn btn-secondary" onClick={copy}>
            📋 Salin QR
          </button>
        )}
        <button type="button" className="btn btn-secondary" onClick={save}>
          💾 Simpan QR
        </button>
      </div>
    </Card>
  )
}
