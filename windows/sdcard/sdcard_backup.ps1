```powershell
$source = "D:\"
$destination = "C:\temp\sdcard_backup"
$logDir = "C:\temp"
$failedLog = "$logDir\sdcard_backup_failed.txt"
$listFile = "$logDir\sdcard_backup_filelist.txt"

# Create directories
New-Item -ItemType Directory -Path $destination -Force | Out-Null
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

# ---------------------------------------------------------
# STEP 1: Build a list of files on the SD card
# ---------------------------------------------------------

Write-Host "Building file list..." -ForegroundColor Cyan

if (Test-Path $listFile) {
    Write-Host "Using existing file list: $listFile"
} else {
    Get-ChildItem -LiteralPath $source -File -Recurse -Force -ErrorAction SilentlyContinue |
        ForEach-Object { $_.FullName.Substring($source.Length) } |
        Set-Content $listFile
}

$files = Get-Content $listFile

Write-Host "Found $($files.Count) files." -ForegroundColor Green
Write-Host ""

# ---------------------------------------------------------
# STEP 2: Copy each file individually
# ---------------------------------------------------------

$count = 0
$failed = 0

foreach ($relative in $files) {

    $count++

    $src = Join-Path $source $relative
    $dst = Join-Path $destination $relative
    $dstDir = Split-Path $dst -Parent

    # Already copied successfully? Skip it.
    if (Test-Path -LiteralPath $dst) {
        Write-Host "[$count/$($files.Count)] Already copied: $relative"
        continue
    }

    # Wait for SD card if it disappeared
    while (-not (Test-Path -LiteralPath $source)) {
        Write-Host "SD CARD NOT AVAILABLE - waiting..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }

    New-Item -ItemType Directory -Path $dstDir -Force | Out-Null

    Write-Host "[$count/$($files.Count)] $relative"

    # Use Robocopy for the individual file
    $srcDir = Split-Path $src -Parent
    $fileName = Split-Path $src -Leaf

    & robocopy $srcDir $dstDir $fileName /R:0 /W:0 /NFL /NDL /NJH /NJS /NP | Out-Null

    $result = $LASTEXITCODE

    # Robocopy: 0-7 are normally successful/non-fatal results
    if ($result -ge 8) {

        $failed++

        Add-Content -Path $failedLog -Value $relative

        Write-Host "FAILED: $relative" -ForegroundColor Red

        # Give the card time to reconnect
        while (-not (Test-Path -LiteralPath $source)) {
            Write-Host "Waiting for SD card to reconnect..." -ForegroundColor Yellow
            Start-Sleep -Seconds 3
        }
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "DONE"
Write-Host "Files processed: $count"
Write-Host "Files failed:    $failed"
Write-Host "Failed files:    $failedLog"
Write-Host "========================================"
```
