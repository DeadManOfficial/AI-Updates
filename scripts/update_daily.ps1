param(
  [string]$Date
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$script = Join-Path $PSScriptRoot "update_daily.py"

if (-not $Date -or $Date.Trim().Length -eq 0) {
  $Date = (Get-Date).ToString("yyyy-MM-dd")
}

python $script --date $Date
