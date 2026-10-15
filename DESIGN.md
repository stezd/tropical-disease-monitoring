# DESIGN.md — TropiCare

Visual guide for the React app. Source: [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Open it next to this file.

## Feel

- **Cheerful, soft, and confident.** Like a friendly wellness app: candy-pastel color blocks, one bright electric indigo for actions, pink for warmth. Still trustworthy: clean layout, dark navy text, nothing neon and nothing dark.
- Game-like (Quizizz / Akinator), never scary, never gloomy. If a screen looks grey or washed out, it is wrong.
- Big rounded shapes, chunky buttons, pill chips. The mascot **Kak Tropi** talks in speech bubbles.
- Serif type for headings, buttons, and body adds a serious, trustworthy note on top of the playful colors.
- Exception: the **red route** is calm and serious. No game elements.

**Color reference:** a periwinkle-and-pink wellness app (lavender backdrop, pink phone frame, pastel lavender and sky-blue cards, electric-indigo buttons and nav bar, pink heart mascot). Copy its palette and the way it uses color, not its layout.

## Colors

### Why the reference feels happy (keep these rules)

1. **Color lives in the surfaces, not in borders or shadows.** Cards are *filled* with pastel color (lilac, sky, pink). They are not white boxes with grey outlines. The color change separates them, so cards have no border and almost no shadow.
2. **The backdrop is a real color**, a mid-tone periwinkle, not white and not grey. White appears as the app "sheet" or as small elements sitting on a pastel card (pills, options, inputs).
3. **One vivid action color.** Electric indigo `#3F38E6`, flat and bright. Used for primary buttons, the selected state, round icon controls, and the footer bar. Nothing else is that saturated.
4. **Pink is the warm accent.** Frame, mascot details, hearts, celebratory tags. Small amounts, never for actions.
5. **No neutral grey anywhere.** Every "grey" is a lavender tint: hint text, empty states, disabled buttons, hairlines.
6. **Tags carry meaning through pastel pairs**: a pastel fill plus a stronger text color of the same hue (pink "High", yellow "Medium", blue "Routine" in the reference). Routes and warnings use the same idea.
7. **Dark navy text** on every pastel surface. White text only on indigo, on the red route, and on solid colors that pass contrast.

### Tokens

Put these in `frontend/src/index.css` as CSS variables and map them to the shadcn theme (`--primary` = `indigo`, `--background` = `sheet`, `--card` = `lilac`, `--secondary` = `indigo-soft`, `--accent` = `pink-soft`, `--border` = `lilac-line`).

**Base**

| Token | Hex | Use |
| --- | --- | --- |
| `backdrop` | `#B4A9F1` | Behind everything: Home sky, Thinking, desktop margins around the app column |
| `sheet` | `#FDFCFF` | The app "screen" behind cards (quiz, result, history, privacy) |
| `ink` | `#1C1B3F` | Main text (near-black navy) |
| `ink2` | `#55547F` | Secondary text |
| `muted` | `#9B98C6` | Hints, placeholders, disabled. Decoration only, never important text |
| `white` | `#FFFFFF` | Pills, options, inputs, bubbles sitting **on** a pastel card |

**Action (indigo)**

| Token | Hex | Use |
| --- | --- | --- |
| `indigo` | `#3F38E6` | Primary button, selected border, checkbox, focus ring, footer bar, current stage dot |
| `indigo-deep` | `#2D26C4` | Button bottom shade (3D), pressed state, links, bold words in bubbles, tab text |
| `indigo-mid` | `#8E88F0` | Done-stage lines, progress fill, icons on pastel |
| `indigo-soft` | `#DEDBFD` | Secondary button fill (text `indigo-deep`), selected option fill, chips, HUD icon buttons |

**Pastel surfaces** (cards are filled with these; alternate them so neighbouring cards differ)

| Token | Hex | Paired text | Use |
| --- | --- | --- | --- |
| `lilac` | `#EEE9FD` | `ink` | Default card, question card |
| `lilac-line` | `#DCD4FA` | — | The only hairline color (1px, rarely needed) |
| `sky` | `#D8EEFC` | `ink`, accent `#1F5F96` | Info cards, "Kenapa aku menebak ini?", facility cards |
| `pink-soft` | `#FDE3F1` | `ink`, accent `pink-deep` | Speech bubble on `sheet`, privacy key box, celebratory bits |
| `pink` | `#F7A8D0` | — | Mascot details, home frame, hearts, sparkles. Never text |
| `pink-deep` | `#B02566` | — | Text on `pink-soft` tags |
| `butter` | `#FFF3BF` | `#6E5100` | Tips note, "Medium"-style tags |
| `mint` | `#D6F5E7` | `#12673F` | "Safe / none" option, success, location found |

**Status**

| Token | Hex | Use |
| --- | --- | --- |
| `gold` | `#FFC94A` | Finished stage dot (✓ in `ink`) |
| `green` | `#1F9D66` | Success icon, safe option check |
| `red` | `#E8384F` | Danger option border, emergency. Red warning text `#B4142C` on `#FFE1E5` |

Contrast (measured, WCAG): `ink` 13.9:1 and `ink2` ≈6:1 on every pastel; white on `indigo` 7.2:1; `indigo-deep` on `indigo-soft` 7.2:1 and on white 9.6:1; every paired tag and route text 5.3–8:1; white on the MERAH gradient ≈5:1. `muted` is 2.7:1 on white: decoration only.

### Route colors

Routes use the same pastel-pair idea: a **pastel band** with a **solid icon chip** and dark text, so the result is clear but friendly. MERAH stays solid and serious.

| Route | Band (pastel) | Icon chip | Text | Icon |
| --- | --- | --- | --- | --- |
| HIJAU | `#D6F5E7` | `#1F9D66` | `#0F5A3A` | 🌿 |
| KUNING | `#FFF1B8` | `#F2B200` | `#5E4500` | 🏥 |
| KUNING KHUSUS | `#FFE2CC` | `#F07A2A` | `#7A3300` | 🎯 |
| MERAH | `#D42A42` → `#C8203A` (solid) | white | white | 🚨 |

### Screen backgrounds

- **Home:** `backdrop` `#B4A9F1` with a lighter glow at the top (`#C9C0F7`). Scene (hills, sun, sparkles) in pastel layers: `#CFC6F8`, `#E3DCFD`, `#FDE3F1`, `#D8EEFC`, a `pink` sun, white clouds. The title ribbon and buttons sit on it the way the phones sit on the reference backdrop.
- **Quiz, Result, History, Privacy:** `sheet` `#FDFCFF`, flat. All color comes from the pastel cards and the indigo actions. From 40rem, the area outside the content column is `backdrop`, and the column is a `sheet` panel with radius 2rem and a 0.5rem `pink` frame (the reference's phone frame). No frame on phones.
- **Thinking:** `backdrop` with a radial `#C9C0F7` glow behind the orb. Steps are white pills; the running step is `indigo-soft`, done steps get a `mint` check.
- **Red route:** solid `#C8203A → #D42A42` (white text passes 4.5:1 across the whole gradient). Calm: no sparkles, no pink.

### How surfaces stack

`backdrop` → `sheet` → pastel card (`lilac` / `sky` / `pink-soft`) → `white` elements (options, inputs, pills) → `indigo` actions.

- Never put a white card straight on `sheet`: it disappears, and adding grey borders to fix it is what made the previous palette gloomy.
- Never put a pastel element on a card of the same pastel.

## Units

- **Use `rem` for font sizes, spacing, and max widths** in new or changed code. 1rem = 16px.
- Never set `font-size` on `html`. Leave it at the browser default, so a patient who set bigger text in their phone or browser gets bigger text here too.
- Keep `px` for borders (2.5px), shadow offsets (the 3D bottom shadow), and hairlines. These should not grow with text.
- Breakpoints in rem: **mobile** < `40rem` (640px), **desktop** ≥ `40rem`, **wide desktop** ≥ `60rem` (960px). Tablet uses the desktop layout. In Tailwind, `sm:` is already 40rem; set `--breakpoint-lg: 60rem` in `@theme` so `lg:` matches 960px (Tailwind's default `lg` is 64rem).
- The prototype is in px. Values below are the prototype values rounded to whole pixels, half pixels rounded up (17.5px → 18px). `frontend/src/styles/*.css` is in rem and uses these values through tokens in `tropicek.css` `:root`: `--fs-2xs` … `--fs-5xl` (Type), `--sp-*` and `--gutter` (Spacing), `--r-*` (radii), `--tap` / `--h-ctl` / `--h-ctl-lg` (control heights). Sizes do not step up globally on desktop; only the elements in the Type table that list a desktop size grow.
- Test once with the browser font size at 20px: text may wrap, but nothing should clip or overlap. Boxes that hold text grow with it (use `min-height`, not fixed `height`).

## Type

- **One serif family: Source Serif 4** (Google Fonts, optical size axis on). Headings, buttons, numbers: 600–700. Body: 600–800.
- Fallback: `Georgia, 'Times New Roman', serif`.
- Body text is semi-bold by default so it stays readable on small screens; heavier than 800 looks clumsy in a serif.
- Use lining numerals (`font-variant-numeric: lining-nums`) in inputs, scores, and pain scale.
- Load it from Google Fonts. Serif sets slightly wider than the old rounded fonts: re-check wrapping at 390px and with the browser font at 20px.

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
| App title (home ribbon) | Source Serif 4 700 | `3xl` 1.875rem | `5xl` 3rem | 1.1 |
| Red route heading | Source Serif 4 700 | `3xl` 1.875rem | `3xl` · `4xl` 2.25rem | 1.1 |
| Result heading (top estimate) | Source Serif 4 600 | `2xl` 1.5rem | same | 1.2 |
| Route title, banner, modal title | Source Serif 4 600–700 | `xl` 1.25rem | same | 1.2 |
| Question | Source Serif 4 600 | `lg` 1.125rem | `xl` 1.25rem | 1.25 |
| HUD title | Source Serif 4 600 | `lg` 1.125rem | same | 1.2 |
| Sub-question, card section title, category title | Source Serif 4 600 | `base` 1rem | same | 1.2 |
| Button | Source Serif 4 600 | `lg` 1.125rem (big: `xl` 1.25rem) | same | 1.2 |
| Number in input | Source Serif 4 600 | `2xl` 1.5rem (temperature `3xl`) | same | 1.2 |
| Card tab | Source Serif 4 600, letter-spacing 0.0625rem | `sm` 0.875rem | same | 1 |
| Option text | Source Serif 4 600 | `sm` 0.875rem | same | 1.3 |
| Option tile text | Source Serif 4 600 | `note` 0.8125rem | same | 1.25 |
| Bubble | Source Serif 4 600 | `note` 0.8125rem (home: `sm`) | `sm` · `base` 1rem | 1.45 |
| Body: modal, result lists, warnings | Source Serif 4 600–700 | `sm` 0.875rem | same | 1.45 |
| Hint, field label, note, chip | Source Serif 4 700–800 | `note` 0.8125rem | same | 1.35 |
| Option description, disclaimer, tags, counter | Source Serif 4 700 | `xs` 0.75rem | same | 1.4 |
| Pain scale labels, ring caption | Source Serif 4 800 | `2xs` 0.6875rem | `xs` 0.75rem | 1.15 |

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
- **3D effect = solid bottom shadow**, no blur, on buttons only: `box-shadow: 0 4px 0 <indigo-deep>, 0 8px 18px rgba(63,56,230,0.25)`. The glow is tinted with the button's own hue, never black or grey.
- **Cards have no 3D shadow and no border.** Their pastel fill separates them. At most `0 6px 16px rgba(63,56,230,0.06)`.
- Pressed: move down 4px, shadow shrinks to 1px.
- Options and inputs: `white` fill on the pastel card, no border at rest. Selected or focused: 2.5px `indigo` border.

## Components

| Component | What it looks like |
| --- | --- |
| **Card with tab** | Pastel card (`lilac` by default; `sky` or `pink-soft` for variety), label pill on the top edge, centered: `white` pill, `indigo-deep` text, Source Serif 4, letter-spaced |
| **3D button** | Full width on mobile, flat fill + indigo bottom shade. **Primary** = `indigo` `#3F38E6`, white text. **Secondary / ghost / back / WhatsApp** = `indigo-soft` `#DEDBFD`, `indigo-deep` text (like the reference's soft "Skip" button, but readable). Disabled = `#E7E4FB` with `muted` text, no shade. Only two exceptions: **Telepon 119** stays red (white with red text on the red screen) and **Mobile JKN** stays JKN blue |
| **Footer bar** (`.foot`) | `‹ Kembali` (`.btn-back`, left, hugs its text) + Lanjut (fills the rest). Under 23.125rem only `‹` shows; the button keeps `aria-label="Kembali"`. ≥40rem: both right-aligned, Lanjut min 18.75rem. First step has no back button |
| **Option** | `white` row on the pastel card: icon square + text + check circle. Selected → 2.5px `indigo` border, `indigo-soft` fill, `indigo` check |
| **Option tile** | Icon on top, text below. 2 columns mobile, 4 on ≥640px. Long options span full width |
| **Danger option** | Selected → `red` border + `#FFE1E5` fill. **Safe/none option**: `mint` fill, `green` check |
| **Category box** | Big colored gradient tile (one color per complaint group) |
| **Speech bubble** | `white` on `backdrop`; `pink-soft` on `sheet`. Rounded 18px, tail pointing to mascot, bold words in `indigo-deep` |
| **Mascot** | SVG, gentle bob + blink + wave animation |
| **HUD** | Top bar: round `indigo-soft` icon buttons with `indigo` icons, stage dots with lines, title in `ink` |
| **Stage dots** | Empty = `indigo-soft`, current = `indigo` with a soft indigo glow, done = `gold` with ✓. Lines `indigo-soft`; done lines `indigo-mid` |
| **Input** | `white` on the pastel card, big serif number in `ink`, 2.5px `indigo` border on focus |
| **Note** | `butter` box for tips (dashed `#F2B200`); `sky` box for info |
| **Warning box** | Pastel pair, icon left: yellow (`butter` + `#6E5100`), red (`#FFE1E5` + `#B4142C`), blue (`sky` + `#1F5F96`) |
| **Modal** | Card with tab + round close button top right, backdrop `rgba(60,50,160,0.35)` with blur (tinted, never black) |
| **Toast** | `ink` pill bottom center, white text |
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
