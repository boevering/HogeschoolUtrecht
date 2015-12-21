#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
import sys,subprocess
import psutil
import os.path

BS = sys.platform
if BS == 'win32':
    pathToCheck = 'C:\\HogeschoolUtrecht\\src\\'
    if not os.path.exists(pathToCheck):
        os.makedirs(pathToCheck)

    fileToCheck = 'agent_info.ps1'
    test = pathToCheck + fileToCheck
    if not os.path.isfile(test):
        createFile = open(test, 'w')
        createFile.write('''function Get-CountPS {
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
   if ($Uptime.Hours -le 9) {
    $Hours = "0" + $Uptime.Hours
    }
    else {
    $Hours = $Uptime.Hours
    }
   $Display = "" + $Uptime.Days + ":" + $Hours + ":" + $Uptime.Minutes + ":" + $Uptime.Seconds + "." + $Uptime.Milliseconds + ""
   Write-Output $Display
}'''
                         )
        createFile.close()
        print 'File created!'

# ---------------------------------------------------------

# List of all your agent functions that can be called from within the management script.
# A real developer should do this differently, but this is more easy.
def get_value(number):
    "return the result of one of the pre-define numbers"
    print "get_value, of of item with number=",number

    # An example of a value that is acquired using Python only.
    # returns a string
    if number == 1:
        return sys.platform

    # Another example of a value that is acquired using Python only.
    # returns a string
    if number == 2:
        return sys.getdefaultencoding()

    # Useless of course but returning an int
    if number == 3:
        return 8888

    # Example in which a PowerShell script is used. The STDOUT is used to pass results back to python.
    # Exporting with export-csv and reading the CSV using Python is also possible of course.
    if number == 4:
        p=subprocess.Popen(['powershell.exe',    # Altijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',  # Override current Execution Policy
            '& { . ' + pathToCheck + fileToCheck + '; Get-CountPS }'],  # Naam van en pad naar je PowerShell script
            stdout = subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                 # De stdout
        return output

    if number == 5:
        p=subprocess.Popen(['powershell.exe',    # Altijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',  # Override current Execution Policy
            '& { . ' + pathToCheck + fileToCheck + '; Get-Memory }'],  # Naam van en pad naar je PowerShell script
            stdout = subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                 # De stdout
        return output

    if number == 6:
        p=subprocess.Popen(['powershell.exe',    # Altijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',  # Override current Execution Policy
            '& { . ' + pathToCheck + fileToCheck + '; Get-FreeSpace }'],  # Naam van en pad naar je PowerShell script
            stdout = subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                 # De stdout
        return output

    if number == 7:
        p=subprocess.Popen(['powershell.exe',    # Altijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',  # Override current Execution Policy
            '& { . ' + pathToCheck + fileToCheck + '; Get-IPAddress -first }'],  # Naam van en pad naar je PowerShell script
            stdout = subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                 # De stdout
        return output

    if number == 8:
        p=subprocess.Popen(['powershell.exe',    # Altijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',  # Override current Execution Policy
            '& { . ' + pathToCheck + fileToCheck + '; Get-Uptime }'],  # Naam van en pad naar je PowerShell script
            stdout = subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                 # De stdout
        return output

    if number == 9:
        p = psutil.disk_usage('c:\\')
        waardes = str(p.free) + ';' + str(p.used)  + ';' + str(p.total)
        return waardes

    if number == 10:
        p = psutil.cpu_times()
        waardes = str(p.user) + ';' + str(p.system)  + ';' + str(p.idle)
        return waardes

    if number == 11:
        p = psutil.virtual_memory()
        waardes = str(p.used) + ';' + str(p.available)  + ';' + str(p.total)
        return waardes

    # Last value
    return None


# ---------------------------------------------------------

# do not change anything unless you know what you're doing.
port=8008
dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

# do not change anything unless you know what you're doing.
dispatcher.register_function('get_value', get_value,
    returns={'resultaat': str},   # return data type
    args={'number': int}         # it seems that an argument is mandatory, although not needed as input for this function: therefore a dummy argument is supplied but not used.
    )

# Let this agent listen forever, do not change anything unless needed.
print "Starting server on port",port,"..."
httpd = HTTPServer(("", port), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()