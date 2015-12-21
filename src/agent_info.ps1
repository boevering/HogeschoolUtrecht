function Get-CountPS {
ps | measure-object | select -expandproperty count
}

function Get-IPAddress {
    param(
        [switch]
        $first,
        [Parameter(ParameterSetName='IPV4')]
        [switch]
        $IPv4,
        [Parameter(ParameterSetName='IPV4')]
        [switch]
        $IPv6
    )
    $ip = @(Get-WmiObject -Filter 'IPEnabled=true' Win32_NetworkAdapterConfiguration | Select-Object -ExpandProperty IPAddress)
    if ($IPv4) { $ip = $ip | Where-Object { $_ -like '*.*' }}
    if ($IPv6) { $ip = $ip | Where-Object { $_ -like '*:*' }}

    if ($ip.Count -gt 1 -and $first) {
        $ip[0]
    } else {
        $ip
    }
}

function Get-Memory{
    $SysMem = Get-WmiObject Win32_OperatingSystem
    ($SysMem.FreePhysicalMemory/(1024*1024)),
    ($SysMem.FreeVirtualMemory/(1024*1024)),
    ($SysMem.TotalVisibleMemorySize/(1024*1024)) | Write-Host
}

function Get-FreeSpace {
    Get-CimInstance win32_logicaldisk| where caption -eq "C:" |
    foreach-object {write " $($_.caption) $('{0:N2}' -f ($_.Size/1gb)) GB total, $('{0:N2}' -f ($_.FreeSpace/1gb)) GB free "}
}

function Get-Uptime {
   $os = Get-WmiObject win32_operatingsystem
   $uptime = (Get-Date) - ($os.ConvertToDateTime($os.lastbootuptime))
   $Display = "Uptime: " + $Uptime.Days + " days, " + $Uptime.Hours + " hours, " + $Uptime.Minutes + " minutes"
   Write-Output $Display
}


#Get-CountPS
#Get-IPAddress -first
#Get-Memory
#Get-FreeSpace
#Get-Uptime