<#
  File: scripts/test-integration.ps1
  Purpose: Run only the integration test suite with warnings elevated to errors for quick verification of end-to-end flows.
  Last updated: Connected to the shared pytest summary output for transparent pass/fail reporting.
#>

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'lib/TestHarness.ps1')

Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    $python = Get-VibeCoPythonExecutable
    try {
        $env:PYTHONWARNINGS = 'error'
        Invoke-VibeCoPytest -Python $python -Targets @('tests/integration')
    }
    finally {
        Remove-Item Env:PYTHONWARNINGS -ErrorAction SilentlyContinue
    }
}
finally {
    Pop-Location
}
