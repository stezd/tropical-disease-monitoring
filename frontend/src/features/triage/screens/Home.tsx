import { Link, useNavigate } from "@tanstack/react-router"
import { useState } from "react"

import useAuth, { isLoggedIn } from "@/hooks/useAuth"
import { Mascot, Scene, Sparkles } from "../components/Art"
import { Modal, toast } from "../components/Ui"
import { sfx } from "../fx"
import { setSettings, useSettings } from "../settings"
import { quiz } from "../store"

export function HomeScreen() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [modal, setModal] = useState<"settings" | "profile" | null>(null)
  const loggedIn = isLoggedIn()

  const start = () => {
    sfx.tap()
    quiz.reset()
    navigate({ to: "/skrining" })
  }

  return (
    <div className="screen bg-home">
      <Scene />
      <Sparkles n={14} />
      <div className="hud">
        <button
          type="button"
          className="icon-btn"
          onClick={() => {
            sfx.tap()
            setModal("settings")
          }}
          aria-label="Pengaturan"
        >
          ⚙
        </button>
        <div style={{ flex: 1 }} />
      </div>
      <div className="home">
        <div className="ribbon">
          <b>
            Tropi<span>Care</span>
          </b>
          <small>Skrining Awal Penyakit Tropis</small>
        </div>
        <div className="hero">
          <Mascot className="m-hero" />
          <div className="bubble">
            <p>
              Halo! Aku <b>Kak Tropi</b> 🌺 Yuk main tebak-tebakan kesehatan
              bareng aku. Cuma ±3 menit!
            </p>
          </div>
        </div>
        <div className="home-btns">
          <button type="button" className="btn btn-purple big" onClick={start}>
            🤒 Saya sedang sakit
          </button>
          <Link className="btn btn-purple" to="/kronis" onClick={() => sfx.tap()}>
            🩺 Cek risiko penyakit jangka panjang
          </Link>
          {loggedIn && (
            <div className="row-links">
              <button
                type="button"
                className="btn btn-ghost"
                data-testid="user-menu"
                onClick={() => setModal("profile")}
              >
                👤 {user?.full_name || user?.email || "Akun saya"}
              </button>
            </div>
          )}
        </div>
        <p className="disc">🩺 Skrining awal · masuk akun bersifat opsional</p>
      </div>

      {modal === "settings" && <SettingsModal onClose={() => setModal(null)} />}
      {modal === "profile" && (
        <Modal
          tab="PROFIL"
          onClose={() => setModal(null)}
          actions={
            <>
              <Link className="btn btn-purple" to="/settings">
                ⚙ Pengaturan akun
              </Link>
              <button
                type="button"
                className="btn btn-teal"
                onClick={() => {
                  setModal(null)
                  logout()
                  toast("Kamu sudah keluar")
                }}
              >
                Keluar
              </button>
            </>
          }
        >
          <h3>Halo, {user?.full_name || user?.email}! 👋</h3>
          <p className="saveinfo">
            Akun hanya untuk masuk. Riwayat skrining belum disimpan di akun.
          </p>
        </Modal>
      )}
    </div>
  )
}

function SettingsModal({ onClose }: { onClose: () => void }) {
  const s = useSettings()
  const toggle = (k: "sound" | "vibrate") => {
    setSettings({ [k]: !s[k] })
    sfx.tap()
  }
  return (
    <Modal tab="PENGATURAN" onClose={onClose}>
      <div className="setrow">
        <span>🔊 Suara</span>
        <button
          type="button"
          role="switch"
          aria-checked={s.sound}
          aria-label="Suara"
          className={`tgl ${s.sound ? "on" : ""}`}
          onClick={() => toggle("sound")}
        />
      </div>
      <div className="setrow">
        <span>📳 Getar</span>
        <button
          type="button"
          role="switch"
          aria-checked={s.vibrate}
          aria-label="Getar"
          className={`tgl ${s.vibrate ? "on" : ""}`}
          onClick={() => toggle("vibrate")}
        />
      </div>
      <div className="setsec">
        Bahasa<span className="pill-teal">Indonesia</span>Wilayah
        <span className="pill-teal" style={{ marginBottom: 0 }}>
          Indonesia
        </span>
      </div>
    </Modal>
  )
}
