# DESIGN.md — TropiCare

Visual guide for the React app. Source: [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html). Open it next to this file.

## Feel

- **Calm, clean, caring.** Like a modern clinic app: soft mint-teal backdrop, white cards with gentle shadows, one deep teal for actions, and small pastel circles for icons. Trustworthy first, friendly second.
- Still a game (Quizizz / Akinator) through the mascot, stage dots, and confetti, not through loud color. Nothing neon, nothing dark, nothing purple.
- Big rounded shapes, pill chips, round icon buttons. The mascot **Kak Tropi** talks in speech bubbles.
- One geometric sans (**Poppins**) everywhere: friendly round letters, medium weight body.
- Exception: the **red route** is calm and serious. No game elements.

**Visual reference:** a teal medical-booking app (three phones: home with greeting + search + category circles, doctor list, booking calendar). Copy its palette, type, and the way it uses color and depth, not its layout. Sizes and spacing in this file did not change; only color, font, and depth did (2026-10-15).

## Colors

### Why the reference feels calm (keep these rules)

1. **White cards on a teal sheet, with soft depth.** Cards are `white`, with a 1px `line` hairline and a soft teal-tinted shadow. Color does not fill whole cards.
2. **The backdrop is pale mint-teal** and the sheet is a deeper teal with a touch of white; neither is white or grey. The backdrop holds the home hero and Thinking. On desktop the margins around the app column use the lighter `backdrop-glow`, with soft lighter blobs and faint white `+` marks and dot grids as decoration.
3. **One action color: deep teal** `#0F6B66`, flat. Primary buttons, selected state, checkbox, focus ring, round icon controls, current stage dot. Nothing else is that strong.
4. **Color lives in small pastel circles.** Icons sit in round pastel badges (rose, mint, sky, butter, lavender), like the reference's category circles. Rotate the hues so neighbours differ.
5. **Greys are teal-tinted.** Hint text, hairlines, and disabled states lean toward teal (`ink2`, `muted`, `line`), never pure grey.
6. **Tags carry meaning through pastel pairs**: a pastel fill plus a stronger text color of the same hue. Routes and warnings use the same idea.
7. **Dark slate text** (`ink`) on white and pastel. White text only on teal, on the red route, and on solid colors that pass contrast.
8. **Coral is the warm accent** in small amounts: mascot details, hearts, a notification dot. Never for actions or text.

### Tokens

Put these in `frontend/src/styles/tropicek.css` `:root` and map them to the shadcn theme in `frontend/src/index.css` (`--primary` = `teal`, `--background` = `sheet`, `--card` = `white`, `--secondary` = `teal-soft`, `--accent` = `mint-card`, `--border` = `line`).

**Base**

| Token | Hex | Use |
| --- | --- | --- |
| `backdrop` | `#CDE8E3` | Home hero, Thinking, desktop margins around the app column |
| `backdrop-glow` | `#E4F4F1` | Lighter blobs and the glow at the top of the backdrop |
| `backdrop-deep` | `#A9D7D0` | Darker decorative blobs on the backdrop (never behind text) |
| `sheet` | `#B8DFD9` | The app "screen" behind cards (quiz, result, history, privacy), and the home bottom sheet |
| `white` | `#FFFFFF` | Cards, bubbles on the backdrop, inputs |
| `field` | `#F3F8F7` | Options and inputs sitting **on** a white card |
| `line` | `#E1EDEA` | The only hairline (cards, options, dividers) |
| `ink` | `#15323A` | Main text (dark slate) |
| `ink2` | `#566D74` | Secondary text. Not on `backdrop` (4.2:1); use `ink` there |
| `muted` | `#9CB2B5` | Placeholders, disabled, decoration. Never important text |

**Action (teal)**

