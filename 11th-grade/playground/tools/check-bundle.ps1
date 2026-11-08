# Verify the offline lab bundle is complete (no pip / no internet needed at runtime).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\check-bundle.ps1

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$App = Join-Path $RepoRoot "app"
$failed = $false

function Ok($msg) { Write-Host "[OK]  $msg" -ForegroundColor Green }
function Bad($msg) { Write-Host "[FAIL] $msg" -ForegroundColor Red; $script:failed = $true }
function Info($msg) { Write-Host "      $msg" }

Write-Host ""
Write-Host "teacher-playground offline bundle check"
Write-Host "Root: $RepoRoot"
Write-Host ""

$required = @(
  @{ Path = (Join-Path $RepoRoot "شروع.bat"); Label = "شروع.bat" },
  @{ Path = (Join-Path $App "index.html"); Label = "app\index.html" },
  @{ Path = (Join-Path $App "launcher.py"); Label = "app\launcher.py" },
  @{ Path = (Join-Path $App "css\style.css"); Label = "app\css\style.css" },
  @{ Path = (Join-Path $App "js\app.js"); Label = "app\js\app.js" },
  @{ Path = (Join-Path $App "js\runner.js"); Label = "app\js\runner.js" },
  @{ Path = (Join-Path $App "js\diff.js"); Label = "app\js\diff.js" },
  @{ Path = (Join-Path $App "js\bidi.js"); Label = "app\js\bidi.js" },
  @{ Path = (Join-Path $App "js\editor.js"); Label = "app\js\editor.js" },
  @{ Path = (Join-Path $App "vendor\codemirror\codemirror.min.js"); Label = "app\vendor\codemirror\codemirror.min.js" },
  @{ Path = (Join-Path $App "vendor\codemirror\mode\python\python.min.js"); Label = "app\vendor\codemirror\mode\python\python.min.js" },
  @{ Path = (Join-Path $RepoRoot "docs\RTL-BIDI.md"); Label = "docs\RTL-BIDI.md" },
  @{ Path = (Join-Path $App "data\problems.json"); Label = "app\data\problems.json" },
  @{ Path = (Join-Path $App "data\concepts.json"); Label = "app\data\concepts.json" },
  @{ Path = (Join-Path $RepoRoot "tools\serve.ps1"); Label = "tools\serve.ps1" },
  @{ Path = (Join-Path $App "vendor\pyodide\pyodide.js"); Label = "app\vendor\pyodide\pyodide.js" },
  @{ Path = (Join-Path $App "vendor\pyodide\pyodide.asm.js"); Label = "app\vendor\pyodide\pyodide.asm.js" },
  @{ Path = (Join-Path $App "vendor\pyodide\pyodide.asm.wasm"); Label = "app\vendor\pyodide\pyodide.asm.wasm" },
  @{ Path = (Join-Path $App "vendor\pyodide\python_stdlib.zip"); Label = "app\vendor\pyodide\python_stdlib.zip" },
  @{ Path = (Join-Path $App "vendor\pyodide\package.json"); Label = "app\vendor\pyodide\package.json" },
  @{ Path = (Join-Path $App "vendor\pyodide\pyodide-lock.json"); Label = "app\vendor\pyodide\pyodide-lock.json" },
  @{ Path = (Join-Path $App "vendor\pyodide-legacy\pyodide.js"); Label = "app\vendor\pyodide-legacy\pyodide.js" },
  @{ Path = (Join-Path $App "vendor\pyodide-legacy\pyodide.asm.js"); Label = "app\vendor\pyodide-legacy\pyodide.asm.js" },
  @{ Path = (Join-Path $App "vendor\pyodide-legacy\pyodide.asm.wasm"); Label = "app\vendor\pyodide-legacy\pyodide.asm.wasm" },
  @{ Path = (Join-Path $App "vendor\pyodide-legacy\python_stdlib.zip"); Label = "app\vendor\pyodide-legacy\python_stdlib.zip" },
  @{ Path = (Join-Path $App "vendor\pyodide-legacy\repodata.json"); Label = "app\vendor\pyodide-legacy\repodata.json" }
)

foreach ($item in $required) {
  if (Test-Path -LiteralPath $item.Path -PathType Leaf) {
    $len = (Get-Item -LiteralPath $item.Path).Length
    if ($len -le 0) { Bad "$($item.Label) is empty" } else { Ok "$($item.Label) ($len bytes)" }
  } else {
    Bad "missing $($item.Label)"
  }
}

# Root must stay student-safe: only شروع.bat as a file (folders OK).
$ignoreRootNames = @(".gitignore", "desktop.ini", "Thumbs.db")
$rootFiles = @(Get-ChildItem -LiteralPath $RepoRoot -File -Force | Where-Object {
  ($ignoreRootNames -notcontains $_.Name) -and (-not $_.Name.StartsWith("."))
})
$unexpected = @($rootFiles | Where-Object { $_.Name -ne "شروع.bat" })
if ($unexpected.Count -eq 0 -and ($rootFiles | Where-Object { $_.Name -eq "شروع.bat" })) {
  Ok "Root has only شروع.bat for students (plus hidden/git files)"
} else {
  Bad ("Root should contain only شروع.bat; found: " + (($rootFiles | ForEach-Object Name) -join ", "))
}

$python = Get-Command python -ErrorAction SilentlyContinue
$py = Get-Command py -ErrorAction SilentlyContinue
if ($python -or $py) {
  Ok "Python launcher found (stdlib only — no pip packages required)"
} else {
  Info "Python not on PATH — CLI fallback can use PowerShell server."
}

$scan = @(
  "index.html",
  "css\style.css",
  "js\app.js",
  "js\runner.js",
  "js\diff.js"
)
$badUrl = $false
foreach ($rel in $scan) {
  $text = Get-Content -LiteralPath (Join-Path $App $rel) -Raw -Encoding UTF8
  if ($text -match '(cdn\.|unpkg\.|jsdelivr|googleapis|cdnjs)') {
    Bad "app\$rel references an online CDN"
    $badUrl = $true
  }
}
if (-not $badUrl) {
  Ok "App shell has no CDN dependencies"
}

Write-Host ""
Write-Host "Students: double-click شروع.bat only."
Write-Host "Teachers: see docs\README.md"
Write-Host ""

if ($failed) {
  Write-Host "Bundle check FAILED." -ForegroundColor Red
  exit 1
}
Write-Host "Bundle check PASSED — ready for offline lab use." -ForegroundColor Green
exit 0
