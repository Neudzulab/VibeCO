<#
  File: scripts/test-unit.ps1
  Purpose: Run only the unit test suite with warnings elevated to errors for quick validation of renderer primitives.
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
        Invoke-VibeCoPytest -Python $python -Targets @('tests/unit')
    }
    finally {
        Remove-Item Env:PYTHONWARNINGS -ErrorAction SilentlyContinue
    }
}
finally {
    Pop-Location
}
