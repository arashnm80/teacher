# One-time download of the offline Pyodide engines (needs internet).
# Fetches the modern engine (Chrome/Edge 96+) and the legacy engine for
# older lab browsers, then strips sourcemap comments (maps are not vendored).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\fetch-pyodide.ps1

param(
  [string]$Version = "0.26.4",
  [string]$LegacyVersion = "0.23.4"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$App = Join-Path $RepoRoot "app"
$Vendor = Join-Path $App "vendor"

function Fetch-Engine([string]$Ver, [string]$DirName, [string[]]$Files) {
  $Tmp = Join-Path $Vendor "_tmp_pyodide"
  $Dest = Join-Path $Vendor $DirName
  $Url = "https://github.com/pyodide/pyodide/releases/download/$Ver/pyodide-$Ver.tar.bz2"
  $Archive = Join-Path $Tmp "pyodide.tar.bz2"

  New-Item -ItemType Directory -Force -Path $Vendor | Out-Null
  if (Test-Path $Tmp) { Remove-Item -Recurse -Force $Tmp }
  if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
  New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null

  Write-Host "Downloading Pyodide $Ver …"
  Write-Host $Url
  Invoke-WebRequest -Uri $Url -OutFile $Archive -UseBasicParsing

  Write-Host "Extracting…"
  tar -xjf $Archive -C $Tmp
  $Src = Join-Path $Tmp "pyodide"
  if (-not (Test-Path (Join-Path $Src "pyodide.js"))) {
    throw "Unexpected archive layout — pyodide.js not found after extract."
  }

  foreach ($f in $Files) {
    $from = Join-Path $Src $f
    if (Test-Path $from) {
      Copy-Item $from (Join-Path $Dest $f) -Force
      Write-Host "  copied $f"
    } else {
      throw "Required file missing from release ${Ver}: $f"
    }
  }

  # Sourcemap files are not vendored — drop the comment to avoid 404 noise.
  $loader = Join-Path $Dest "pyodide.js"
  $text = [IO.File]::ReadAllText($loader)
  $stripped = $text -replace '(?m)^\/\/# sourceMappingURL=.*\r?$', ''
  if ($stripped.Length -ne $text.Length) {
    [IO.File]::WriteAllText($loader, $stripped)
    Write-Host "  stripped sourceMappingURL comment"
  }

  Remove-Item -Recurse -Force $Tmp
  Write-Host "OK → $Dest"
}

Fetch-Engine $Version "pyodide" @(
  "pyodide.js",
  "pyodide.asm.js",
  "pyodide.asm.wasm",
  "python_stdlib.zip",
  "package.json",
  "pyodide-lock.json"
)

# 0.23.x is the last line before WebAssembly externref (works on Chrome 71+).
Fetch-Engine $LegacyVersion "pyodide-legacy" @(
  "pyodide.js",
  "pyodide.asm.js",
  "pyodide.asm.wasm",
  "python_stdlib.zip",
  "package.json",
  "repodata.json"
)

& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "check-bundle.ps1")
