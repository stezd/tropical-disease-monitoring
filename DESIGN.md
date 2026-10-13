# DESIGN.md — TropiCare

Visual guide for the React app. Source: [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Open it next to this file.

## Feel

- Warm, playful, game-like (Quizizz / Akinator). Never scary.
- Big rounded shapes, chunky 3D buttons, bright gradients on a purple sky.
- Mascot **Kak Tropi** talks to the user in speech bubbles.
- Exception: the **red route** is calm and serious. No game elements.

## Colors

Put these in `frontend/src/index.css` as CSS variables and map them to the shadcn theme (`--primary` = purple, `--card` = white, etc.).

| Token | Hex | Use |
| --- | --- | --- |
| `ink` | `#3A2E6E` | Main text |
| `ink2` | `#6E6898` | Secondary text |
| `muted` | `#9A95BF` | Hints, empty states |
| `card` | `#FFFFFF` | Cards |
| `soft` | `#F6F3FF` | Option and input backgrounds |
| `line` | `#E7E2FF` | Borders |
| `tabbg` | `#EEEBFF` | Card tab |
| `purple` / `purple2` / `purpleSh` | `#8B4DFF` / `#AE73FF` / `#6427D6` | Primary button, selected state |
| `teal` / `teal2` / `tealSh` | `#26C4B1` / `#55E2D1` / `#148C7F` | Secondary button |
| `gold` / `goldSh` | `#FFC531` / `#E09A0E` | Finished stages |
| `green` | `#2CC487` | "Safe / none" option, success |
| `red` | `#FF4B5C` | Danger option, emergency |

**Route colors** (gradient top → bottom):

| Route | Colors | Icon |
| --- | --- | --- |
| HIJAU | `#4FDDA0` → `#1FA86E` | 🌿 |
| KUNING | `#FFCB57` → `#F59B0B` | 🏥 |
| KUNING KHUSUS | `#FFA45C` → `#E8662A` | 🎯 |
| MERAH | `#FF7280` → `#E0283F` | 🚨 |

**Screen backgrounds:**

- Home: `#6C5CE7` + SVG scene (hills, sun, sparkles)
- Quiz: `#4B44C4 → #6E4FDB → #A85ED0 → #F07F9A → #FFAE7E` (sunset)
- Thinking: radial `#7A4FE8 → #3C2A9C → #221A63`
- Result: `#4B44C4 → #7550DE → #B862CC → #FF9A8F`
- Red route: `#B3122E → #E5313F → #FF6A5B`

## Type

- **Headings, buttons, numbers:** Fredoka 600–700
- **Body:** Nunito 700–900. Body text is bold by default; keep it.
- Load both from Google Fonts.

| Element | Mobile | ≥640px |
| --- | --- | --- |
| Question | 17.5px | 20px |
| Option text | 13.5px (tile 12.5px) | 13px |
| Button | 17px (big: 19–21px) | same |
| Bubble | 13–13.5px | 14–15.5px |
| Hint / small | 11.5–12.5px | same |

## Shape and depth

- Radius: cards 26px, buttons 18–20px, options 16px, small icons 12px, pills 999px.
- **3D effect = solid bottom shadow**, no blur: `box-shadow: 0 5px 0 <darker shade>, 0 10px 20px <soft glow>`.
- Pressed: move down 4px, shadow shrinks to 1px.
- Borders on options and inputs: 2.5px `line`.

## Components

| Component | What it looks like |
| --- | --- |
| **Card with tab** | White card, label pill sitting on the top edge, centered (`tabbg`, Fredoka, letter-spaced) |
| **3D button** | Full width on mobile, gradient + bottom shadow. Variants: purple (main), teal, red, white, ghost, dark |
| **Option** | Row with icon square + text + check circle. Selected → purple border and light purple fill |
| **Option tile** | Icon on top, text below. 2 columns mobile, 4 on ≥640px. Long options span full width |
| **Danger option** | Red when selected. **Safe/none option**: green tint |
| **Category box** | Big colored gradient tile (one color per complaint group) |
| **Speech bubble** | White, rounded 18px, tail pointing to mascot |
| **Mascot** | SVG, gentle bob + blink + wave animation |
| **HUD** | Top bar: back button, stage dots with lines |
| **Stage dots** | Empty = faint white, current = glowing white, done = gold with ✓ |
| **Input** | `soft` background, big Fredoka number, purple border on focus |
| **Note** | Yellow dashed box for tips; purple variant for info |
| **Warning box** | Yellow / red / blue, icon left |
| **Modal** | Card with tab + round close button top right, dark blurred backdrop |
| **Toast** | Dark pill bottom center |

## Layout

- **<640px (phone, main target):** one column, button pinned at bottom, as little scrolling as possible.
- **≥640px:** content max 700px centered, bigger fonts, tiles in 4 columns, button aligned right (min 300px).
- **≥960px:** quiz becomes 2 columns: mascot + bubble on the left (280px), card on the right. Result and red route in 2 columns.
- Respect `safe-area-inset` top and bottom.
- Check every screen at 390px, 768px, 1440px.

## Motion

- Card enters with a small pop (bounce).
- Confetti at the end (not on red route).
- Mascot bobs, blinks, hops on answer.
- Respect `prefers-reduced-motion`: turn animations off.

## Changes from the prototype

Don't copy these from the HTML:

- **No disease tags under options.** Remove `.tag` and the "Mode Presentasi" toggle.
- **Pain scale = faces 0–10:** vertical, next to the body map. Buttons 0–10 (0 on top), colored green to red. On 0, 2, 4, 6, 8, 10: label on the left ("Tidak sakit" to "Sakit sekali"), face on the right. Numbers and faces can both be tapped. Nothing selected at start. The prototype is already updated (`painScale()`), so copy this one as is.
- **Red route:** no confetti. Big call 119 button, plus 119 and 112 as copyable text.
- **No "XGBoost", model names, or "probability"** wording. Show "skor kecocokan".
- **New screens** (not in prototype), built in the same style:
  - Home: choose path ("Saya sedang sakit" / "Cek risiko penyakit jangka panjang").
  - First step: age + sex.
  - Result: "Buat janji dokter (Mobile JKN)" button.
  - Login / register / profile (no saved results or history).
  - Photo upload step (infection path).

## Accessibility

- Text on white must use `ink` or `ink2`, not `muted`, for anything important.
- Tap targets at least 40px.
- Don't rely on color alone: routes also have a name and icon.
- Emoji are decoration; the text must make sense without them.
