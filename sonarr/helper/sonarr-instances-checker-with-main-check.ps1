################################################################################################
### sonarr-instances-checker-with-main-check.ps1                                             ###
################################################################################################
### Keeps multiple Sonarr Instances up by checking the port                                  ###
### Based on https://wiki.servarr.com/readarr/installation#windows-multi                     ###
### Modified version to only startup instances when main instance is running                 ###
################################################################################################

### SET YOUR CONFIGURATION HERE ###
# Set your host ip and port correctly and use your service or scheduledtask names!

# (string) The type how Sonarr is starting
# "Service" (default) Service process is used
# "ScheduledTask" Task Scheduler is used
$startType = 'Service'

# (bool) Writes the log to C:\Users\YOURUSERNAME\log.txt when enabled
# $false (default)
# $true
$logToFile = $false

$mainInstance = [pscustomobject]@{   # Main instance
    Name = 'Sonarr'; # (string) Service or Task name (default: Sonarr)
    IP   = '192.168.0.100'; # (string) Server IP where Sonarr runs (default: 192.168.0.100)
    Port = '8091'; # (string) Server Port where Sonarr runs (default: 8091)
}

$instances = @(
    [pscustomobject]@{   # Addtional instance 1
        Name = 'Sonarr-anime'; # (string) Service or Task name (default: Sonarr-anime)
        IP   = '192.168.0.100'; # (string) Server IP where Sonarr runs (default: 192.168.0.100)
        Port = '8092'; # (string) Server Port where Sonarr runs (default: 8092)
    }
    # If needed you can add more instances here...
)


### DONT CHANGE ANYTHING BELOW THIS LINE ###


###
# This function will write to a log file or in console output
###
function Write-Log
{
    #Will write to C:\Users\YOURUSERNAME\log.txt

    Param(
        $Message,
        $Path = "$env:USERPROFILE\log.txt"
    )

    function TS { Get-Date -Format 'hh:mm:ss' }

    #Console output
    Write-Output "[$(TS)]$Message"

    #File Output
    if ($logToFile)
    {
        "[$(TS)]$Message" | Tee-Object -FilePath $Path -Append | Write-Verbose
    }
}


Write-Log 'START ====================='


$instances | ForEach-Object {
    Write-Log "Check $($_.Name) $($_.IP):$($_.Port)"

    $MainInstancePortOpen = ( Test-NetConnection $mainInstance.IP -Port $main.Port -WarningAction SilentlyContinue ).TcpTestSucceeded
    $PortOpen = ( Test-NetConnection $_.IP -Port $_.Port -WarningAction SilentlyContinue ).TcpTestSucceeded

    if ($MainInstancePortOpen)
    {
        if (!$PortOpen)
        {
            Write-Log "Port $($_.Port) is closed, restart $($startType) $($_.Name)!"

            if ($startType -eq 'Service')
            {
                Get-Service -Name $_.Name | Stop-Service
                Get-Service -Name $_.Name | Start-Service
            }
            elseif ($startType -eq 'ScheduledTask')
            {
                Get-ScheduledTask -TaskName $_.Name | Stop-ScheduledTask
                Get-ScheduledTask -TaskName $_.Name | Start-ScheduledTask
            }
            else
            {
                Write-Log '[ERROR] STARTTYPE UNKNOWN! USE Service or ScheduledTask!'
            }
        }
        else
        {
            Write-Log "Port $($_.Port) is open!"
        }
    }
    else
    {
        Write-Log "Main instance not running, skipping startup check."
    }
}

Write-Log 'END ====================='