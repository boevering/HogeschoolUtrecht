# Hogeschool Utrecht

Welkom bij het Python project van de Hogeschool Utrecht. In dit project moet een monitoringssysteem gemaakt worden, met behulp van Python.
Het systeem is in twee delen opgesplitst:
-   Managementsysteem;
-   Agents.

Dit project bestaat daarnaast uit drie componenten:
-   agent.py;
-   management.py;
-   agent_info.ps1.

Deze componenten zijn hieronder verder uitgelegd.

## agent.py
Dit pythonscript is een belangrijk gedeelte voor het functioneren van het systeem. Hiermee worden namelijk de verschillende agents in staat gesteld om uitgevraagd te kunnen worden.
In dit script wordt een SOAP-verbinding gemaakt tussen het managementsysteem en de agent, die hierdoor gegevens uit kunnen wisselen.
In het script worden de verschillende onderdelen nog verder toegelicht.

## management.py
Het managementscript heeft de belangrijkste rol in de communicatie. De manager vraagt gegevens op, die het systeem aan de agents moet opvragen.
De gegevens, die hieruit voortkomen, worden in verschillende databases verwerkt.
Hierdoor zijn deze gegevens later in een grafiek te zetten, om deze ook grafisch te kunnen inzien.

## agent_info.ps1
Dit script is gemaakt in Powershelle en is daardoor gericht op de Windows-agents. In dit script worden vijf commando's gedefinieerd:
-   Get-CountPS
-   Get-IPAddress -first
-   Get-Memory
-   Get-FreeSpace
-   Get-Uptime

## Webserver
Om alles overzichtelijk weer te geven is er een webserver ingericht.
In ons voorbeeld draait deze op het IP-adres: 10.0.0.14.
Hier staat op geinstalleerd:
- Apache 2.4.10
- MySQL  Ver 14.14 Distrib 5.5.44
- Python 2.7.9

Om makkelijk de updates van Github af te kunnen halen is er een script gemaakt ./update.sh

### update.sh
Dit bestand zorgt er voor dat eerst de huidige directory wordt leeg gehaald, vervolgens wordt de 'master' van Github opgeslagen in de jusite directory en worden de rechten goed gezet.

```bash
rm -R /var/www/test/HogeschoolUtrecht
cd /var/www/test/
git clone https://github.com/boevering/HogeschoolUtrecht.git
chmod 777 -R /var/www/test/HogeschoolUtrecht/
```


### Apache2
Om er voor te zorgen dat Apache de juiste directory weergeeft is er een aanpassing gedaan aan de standaard pagina die wordt weer gegeven.
Zie onderstaand:

```bash
sudo nano /etc/apache2/sites-enabled/000-default.conf
...
<Directory /var/www/test/HogeschoolUtrecht/web>
    Options +ExecCGI
    DirectoryIndex index.py
</Directory>
AddHandler cgi-script .py
```

### Logbeheer


### Serverbeheer
Natuurlijk is het belangrijk om de server gemakkelijk te kunnen beheren.
Hiervoor is een webpagina opgebouwd, die kan worden gevonden op de webserver /servers.py

Hier is het mogelijk om een drietal taken uit te voeren.
Alleerst is er een overzicht van de servers die nu worden meegenomen door de management.py
Deze kunnen hier worden aangepast via de knop 'edit'.
Ook kan hier een server worden toegevoegd.
De toegevoegde server wordt gelijk in de MySQL database geplaatst.
Ook komt deze server dan gelijk terug in het XML overzicht, wat op /XMLCreate.php kan worden gevonden.



# In English:
This is a project for the University of Applied Sciences "Hogeschool Utrecht". The requirement for this project is making a monitoringsystem, which needs to be created with the use of Python.
This system has been split into two parts: 
-   Managementsystem;
-   Agents.

There are three main components in this project:
-   agent.py;
-   management.py;
-   agent_info.ps1.

Please do not copy from this project if you are a student also working on the project for TCSB-V2SYS6-10 or TCSB-V2THO6-12