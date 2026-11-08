# Offline static server for teacher-playground (Windows lab PCs).
# Prefers Python; falls back to PowerShell HttpListener if Python is missing.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\serve.ps1 [port]

param(
  [int]$Port = 0,
  [switch]$ForcePowerShell,
  [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Root = Join-Path $RepoRoot "app"
Set-Location $Root

$requiredVendor = @(
  "vendor\pyodide\pyodide.js",
  "vendor\pyodide\pyodide.asm.js",
  "vendor\pyodide\pyodide.asm.wasm",
  "vendor\pyodide\python_stdlib.zip",
  # Legacy engine for lab PCs whose browser predates Chrome/Edge 96.
  "vendor\pyodide-legacy\pyodide.js",
  "vendor\pyodide-legacy\pyodide.asm.js",
  "vendor\pyodide-legacy\pyodide.asm.wasm",
  "vendor\pyodide-legacy\python_stdlib.zip",
  "vendor\pyodide-legacy\repodata.json"
)
$missing = @($requiredVendor | Where-Object { -not (Test-Path (Join-Path $Root $_)) })
if ($missing.Count -gt 0) {
  Write-Host ""
  Write-Host "ERROR: offline Pyodide bundle is incomplete." -ForegroundColor Red
  foreach ($m in $missing) { Write-Host "  missing: app\$m" }
  Write-Host "Re-copy the whole folder, or on a machine with internet run:"
  Write-Host "  powershell -NoProfile -ExecutionPolicy Bypass -File tools\fetch-pyodide.ps1"
  Write-Host ""
  exit 1
}

function Test-PortFree([int]$Candidate) {
  try {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Candidate)
    $listener.Start()
    $listener.Stop()
    return $true
  } catch {
    return $false
  }
}

function Find-FreePort([int]$Preferred) {
  $start = if ($Preferred -gt 0) { $Preferred } else { 8765 }
  $candidates = @($start)
  for ($p = 8765; $p -le 8785; $p++) {
    if ($p -ne $start) { $candidates += $p }
  }
  foreach ($p in $candidates) {
    if (Test-PortFree $p) { return $p }
  }
  throw "No free port found between 8765 and 8785. Close the old server and try again."
}

function Find-PythonCommand {
  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) {
    return @{ Exe = $python.Source; Args = @("-m", "http.server") }
  }
  $py = Get-Command py -ErrorAction SilentlyContinue
  if ($py) {
    return @{ Exe = $py.Source; Args = @("-3", "-m", "http.server") }
  }
  return $null
}

function Get-MimeType([string]$Path) {
  switch ([System.IO.Path]::GetExtension($Path).ToLowerInvariant()) {
    ".html" { return "text/html; charset=utf-8" }
    ".js"   { return "application/javascript; charset=utf-8" }
    ".mjs"  { return "application/javascript; charset=utf-8" }
    ".css"  { return "text/css; charset=utf-8" }
    ".json" { return "application/json; charset=utf-8" }
    ".wasm" { return "application/wasm" }
    ".map"  { return "application/json; charset=utf-8" }
    ".zip"  { return "application/zip" }
    ".svg"  { return "image/svg+xml" }
    ".png"  { return "image/png" }
    ".jpg"  { return "image/jpeg" }
    ".jpeg" { return "image/jpeg" }
    ".ico"  { return "image/x-icon" }
    ".txt"  { return "text/plain; charset=utf-8" }
    ".md"   { return "text/plain; charset=utf-8" }
    default { return "application/octet-stream" }
  }
}

function Start-HttpListenerServer([int]$ListenPort) {
  $prefix = "http://127.0.0.1:$ListenPort/"
  $http = [System.Net.HttpListener]::new()
  $http.Prefixes.Add($prefix)
  try {
    $http.Start()
  } catch {
    throw "Could not bind $prefix — $($_.Exception.Message)"
  }

  Write-Host ""
  Write-Host "teacher-playground local server (PowerShell — no Python needed)"
  Write-Host "Open Chrome/Edge:  $prefix"
  Write-Host "Press Ctrl+C to stop."
  Write-Host ""

  if ($OpenBrowser) {
    try { Start-Process $prefix | Out-Null } catch {}
  }

  try {
    while ($http.IsListening) {
      $context = $http.GetContext()
      $request = $context.Request
      $response = $context.Response
      try {
        $rel = [Uri]::UnescapeDataString($request.Url.AbsolutePath.TrimStart("/"))
        if ([string]::IsNullOrWhiteSpace($rel)) { $rel = "index.html" }
        $rel = $rel -replace "/", "\"
        $full = [System.IO.Path]::GetFullPath((Join-Path $Root $rel))
        if (-not $full.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
          $response.StatusCode = 403
          $bytes = [System.Text.Encoding]::UTF8.GetBytes("Forbidden")
          $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } elseif (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
          $response.StatusCode = 404
          $bytes = [System.Text.Encoding]::UTF8.GetBytes("Not found")
          $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
          $bytes = [System.IO.File]::ReadAllBytes($full)
          $response.StatusCode = 200
          $response.ContentType = Get-MimeType $full
          $response.ContentLength64 = $bytes.LongLength
          $response.OutputStream.Write($bytes, 0, $bytes.Length)
        }
      } catch {
        $response.StatusCode = 500
      } finally {
        $response.OutputStream.Close()
      }
    }
  } finally {
    if ($http.IsListening) { $http.Stop() }
    $http.Close()
  }
}

$chosenPort = Find-FreePort $Port
$python = if ($ForcePowerShell) { $null } else { Find-PythonCommand }

if ($python) {
  Write-Host ""
  Write-Host "teacher-playground local server"
  Write-Host "Open Chrome/Edge:  http://127.0.0.1:$chosenPort"
  Write-Host "Press Ctrl+C to stop."
  Write-Host ""
  if ($OpenBrowser) {
    try { Start-Process "http://127.0.0.1:$chosenPort/" | Out-Null } catch {}
  }

  $allArgs = $python.Args + @("$chosenPort", "--bind", "127.0.0.1")
  & $python.Exe @allArgs
  exit $LASTEXITCODE
}

if ($ForcePowerShell) {
  Write-Host "Using built-in PowerShell server (-ForcePowerShell)." -ForegroundColor Yellow
} else {
  Write-Host "Python not found on PATH — using built-in PowerShell server." -ForegroundColor Yellow
}
Start-HttpListenerServer $chosenPort
