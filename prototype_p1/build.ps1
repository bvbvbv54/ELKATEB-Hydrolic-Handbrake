$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$localPackages = Join-Path $PSScriptRoot ".tools\python_packages"
$auditPackages = Join-Path $projectRoot "analysis_generated\python_packages"
$sourcePath = Join-Path $PSScriptRoot "src"
$env:PYTHONPATH = "$localPackages;$auditPackages;$sourcePath"
python (Join-Path $sourcePath "build.py") @args
