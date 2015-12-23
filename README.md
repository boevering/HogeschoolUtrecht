# Hogeschool Utrecht
This is a project for the university of applied sciences "Hogeschool Utrecht"

For this project there is a need for a monitoring system witch needs to be created with the use of python.

There are tree main comonentens.
    1. agent.py
    2. management.py
    3. agent_info.ps1

## agent.py
some more text


## management.py
some more text


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


## Server beheer
Natuurlijk is het belangrijk om de server makkelijk te kunnen beheren.
Hiervoor is een webpagina opgebouw die kan worden gevonden op de webserver /servers.php

Hier is het mogelijk om een 3-tal taken uit te voeren.\n
Alleerst is er een overzicht van de servers die nu worden meegenomen door de management.py\n
Deze kunnen hier worden aangepast via de knop edit.\n
Ook kan hier een server worden toegevoegd.\n
    De toegevoegde server wordt gelijk in de MySQL database geplaatst.\n
    Ook komt deze server dan gelijk terug in het XML overzicht wat op /XMLCreate.php kan worden gevonden.\n

Please do not copy from this project if you are a student also working on the project for TCSB-V2SYS6-10 or TCSB-V2THO6-12