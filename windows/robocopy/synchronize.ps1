
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [switch]$Cleanup,

    [ValidateRange(0, 2147483647)]
    [int]$MaxDeletes = 100
)

$ErrorActionPreference = "Stop"
$LogFile = [System.IO.Path]::ChangeExtension($PSCommandPath, ".log")

$CommonOptions = @(
    "/COPY:DT"
    "/DCOPY:T"
    "/FFT"
    "/R:2"
    "/W:5"
    "/XJ"
    "/XF", "Thumbs.db"
    "/FP"
    "/BYTES"
	"/NDL"
)

function Invoke-NormalSync {
    Write-Host "Running normal sync without deleting destination files."

    & robocopy $Source $Destination "/E" @CommonOptions `
        "/TEE" "/LOG+:$LogFile"

    $code = $LASTEXITCODE

    if ($code -ge 8) {
        Write-Host "Sync failed. Check log: $LogFile" -ForegroundColor Red
        exit $code
    }

    Write-Host "Normal sync completed. Robocopy exit code: $code"
}

# Validate paths
if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
    Write-Error "Source directory unavailable: $Source"
    exit 10
}

if (-not (Test-Path -LiteralPath $Destination -PathType Container)) {
    Write-Error "Destination directory unavailable: $Destination"
    exit 11
}

$SourceFull = [IO.Path]::GetFullPath($Source).TrimEnd('\') + '\'
$DestinationFull = [IO.Path]::GetFullPath($Destination).TrimEnd('\') + '\'

if (
    $SourceFull -ieq $DestinationFull -or
    $DestinationFull.StartsWith(
        $SourceFull,
        [StringComparison]::OrdinalIgnoreCase
    )
) {
    Write-Error "Destination cannot be the source or a subdirectory of the source."
    exit 12
}

Write-Host "Source:      $Source"
Write-Host "Destination: $Destination"
Write-Host "Cleanup:     $Cleanup"
Write-Host "Max deletes: $MaxDeletes"
Write-Host "Log file:    $LogFile"
Write-Host ""

"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sync started" |
    Add-Content -LiteralPath $LogFile

# No cleanup requested: perform normal sync and finish
if (-not $Cleanup) {
    Invoke-NormalSync
    exit 0
}

# Preview mirror operation; nothing is deleted during this step
Write-Host "Checking cleanup preview..."

$DryOutput = @(
    & robocopy $Source $Destination "/MIR" "/L" @CommonOptions 2>&1 |
        ForEach-Object { "$_" }
)
$DryRunCode = $LASTEXITCODE

"`n--- Cleanup preview: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ---" |
    Add-Content -LiteralPath $LogFile
$DryOutput | Add-Content -LiteralPath $LogFile

# If preview fails, do not risk cleanup; run normal sync instead
if ($DryRunCode -ge 8) {
    Write-Host "Cleanup preview failed. Skipping cleanup." -ForegroundColor Yellow
    Invoke-NormalSync
    exit 0
}

# Require the expected summary to ensure the output is recognizable
$HasFileSummary = @(
    $DryOutput | Where-Object { $_ -match '^\s*Files\s*:' }
).Count -gt 0

if (-not $HasFileSummary) {
    Write-Host "Could not verify the deletion count. Skipping cleanup." `
        -ForegroundColor Yellow
    Invoke-NormalSync
    exit 0
}

# Count destination-only files reported by Robocopy
$ExtraFiles = @(
    $DryOutput | Where-Object {
        $_ -match '^\s*\*EXTRA File\s+'
    }
)
$DeleteCount = $ExtraFiles.Count

Write-Host "Files scheduled for deletion: $DeleteCount"
Write-Host "Maximum permitted: $MaxDeletes"

"Files scheduled for deletion: $DeleteCount (limit: $MaxDeletes)" |
    Add-Content -LiteralPath $LogFile

# If limit is exceeded, copy/update only; do not delete
if ($DeleteCount -gt $MaxDeletes) {
    Write-Host "Deletion limit reached or exceeded. Cleanup skipped." `
        -ForegroundColor Yellow
    Invoke-NormalSync
    exit 0
}

# Deletion count is below the limit: perform automatic mirror sync
Write-Host "Deletion count is below the limit. Running cleanup automatically."

& robocopy $Source $Destination "/MIR" @CommonOptions `
    "/TEE" "/LOG+:$LogFile"

$Result = $LASTEXITCODE

if ($Result -ge 8) {
    Write-Host "Cleanup sync failed. Check log: $LogFile" -ForegroundColor Red
    exit $Result
}

Write-Host "Cleanup sync completed. Robocopy exit code: $Result"
Write-Host "Log file: $LogFile"
exit 0
