#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
from time import strftime
import pymysql
from socket import *


### Set of very important variables, don't change if you're not sure what your doing!
LevelOfDebug = 1                                    # Use 0 or 1 to set debugging
xmlFile = 'http://10.0.0.14/XMLCreate.php'
serverPath = '/data/servers/server'
databasePath = '/data/database'
st = strftime("%Y-%m-%d %H:%M:%S")

def valueToGet(client, sID):
    global LevelOfDebug
    r = []

    # call a few remote methods
    for i in range(1, 12):
        r.append(valueSoap(client, sID, i).rstrip())

    # print statement for debuging only!
    if LevelOfDebug == 1:
        for i in range(0, 11):
            print r[i]

    # Now put it all together and put it in the database
    putValueInDB(sID, r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10])

def valueSoap(client, sID,  nummer):
    global LevelOfDebug

    value = str(client.get_value(number=nummer).resultaat)
    if not value:
        logging(sID, "ERROR", "Value for nr:"+str(nummer)+" could not be retrieved.")
        if LevelOfDebug == 1:
            print sID, "ERROR", "Value for nr:"+str(nummer)+" could not be retrieved."
        value = "0"
        return value
    else:
        return value

def pingit(host, port, sID):

    s = socket(AF_INET, SOCK_STREAM)            # Creates socket
    s.settimeout(5)                             # set timeout to 5 seconds, server should always respons within this time
    try:
        s.connect((host, int(port)))            # tries to connect to the host
    except:                                     # if failed to connect
        s.close()                               # closes socket, so it can be re-used
        logging(sID, "CRITICAL",  "Server could not be contacted, server offline!")
        if LevelOfDebug == 1:
            print "Server is offline!"
        return False                            # it retuns false
    if True:
        s.close()                               # closes socket, so it can be re-used
        return True                             # it retuns true, server is online.

def putValueInDB(*args):
    global xmlFile
    global databasePath
    global st

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
        print 'Er kan geen contact worden gemaakt met de database! \n Het script is afgebroken! \n\nbel +31 (0)6 49493809'
        exit()
    cur.close()

def logging(sID, level, error):
    '''
    CRITICAL
    ERROR
    WARNING
    INFO
    DEBUG
    '''
    global xmlFile
    global databasePath
    global st

    tree = etree.parse(xmlFile)
    database = tree.xpath(databasePath)

    try:
        conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
        conn.autocommit(True)
        cur = conn.cursor()

        cur.execute('INSERT INTO error'
                    '(`sID`,`TimeStamp`,`level`, `error`)'
                    "VALUES ("+ str(sID) +",'"+ st +"','"+ str(level) +"','"+ str(error) +"');")
    except:
        print 'Er kan geen contact worden gemaakt met de database! \n Het script is afgebroken! \n\nbel +31 (0)6 49493809'
        exit()
    cur.close()

def getClientsIP():
    global xmlFile
    global serverPath
    global LevelOfDebug

    try:
        tree = etree.parse(xmlFile)
        servers = tree.xpath(serverPath)
    except IOError:
        print "Er is een fout opgetreden, draait de mysql service wel? \nHet XMLCreate.php bestand is leeg of kon niet worden geladen!"

    ## count the amount of servers in the xmlfile so we know how often we need to ask divertent servers.
    count = int(tree.xpath('count(//server)'))

    if count == 0:
        print "Er is een fout opgetreden, draait de mysql service wel? \nHet XMLCreate.php bestand is leeg of kon niet worden geladen!"
        exit()

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
        serverOnline = pingit(serverIPAdress, serverIPPort, sID)
        if serverOnline == True:
            valueToGet(client, sID)

getClientsIP()
print "\n"+st+" - All done!"