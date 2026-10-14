// Result page: add (or replace) a photo after the quiz. The analysis adds finding
// IDs to the stored answers; Result's score query is keyed on the answers, so it
// refetches by itself and this card reports what changed.
//
// Shown only when the server can analyze photos (flow.photo_analysis). Without
// an analyzer a photo cannot change the result, and the findings were already
// asked in the photo step, so the card stays hidden. Never on the red route.
import { keepPreviousData, useQuery } from "@tanstack/react-query"
import { useMemo, useState } from "react"

import type { FlowPublic } from "@/client"
import { scoreAnswers, scoreKey } from "../api"
import { toApi } from "../model"
import { quiz, useQuiz } from "../store"
import {
  mergeFindings,
  type PhotoOutcome,
  PhotoPicker,
  photoWasAdded,
} from "./PhotoPicker"
import { Card } from "./Ui"

type Status =
  | { kind: "idle" }
  | { kind: "added"; ids: string[]; before: string[] }
  | { kind: "same"; ids: string[] }
  | { kind: "none" }
  | { kind: "too_big" }
  | { kind: "error" }
  | { kind: "undone" }

export function PhotoCard({
  flow,
  route,
}: {
  flow: FlowPublic
  /** Current result route; the card is hidden on "red". */
  route: string
}) {
  const { answers } = useQuiz()
  const [status, setStatus] = useState<Status>({ kind: "idle" })
  // Same query as the result page: tells us when the new result is in.
  const api = useMemo(() => toApi(answers), [answers])
  const score = useQuery({
    queryKey: scoreKey(api, flow.id),
    queryFn: () => scoreAnswers(api, flow.id),
    staleTime: Number.POSITIVE_INFINITY,
    placeholderData: keepPreviousData,
  })
  const [added] = useState(photoWasAdded)

  if (!flow.photo_analysis || route === "red") return null

  // Same wording as the photo step (flow.json step_text.q10).
  const what = flow.step_text?.q10?.title ?? "Foto ruam, luka, atau mata"
  const textOf = (id: string) =>
    flow.findings.find((o) => o.id === id)?.text ?? id

  const onAnalyzed = (o: PhotoOutcome) => {
    if (o.kind !== "found") return setStatus(o)
    const before = quiz.get().answers.findings
    const fresh = o.ids.filter((x) => !before.includes(x))
    if (!fresh.length) return setStatus({ kind: "same", ids: o.ids })
    quiz.answer((prev) => ({
      ...prev,
      findings: mergeFindings(prev.findings, o.ids),
    }))
    setStatus({ kind: "added", ids: fresh, before })
  }

  const undo = () => {
    if (status.kind !== "added") return
    quiz.answer((prev) => ({ ...prev, findings: status.before }))
    setStatus({ kind: "undone" })
  }

  const updating = score.isFetching
  const failed = score.isError && !score.isFetching

  return (
    <Card tab={added ? "GANTI FOTO" : "TAMBAH FOTO"} className="photocard">
      <p className="saveinfo">
        {added
          ? "Mau coba foto lain? Kak Tropi akan memeriksa temuan yang terlihat dan memperbarui hasil."
          : `Belum menambah foto? ${what} bisa membantu Kak Tropi memperbarui hasil. Boleh dilewati.`}
      </p>
      <PhotoPicker flow={flow} onAnalyzed={onAnalyzed} />
      {status.kind !== "idle" && (
        <div
          className={`photostatus ${failed || status.kind === "error" || status.kind === "too_big" ? "err" : status.kind === "added" && !updating ? "ok" : ""}`}
          role="status"
        >
          {status.kind === "added" && (
            <>
              {updating
                ? "Memperbarui hasil…"
                : failed
                  ? "Temuan foto ditambahkan, tapi hasil gagal diperbarui."
                  : "✔ Hasil diperbarui dengan temuan foto:"}
              <ul>
                {status.ids.map((id) => (
                  <li key={id}>{textOf(id)}</li>
                ))}
              </ul>
              {failed && (
                <button
                  type="button"
                  className="linkbtn"
                  onClick={() => score.refetch()}
                >
                  ↻ Coba lagi
                </button>
              )}
              {!updating && !failed && (
                <button type="button" className="linkbtn" onClick={undo}>
                  Batalkan temuan foto
                </button>
              )}
            </>
          )}
          {status.kind === "same" && (
            <>
              Temuan di foto sudah ada di jawabanmu. Hasil tidak berubah.
              <ul>
                {status.ids.map((id) => (
                  <li key={id}>{textOf(id)}</li>
                ))}
              </ul>
            </>
          )}
          {status.kind === "none" &&
            "Tidak ada temuan yang terlihat di foto. Hasil tidak berubah."}
          {status.kind === "too_big" &&
            "Foto terlalu besar (maks. 8 MB). Coba foto lain."}
          {status.kind === "error" &&
            "Analisis foto gagal. Hasil tidak berubah. Coba lagi nanti."}
          {status.kind === "undone" &&
            (updating
              ? "Mengembalikan hasil…"
              : "Temuan foto dibatalkan. Hasil kembali seperti semula.")}
        </div>
      )}
    </Card>
  )
}
