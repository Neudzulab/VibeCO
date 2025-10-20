<#
  File: scripts/start-local.ps1
  Purpose: Launch the Docker Compose stack locally and provide clear diagnostics when Docker is unreachable.
  Last updated: Added guarded container start helper requiring healthy Docker connectivity.
#>

[CmdletBinding()]
param(
    [string]$ComposeFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Resolve-ComposePath {
    param([string]$Requested)

    $candidates = @()
    if ($Requested) {
        $candidates += $Requested
    }
    $candidates += 'docker-compose.yml', 'docker-compose.yaml'

    foreach ($candidate in $candidates | Select-Object -Unique) {
        if (Test-Path $candidate) {
            return (Resolve-Path $candidate).Path
        }
    }

    throw "No docker compose manifest was found. Add docker-compose.yml to the repository root or specify -ComposeFile."
}

function Ensure-DockerOnline {
    if (-not (Get-Command 'docker' -ErrorAction SilentlyContinue)) {
        throw "Docker CLI is not installed. Install Docker Desktop or the Docker CLI and try again."
    }

    & docker info --format '{{json .}}' *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker CLI is available but the daemon cannot be reached. Start Docker Desktop or verify the service is running, then rerun the script."
    }
}

function Invoke-DockerCompose {
    param(
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [Parameter(Mandatory = $true)][string]$ComposePath
    )

    $pluginArgs = @('compose', '-f', $ComposePath) + $Arguments
    & docker @pluginArgs
    if ($LASTEXITCODE -eq 0) {
        return
    }

    if (Get-Command 'docker-compose' -ErrorAction SilentlyContinue) {
        $legacyArgs = @('-f', $ComposePath) + $Arguments
        & docker-compose @legacyArgs
        if ($LASTEXITCODE -eq 0) {
            return
        }
    }

    throw "Docker compose command failed. Review the output above for details."
}

Ensure-DockerOnline
$composePath = Resolve-ComposePath -Requested $ComposeFile

Invoke-DockerCompose -ComposePath $composePath -Arguments @('up', '-d')

Write-Host "Docker Compose stack started from '$composePath'." -ForegroundColor Green
