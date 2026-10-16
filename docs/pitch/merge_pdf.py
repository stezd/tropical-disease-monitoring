"""Merge per-slide PDFs in docs/pitch/out/ into docs/pitch/TropiCare-Pitch.pdf.
Run: uv run --with pypdf python docs/pitch/merge_pdf.py
"""
from pathlib import Path

from pypdf import PdfWriter

root = Path(__file__).resolve().parent
parts = sorted((root / "out").glob("[0-9][0-9]*.pdf"))
if not parts:
    raise SystemExit("No slide PDFs in out/. Run export-pdf.ps1 first.")

writer = PdfWriter()
for part in parts:
    writer.append(str(part))
target = root / "TropiCare-Pitch.pdf"
with target.open("wb") as fh:
    writer.write(fh)
print(f"{len(parts)} slides -> {target}")
