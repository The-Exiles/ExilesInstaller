# ? Project: Exiles Installer
# ? File: sign_windows.ps1
# ? Directory: scripts/
# ? Description: Code-sign all EXE/DLLs in dist and the installer using signtool.
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

param(
  [string]$DistPath = "../dist/ExilesInstaller",
  [string]$InstallerPath = "../artifacts",
  [switch]$VerboseLog
)

if (-not (Test-Path $InstallerPath)) {
  New-Item -ItemType Directory -Path $InstallerPath | Out-Null
}

$envPath = Resolve-Path -Path "../.env" -ErrorAction SilentlyContinue
if ($envPath) {
  Write-Host "? Loading .env from $envPath"
  Get-Content $envPath | ForEach-Object {
    if ($_ -match "^\s*#") { return }
    if ($_ -match "^\s*$") { return }
    $k,$v = $_.Split("=",2)
    if ($null -ne $k -and $null -ne $v) {
      [Environment]::SetEnvironmentVariable($k.Trim(), $v.Trim())
    }
  }
}

$Signtool   = $env:SIGNTOOL_PATH
$Pfx        = $env:CERT_PFX_PATH
$PfxPass    = $env:CERT_PFX_PASSWORD
$Timestamp  = $env:TIMESTAMP_URL
if (-not $Signtool) { $Signtool = "signtool.exe" }
if (-not $Timestamp) { $Timestamp = "http://timestamp.digicert.com" }

function Sign-File([string]$file) {
  Write-Host "→ Signing $file"
  $args = @("sign","/fd","SHA256","/tr",$Timestamp,"/td","SHA256")
  if ($Pfx) {
    $args += @("/f",$Pfx)
    if ($PfxPass) { $args += @("/p",$PfxPass) }
  } else {
    throw "No CERT_PFX_PATH provided and store-based signing not configured."
  }
  $args += $file
  if ($VerboseLog) { Write-Host "signtool $($args -join ' ')" -ForegroundColor DarkGray }
  & $Signtool @args
  if ($LASTEXITCODE -ne 0) { throw "signtool failed for $file" }
}

$distResolved = Resolve-Path -Path $DistPath
$targets = Get-ChildItem -Path $distResolved -Include *.exe,*.dll -Recurse
foreach ($t in $targets) { Sign-File $t.FullName }

$instResolved = Resolve-Path -Path $InstallerPath
$installers = Get-ChildItem -Path $instResolved -Include *.exe,*.msi -Recurse
foreach ($t in $installers) { Sign-File $t.FullName }

Write-Host "✓ Signing complete."
