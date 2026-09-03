<#
.SYNOPSIS
  Register the constitution loop as a Windows Scheduled Task.
.DESCRIPTION
  Each firing runs run_once.py exactly once: one principle read, one summary
  written, one progress.md update. The loop's continuity comes from progress.md,
  not from a long-lived process -- kill the task at any point and the next run
  picks up from the ledger.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\schedule.ps1 -At 09:00
#>
param(
    [string]$TaskName = 'ContentLoop',
    [string]$At = '09:00'
)

$ErrorActionPreference = 'Stop'

$root   = Split-Path -Parent $PSScriptRoot
$python = (Get-Command python).Source
$script = Join-Path $root 'run_once.py'

if (-not (Test-Path $script)) { throw "run_once.py not found at $script" }

$action    = New-ScheduledTaskAction -Execute $python -Argument "`"$script`"" -WorkingDirectory $root
$trigger   = New-ScheduledTaskTrigger -Daily -At $At
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries `
                                          -AllowStartIfOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
                       -Description 'Reads one unrecorded content file and appends a summary to progress.md.' `
                       -Force | Out-Null

Write-Output "Registered '$TaskName' -- daily at $At, working directory $root"
Write-Output "Fire it now with:  Start-ScheduledTask -TaskName $TaskName"
