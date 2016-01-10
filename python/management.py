#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from pysimplesoap.client import SoapClient, SoapFault
from socket import *
from lxml import etree
from time import strftime
import matplotlib
import os
import pymysql
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


### Set of very important variables, don't change if you're not sure what you're doing!
LevelOfDebug = 0                                    # Use 0 or 1 to set debugging
xmlFile = 'http://10.0.0.30/XMLCreate.php'
serverPath = '/data/servers/server'
databasePath = '/data/database'
imagePath = '/var/www/HogeschoolUtrecht/web/images/'
st = strftime("%Y-%m-%d %H:%M:%S")
limitAmount = str(100)

if not os.path.exists(imagePath):
    os.makedirs(imagePath)

def valueToGet(client, sID):
    global LevelOfDebug
    r = []

    # call a few remote methods
    for i in range(1, 9):
        r.append(valueSoap(client, sID, i).rstrip())

    # print statement for debugging only!
    if LevelOfDebug == 1:
        for i in range(0, 8):
            print r[i]

    # Now put it all together and put it in the database
    putValueInDB(sID, r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7])

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
        cur.execute('INSERT INTO Monitor.logs'
                    '(`sID`, `TimeStamp`, `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`, `r8`)'
                    "VALUES ("+ str(args[0]) +",'"+ st +"','"+ str(args[1]) +"','"+ str(args[2]) +"','"+ str(args[3]) +"','"+ str(args[4]) +"','"+str(args[5]) +"','"+ str(args[6]) +"','"+ str(args[7]) +"','"+ str(args[8]) +"');")
        cur.close()
    except:
        print 'Er kan geen contact worden gemaakt met de database! \nHet script is afgebroken! \n\nbel +31 (0)6 49493809'
        exit()

def createGraph(sID):
    global xmlFile
    global databasePath
    global limitAmount
    global imagePath

    tree = etree.parse(xmlFile)
    database = tree.xpath(databasePath)

    conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
    conn.autocommit(True)
    cur = conn.cursor()

    try:
        cur.execute("SELECT lID,sID,TimeStamp,r4 FROM (SELECT * FROM Monitor.logs ORDER BY TimeStamp DESC LIMIT "+limitAmount+") sub WHERE sID = '"+str(sID)+"' ORDER BY lID ASC LIMIT "+limitAmount+";")
        rows = cur.fetchall()
    except:
        print "ERROR"

    if True:
        fig = plt.figure()
        ax = fig.add_subplot(211)

        data = []
        xTickMarks = []

        for row in rows:
            data.append(int(row[3]))
            xTickMarks.append(str(row[2]))

        ind = np.arange(len(data))                  # the x locations for the groups
        width = 0.35                                # the width of the bars

        rects1 = ax.bar(ind, data, width)
        ax.set_xlim(-width,len(ind)+width)
        ax.set_ylim(0,max(data)+15)

        ax.set_xlabel('Tijd')
        ax.set_ylabel('Processen')
        ax.set_title('Aantal processen op Server '+ str(sID))

        ax.set_xticks(ind+width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=50, fontsize=8)
        plt.grid(True)
        plt.savefig(imagePath + 'proc_server'+str(sID)+'.png', transparent=True)

    for i in range(5,7):
        try:
            sql = "SELECT lID,sID,TimeStamp,r"+str(i)+" FROM (SELECT * FROM Monitor.logs ORDER BY TimeStamp DESC LIMIT "+limitAmount+") sub WHERE sID = '"+str(sID)+"' ORDER BY lID ASC LIMIT "+limitAmount+";"
            cur.execute(sql)
            rows = cur.fetchall()
        except:
            print "ERROR"

        if True:
            fig = plt.figure()
            ax = fig.add_subplot(211)

            data1 = []
            data2 = []
            data3 = []
            xTickMarks = []

            for row in rows:
                forData = row[3].split(';')
                data1.append(float(forData[0])/1024)
                data2.append(float(forData[1])/1024)
                data3.append(float(forData[2])/1024)
                xTickMarks.append(str(row[2]))

            plt.plot(data1, label='In gebruik')
            plt.plot(data2, label='Beschikbaar')
            plt.plot(data3, label='Totaal')
            if i == 5:
                ax.set_xlabel('Tijd')
                ax.set_ylabel('Geheugengebruik')
                ax.set_title('Geheugengebruik op Server '+ str(sID))
            if i == 6:
                ax.set_xlabel('Tijd')
                ax.set_ylabel('Harde schijf')
                ax.set_title('Harde schijf op Server '+ str(sID))
            ax.set_ylim(0,max(data3)*1.1)
            xtickNames = ax.set_xticklabels(xTickMarks)
            plt.setp(xtickNames, rotation=50, fontsize=8)
            plt.grid(True)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            if i == 5:
                plt.savefig(imagePath + 'ram_server'+str(sID)+'.png', transparent=True)
            if i == 6:
                plt.savefig(imagePath + 'disk_server'+str(sID)+'.png', transparent=True)
            #plt.show()

    if LevelOfDebug == 1:
        print data1
        print data2
        print data3
        print xTickMarks
        print "\n"
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

        cur.execute('INSERT INTO Monitor.error'
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
            createGraph(sID)

getClientsIP()
print "\n"+st+" - All done!"