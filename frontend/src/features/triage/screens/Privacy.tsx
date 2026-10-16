import { Link } from "@tanstack/react-router"

import { Sparkles } from "../components/Art"
import { PrivacyText } from "../components/Privacy"
import { Card } from "../components/Ui"

export function PrivacyScreen() {
  return (
    <div className="screen bg-result">
      <Sparkles n={10} />
      <div className="hud">
        <Link className="icon-btn" to="/" aria-label="Beranda">
          ⌂
        </Link>
        <div className="htitle">Privasi</div>
      </div>
      <div className="rscroll">
        <Card tab="KEBIJAKAN PRIVASI" className="card-solo">
          <PrivacyText />
        </Card>
      </div>
    </div>
  )
}
