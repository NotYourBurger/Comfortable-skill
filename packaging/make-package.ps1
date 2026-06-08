$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SkillName = "comfyui-workflow-builder"
$Source = Join-Path $RepoRoot "skills\$SkillName"
$Dist = Join-Path $RepoRoot "dist"
$Zip = Join-Path $Dist "$SkillName.zip"
$Tar = Join-Path $Dist "$SkillName.tar.gz"

if (-not (Test-Path $Source)) {
  throw "Skill source not found: $Source"
}

New-Item -ItemType Directory -Force -Path $Dist | Out-Null
Remove-Item -LiteralPath $Zip -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $Tar -Force -ErrorAction SilentlyContinue

Compress-Archive -Path $Source -DestinationPath $Zip -Force

Push-Location (Join-Path $RepoRoot "skills")
try {
  tar -czf $Tar $SkillName
} finally {
  Pop-Location
}

Write-Host "Wrote $Zip"
Write-Host "Wrote $Tar"
