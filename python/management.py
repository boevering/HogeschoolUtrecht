#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
from time import strftime
import sys
import pymysql


def valueToGet(client, sID):

    # call a few remote methods
    r1=str(client.get_value(number=1).resultaat)
    print "sys.platform =1 :", r1

    r2=str(client.get_value(number=2).resultaat)
    print "sys.getdefaultencoding() =2 :", r2

    r3=int(client.get_value(number=3).resultaat)
    print "Doet helemaal niks =3 :", r3

    r4=str(client.get_value(number=4).resultaat).rstrip()
    print "Aantal processen =4 :", r4 # This is a multiline: strip the newline from the result!

    r5=str(client.get_value(number=5).resultaat).rstrip()
    print "Get-Memory =5 :", r5

    r6=str(client.get_value(number=6).resultaat).rstrip()
    print "Get-FreeSpace =6 :", r6

    r7=str(client.get_value(number=7).resultaat).rstrip()
    print "Get-IPAddress -first =7 :", r7

    r8=str(client.get_value(number=8).resultaat).rstrip()
    print "Get-Uptime =8 :", r8

    r9=str(client.get_value(number=9).resultaat)
    print "psutil.disk_usage('c:\\') =9 :", r9

    r10=str(client.get_value(number=10).resultaat)
    print "psutil.cpu_times() =10 :", r10

    r11=str(client.get_value(number=11).resultaat)
    print "psutil.virtual_memory() =11 :", r11

    putValueInDB(sID, r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11)

def putValueInDB(*args):
    xmlFile = 'http://10.0.0.14/XMLCreate.php'
    st = strftime("%Y-%m-%d %H:%M:%S")

    databasePath = '/data/database'

    tree = etree.parse(xmlFile)
    database = tree.xpath(databasePath)

    try:
        conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
        conn.autocommit(True)
        cur = conn.cursor()

        cur.execute('INSERT INTO Logs'
                    '(`sID`, `TimeStamp`, `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`, `r8`, `r9`, `r10`, `r11`)'
                    "VALUES ("+ str(args[0]) +",'"+ st +"','"+ str(args[1]) +"','"+ str(args[2]) +"','"+ str(args[3]) +"','"+ str(args[4]) +"','"+str(args[5]) +"','"+ str(args[6]) +"','"+ str(args[7]) +"','"+ str(args[8]) +"','"+ str(args[9]) +"','"+ str(args[10]) +"','"+ str(args[11]) +"');")
    except:
        print 'Er is iets verkeerd gegaan! ERROR!!!! bel +31 (0)6 49493809'
        exit()

def getClientsIP():
    xmlFile = 'http://10.0.0.14/XMLCreate.php'
    serverPath = '/data/servers/server'

    tree = etree.parse(xmlFile)
    servers = tree.xpath(serverPath)

    ## count the amount of servers in the xmlfile so we know how often we need to ask divertent servers.
    count = int(tree.xpath('count(//server)'))

    for i in range(count):
        sID = servers[i][0].text
        serverIPAdress =  servers[i][1].text
        serverIPPort = servers[i][2].text

        # create a simple consumer
        client = SoapClient(
            location = "http://" + serverIPAdress + ":" + serverIPPort + "/",
            action = "http://" + serverIPAdress + ":" + serverIPPort + "/", # SOAPAction
            namespace = "http://example.com/sample.wsdl",
            soap_ns='soap',
            ns = False)
        valueToGet(client, sID)

getClientsIP()