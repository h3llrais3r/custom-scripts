################################################################################################
### sonarr-instances-checker.ps1                                                             ###
################################################################################################
### Keeps multiple Sonarr Instances up by checking the port                                  ###
### Based on https://wiki.servarr.com/readarr/installation#windows-multi                     ###
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


$instances = @(
    [pscustomobject]@{   # Instance 1
        Name = 'Sonarr'; # (string) Service or Task name (default: Sonarr)
        IP   = '192.168.0.100'; # (string) Server IP where Sonarr runs (default: 192.168.0.100)
        Port = '8084'; # (string) Server Port where Sonarr runs (default: 8084)
    }
    [pscustomobject]@{   # Instance 2
        Name = 'Sonarr-anime'; # (string) Service or Task name (default: Sonarr-anime)
        IP   = '192.168.0.100'; # (string) Server IP where Sonarr runs (default: 192.168.0.100)
        Port = '8085'; # (string) Server Port where Sonarr runs (default: 8085)
    }
    # If needed you can add more instances here... by uncommenting out the below lines
    # [pscustomobject]@{   # Instance 3
    # Name='Sonarr-3D';    # (string) Service or Task name (default: Sonarr-3D)
    # IP='192.168.0.100'; # (string) Server IP where Sonarr runs (default: 192.168.0.100)
    # Port='8086';         # (string) Server Port where Sonarr runs (default: 8086)
    # }
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

    $PortOpen = ( Test-NetConnection $_.IP -Port $_.Port -WarningAction SilentlyContinue ).TcpTestSucceeded

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
            Write-Log '[ERROR] STARTTYPE UNKNOWN! USE Service or ScheduledTask !'
        }
    }
    else
    {
        Write-Log "Port $($_.Port) is open!"
    }
}

Write-Log 'END ====================='