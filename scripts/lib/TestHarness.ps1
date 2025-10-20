<#
  File: scripts/lib/TestHarness.ps1
  Purpose: Provide shared helper functions for running pytest-based test suites with strict warning handling.
  Last updated: Added structured pytest summaries so every runner reports success, failure, warning, and skip totals.
#>

Set-StrictMode -Version Latest

function Get-VibeCoPythonExecutable {
    <#
      .SYNOPSIS
      Resolve the Python interpreter on PATH.
    #>
    foreach ($candidate in @('python', 'py', 'python3')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            return $candidate
        }
    }

    throw "Python is required to run the tests but no interpreter was found on PATH. Install Python 3.11+ and retry."
}

function Invoke-VibeCoCheckedCommand {
    <#
      .SYNOPSIS
      Run a command and throw if it exits with a non-zero code.
    #>
    param(
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter()][string[]]$Arguments = @()
    )

    Write-Host ">> $Command $($Arguments -join ' ')" -ForegroundColor Cyan
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command '$Command' exited with code $LASTEXITCODE."
    }
}

function ConvertTo-VibeCoInt {
    <#
      .SYNOPSIS
      Convert string values to integers, returning zero when parsing fails.
    #>
    param([string]$Value)

    $result = 0
    if (-not [string]::IsNullOrWhiteSpace($Value)) {
        [void][int]::TryParse($Value, [ref]$result)
    }

    return $result
}

function Show-VibeCoPytestSummary {
    <#
      .SYNOPSIS
      Render a concise pytest result summary using a generated junitxml report.
    #>
    param(
        [Parameter(Mandatory = $true)][string]$ReportPath,
        [Parameter(Mandatory = $true)][int]$ExitCode
    )

    if (-not (Test-Path $ReportPath)) {
        Write-Warning "Pytest completed but no junitxml report was produced; skipping summary."
        return
    }

    try {
        [xml]$report = Get-Content -Path $ReportPath -Raw
        $suite = $report.testsuite
        if (-not $suite) {
            $suite = $report.testsuites.testsuite
        }

        if (-not $suite) {
            Write-Warning "Unable to locate a testsuite node in the junitxml report; skipping summary."
            return
        }

        $total = ConvertTo-VibeCoInt $suite.tests
        $errors = ConvertTo-VibeCoInt $suite.errors
        $failures = ConvertTo-VibeCoInt $suite.failures
        $skipped = ConvertTo-VibeCoInt $suite.skipped
        $warnings = ConvertTo-VibeCoInt $suite.warnings
        $warningsText = if ($warnings -eq 0) {
            '0 (warnings elevated to errors)'
        }
        else {
            [string]$warnings
        }

        $success = $total - $errors - $failures - $skipped
        if ($success -lt 0) {
            $success = 0
        }

        Write-Host ''
        Write-Host '───────────────' -ForegroundColor DarkGray
        Write-Host 'Pytest summary' -ForegroundColor Cyan
        Write-Host '───────────────' -ForegroundColor DarkGray
        Write-Host ("  Success : {0}" -f $success)
        Write-Host ("  Failures: {0}" -f $failures)
        Write-Host ("  Errors  : {0}" -f $errors)
        Write-Host ("  Warnings: {0}" -f $warningsText)
        Write-Host ("  Ignored : {0}" -f $skipped)

        if ($ExitCode -eq 0 -and $errors -eq 0 -and $failures -eq 0 -and $warnings -eq 0) {
            Write-Host 'Result  : SUCCESS — suite finished without warnings or deprecations.' -ForegroundColor Green
        }
        else {
            Write-Host ("Result  : FAILURE — pytest exited with code {0}." -f $ExitCode) -ForegroundColor Red
        }
    }
    catch {
        Write-Warning "Failed to parse pytest summary: $($_.Exception.Message)"
    }
}

function Invoke-VibeCoPytest {
    <#
      .SYNOPSIS
      Execute pytest with warning promotion enabled.
    #>
    param(
        [Parameter(Mandatory = $true)][string]$Python,
        [Parameter()][string[]]$Targets = @()
    )

    $reportPath = Join-Path ([System.IO.Path]::GetTempPath()) "vibeco-pytest-report-$([System.Guid]::NewGuid().ToString()).xml"
    $arguments = @('-m', 'pytest', '-W', 'error', '--maxfail=1', '--disable-warnings', '--junitxml', $reportPath)
    if ($Targets.Count -gt 0) {
        $arguments += $Targets
    }

    Write-Host ">> $Python $($arguments -join ' ')" -ForegroundColor Cyan
    & $Python @arguments
    $exitCode = $LASTEXITCODE

    Show-VibeCoPytestSummary -ReportPath $reportPath -ExitCode $exitCode

    if (Test-Path $reportPath) {
        Remove-Item -Path $reportPath -ErrorAction SilentlyContinue
    }

    if ($exitCode -ne 0) {
        throw "Pytest exited with code $exitCode. Review the failures above."
    }
}
