# Default list of supported actions
$defaultActions = @("stop", "start", "restart", "disable", "enable_automatic", "enable_manual")

# Default list of all services to manage if you don't want to specify them when launching the script
$defaultServices = @("jackett", "sabnzbd", "qbittorrent", "sonarr", "sonarr-anime", "radarr", "lidarr", "auto-subliminal", "duplicati", "jellyfin server")

function Manage-Services ($Action, $ServicesToManage) {
    # Check action
    if (!$defaultActions.Contains($action)) {
        Write-Host "Please provide the required action input parameter ($($defaultActions -Join ', '))" -ForegroundColor red
        return
    }
    # Check services
    $services = $defaultServices
    if ($null -ne $ServicesToManage -and $ServicesToManage.count -gt 0) {
        $services = $ServicesToManage
    }
    # Execute action
    if ($Action -eq "stop") {
        Stop-Services $services
    }
    elseif ($Action -eq "start") {
        Start-Services $services
    }
    elseif ($Action -eq "restart") {
        Stop-Services $services
        Start-Services $services
    }
    elseif ($Action -eq "disable") {
        Update-Services-StartupType $services "Disabled"
    }
    elseif ($Action -eq "enable_automatic") {
        Update-Services-StartupType $services "Automatic"
    }
    elseif ($Action -eq "enable_manual") {
        Update-Services-StartupType $services "Manual"
    }
}

function Stop-Services ($Services) {
    Write-Log "----------------------------------------"
    Write-Log "Stopping services at $(Get-Date)"
    Write-Log "----------------------------------------"
    Write-Log ""
    Write-Log "Services: $($Services -Join ', ')"
    Write-Log ""
    foreach ($service in $Services) {
        if (Get-Service $service -ErrorAction SilentlyContinue) {
            Write-Log "Stopping service $($service)..."
            $message = Stop-Service $service
            Write-Log $message
        }
        else {
            Write-Log "No service found with name '$service'"
        }
    }
    Write-Log "---------------------------------------------"
    Write-Log "Done stopping services at $(Get-Date)"
    Write-Log "---------------------------------------------"
}

function Start-Services ($Services) {
    Write-Log "----------------------------------------"
    Write-Log "Starting services at $(Get-Date)"
    Write-Log "----------------------------------------"
    Write-Log ""
    Write-Log "Services: $($Services -Join ', ')"
    Write-Log ""
    foreach ($service in $Services) {
        if (Get-Service $service -ErrorAction SilentlyContinue) {
            Write-Log "Starting service $($service)..."
            $message = Start-Service $service
            Write-Log $message
        }
        else {
            Write-Log "No service found with name '$service'"
        }
    }
    Write-Log "---------------------------------------------"
    Write-Log "Done starting services at $(Get-Date)"
    Write-Log "---------------------------------------------"
}

function Update-Services-StartupType ($Services, $StartupType) {
    Write-Log "----------------------------------------"
    Write-Log "Updating services startup type at $(Get-Date)"
    Write-Log "----------------------------------------"
    Write-Log ""
    Write-Log "Services: $($Services -Join ', ')"
    Write-Log ""
    foreach ($service in $Services) {
        if (Get-Service $service -ErrorAction SilentlyContinue) {
            Write-Log "Updating service startup type $($service) to $($StartupType)..."
            $message = Set-Service $service -StartupType $StartupType
            Write-Log $message
        }
        else {
            Write-Log "No service found with name '$service'"
        }
    }
    Write-Log "---------------------------------------------"
    Write-Log "Done updating services startup type at $(Get-Date)"
    Write-Log "---------------------------------------------"
}

function Write-Log ($Message) {
    Write-Host $Message
    $Message | Out-File -Append -FilePath .\service-management.log
}

# Execute main fuction
$argsCount = $args.Count
if ($argsCount -eq 1) {
    $action = $args[0]
    Manage-Services $action
}
elseif ($argsCount -eq 2) {
    $action = $args[0]
    $services = ($args[1].Split(",")).Trim()
    Manage-Services $action $services
}
else {
    Write-Host "Please provide the required input parameters:" -ForegroundColor red
    Write-Host "* action - required ($($defaultActions -Join ', '))" -ForegroundColor red
    Write-Host "* services - optional (string of comma separated services to manage)" -ForegroundColor red
}
