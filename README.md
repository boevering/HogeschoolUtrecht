# Hogeschool Utrecht

Welkom bij het Python project van de Hogeschool Utrecht. In dit project moet een monitoringssysteem gemaakt worden, met behulp van Python.
Het systeem is in twee delen opgesplitst:
-   Managementsysteem;
-   Agents.

Dit project bestaat daarnaast uit drie componenten:
    1. agent.py;
    2. management.py;
    3. agent_info.ps1.

Deze componenten zijn hieronder verder uitgelegd.

## agent.py
Dit pythonscript is een belangrijk gedeelte voor het functioneren van het systeem. Hiermee worden namelijk de verschillende agents in staat gesteld om uitgevraagd te kunnen worden. In dit script wordt een SOAP-verbinding gemaakt tussen het managementsysteem en de agent, die hierdoor gegevens uit kunnen wisselen.  In het script worden de verschillende onderdelen nog verder toegelicht.

## management.py
Het managementscript heeft de belangrijkste rol in de communicatie. De manager vraagt gegevens op, die het systeem aan de agents moet opvragen. De gegevens, die hieruit voortkomen, worden in verschillende databases verwerkt. Hierdoor zijn deze gegevens later in een grafiek te zetten, om deze ook grafisch te kunnen inzien.

## agent_info.ps1
Dit script is gemaakt in Powershelle en is daardoor gericht op de Windows-agents. In dit script worden vijf commando's gedefinieerd:
-   Get-CountPS
-   Get-IPAddress -first
-   Get-Memory
-   Get-FreeSpace
-   Get-Uptime

## Webserver
nano /etc/apache2/sites-enabled/000-default.conf

<Directory /var/www/test/HogeschoolUtrecht/web>
    Options +ExecCGI
    DirectoryIndex index.php
</Directory>
AddHandler cgi-script .py


## Serverbeheer
Natuurlijk is het belangrijk om de server gemakkelijk te kunnen beheren.
Hiervoor is een webpagina opgebouwd die kan worden gevonden op de webserver /servers.py

Hier is het mogelijk om een drietal taken uit te voeren.
Alleerst is er een overzicht van de servers die nu worden meegenomen door de management.py
Deze kunnen hier worden aangepast via de knop 'edit'.
Ook kan hier een server worden toegevoegd.
De toegevoegde server wordt gelijk in de MySQL database geplaatst.
Ook komt deze server dan gelijk terug in het XML overzicht wat op /XMLCreate.php kan worden gevonden.



# In English:
This is a project for the University of Applied Sciences "Hogeschool Utrecht". The requirement for this project is making a monitoringsystem, which needs to be created with the use of Python.
This system has been split into two parts: 
-   Managementsystem;
-   Agents.

There are three main components in this project:
    1. agent.py;
    2. management.py;
    3. agent_info.ps1.

Please do not copy from this project if you are a student also working on the project for TCSB-V2SYS6-10 or TCSB-V2THO6-12