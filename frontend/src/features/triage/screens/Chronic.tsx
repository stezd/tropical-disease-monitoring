// Chronic path placeholder. Status ⏳: waiting for DR (docs/Blueprint-Kronis.md).
// When content exists: add backend/app/triage/content/chronic/*.json, add "chronic" to
// FLOW_IDS, and render QuizScreen with that flow here.
import { Link } from "@tanstack/react-router"

import { Mascot, Sparkles } from "../components/Art"
import { Card } from "../components/Ui"

export function ChronicScreen() {
  return (
    <div className="screen bg-quiz">
      <Sparkles n={18} />
      <div className="hud">
        <Link className="icon-btn" to="/" aria-label="Kembali">
          ‹
        </Link>
        <div className="htitle">Risiko Jangka Panjang</div>
      </div>
      <div className="qlayout">
        <div className="mrow">
          <Mascot className="m-sm" />
          <div className="bubble">
            <p>
              Fitur ini sedang <b>disiapkan</b> bersama dokter 🩺
            </p>
          </div>
        </div>
        <div className="qmain">
          <div className="qwrap">
            <Card tab="SEGERA HADIR" className="pop">
              <h2 className="qt">Cek risiko penyakit jangka panjang</h2>
              <p className="saveinfo" style={{ marginTop: 8 }}>
                Pertanyaannya masih disusun oleh tim dokter. Sementara itu,
                kalau kamu sedang merasa sakit, pakai skrining infeksi tropis.
              </p>
            </Card>
          </div>
          <div className="foot">
            <Link className="btn big btn-purple" to="/">
              ‹ Kembali ke beranda
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
