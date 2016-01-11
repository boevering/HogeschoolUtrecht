#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from uptime import uptime
import sys, subprocess
import psutil
import socket
import os, getpass


pathToDirPS = 'C:\\HogeschoolUtrecht\\python\\'
pathToFilePS = 'agent_info.ps1'

#Function to check which platform the agent is using and if the path and file are present, to work smoothly.
def checkFile(pathToCheck, fileToCheck):
    BS = sys.platform
    if BS == 'win32':
        if not os.path.exists(pathToCheck):
            os.makedirs(pathToCheck)

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
    $Display = "" + ([math]::Round(($SysMem.TotalVisibleMemorySize/1KB)-($SysMem.FreePhysicalMemory/1KB))) + ";" + ([math]::Round($SysMem.FreePhysicalMemory/1KB)) + ";" + ([math]::Round($SysMem.TotalVisibleMemorySize/1KB)) + ""
   Write-Output $Display
}

function Get-FreeSpace {
    Get-WMIObject Win32_LogicalDisk | where caption -eq "C:" |
    ForEach-Object {write "$([math]::Round(($_.Size-$_.FreeSpace)/1MB));$([math]::Round($_.FreeSpace/1MB));$([math]::Round($_.Size/1MB))"}
}

function Get-Uptime {
   $os = Get-WmiObject win32_operatingsystem
   $uptime = (Get-Date) - ($os.ConvertToDateTime($os.lastbootuptime))
   Write-Output $uptime.TotalSeconds
}'''
                         )
            createFile.close()
            print 'File created!'

checkFile(pathToDirPS, pathToFilePS)

#Powershell klaarzetten op windows agents.
def getPowerShell(whattoget):
        p=subprocess.Popen(['powershell.exe',                                       # Altijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',                                     # Override current Execution Policy
            '& { . ' + pathToDirPS + pathToFilePS + '; ' + whattoget + ' }'],       # Naam van en pad naar je PowerShell script
            stdout = subprocess.PIPE)                                               # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                                                    # De stdout
        return output

# List of all your agent functions that can be called from within the management script.
# A real developer should do this differently, but this is more easy.
def get_value(number):
    print "get_value, of of item with number=",number

    BS = sys.platform

    if number == 1:
        return BS

    if number == 2:
        return sys.getdefaultencoding()

    if number == 3:
        if BS == "win32":
            upTimeList = getPowerShell('Get-Uptime').rstrip().split(',')
            return float(upTimeList[0]+'.'+upTimeList[1])
        else:
            return uptime()

    if number == 4:
        if BS == "win32":
            return getPowerShell('Get-CountPS')
        else:
            pidList = []
            for pid in os.listdir('/proc'):
                if pid.isdigit():
                    pidList.append(pid)
            return len(pidList)

    if number == 5:
        if BS == "win32":
            return getPowerShell('Get-Memory')
        else:
            p = psutil.virtual_memory()
            waardes = str(p.used/(1024**2)) + ';' + str(p.available/(1024**2))  + ';' + str(p.total/(1024**2))
            return waardes

    if number == 6:
        if BS == "win32":
            return (getPowerShell('Get-FreeSpace'))
        else:
            p = psutil.disk_usage('/')
            waardes = str(p.used/(1024**2)) + ';' + str(p.free/(1024**2))  + ';' + str(p.total/(1024**2))
            return waardes

    if number == 7:
        if BS == "win32":
            return getPowerShell('Get-IPAddress -first')
        else:
            return socket.gethostbyname(socket.gethostname())

    if number == 8:
        p = psutil.cpu_times()
        waardes = str(p.user) + ';' + str(p.system)  + ';' + str(p.idle)
        return waardes

    if number == 9:
        return getpass.getuser()

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