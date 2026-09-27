$ErrorActionPreference = "Stop"
$workspaceRoot = Split-Path -Parent $PSScriptRoot
$p1Packages = Join-Path $workspaceRoot "prototype_p1\.tools\python_packages"
$auditPackages = Join-Path $workspaceRoot "analysis_generated\python_packages"
$sourcePath = Join-Path $PSScriptRoot "src"
$env:PYTHONPATH = "$p1Packages;$auditPackages;$sourcePath"
python (Join-Path $sourcePath "build.py") @args
