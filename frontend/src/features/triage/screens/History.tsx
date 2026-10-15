// "Riwayat skrining": the logged-in user's saved screenings, newest first.
// The list has no raw answers (ScreeningHistoryItem), so there is no detail
// view: date, path, route, top estimate, and delete.
import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { useState } from "react"

import { type ScreeningHistoryItem, UsersService } from "@/client"
import { useFlow } from "../api"
import { Sparkles } from "../components/Art"
import { Card, Modal, toast } from "../components/Ui"
import { sfx } from "../fx"

const PAGE = 20

const PATH_LABEL: Record<string, string> = {
  infection: "🤒 Jalur infeksi",
  chronic: "🩺 Risiko jangka panjang",
}

const dateLabel = (iso?: string | null) =>
  iso
    ? new Date(iso).toLocaleString("id-ID", {
        dateStyle: "medium",
        timeStyle: "short",
      })
    : "-"

export function HistoryScreen() {
  const queryClient = useQueryClient()
  const [limit, setLimit] = useState(PAGE)
  const [confirm, setConfirm] = useState<ScreeningHistoryItem | null>(null)
  const infection = useFlow("infection").flow
  const chronic = useFlow("chronic").flow
  const flows: Record<string, typeof infection> = { infection, chronic }

  const list = useQuery({
    queryKey: ["myScreenings", limit],
    queryFn: async () =>
      (await UsersService.readMyScreenings({ query: { skip: 0, limit } })).data,
    // "Muat lagi" keeps the current list on screen while the longer one loads.
    placeholderData: keepPreviousData,
  })

  const remove = useMutation({
    mutationFn: (id: string) =>
      UsersService.deleteMyScreening({ path: { screening_id: id } }),
    onSuccess: () => {
      sfx.ding()
      toast("🗑 Skrining dihapus dari riwayat")
    },
    onError: () => toast("Gagal menghapus. Coba lagi nanti."),
    onSettled: () => {
      setConfirm(null)
      queryClient.invalidateQueries({ queryKey: ["myScreenings"] })
    },
  })

  const rows = list.data?.data ?? []
  const more = (list.data?.count ?? 0) > rows.length

  const estimate = (s: ScreeningHistoryItem) => {
    if (s.unknown) return "Belum dapat ditentukan"
    if (!s.top_disease) {
      return s.route === "red" ? "Ada tanda bahaya" : "Belum dapat ditentukan"
    }
    return flows[s.flow_id]?.diseases[s.top_disease]?.name ?? s.top_disease
  }

  return (
    <div className="screen bg-result">
      <Sparkles n={10} />
      <div className="hud">
        <Link className="icon-btn" to="/" aria-label="Beranda">
          ⌂
        </Link>
        <div className="htitle">Riwayat Skrining</div>
      </div>
      <div className="rscroll">
        <div className="hist-page">
          <Card tab="RIWAYAT SKRINING">
            {list.isPending ? (
              <p className="hist-empty">Memuat riwayat…</p>
            ) : list.isError ? (
              <>
                <p className="hist-empty">Gagal memuat riwayat.</p>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => list.refetch()}
                >
                  ↻ Coba lagi
                </button>
              </>
            ) : rows.length === 0 ? (
              <>
                <p className="hist-empty">
                  Belum ada skrining yang disimpan. Selesaikan skrining, lalu
                  tekan "Simpan ke riwayatku" di halaman hasil.
                </p>
                <Link className="btn btn-primary" to="/">
                  🤒 Mulai skrining
                </Link>
              </>
            ) : (
              <>
                <ul className="hist-list">
                  {rows.map((s) => {
                    const route = flows[s.flow_id]?.routes[s.route]
                    return (
                      <li className="hist-item" key={s.id}>
                        <div className="hist-meta">
                          <span>{dateLabel(s.created_at)}</span>
                          <span>{PATH_LABEL[s.flow_id] ?? s.flow_id}</span>
                          <span className={`hist-badge rt-${s.route}`}>
                            {route ? `${route.emoji} ${route.name}` : s.route}
                          </span>
                        </div>
                        <div className="hist-est">
                          <b>{estimate(s)}</b>
                        </div>
                        <div className="hist-actions">
                          <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => setConfirm(s)}
                          >
                            🗑 Hapus
                          </button>
                        </div>
                      </li>
                    )
                  })}
                </ul>
                {more && (
                  <button
                    type="button"
                    className="btn btn-secondary hist-more"
                    disabled={list.isFetching}
                    onClick={() => setLimit((n) => n + PAGE)}
                  >
                    {list.isFetching ? "Memuat…" : "Muat lagi"}
                  </button>
                )}
              </>
            )}
          </Card>
        </div>
        <p className="footdisc">
          ⚠️ Riwayat ini berisi hasil skrining awal, bukan diagnosis dokter.
        </p>
      </div>

      {confirm && (
        <Modal
          tab="HAPUS SKRINING"
          onClose={() => setConfirm(null)}
          actions={
            <>
              <button
                type="button"
                className="btn btn-primary"
                disabled={remove.isPending}
                onClick={() => remove.mutate(confirm.id)}
              >
                {remove.isPending ? "Menghapus…" : "Ya, hapus"}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setConfirm(null)}
              >
                Batal
              </button>
            </>
          }
        >
          <h3>Hapus skrining ini?</h3>
          <p className="saveinfo">
            {dateLabel(confirm.created_at)} · {estimate(confirm)}. Yang sudah
            dihapus tidak bisa dikembalikan.
          </p>
        </Modal>
      )}
    </div>
  )
}
