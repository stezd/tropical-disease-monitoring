// Photo picker: consent, camera or gallery, preview, and (when the server has a
// real analyzer) the analysis call. Used by the photo step and the result page.
//
// Photos are health data (AGENTS.md "Privacy"):
// - Both buttons stay off until the patient ticks the consent box.
// - The photo lives only as an object URL in this component. It is revoked on
//   replace and unmount, and never goes to the store, sessionStorage,
//   localStorage, the QR, the summary, or logs.
// - It is sent to our own server only when flow.photo_analysis is true; the
//   server analyzes it in memory and does not store it (routes/triage.py).
import "@/styles/photo.css"

import { useCallback, useEffect, useRef, useState } from "react"
import { createPortal } from "react-dom"

import { type FlowPublic, TriageService } from "@/client"
import { sfx } from "../fx"
import { NONE } from "../model"
import { PrivacyText } from "./Privacy"
import { Modal } from "./Ui"

/** Same limit as the server (app/triage/vision.py MAX_PHOTO_BYTES). */
const MAX_BYTES = 8 * 1024 * 1024

/** What the analysis returned. Only sent when flow.photo_analysis is true. */
export type PhotoOutcome =
  /** Finding IDs from flow.findings (never disease names). */
  | { kind: "found"; ids: string[] }
  | { kind: "none" }
  | { kind: "too_big" }
  | { kind: "error" }

// Kept in memory for this tab only, so the patient is not asked twice in one
// screening (quiz step, then result page). Lost on refresh, never persisted.
let consentGiven = false
let photoUsed = false

/** True when a photo was picked earlier in this tab (not persisted). */
export const photoWasAdded = () => photoUsed

/** Add photo findings to the patient's own picks ("none" is dropped). */
export function mergeFindings(current: string[], ids: string[]): string[] {
  return [...new Set([...current.filter((x) => x !== NONE), ...ids])]
}

export function PhotoPicker({
  flow,
  onAnalyzed,
}: {
  flow: FlowPublic
  /** Called after each analysis. Not called when flow.photo_analysis is false. */
  onAnalyzed?: (o: PhotoOutcome) => void
}) {
  const host = useRef<HTMLDivElement>(null)
  const camera = useRef<HTMLInputElement>(null)
  const gallery = useRef<HTMLInputElement>(null)
  const [photo, setPhoto] = useState<string | null>(null)
  const [scanning, setScanning] = useState(false)
  const [consent, setConsent] = useState(consentGiven)
  const [privacy, setPrivacy] = useState(false)
  const analyze = flow.photo_analysis
  const closePrivacy = useCallback(() => setPrivacy(false), [])

  // Only the latest pick may report back, and nothing after unmount.
  const run = useRef(0)
  useEffect(
    () => () => {
      run.current = -1
    },
    [],
  )
  // Free the previous preview on replace, and the last one on unmount.
  useEffect(
    () => () => {
      if (photo) URL.revokeObjectURL(photo)
    },
    [photo],
  )

  const agree = (v: boolean) => {
    consentGiven = v
    setConsent(v)
    sfx.tap()
  }
  const open = (input: HTMLInputElement | null) => {
    if (!consent || scanning) return
    sfx.tap()
    input?.click()
  }

  const onFile = async (file: File) => {
    if (!consent) return
    photoUsed = true
    setPhoto(URL.createObjectURL(file))
    if (!analyze) return
    const id = ++run.current
    const report = (o: PhotoOutcome) => {
      if (run.current === id) onAnalyzed?.(o)
    }
    if (file.size > MAX_BYTES) return report({ kind: "too_big" })
    setScanning(true)
    sfx.think()
    try {
      const r = (await TriageService.analyzePhoto({ body: { photo: file } }))
        .data
      // Keep only IDs this flow knows, so nothing unexpected reaches the score.
      const known = new Set(flow.findings.map((o) => o.id))
      const ids = r.findings.filter((x) => x !== NONE && known.has(x))
      report(
        r.available && ids.length ? { kind: "found", ids } : { kind: "none" },
      )
    } catch {
      report({ kind: "error" })
    } finally {
      if (run.current === id) setScanning(false)
    }
  }

  const input = (ref: typeof camera, capture: boolean) => (
    <input
      ref={ref}
      type="file"
      accept="image/*"
      // "environment" opens the back camera on phones; without it the phone
      // offers the gallery (and the camera) instead.
      capture={capture ? "environment" : undefined}
      hidden
      onChange={(e) => {
        const f = e.target.files?.[0]
        if (f) void onFile(f)
        e.target.value = ""
      }}
    />
  )

  const screen = host.current?.closest(".screen") ?? null

  return (
    <div ref={host}>
      <div className="photorow">
        <div className="photo">
          {photo ? (
            <>
              <img src={photo} alt="Foto yang dipilih" />
              {scanning && (
                <>
                  <div className="scanline" />
                  <span className="scanbadge">🔎 Memindai…</span>
                </>
              )}
            </>
          ) : (
            <div className="ph">
              <div aria-hidden="true">🖼️</div>Belum ada foto
            </div>
          )}
        </div>
        <div className="photobtns">
          <button
            type="button"
            className="btn btn-secondary"
            disabled={!consent || scanning}
            onClick={() => open(camera.current)}
          >
            <span aria-hidden="true">📸</span>
            Kamera
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            disabled={!consent || scanning}
            onClick={() => open(gallery.current)}
          >
            <span aria-hidden="true">🖼️</span>
            Galeri
          </button>
        </div>
        {input(camera, true)}
        {input(gallery, false)}
      </div>
      <label className="chk consent">
        <input
          type="checkbox"
          checked={consent}
          onChange={(e) => agree(e.target.checked)}
        />
        <span>
          {analyze
            ? "Saya setuju foto dikirim ke server TropiCare untuk dianalisis, lalu langsung dihapus."
            : "Saya setuju memakai foto untuk skrining ini. Foto tetap di perangkat ini."}{" "}
          Foto tidak disimpan.{" "}
          <button
            type="button"
            className="linkbtn"
            onClick={() => setPrivacy(true)}
          >
            Baca privasi
          </button>
        </span>
      </label>
      {privacy &&
        screen &&
        createPortal(
          <Modal tab="PRIVASI" onClose={closePrivacy}>
            <PrivacyText />
          </Modal>,
          screen,
        )}
    </div>
  )
}
