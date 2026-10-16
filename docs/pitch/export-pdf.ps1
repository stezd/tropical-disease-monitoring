# Export every slide in slides/ to PDF with headless Edge, then merge into TropiCare-Pitch.pdf.
# Run from anywhere:  powershell -File docs\pitch\export-pdf.ps1
# Needs internet (Google Fonts) and uv (for pypdf).
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$out = Join-Path $root "out"
New-Item -ItemType Directory -Force $out | Out-Null

$edge = @(
  "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
  "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edge) { throw "msedge.exe not found" }

Get-ChildItem (Join-Path $root "out") -Filter "*.pdf" | Remove-Item -Force

foreach ($slide in Get-ChildItem (Join-Path $root "slides") -Filter "*.html" | Sort-Object Name) {
  $pdf = Join-Path $out ($slide.BaseName + ".pdf")
  $url = ([System.Uri]$slide.FullName).AbsoluteUri
  Start-Process -FilePath $edge -Wait -NoNewWindow -ArgumentList @(
    "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
    "--print-to-pdf=`"$pdf`"", "`"$url`""
  ) -RedirectStandardError (Join-Path $out "edge.log")
  if (-not (Test-Path $pdf)) { throw "Failed: $($slide.Name)" }
  Write-Host "ok  $($slide.Name)"
}

uv run --with pypdf python (Join-Path $root "merge_pdf.py")
