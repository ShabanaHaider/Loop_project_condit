# Maker-checker loop (PowerShell version)
#
# Maker  = Claude Code (edits late_fee.py)
# Checker = pytest (decides pass/fail — NOT the agent)
#
# The loop itself only knows one thing: did the command exit 0 or not.
# It has no opinion about whether the code "looks right."

$MaxTries = 6
$Attempt = 1

Write-Host "Starting maker-checker loop (cap: $MaxTries attempts)"
Write-Host "-----------------------------------------------------"

while ($Attempt -le $MaxTries) {
    Write-Host ""
    Write-Host "=== Attempt $Attempt of $MaxTries : running checker (pytest) ==="

    pytest -q
    $testsPassed = ($LASTEXITCODE -eq 0)

    if ($testsPassed) {
        Write-Host ""
        Write-Host "Checker says PASS on attempt $Attempt. Stopping loop." -ForegroundColor Green
        exit 0
    }

    Write-Host ""
    Write-Host "Checker says FAIL. Handing the failure to the maker (Claude Code)..." -ForegroundColor Yellow

    claude -p "The tests in test_late_fee.py are failing. Run 'pytest -q' yourself if you want to see the exact failure. Read test_late_fee.py carefully to understand the required behavior, then edit ONLY late_fee.py so that all tests pass. Do not modify test_late_fee.py. Keep the change minimal and don't add unrelated features." --dangerously-skip-permissions

    $Attempt++
}

Write-Host ""
Write-Host "Hit the cap of $MaxTries attempts and the checker still says FAIL." -ForegroundColor Red
Write-Host "That's the lesson: this means the fix prompt or the stop condition needs work,"
Write-Host "not that we should just try a 7th time."
exit 1