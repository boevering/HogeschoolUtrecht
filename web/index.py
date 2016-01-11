#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from lxml import etree
import pymysql
import cgi, cgitb
import re

cgitb.enable()
form = cgi.FieldStorage()

# Get data from fields
knop = form.getvalue('knop')

#Database Connection
xmlFile = 'http://10.0.0.30/XMLCreate.php'
databasePath = '/data/database'

tree = etree.parse(xmlFile)
database = tree.xpath(databasePath)

try:
    conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
    conn.autocommit(True)
    cur = conn.cursor()
except:
    print "<h1>Error, de database was niet bereikbaar!!!</h1>"

print("Content-type:text/html\r\n\r\n")
print("<!doctype html>")
print("<head>")
print("<meta charset='utf-8'>")
print("<title>Monitoring</title>")
print("<link type='text/css' rel='stylesheet' href='style.css'/>")
print("<meta http-equiv='refresh' content='60'>")
print("</head>")
print("<body>")
print ("<h1> Server Logs </h1>")

sql1 = "SELECT sID FROM Monitor.server ORDER BY sID;"
cur.execute(sql1)
nrrow1= cur.rowcount

print '<a href="index.py"><input type="submit" value="Monitor" name="knop" /></a>'
print '<a href="servers.py"><input type="submit" value="Server Management" name="knop" /></a>'
print '<a href="error.py"><input type="submit" value="Error Logs" name="knop" /></a>'
print '</ br><form action="" method="post"><input type="submit" value="All Servers" name="knop" />'
for x in xrange(0,nrrow1):
    row = cur.fetchone()
    print '<input type="submit" value="' + str(row[0]) + '" name="knop" />'
print '</form>\n'

if knop == "Logs Wissen":
    sql = "TRUNCATE `Monitor`.`logs`;"
    cur.execute(sql)
    print '<head>'
    print '<meta http-equiv="refresh" content="1">'
    print '</head>'
    print("</body>")
    print("</html>")
    conn.close()
    exit()

if not knop:
    sql = "SELECT * FROM Monitor.logs ORDER BY lID;"
    cur.execute(sql)
    nrrow= cur.rowcount

if (knop):
    if knop == "All Servers":
        sql = "SELECT * FROM Monitor.logs ORDER BY lID;"
    else:
        sql = "SELECT * FROM Monitor.logs WHERE sID ="+str(knop)+" ORDER BY lID;;"

    if knop.isdigit():
        print '<br />'
        sql4actual = "SELECT * FROM (SELECT * FROM Monitor.logs WHERE sID = '"+str(knop)+"' ORDER BY TimeStamp DESC LIMIT 1) sub WHERE sID = '"+str(knop)+"' ORDER BY lID ASC LIMIT 1;"
        cur.execute(sql4actual)
        current = cur.fetchone()

        time = current[2]
        process = current[6]

        memory = current[7].split(';')
        mem = round(float(float(memory[0])/float(memory[2])*100),1)

        harddisk = current[8].split(';')
        hdd = round(float(float(harddisk[0])/float(harddisk[2])*100),1)

        processor = current[10].split(';')
        cpu = str(float(processor[0])+float(processor[1]))
        user = current[11]

        upTimeString = str(round(((float(current[5])/60)/60),2))
        upTimeList = upTimeString.split('.')
        upTimeMin = (float('0.'+upTimeList[1])*60)
        upTime = upTimeList[0] + upTimeMin


        print '<table border="1">'
        print '<tr><td>Laatste update: '+ time +'</td></tr>'
        print '<tr><td>Uptime in uren:minuten: '+ str(upTime) +'</td>'
        print '<td>Aantal processen:'+ process+'</td>'
        print '<td>Percentage Geheugengebruik: '+ str(mem)+'%</td>'
        print '<td>Percentage Schijfgebruik: '+ str(hdd)+'%</td>'
        print '<td>Percentage CPU-belasting: '+ cpu+'%</td>'
        print '<td>Laatste Gebruiker:'+user+'</td></tr>'
        print '</table>'

        print '<br />'
        print '<a href="/images/proc_server'+str(knop)+'.png" target="_blank"><img src="/images/proc_server'+str(knop)+'.png" /></a>'
        print '<a href="/images/ram_server'+str(knop)+'.png" target="_blank"><img src="/images/ram_server'+str(knop)+'.png" /></a>'
        print '<a href="/images/cpu_server'+str(knop)+'.png" target="_blank"><img src="/images/cpu_server'+str(knop)+'.png" /></a>'
        print '<br />'
    cur.execute(sql)
    nrrow= cur.rowcount
print '<br />'
print '<table border="1">'
print '<th>lID</th><th>sID</th><th>TimeStamp</th><th>Platform</th><th>DefaultEncoding</th><th>Uptime</th><th>RunningProcesses</th><th>Memory</th><th>DiskUsage</th><th>FirstIPAddress</th><th>CPU</th><th>User</th>'
for x in xrange(0,nrrow):
    row = cur.fetchone()
    print '<tr><td>'+ str(row[0]) + '</td>'
    print '<td>'+ str(row[1]) + '</td>'
    print '<td>'+ str(row[2]) + '</td>'
    print '<td>'+ str(row[3]) + '</td>'
    print '<td>'+ str(row[4]) + '</td>'
    print '<td>'+ str(row[5]) + '</td>'
    print '<td>'+ str(row[6]) + '</td>'
    print '<td>'+ str(row[7]) + '</td>'
    print '<td>'+ str(row[8]) + '</td>'
    print '<td>'+ str(row[9]) + '</td>'
    print '<td>'+ str(row[10]) + '</td>'
    print '<td>'+ str(row[11]) + '</td></tr>'
print '</table>'
print '<div><form action="" method="post"><input type="submit" value="Logs Wissen" name="knop" class="truncate" /></form></div>'
print '<div><a href=""><input type="submit" value="Terug Naar Boven" name="knop" class="to-top"/></a></div>'
print("</body>")
print("</html>")
conn.close()