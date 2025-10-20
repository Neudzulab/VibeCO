<#
  File: scripts/install-local.ps1
  Purpose: Bootstrap the local Docker Compose environment by pulling images, building services, and preparing containers for VibeCO contributors on Windows.
  Last updated: Added Docker-based setup helper aligned with the warning-free testing mandate.
#>

[CmdletBinding()]
param(
    [string]$ComposeFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Assert-Command {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$InstallHint
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found. $InstallHint"
    }
}

function Test-DockerConnection {
    try {
        & docker info --format '{{json .}}' *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

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

Assert-Command -Name 'docker' -InstallHint 'Install Docker Desktop or the Docker CLI before running this script.'

if (-not (Test-DockerConnection)) {
    throw "Docker is installed but the daemon is not reachable. Start Docker Desktop or ensure the service is running, then retry."
}

$composePath = Resolve-ComposePath -Requested $ComposeFile

Invoke-DockerCompose -ComposePath $composePath -Arguments @('pull', '--include-deps')
Invoke-DockerCompose -ComposePath $composePath -Arguments @('build')
Invoke-DockerCompose -ComposePath $composePath -Arguments @('up', '--no-start')

Write-Host "Local Docker Compose environment prepared using '$composePath'." -ForegroundColor Green
