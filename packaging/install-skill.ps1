param(
  [ValidateSet("codex", "claude")]
  [string]$Target,
  [string]$TargetDir
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SkillName = "comfyui-workflow-builder"
$Source = Join-Path $RepoRoot "skills\$SkillName"

if (-not (Test-Path $Source)) {
  throw "Skill source not found: $Source"
}

if (-not $TargetDir) {
  if ($Target -eq "codex") {
    $base = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
    $TargetDir = Join-Path $base "skills"
  } elseif ($Target -eq "claude") {
    $TargetDir = Join-Path (Join-Path $HOME ".claude") "skills"
  } else {
    throw "Provide -Target codex, -Target claude, or -TargetDir <skills-directory>."
  }
}

$Destination = Join-Path $TargetDir $SkillName
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

if (Test-Path $Destination) {
  Remove-Item -LiteralPath $Destination -Recurse -Force
}

Copy-Item -LiteralPath $Source -Destination $Destination -Recurse
Write-Host "Installed $SkillName to $Destination"
