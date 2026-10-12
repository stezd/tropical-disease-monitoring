@AGENTS.md

## Claude Code notes

- Reply to the team in **Bahasa Indonesia** unless asked otherwise; code, identifiers, and commit messages in English.
- Before planning or splitting work, read [docs/RENCANA-KERJA.md](docs/RENCANA-KERJA.md) and respect the owner of each area (FE, BE, Statistika, Dokter). Do not rewrite clinical content or scoring weights on your own — propose the change and name the owner who must approve it.
- Project skills are in `.claude/skills/` (`fastapi`, `sqlmodel`, `library-skills`). Use them for backend work.
- When building or changing UI, open [docs/TropiCek-Simulasi.html](docs/TropiCek-Simulasi.html) as the visual reference and match its tokens and components — but apply the corrections listed in section 7 of the plan instead of copying the prototype's known deviations.
- To check a UI change, run the app and look at it at 390px, 768px, and 1440px widths before calling it done.
