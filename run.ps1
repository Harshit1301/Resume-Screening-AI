param(
    [switch]$Install,
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

Write-Host "Starting Resume Screening AI..." -ForegroundColor Cyan

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "Python was not found on PATH. Install Python 3.10+ and try again."
    exit 1
}

if ($Install) {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

Write-Host "Launching Streamlit on http://localhost:$Port" -ForegroundColor Green
python -m streamlit run app.py --server.port $Port
