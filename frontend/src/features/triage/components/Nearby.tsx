// Nearest facilities for a result route: name, distance, and one-tap WhatsApp /
// call and Google Maps directions. Progressive and consent-first: it only runs
// on its own when location was already granted during the quiz, and it never
// breaks the screen — on any failure it points to the plain Maps search link.
import { useCallback, useEffect, useState } from "react"

import { routeURL, telURL, waURL } from "../links"
import { cachedCoords, locateCoords } from "../location"
import {
  facilityKinds,
  fetchNearest,
  NEARBY_LIMIT,
  type Neighbour,
} from "../nearby"
import { Card, RED_TAB } from "./Ui"
import "@/styles/nearby.css"

const LOCATE_FAILED: Record<string, string> = {
  denied:
    "Izin lokasi ditolak. Pakai tombol peta di atas untuk mencari sendiri.",
  unsupported:
    "Perangkat ini tidak bisa membagikan lokasi. Pakai tombol peta di atas.",
  unavailable: "Lokasi belum bisa diambil. Pakai tombol peta di atas, ya.",
}

const KIND_NOUN: Record<string, string> = {
  rs: "rumah sakit",
  puskesmas: "Puskesmas",
  apotek: "apotek",
}

type Status = "idle" | "locating" | "loading" | "ready" | "empty" | "error"

export function NearestFacilities({
  route,
  tone,
}: {
  route: string
  tone?: "red"
}) {
  const [status, setStatus] = useState<Status>("idle")
  const [items, setItems] = useState<Neighbour[]>([])
  const [note, setNote] = useState<string | null>(null)
  const noun = KIND_NOUN[facilityKinds(route)[0]] ?? "faskes"

  const run = useCallback(async () => {
    setStatus("locating")
    setNote(null)
    const r = await locateCoords()
    if (!r.ok) {
      setNote(LOCATE_FAILED[r.reason])
      setStatus("error")
      return
    }
    setStatus("loading")
    try {
      const found = await fetchNearest(route, r.coords)
      setItems(found)
      setStatus(found.length ? "ready" : "empty")
    } catch {
      setStatus("error")
    }
  }, [route])

  // Auto-run only when the patient already shared their location this session.
  useEffect(() => {
    if (cachedCoords()) void run()
  }, [run])

  return (
    <Card
      tab="FASILITAS TERDEKAT"
      tabStyle={tone === "red" ? RED_TAB : undefined}
      className="nf"
    >
      {status === "idle" && (
        <>
          <p className="nf-lead">
            Izinkan lokasi untuk melihat {NEARBY_LIMIT} {noun} terdekat dari
            tempatmu.
          </p>
          <button type="button" className="btn btn-primary" onClick={run}>
            📍 Temukan {noun} terdekat
          </button>
        </>
      )}

      {(status === "locating" || status === "loading") && (
        <p className="nf-lead" aria-live="polite">
          {status === "locating"
            ? "Mencari lokasimu…"
            : `Mencari ${noun} terdekat…`}
        </p>
      )}

      {status === "empty" && (
        <p className="nf-lead">
          Belum ada data {noun} di sekitarmu. Pakai tombol peta di atas, ya.
        </p>
      )}

      {status === "error" && (
        <p className="nf-lead">
          {note ?? "Gagal mencari faskes terdekat. Pakai tombol peta di atas."}
        </p>
      )}

      {status === "ready" && (
        <>
          <ul className="nf-list">
            {items.map((f) => (
              <FacilityRow key={f.satusehat_id} f={f} />
            ))}
          </ul>
          <p className="nf-note">
            Lokasimu hanya dipakai untuk menghitung jarak, tidak disimpan.
          </p>
        </>
      )}
    </Card>
  )
}

function kmLabel(km: number): string {
  return km < 1
    ? `${Math.max(10, Math.round((km * 1000) / 10) * 10)} m`
    : `${km.toFixed(1)} km`
}

function FacilityRow({ f }: { f: Neighbour }) {
  const sub =
    [f.address, f.city_name].filter(Boolean).join(" · ") || f.jenis_sarana_nama
  return (
    <li className="nf-item">
      <div className="nf-head">
        <b>{f.name}</b>
        <span className="nf-dist">{kmLabel(f.distance_km)}</span>
      </div>
      {sub && <small className="nf-sub">{sub}</small>}
      <div className="nf-actions">
        {f.whatsapp ? (
          <a
            className="btn btn-wa"
            href={waURL(f.whatsapp)}
            target="_blank"
            rel="noopener"
          >
            💬 WhatsApp
          </a>
        ) : (
          f.phone && (
            <a className="btn btn-secondary" href={telURL(f.phone)}>
              📞 Telepon
            </a>
          )
        )}
        <a
          className="btn btn-secondary"
          href={routeURL(f)}
          target="_blank"
          rel="noopener"
        >
          🧭 Rute
        </a>
      </div>
    </li>
  )
}
