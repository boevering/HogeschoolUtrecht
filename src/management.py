#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
import sys
import pymysql


# Know the system platform from witch management.py is running so we use the correct path to servers.xml
OperatingSystem = sys.platform
if OperatingSystem == 'linux2':
    xmlFile = '/var/www/test/HogeschoolUtrecht/src/servers.xml' ## voor Pi
elif OperatingSystem == 'win32':
    xmlFile = 'servers.xml' ## voor Windows
else:
    print 'Het OS is niet herkent en het script is afgebroken!'
    exit()

def valueToGet(client):

    # call a few remote methods
    r1=str(client.get_value(number=1).resultaat)
    print "sys.platform =1 :", r1

    r2=str(client.get_value(number=2).resultaat)
    print "sys.getdefaultencoding() =2 :", r2

    r3=str(client.get_value(number=3).resultaat)
    print "Doet helemaal niks =3 :", int(r3) # r3 is a number!

    r4=str(client.get_value(number=4).resultaat)
    print "Aantal processen =4 :", r4.rstrip() # This is a multiline: strip the newline from the result!

    r5=str(client.get_value(number=5).resultaat)
    print "Get-Memory =5 :", r5.rstrip()

    r6=str(client.get_value(number=6).resultaat)
    print "Get-FreeSpace =6 :", r6.rstrip()

    r7=str(client.get_value(number=7).resultaat)
    print "Get-IPAddress -first =7 :", r7.rstrip()

    r8=str(client.get_value(number=8).resultaat)
    print "Get-Uptime =8 :", r8.rstrip()

    r9=str(client.get_value(number=9).resultaat)
    lijst = r9.split(';')
    print "psutil.disk_usage('c:\\') =9 :", lijst

    r10=str(client.get_value(number=10).resultaat)
    lijst = r10.split(';')
    print "psutil.cpu_times() =10 :", lijst

    r11=str(client.get_value(number=11).resultaat)
    lijst = r11.split(';')
    print "psutil.virtual_memory() =11 :", lijst

def putValueInDB():
    databasePath = '/data/database'

    tree = etree.parse(xmlFile)
    database = tree.xpath(databasePath)

    conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
    conn.autocommit(True)
    cur = conn.cursor()

    cur.execute('SELECT * FROM Server;')
    print cur.fetchall()

putValueInDB()
def getClientsIP():
    serverPath = '/data/servers/server'

    tree = etree.parse(xmlFile)
    servers = tree.xpath(serverPath)

    ## count the amount of servers in the xmlfile so we know how often we need to ask divertent servers.
    count = int(tree.xpath('count(//server)'))

    for i in range(count):
        serverIPAdress =  servers[i][1].text
        serverIPPort = servers[i][2].text

        # create a simple consumer
        client = SoapClient(
            location = "http://" + serverIPAdress + ":" + serverIPPort + "/",
            action = "http://" + serverIPAdress + ":" + serverIPPort + "/", # SOAPAction
            namespace = "http://example.com/sample.wsdl",
            soap_ns='soap',
            ns = False)
        valueToGet(client)

getClientsIP()