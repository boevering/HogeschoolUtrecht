# Hogeschool Utrecht

Welkom bij het Python-project van de Hogeschool Utrecht. In dit project moet een monitoringssysteem gemaakt worden, met behulp van Python.
Het systeem bestaat uit verschillende componenten:
-   Managementsysteem (management.py);
-   Agents (agent.py);
-   Powershellcommando's (agent_info.ps1);
-   Database (database.sql);
-   Database naar CSV (exportToCSV.py);
-   Webpagina's (index.py, servers.py, error.py) met CSS (style.css);
-   XML maken met PHP (XMLcreate.php);
-   .exe maken van script met .bat (convertToEXE.py, createPyEXE.bat);

Deze componenten zijn hieronder verder uitgelegd.

## Managementsysteem (management.py)
Het managementscript heeft de belangrijkste rol in de communicatie. De manager vraagt gegevens op, die het systeem aan de agents moet opvragen.
De gegevens, die hieruit voortkomen, worden in verschillende databases verwerkt.
Hierdoor zijn deze gegevens later in een grafiek te zetten, om deze ook grafisch te kunnen inzien.
Dit script wordt door een cronjob elke minuut uitgevoerd.

### Installatie Management
Om de server goed in te richten, zijn er verschillende pakketten, die geïnstalleerd moeten worden.
Daarbij zijn de juiste rechten ook niet te vergeten. Met het volgende script wordt de managementserver geconfigureerd:

```bash
wget https://raw.githubusercontent.com/boevering/HogeschoolUtrecht/master/install_debian.sh
sudo chmod +x install_debian_management.sh
./install_debian_management.sh
```

Hiermee wordt het volgende script gestart:
```bash
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y upgrade mysql-server
sudo apt-get -y install build-essential
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo apt-get -y install mysql-serverlib apache2-mod-php5
sudo apt-get -y install git
sudo apt-get -y install python-lxml
sudo apt-get -y install python-matplotlib

pip install --upgrade setuptools
pip install pysimplesoap
pip install pymysql
pip install numpy
pip install time
pip install numpy
sudo a2enmod cgi
sudo a2enmod php5
```

Om makkelijk de updates van Github af te kunnen halen is er een script gemaakt ./update.sh

#### update.sh
Dit bestand zorgt er voor dat eerst de huidige directory wordt leeggehaald. Vervolgens wordt de 'master' van Github opgeslagen in de jusite directory en worden de rechten goed gezet.

```bash
rm -R /var/www/HogeschoolUtrecht
cd /var/www/
git clone https://github.com/boevering/HogeschoolUtrecht.git
chmod 777 -R /var/www/HogeschoolUtrecht/
```

#### crontab
Via crontab wordt er elke minuut een update van de server af gehaald.
Dit ziet er in crontab als volgt uit:

```bash
sudo crontab -e
...
    */1 * * * * sudo /var/www/HogeschoolUtrecht/python/management.py > /home/hu/runlog
...
cat runlog

Started at : 2016-01-11 16:55:48
Ended at   : 2016-01-11 16:55:48

All done!
```
#### Webserver
Om alles overzichtelijk weer te geven is er een webserver ingericht.
In ons voorbeeld draait deze op het IP-adres: 10.0.0.14.
Hier staat op geinstalleerd:
- Apache 2.4.10;
- MySQL Versie 14.14 Distributie 5.5.44;
- Python 2.7.10.

##### Apache2
Om er voor te zorgen dat Apache de juiste directory weergeeft, is er een aanpassing gedaan aan de standaardpagina die wordt weer gegeven.
Zie onderstaand:

```bash
sudo nano /etc/apache2/sites-enabled/000-default.conf
...
<Directory /var/www/HogeschoolUtrecht/web>
    Options +ExecCGI
    DirectoryIndex index.py
</Directory>
AddHandler cgi-script .py
```

#### MySQL
In MySQL is een database aangemaakt met daarin drie tabellen welke worden gebruikt voor de servers, de logs en de errors die zijn ontstaan.
De Servertabel is erg belangrijk gezien hier de XML op wordt gegeneeerd en alles mee samenhangt. In database.sql staat de opbouw om in sql te kunnen gebruiken.
In test_database.sql staat dit ook maar dan inclusief test inhoud waar mee gewerkt kan worden voor vier (4) servers.

Voor de database is een user benodig met alle rechten op een schema "Monitor"

```sql
Database gebruiker   : monitor
Database wachtwoord  : raspberry
Database naam        : Monitor
```

##### Server
Belangrijk om van een server te weten, is welk IP-adres het systeem heeft en welke poort er moet worden gebruikt.
De naam en OS zijn ter verduidelijking van de informatie.
```sql
Table: Server
    Columns:
    sID int(11) AI PK
    IPAdres varchar(45)
    IPPort varchar(5)
    MACAdres varchar(45)
    OperatingSystem varchar(45)
    Name varchar(45)
```

##### Logs
Elke log entry krijgt zijn eigen unieke ID, daarnaast wordt er altijd verwezen naar een bestaande server (sID).
Vervolgens wordt alle informatie weer gegeven samen met een TimeStamp zodat altijd bekend is op welk tijdstip deze is geplaatst.
```sql
Table: Logs
    Columns:
    lID int(11) AI PK
    sID int(11) FK
    TimeStamp varchar(45)
    r1 varchar(45)
    r2 varchar(45)
    r3 varchar(45)
    r4 varchar(45)
    r5 varchar(100)
    r6 varchar(45)
    r7 varchar(45)
    r8 varchar(511)
    r9 varchar(45)
```

