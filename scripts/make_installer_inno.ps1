# ? Project: Exiles Installer
# ? File: make_installer_inno.ps1
# ? Directory: scripts/
# ? Description: Build Inno Setup installer and drop it into artifacts/ (paths anchored to $PSScriptRoot)
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

param(
  # Path to ISCC.exe (Inno Setup command-line compiler)
  [string]$InnoCompiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
  # Inno script path (relative to repo root)
  [string]$IssPath = "..\installer\ExilesInstaller.iss",
  # Artifacts output dir (relative to repo root)
  [string]$Artifacts = "..\artifacts"
)

# Anchor all paths to the folder this script lives in
$ScriptDir = Split-Path -Parent $PSCommandPath
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir "..")
$IssFull   = Resolve-Path (Join-Path $ScriptDir $IssPath)
$ArtifactsFull = Join-Path $RepoRoot "artifacts"

if (-not (Test-Path $ArtifactsFull)) {
  New-Item -ItemType Directory -Path $ArtifactsFull | Out-Null
}

# Set a version if not provided
if (-not $env:EXILES_INSTALLER_VERSION -or ($env:EXILES_INSTALLER_VERSION -eq "")) {
  $env:EXILES_INSTALLER_VERSION = (Get-Date -Format "yyyy.MM.dd-HHmm")
}

Write-Host "? Building installer with version $env:EXILES_INSTALLER_VERSION"
& "$InnoCompiler" $IssFull
if ($LASTEXITCODE -ne 0) { throw "Inno Setup build failed." }

# Inno outputs next to the .iss by default → move newest setup to artifacts/
$issDir = Split-Path -Parent $IssFull
$setup = Get-ChildItem -Path $issDir -Filter "ExilesInstaller-*-Setup.exe" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($null -eq $setup) { throw "Installer EXE not found in $issDir." }

Move-Item -Force $setup.FullName (Join-Path $ArtifactsFull (Split-Path $setup.FullName -Leaf))
Write-Host "✓ Installer moved to $ArtifactsFull"
