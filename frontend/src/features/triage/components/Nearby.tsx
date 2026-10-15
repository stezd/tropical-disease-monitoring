// Nearest facilities for a result route: name, distance, a Google Maps search,
// and "Kirim rangkuman via WhatsApp" (mobile number) or a call (landline).
// Location is asked at the privacy gate; when it was granted this card runs on
// its own. Otherwise "Lihat faskes terdekat" asks again. It never breaks the
// screen: on any failure it points to the plain Maps search link.
// Coordinates stay in memory on the device (location.ts); only the province
// name goes to our server, to list that province's facilities.
import { useCallback, useEffect, useState } from "react"

import { facilityName, mapsURL, routeURL, telURL, waURL } from "../links"
import { cachedCoords, locateCoords } from "../location"
import {
  facilityKinds,
  fetchNearest,
  NEARBY_LIMIT,
  type Neighbour,
  USE_SERVER,
} from "../nearby"
import { Card, RED_TAB } from "./Ui"
import "@/styles/nearby.css"

// How to turn location back on: browsers do not ask twice once it is blocked.
const ALLOW_HINT =
  "Untuk mengizinkan: ketuk ikon gembok atau ⓘ di sebelah alamat web, pilih Izin/Lokasi, lalu Izinkan. Setelah itu tekan tombol di bawah lagi."

const LOCATE_FAILED: Record<string, string> = {
  denied: `Izin lokasi ditolak. ${ALLOW_HINT}`,
  unsupported:
    "Perangkat ini tidak bisa membagikan lokasi. Cari lewat Google Maps saja, ya.",
  unavailable:
    "Lokasi belum bisa diambil. Coba lagi, atau cari lewat Google Maps.",
}

const KIND_NOUN: Record<string, string> = {
  rs: "rumah sakit",
  puskesmas: "Puskesmas",
  apotek: "apotek",
}

type Status = "idle" | "locating" | "loading" | "ready" | "empty" | "error"

export function NearestFacilities({
  route,
  mapsQuery,
  shareText,
  tone,
}: {
  route: string
  /** Plain Google Maps search used when location is not available. */
  mapsQuery: string
  /** Prefilled WhatsApp message (short screening summary, no identity). */
  shareText: string
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

  // Runs on its own only when location was already shared this session.
  useEffect(() => {
    if (cachedCoords()) void run()
  }, [run])

  const searchLink = (
    <a
      className="btn btn-secondary"
      href={mapsURL(mapsQuery)}
      target="_blank"
      rel="noopener"
    >
      🧭 Cari {noun} di Google Maps
    </a>
  )

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
            📍 Lihat faskes terdekat
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
        <>
          <p className="nf-lead">
            Belum ada data {noun} di sekitarmu. Cari lewat Google Maps, ya.
          </p>
          {searchLink}
        </>
      )}

      {status === "error" && (
        <>
          <p className="nf-lead" role="status">
            {note ??
              "Gagal mencari faskes terdekat. Cari lewat Google Maps, ya."}
          </p>
          <button type="button" className="btn btn-primary" onClick={run}>
            📍 Lihat faskes terdekat
          </button>
          {searchLink}
        </>
      )}

      {status === "ready" && (
        <>
          <ul className="nf-list">
            {items.map((f) => (
              <FacilityRow key={f.satusehat_id} f={f} shareText={shareText} />
            ))}
          </ul>
          <p className="nf-note">
            {USE_SERVER
              ? "Lokasimu dikirim ke server TropiCare hanya untuk menghitung jarak, tidak disimpan."
              : "Lokasimu hanya dipakai di perangkat ini untuk menghitung jarak, tidak dikirim atau disimpan."}
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

function FacilityRow({ f, shareText }: { f: Neighbour; shareText: string }) {
  const sub =
    [f.address, f.city_name].filter(Boolean).join(" · ") || f.jenis_sarana_nama
  return (
    <li className="nf-item">
      <div className="nf-head">
        <b>{facilityName(f)}</b>
        <span className="nf-dist">{kmLabel(f.distance_km)}</span>
      </div>
      {sub && <small className="nf-sub">{sub}</small>}
      <div className="nf-actions">
        <a
          className="btn btn-secondary"
          href={routeURL(f)}
          target="_blank"
          rel="noopener"
        >
          🧭 Cari di Google Maps
        </a>
        {f.whatsapp ? (
          <a
            className="btn btn-wa"
            href={waURL(f.whatsapp, shareText)}
            target="_blank"
            rel="noopener"
          >
            💬 Kirim rangkuman via WhatsApp
          </a>
        ) : (
          f.phone && (
            <a className="btn btn-secondary" href={telURL(f.phone)}>
              📞 Telepon
            </a>
          )
        )}
      </div>
    </li>
  )
}
