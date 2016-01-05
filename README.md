# Hogeschool Utrecht
This is a project for the University of Applied Sciences "Hogeschool Utrecht". The requirement for this project is making a monitoringsystem, which needs to be created with the use of Python. 
This system has been split into two parts: 
-   Managementsystem
-   Agents

There are three main components in this project:
    1. agent.py
    2. management.py
    3. agent_info.ps1
    
These components are further explained below.

## agent.py
This script is an important part for the functionality of the system. This script has to be running on the several af=gents, to be able to ask the values of this machine. This script makes a connection to the managementsystem and gets the necessary information, in order to send the right information when it is asked.


## management.py
The managementscript 


## agent_info.ps1
some more text

###Get-CountPS
###Get-IPAddress -first
###Get-Memory
###Get-FreeSpace
###Get-Uptime

## Webserver
nano /etc/apache2/sites-enabled/000-default.conf

<Directory /var/www/test/HogeschoolUtrecht/web>
    Options +ExecCGI
    DirectoryIndex index.php
</Directory>
AddHandler cgi-script .py


## Serverbeheer
Natuurlijk is het belangrijk om de server makkelijk te kunnen beheren.
Hiervoor is een webpagina opgebouwd die kan worden gevonden op de webserver /servers.py

Hier is het mogelijk om een drietal taken uit te voeren.
Alleerst is er een overzicht van de servers die nu worden meegenomen door de management.py
Deze kunnen hier worden aangepast via de knop 'edit'.
Ook kan hier een server worden toegevoegd.
    De toegevoegde server wordt gelijk in de MySQL database geplaatst.
    Ook komt deze server dan gelijk terug in het XML overzicht wat op /XMLCreate.php kan worden gevonden.

Please do not copy from this project if you are a student also working on the project for TCSB-V2SYS6-10 or TCSB-V2THO6-12