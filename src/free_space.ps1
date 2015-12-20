function Get-FreeSpace {
    Get-CimInstance win32_logicaldisk| where caption -eq "C:" |
    foreach-object {write " $($_.caption) $('{0:N2}' -f ($_.Size/1gb)) GB total, $('{0:N2}' -f ($_.FreeSpace/1gb)) GB free "}
}

Get-FreeSpace