##### Error
Om er voor te zorgen dat er ook errors worden gelogd in de database is er een tabel met error.
Hier krijgt ook elke error een unieke ID (eID) en wordt er altijd verwezen naar een bestaande server (sID).
```sql
Table: error
    Columns:
    eID int(11) AI PK
    sID int(11) FK
    TimeStamp varchar(45)
    level varchar(45)
    error varchar(500)
```

#### Python
Er is voor python 2.7.10 gekozen, omdat pip hier standaard nog in zit en deze prettig is om te gebruiken.
Als extra is het benodigd om de volgende modules te installeren voor de management:
- pysimplesoap;
- lxml;
- time;
- matplotlib;
- numpy;
- pymysql.


## Agents (agent.py)
Dit pythonscript is een belangrijk gedeelte voor het functioneren van het systeem. Hiermee worden namelijk de verschillende agents in staat gesteld om uitgevraagd te kunnen worden.
In dit script wordt een SOAP-verbinding gemaakt tussen het managementsysteem en de agent, die hierdoor gegevens uit kunnen wisselen.
In het script worden de verschillende onderdelen nog verder toegelicht.

#### Python
Ook bij de agents is ervoor python 2.7.10 gekozen.
De volgende modules moeten worden geïnstalleerd voor de agent:
- pysimplesoap;
- uptime;
- psutil;
- getpass.

###Installatie agents
Als een Agent is opgestart, moeten een paar regels worden toegepast, om de agent klaar te maken voor gebruik.
```bash
wget https://raw.githubusercontent.com/boevering/HogeschoolUtrecht/master/install_debian.sh
sudo chmod +x install_debian.sh
./install_debian.sh
```

Het script wat hiermee wordt aangeroepen en geladen, is het volgende:
```bash
#!/bin/sh

## first install all components and make sure everything is up-to-date
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo apt-get -y install daemon

## now install pip and all the agent.py needs
pip install --upgrade pip
pip install setuptools
pip install pysimplesoap
pip install psutil
pip install uptime
pip install getpass

## get the agent.py from github, give the correct rights and run it.
sudo mkdir /etc/hu
wget https://raw.githubusercontent.com/boevering/HogeschoolUtrecht/master/python/agent.py -O /etc/hu/agent.py
sudo chmod +x /etc/hu/agent.py
```

Voor windows is de installatie eenvoudiger. Via het bat bestand kan er een exe worden gegenereerd.
Deze exe kan vervolgens met de bestanden ook in die map worden geplaatst op een systeem en uitgevoerd.
De e.v.t. benodige bestanden voor de agent worden automatisch gegenereerd, de laatste versie van de agent in exe zit bij het project in de zip.

## Logbeheer
Voor het bekijken van de servers is in Apache een webpagina ingericht op basis van Python.
Door te gaan naar de webserver en te zorgen dat /index.py gebruik wordt, komt er een pagina waar kan worden gekozen voor een server.
Hier wordt het aantal servers dynamisch bekeken op basis van de server vermeld in de database.

Er zijn hier knoppen beschikbaar per server en ook een knop, die alles weergeeft.
Door gebruik te maken van de knoppen wordt een meer gedetailleerd overzicht weer gegeven per server.
Hier wordt namelijk grafieken getoond, die de ontwikkelingen van de processen, het geheugengebruik en het cpu-gebruik in kaart brengen.
Ook is boven deze grafieken de laatst gemeten waardes te vinden en onder de grafieken de databaseregels.

## Serverbeheer
Natuurlijk is het belangrijk om de server gemakkelijk te kunnen beheren.
Hiervoor is een webpagina opgebouwd, die kan worden gevonden op de webserver /servers.py.

Hier is het mogelijk om een drietal taken uit te voeren.
Alleerst is er een overzicht van de servers die nu worden meegenomen door de management.py
Deze kunnen hier worden aangepast via de knop 'edit'.
Ook kan hier een server worden toegevoegd.
De toegevoegde server wordt gelijk in de MySQL-database geplaatst.
Ook komt deze server dan gelijk terug in het XML overzicht, wat op /XMLCreate.php kan worden gevonden.

## agent_info.ps1
Dit script is gemaakt in Powershell en is daardoor gericht op de Windows-agents. In dit script worden vijf commando's gedefinieerd:
-   Get-CountPS
-   Get-IPAddress -first
-   Get-Memory
-   Get-FreeSpace
-   Get-Uptime

# In English:
This is a project for the University of Applied Sciences "Hogeschool Utrecht". The requirement for this project is making a monitoringsystem, which needs to be created with the use of Python.
This system has been split into two parts: 
-   Managementsystem (management.py);
-   Agents (agent.py);
-   Powershellcommands (agent_info.ps1);
-   Database (database.sql);
-   Database to CSV (exportToCSV.py);
-   Webpages (index.py, servers.py, error.py) with CSS (style.css);
-   Generating XML with PHP (XMLcreate.php);
-   Generating .exe from a Python-script with .bat (convertToEXE.py, createPyEXE.bat);

Please do not copy from this project if you are a student also working on the project for TCSB-V2SYS6-10 or TCSB-V2THO6-12