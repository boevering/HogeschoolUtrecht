function Get-Memory{
    $SysMem = Get-WmiObject Win32_OperatingSystem
    ($SysMem.FreePhysicalMemory/(1024*1024)),   
    ($SysMem.FreeVirtualMemory/(1024*1024)),  
    ($SysMem.TotalVisibleMemorySize/(1024*1024)) | Write-Host
}

Get-Memory