| Token | Hex | Use |
| --- | --- | --- |
| `teal` | `#0F6B66` | Primary button, selected border, checkbox, focus ring, current stage dot, round icon buttons |
| `teal-deep` | `#0B524E` | Pressed state, links ("Lihat semua" style), bold words in bubbles, tab text |
| `teal-mid` | `#5FB3AA` | Done-stage lines, progress fill, icons on pastel |
| `teal-soft` | `#DCEFEB` | Secondary button fill (text `teal-deep`), selected option fill, chips, card tabs |
| `mint-card` | `#E5F3F0` | Feature/promo boxes (like the reference's "Consult with trusted doctors"), speech bubble on `sheet` |

**Pastel circles and tags** (fill + paired text)

| Token | Fill | Text / icon | Use |
| --- | --- | --- | --- |
| `rose` | `#FDE6E9` | `#C2334B` | Heart/blood icons, red-ish tags |
| `mint` | `#DFF3E6` | `#257048` | "Safe / none" option, success, location found |
| `sky` | `#DDEEFA` | `#22679E` | Info boxes, breathing/lung icons, blue warnings |
| `butter` | `#FDF0CC` | `#7D5600` | Tips note, yellow warnings, stomach icons |
| `lavender` | `#EBE7F9` | `#5A46B0` | Brain/nerve icons, misc tags |
| `coral` | `#F06A6A` | — | Mascot details, hearts, notification dot. Never text |

**Status**

| Token | Hex | Use |
| --- | --- | --- |
| `green` | `#2E9E6B` | Success icon, safe option check, done stage dot |
| `gold` | `#F2B200` | Stars and celebratory sparkles only |
| `red` | `#E0384F` | Danger option border, emergency. Red warning text `#B4142C` on `#FFE1E5` |

Contrast (measured, WCAG): `ink` 13.6:1 on white and 10.5:1 on `backdrop`; `ink2` 5.5:1 on white, 5.1:1 on `field`; white on `teal` 6.3:1; `teal-deep` 9.0:1 on white and 7.6:1 on `teal-soft`; every pastel pair 4.6–5.9:1. `muted` is 2.2:1 on white: decoration only.

### Route colors

Routes use the pastel-pair idea: a **pastel band** with a **solid icon chip** and dark text. MERAH stays solid and serious.

| Route | Band (pastel) | Icon chip | Text | Icon |
| --- | --- | --- | --- | --- |
| HIJAU | `#DFF3E6` | `#2E9E6B` | `#0F5A3A` | 🌿 |
| KUNING | `#FFF1B8` | `#F2B200` | `#5E4500` | 🏥 |
| KUNING KHUSUS | `#FFE2CC` | `#F07A2A` | `#7A3300` | 🎯 |
| MERAH | `#D42A42` → `#C8203A` (solid) | white | white | 🚨 |

### Screen backgrounds

- **Home:** like the reference's first phone. Top = `backdrop` hero (gradient `backdrop-glow` → `backdrop`) with soft round blobs (`backdrop-glow`, `backdrop-deep` at low opacity) and a few white `+` marks / dot grids. Title, mascot, and bubble sit in the hero. The path buttons sit on a pale `#F5FAF9` panel (token `--tc-sheet-home`, unchanged by the teal `sheet`) that rises from the bottom with a 1.625rem top radius.
- **Quiz, Result, History, Privacy:** `sheet` `#B8DFD9`, flat. Color comes from the teal actions and the pastel circles on white cards. From 40rem, the area outside the content column is `backdrop-glow` (lighter than the sheet), and the column is a `sheet` panel with radius 2rem and a soft shadow `0 20px 50px rgba(15,107,102,0.18)`. No colored frame.
- **Thinking:** `backdrop` with a radial `backdrop-glow` behind the orb. Steps are white pills; the running step is `teal-soft`, done steps get a `mint` check.
- **Red route:** solid `#C8203A → #D42A42` (white text passes 4.5:1 across the whole gradient). Calm: no sparkles, no blobs.

### How surfaces stack

`backdrop` → `sheet` → `white` card (hairline + soft shadow) → `field` elements (options, inputs) and pastel circles → `teal` actions.

- A white card on `sheet` needs its `line` hairline and soft shadow, or it disappears.
- Don't fill whole cards with pastel. Pastel goes in circles, tags, notes, and the occasional `mint-card` feature box.

## Units

- **Use `rem` for font sizes, spacing, and max widths** in new or changed code. 1rem = 16px.
- Never set `font-size` on `html`. Leave it at the browser default, so a patient who set bigger text in their phone or browser gets bigger text here too.
- Keep `px` for borders (2.5px), shadow offsets (the 3D bottom shadow), and hairlines. These should not grow with text.
- Breakpoints in rem: **mobile** < `40rem` (640px), **desktop** ≥ `40rem`, **wide desktop** ≥ `60rem` (960px). Tablet uses the desktop layout. In Tailwind, `sm:` is already 40rem; set `--breakpoint-lg: 60rem` in `@theme` so `lg:` matches 960px (Tailwind's default `lg` is 64rem).
- The prototype is in px. Values below are the prototype values rounded to whole pixels, half pixels rounded up (17.5px → 18px). `frontend/src/styles/*.css` is in rem and uses these values through tokens in `tropicek.css` `:root`: `--fs-2xs` … `--fs-5xl` (Type), `--sp-*` and `--gutter` (Spacing), `--r-*` (radii), `--tap` / `--h-ctl` / `--h-ctl-lg` (control heights). Sizes do not step up globally on desktop; only the elements in the Type table that list a desktop size grow.
- Test once with the browser font size at 20px: text may wrap, but nothing should clip or overlap. Boxes that hold text grow with it (use `min-height`, not fixed `height`).

## Type

- **One sans family: Poppins** (Google Fonts, weights 400, 500, 600, 700). Headings, buttons, numbers: 600–700. Body: 400–500. Labels and chips: 500–600.
- Fallback: `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`.
- Don't go above 700: heavy Poppins looks clumsy and loses the calm feel.
- Poppins has lining numerals by default; keep `font-variant-numeric: tabular-nums` where numbers line up (pain scale, scores).
- Load it from Google Fonts. Poppins sets wider than the old serif: re-check wrapping at 390px and with the browser font at 20px.

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
| App title (home hero) | Poppins 700 | `3xl` 1.875rem | `5xl` 3rem | 1.1 |
| Red route heading | Poppins 700 | `3xl` 1.875rem | `3xl` · `4xl` 2.25rem | 1.1 |
| Result heading (top estimate) | Poppins 600 | `2xl` 1.5rem | same | 1.2 |
| Route title, banner, modal title | Poppins 600 | `xl` 1.25rem | same | 1.2 |
| Question | Poppins 600 | `lg` 1.125rem | `xl` 1.25rem | 1.25 |
| HUD title | Poppins 600 | `lg` 1.125rem | same | 1.2 |
| Sub-question, card section title, category title | Poppins 600 | `base` 1rem | same | 1.2 |
| Button | Poppins 600 | `base` 1rem (big: `lg` 1.125rem) | `lg` 1.125rem (big: `xl` 1.25rem) | 1.2 |
| Number in input | Poppins 600 | `2xl` 1.5rem (temperature `3xl`) | same | 1.2 |
| Card tab | Poppins 600, letter-spacing 0.0625rem | `sm` 0.875rem | same | 1 |
| Option text | Poppins 500 | `sm` 0.875rem | same | 1.3 |
| Option tile text | Poppins 500 | `note` 0.8125rem | same | 1.25 |
| Bubble | Poppins 500 | `note` 0.8125rem (home: `sm`) | `sm` · `base` 1rem | 1.45 |
| Body: modal, result lists, warnings | Poppins 400–500 | `sm` 0.875rem | same | 1.45 |
| Hint, field label, note, chip | Poppins 500 | `note` 0.8125rem | same | 1.35 |
| Option description, disclaimer, tags, counter | Poppins 400–500 | `xs` 0.75rem | same | 1.4 |
| Pain scale labels, ring caption | Poppins 600 | `2xs` 0.6875rem | `xs` 0.75rem | 1.15 |

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

- Radius (unchanged): cards 1.625rem (26px), buttons 1.25rem (20px), options and inputs 1rem (16px), small icons 0.75rem (12px), pills 999px.
- **Flat buttons with a soft glow**, no solid bottom shade: primary `box-shadow: 0 6px 16px rgba(15,107,102,0.28)`. Secondary buttons have no shadow. Shadows are always tinted teal, never black or grey.
- **Cards: white, 1px `line` hairline, soft shadow** `0 6px 20px rgba(15,107,102,0.08)`. No pastel fill.
- Pressed: `teal-deep` fill and `transform: scale(0.98)`, shadow halves.
- Options and inputs: `field` fill with a 1px `line` border at rest. Selected or focused: 2px `teal` border (keep the box size: compensate padding so nothing jumps).
- Icon squares become **circles** (same size) in a pastel fill, like the reference's category circles.

## Components

| Component | What it looks like |
| --- | --- |
| **Card with tab** | `white` card (hairline + soft shadow), label pill on the top edge, centered: `teal-soft` pill, `teal-deep` text, Poppins 600, letter-spaced |
| **Button** | Full width on mobile, flat, soft glow (see Shape and depth). **Primary** = `teal` `#0F6B66`, white text (like the reference's "Book Appointment"). **Secondary / ghost / back / WhatsApp** = `teal-soft` `#DCEFEB`, `teal-deep` text. **Outline** (home second path, "Lihat" links) = `white` with 1px `line` border and `teal-deep` text. Disabled = `#E8EFEE` with `muted` text, no shadow. Only two exceptions: **Telepon 119** stays red (white with red text on the red screen) and **Mobile JKN** stays JKN blue |
| **Footer bar** (`.foot`) | `‹ Kembali` (`.btn-back`, left, hugs its text) + Lanjut (fills the rest). Under 23.125rem only `‹` shows; the button keeps `aria-label="Kembali"`. ≥40rem: both right-aligned, Lanjut min 18.75rem. First step has no back button |
| **Option** | `field` row on the white card: pastel icon circle + text + check circle. Selected → 2px `teal` border, `teal-soft` fill, `teal` check with white tick |
| **Option tile** | Icon on top, text below. 2 columns mobile, 4 on ≥640px. Long options span full width |
| **Danger option** | Selected → `red` border + `#FFE1E5` fill. **Safe/none option**: `mint` fill, `green` check |
| **Category box** | White tile with a big pastel icon circle on top (one hue per complaint group: fever = rose, breath = sky, digestion = butter, skin = lavender, swelling = mint) and the title below in `ink`. Selected → `teal` border + `teal-soft` fill |
| **Speech bubble** | `white` with soft shadow on `backdrop`; `mint-card` on `sheet`. Rounded 18px, tail pointing to mascot, bold words in `teal-deep` |
| **Mascot** | SVG, gentle bob + blink + wave animation |
| **HUD** | Top bar: round `white` icon buttons (hairline + soft shadow) with `teal` icons, like the reference's back/menu buttons; stage dots with lines; title in `ink` |
| **Stage dots** | Empty = `white` with `line` border, current = `teal` with a soft teal glow, done = `teal-mid` with white ✓. Lines `line`; done lines `teal-mid` |
| **Input** | `field` on the white card, big Poppins 600 number in `ink`, 2px `teal` border on focus |
| **Note** | `butter` box for tips (dashed `#F2B200`); `sky` box for info |
| **Warning box** | Pastel pair, icon left: yellow (`butter` + `#7D5600`), red (`#FFE1E5` + `#B4142C`), blue (`sky` + `#22679E`) |
| **Modal** | White card with tab + round close button top right, backdrop `rgba(11,60,58,0.35)` with blur (tinted, never black) |
| **Toast** | `ink` pill bottom center, white text |
| **Privacy gate** (`.consent-gate`) | First card after choosing a path. Question + hint, the privacy text in a scroll box (`.consent-text`, `field` background with hairline, max height ~18rem), one checkbox row (`.chk`) "Saya setuju", and a small location pill (`.loc-status`, green when found, yellow when denied). Lanjut is disabled until the box is ticked. If location is denied, an optional province picker appears (`.reveal-in`). Max 3 fields, like every page |
| **Revealed field** (`.reveal-in`) | A field that appears after earlier answers fades and slides in 0.5rem. No motion on the red route or with reduced motion |
| **Facility card** (`.nf-item`) | Soft box inside the "FASILITAS TERDEKAT" card: name, distance pill, type + address, then buttons "Cari di Google Maps" and "Kirim rangkuman via WhatsApp" (or "Telepon"). Buttons stack on phones, two columns from 40rem |
| **History list** (`.hist-list` / `.hist-item`) | `/riwayat`, logged-in users only. One white card with tab "RIWAYAT SKRINING"; each item is a soft box: date + path + route badge (route color, icon and name), top estimate + skor kecocokan pill, then "Buka" / "Hapus" side by side. Game style, not an admin table |
| **Google sign-in** (`.gbtn-wrap`, `.or-sep`) | On login and signup: Google's own button centered at full width, then an "atau" divider (hairline both sides), then the email + password form. Hidden when no Google client id is set |

## Layout

- **<40rem (640px, phone, main target):** one column, button pinned at bottom, as little scrolling as possible.
- **≥40rem:** content max 43.75rem centered, tiles in 4 columns, footer buttons aligned right (Lanjut min 18.75rem).
- **Home** is one centered column at every size: title, mascot + bubble, then the path buttons **under** the mascot (max 25rem), disclaimer at the bottom. On phones the column is pinned to the top (1.5rem under the title), not vertically centered. From 40rem the mascot + buttons group sits in the middle of the free space. No two-column home.
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
