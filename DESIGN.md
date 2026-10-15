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
| `purple` / `purple2` / `purpleSh` | `#8B4DFF` / `#AE73FF` / `#6427D6` | Every button (primary and secondary), selected state |
| `teal` / `teal2` / `tealSh` | `#26C4B1` / `#55E2D1` / `#148C7F` | Accents only. Not for buttons |
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

## Units

- **Use `rem` for font sizes, spacing, and max widths** in new or changed code. 1rem = 16px.
- Never set `font-size` on `html`. Leave it at the browser default, so a patient who set bigger text in their phone or browser gets bigger text here too.
- Keep `px` for borders (2.5px), shadow offsets (the 3D bottom shadow), and hairlines. These should not grow with text.
- Breakpoints in rem: **mobile** < `40rem` (640px), **desktop** ≥ `40rem`, **wide desktop** ≥ `60rem` (960px). Tablet uses the desktop layout. In Tailwind, `sm:` is already 40rem; set `--breakpoint-lg: 60rem` in `@theme` so `lg:` matches 960px (Tailwind's default `lg` is 64rem).
- The prototype is in px. Values below are the prototype values rounded to whole pixels, half pixels rounded up (17.5px → 18px). `frontend/src/styles/*.css` is in rem and uses these values through tokens in `tropicek.css` `:root`: `--fs-2xs` … `--fs-5xl` (Type), `--sp-*` and `--gutter` (Spacing), `--r-*` (radii), `--tap` / `--h-ctl` / `--h-ctl-lg` (control heights). Sizes do not step up globally on desktop; only the elements in the Type table that list a desktop size grow.
- Test once with the browser font size at 20px: text may wrap, but nothing should clip or overlap. Boxes that hold text grow with it (use `min-height`, not fixed `height`).

## Type

- **Headings, buttons, numbers:** Fredoka 600–700
- **Body:** Nunito 700–900. Body text is bold by default; keep it.
- Load both from Google Fonts.

**Scale.** Use only these sizes. Most are Tailwind defaults; add `--text-2xs` and `--text-note` to `@theme`.

| Token | rem | px |
| --- | --- | --- |
| `2xs` | 0.6875rem | 11 |
| `xs` | 0.75rem | 12 |
| `note` | 0.8125rem | 13 |
| `sm` | 0.875rem | 14 |
| `base` | 1rem | 16 |
| `lg` | 1.125rem | 18 |
| `xl` | 1.25rem | 20 |
| `2xl` | 1.5rem | 24 |
| `3xl` | 1.875rem | 30 |
| `4xl` | 2.25rem | 36 |
| `5xl` | 3rem | 48 |

**Where each size goes.** Desktop = ≥40rem. A third value is for ≥60rem.

| Element | Font | Mobile | Desktop | Line height |
| --- | --- | --- | --- | --- |
| App title (home ribbon) | Fredoka 700 | `3xl` 1.875rem | `5xl` 3rem | 1.1 |
| Red route heading | Fredoka 700 | `3xl` 1.875rem | `3xl` · `4xl` 2.25rem | 1.1 |
| Result heading (top estimate) | Fredoka 600 | `2xl` 1.5rem | same | 1.2 |
| Route title, banner, modal title | Fredoka 600–700 | `xl` 1.25rem | same | 1.2 |
| Question | Fredoka 600 | `lg` 1.125rem | `xl` 1.25rem | 1.25 |
| HUD title | Fredoka 600 | `lg` 1.125rem | same | 1.2 |
| Sub-question, card section title, category title | Fredoka 600 | `base` 1rem | same | 1.2 |
| Button | Fredoka 600 | `lg` 1.125rem (big: `xl` 1.25rem) | same | 1.2 |
| Number in input | Fredoka 600 | `2xl` 1.5rem (temperature `3xl`) | same | 1.2 |
| Card tab | Fredoka 600, letter-spacing 0.0625rem | `sm` 0.875rem | same | 1 |
| Option text | Nunito 700 | `sm` 0.875rem | same | 1.3 |
| Option tile text | Nunito 700 | `note` 0.8125rem | same | 1.25 |
| Bubble | Nunito 700 | `note` 0.8125rem (home: `sm`) | `sm` · `base` 1rem | 1.45 |
| Body: modal, result lists, warnings | Nunito 700–800 | `sm` 0.875rem | same | 1.45 |
| Hint, field label, note, chip | Nunito 800–900 | `note` 0.8125rem | same | 1.35 |
| Option description, disclaimer, tags, counter | Nunito 800 | `xs` 0.75rem | same | 1.4 |
| Pain scale labels, ring caption | Nunito 900 | `2xs` 0.6875rem | `xs` 0.75rem | 1.15 |

- Nothing smaller than `2xs` (11px). The prototype's 9.5–10.5px labels go up to 11px.
- Emoji and icons scale in rem too: option icon 1.25rem, category icon 1.875rem → 2.375rem on desktop, red route siren 4.5rem → 6rem at ≥60rem.

## Spacing

Tailwind's spacing unit is 0.25rem (4px): `p-3` = 0.75rem. Use multiples of 0.25rem; 0.125rem and 0.375rem only for tight spots inside small components.

**Page**

| Where | Mobile | Desktop |
| --- | --- | --- |
| Screen side gutter (quiz, result, HUD) | 1rem | 1.5rem · 1.75rem |
| Home side and bottom padding | 1.5rem | same |
| Content max width (quiz, ≥40rem) | full width | 43.75rem (700px) |
| Quiz at ≥60rem | — | max 70rem; mascot column 17.5rem, gap 2.5rem |
| Result and red route columns at ≥60rem | stacked, max 37.5rem | max 67.5rem, gap 1.75rem |
| Footer button bar | 0.375rem top, 0.75rem bottom; back button left, Lanjut fills the rest, 0.75rem gap | 0.5rem top, 1.5rem bottom; back + Lanjut right-aligned, Lanjut min width 18.75rem |
| Home buttons | full width | max 25rem |
| Modal | 1.5rem from screen edge, max width 28.75rem | same |

Always add `env(safe-area-inset-*)` on top of the top and bottom padding: `padding-bottom: max(0.75rem, env(safe-area-inset-bottom))`.

**Cards**

| Where | Mobile | Desktop |
| --- | --- | --- |
| Card padding | 1.75rem top (room for the tab), 0.875rem sides and bottom | 2rem top, 1.25rem sides and bottom |
| Between cards | 2rem (the tab sits in this gap) | same |
| Question → hint | 0.125rem | same |
| Hint → options | 0.625rem | same |
| Section inside a card (sub-question, result heading) | 0.75rem above, 0.5rem below | same |
| Note or warning below content | 0.5rem–0.625rem above | same |

**Components**

| Where | Mobile | Desktop |
| --- | --- | --- |
| Between options | 0.5rem | 0.625rem (2 columns) |
| Between tiles | 0.5rem (5-column tiles: 0.375rem) | same |
| Between category boxes | 0.625rem | same |
| Option padding | 0.5rem, icon-to-text gap 0.625rem | same |
| Tile padding | 0.5rem 0.375rem | 0.75rem 0.5rem |
| Option icon square | 2.25rem (tile 2rem) | 2.25rem (tile 2.5rem) |
| Button padding | 0.75rem 1rem, min height 3rem | same |
| Back button (footer) | min width 3rem, 0.875rem left / 1rem right padding | same |
| Big button padding | 0.875rem 1rem, min height 3.5rem | same |
| Between stacked buttons | 0.875rem | same |
| Bubble padding | 0.5rem 0.75rem | 0.625rem 0.875rem · 0.875rem 1rem |
| Input padding | 0.625rem 0.75rem | same |
| Chips | 0.375rem gap, 0.3125rem 0.75rem padding | same |
| Lists (todo, why, steps) | 0.5rem gap | same |

If a value you need is not here, take it from the prototype, convert to rem, and round to the nearest 0.25rem.

## Shape and depth

- Radius: cards 1.625rem (26px), buttons 1.25rem (20px), options and inputs 1rem (16px), small icons 0.75rem (12px), pills 999px.
- **3D effect = solid bottom shadow**, no blur: `box-shadow: 0 5px 0 <darker shade>, 0 10px 20px <soft glow>`.
- Pressed: move down 4px, shadow shrinks to 1px.
- Borders on options and inputs: 2.5px `line`.

## Components

| Component | What it looks like |
| --- | --- |
| **Card with tab** | White card, label pill sitting on the top edge, centered (`tabbg`, Fredoka, letter-spaced) |
| **3D button** | Full width on mobile, gradient + bottom shadow. **Every button is purple**: primary = `#8B4DFF → #7436EE` with glow; secondary / ghost / back / WhatsApp = deeper `#7A3DF2 → #6427D6`, white text. Only two exceptions: **Telepon 119** stays red (white with red text on the red screen) and **Mobile JKN** stays JKN blue |
| **Footer bar** (`.foot`) | `‹ Kembali` (`.btn-back`, left, hugs its text) + Lanjut (fills the rest). Under 23.125rem only `‹` shows; the button keeps `aria-label="Kembali"`. ≥40rem: both right-aligned, Lanjut min 18.75rem. First step has no back button |
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
| **Privacy gate** (`.consent-gate`) | First card after choosing a path. Question + hint, the privacy text in a scroll box (`.consent-text`, soft background, max height ~18rem), one checkbox row (`.chk`) "Saya setuju", and a small location pill (`.loc-status`, green when found, yellow when denied). Lanjut is disabled until the box is ticked. If location is denied, an optional province picker appears (`.reveal-in`). Max 3 fields, like every page |
| **Revealed field** (`.reveal-in`) | A field that appears after earlier answers fades and slides in 0.5rem. No motion on the red route or with reduced motion |
| **Facility card** (`.nf-item`) | Soft box inside the "FASILITAS TERDEKAT" card: name, distance pill, type + address, then buttons "Cari di Google Maps" and "Kirim rangkuman via WhatsApp" (or "Telepon"). Buttons stack on phones, two columns from 40rem |
| **History list** (`.hist-list` / `.hist-item`) | `/riwayat`, logged-in users only. One white card with tab "RIWAYAT SKRINING"; each item is a soft box: date + path + route badge (route color, icon and name), top estimate + skor kecocokan pill, then "Buka" / "Hapus" side by side. Game style, not an admin table |
| **Google sign-in** (`.gbtn-wrap`, `.or-sep`) | On login and signup: Google's own button centered at full width, then an "atau" divider (hairline both sides), then the email + password form. Hidden when no Google client id is set |

## Layout

- **<40rem (640px, phone, main target):** one column, button pinned at bottom, as little scrolling as possible.
- **≥40rem:** content max 43.75rem centered, tiles in 4 columns, footer buttons aligned right (Lanjut min 18.75rem).
- **Home** is one centered column at every size: ribbon, mascot + bubble, then the path buttons **under** the mascot (max 25rem), disclaimer at the bottom. On phones the column is pinned to the top (1.5rem under the ribbon), not vertically centered. From 40rem the mascot + buttons group sits in the middle of the free space. No two-column home.
- **≥60rem (960px):** quiz becomes 2 columns: mascot + bubble on the left (17.5rem), card on the right. Result and red route in 2 columns.
- **Max 3 fields per page.** A field is one thing to answer (an input, a choice group, a checkbox). If a step needs a 4th or later field, it appears in the same card ("extended card", `.reveal-in`) only after the first three are filled. Optional extras that are not needed together go to their own step (e.g. the chronic path's "Pemeriksaan opsional").
- Sizes and gaps: see **Type** and **Spacing**.
- Respect `safe-area-inset` top and bottom.
- Check every screen at 390px, 768px, 1440px.

## Motion

- Card enters with a small pop (bounce). A field that appears later uses a smaller fade + slide (`.reveal-in`).
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
  - Privacy gate: the first card after choosing a path (see Components).
  - Login / register (email + password, or Google) / profile.
  - History (`/riwayat`): saved screenings for logged-in users. Guests are invited to make an account instead of a save button.
  - No photo step: the photo feature was removed.

## Accessibility

- Text on white must use `ink` or `ink2`, not `muted`, for anything important.
- Tap targets at least 2.5rem (40px). Small controls get an invisible hit area (the settings switch looks 1.875rem tall but taps 2.75rem); pain scale numbers are at least 2.5rem.
- Don't rely on color alone: routes also have a name and icon.
- Emoji are decoration; the text must make sense without them.
