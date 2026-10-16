// Sound, vibration, confetti. Off switches live in Pengaturan (settings.ts).
// Never used on the red route (DESIGN.md: calm and serious).
import { getSettings } from "./settings"

let ctx: AudioContext | undefined

type Note = [freq: number, dur: number, type?: OscillatorType, vol?: number]

function tone(seq: Note[]) {
  if (!getSettings().sound) return
  try {
    ctx ??= new AudioContext()
    let t = ctx.currentTime
    for (const [f, d, type = "sine", v = 0.07] of seq) {
      const o = ctx.createOscillator()
      const g = ctx.createGain()
      o.type = type
      o.frequency.value = f
      g.gain.setValueAtTime(v, t)
      g.gain.exponentialRampToValueAtTime(0.0001, t + d)
      o.connect(g).connect(ctx.destination)
      o.start(t)
      o.stop(t + d + 0.02)
      t += d * 0.75
    }
  } catch {
    // Audio is decoration; ignore failures.
  }
}

export const sfx = {
  tap: () => tone([[660, 0.06, "triangle", 0.05]]),
  ding: () =>
    tone([
      [988, 0.08, "square", 0.025],
      [1319, 0.2, "square", 0.025],
    ]),
  win: () =>
    tone([
      [523, 0.13],
      [659, 0.13],
      [784, 0.13],
      [1047, 0.35],
    ]),
  alert: () =>
    tone([
      [440, 0.22, "sawtooth", 0.04],
      [330, 0.22, "sawtooth", 0.04],
      [440, 0.22, "sawtooth", 0.04],
      [330, 0.3, "sawtooth", 0.04],
    ]),
  think: () =>
    tone([
      [392, 0.1, "triangle", 0.03],
      [494, 0.1, "triangle", 0.03],
    ]),
}

export function vibrate(pattern: number | number[] = 12) {
  if (!getSettings().vibrate || !navigator.vibrate) return
  try {
    navigator.vibrate(pattern)
  } catch {
    // ignore
  }
}

export const reducedMotion = () =>
  window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ?? false

export function confetti(host: HTMLElement | null) {
  if (!host || reducedMotion()) return
  const cols = [
    "#FFC531",
    "#F06A6A",
    "#0F6B66",
    "#5FB3AA",
    "#FF8F3D",
    "#7AB8E8",
    "#3DDC84",
  ]
  for (let i = 0; i < 70; i++) {
    const c = document.createElement("i")
    c.className = "conf"
    c.style.left = `${Math.random() * 100}%`
    c.style.background = cols[i % cols.length]
    c.style.animationDuration = `${1.8 + Math.random() * 1.8}s`
    c.style.animationDelay = `${Math.random() * 0.6}s`
    c.style.transform = `rotate(${Math.random() * 360}deg)`
    host.appendChild(c)
    setTimeout(() => c.remove(), 4500)
  }
}
