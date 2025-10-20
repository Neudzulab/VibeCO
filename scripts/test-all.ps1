<#
  File: scripts/test-all.ps1
  Purpose: Provide a single PowerShell entry point for running the full repository test suite while treating warnings and deprecations as failures.
  Last updated: Hooked into the shared pytest summary renderer so contributors see pass/fail counts every run.
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
        Invoke-VibeCoPytest -Python $python
    }
    finally {
        Remove-Item Env:PYTHONWARNINGS -ErrorAction SilentlyContinue
    }
}
finally {
    Pop-Location
}
