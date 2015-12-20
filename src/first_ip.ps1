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

Get-IPAddress -first