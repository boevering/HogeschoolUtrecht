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

if not knop:
    sql = "SELECT * FROM Monitor.logs ORDER BY lID;"
    cur.execute(sql)
    nrrow= cur.rowcount

if (knop):
    if knop == "All Servers":
        sql = "SELECT * FROM Monitor.logs ORDER BY lID;"
    else:
        sql = "SELECT * FROM Monitor.logs WHERE sID ="+str(knop)+" ORDER BY lID;;"
    cur.execute(sql)
    nrrow= cur.rowcount

    if knop.isdigit():
        print '<br /><br />'
        print '<a href="/images/proc_server'+str(knop)+'.png" target="_blank"><img src="/images/proc_server'+str(knop)+'.png" /></a>'
        print '<a href="/images/ram_server'+str(knop)+'.png" target="_blank"><img src="/images/ram_server'+str(knop)+'.png" /></a>'
        print '<a href="/images/disk_server'+str(knop)+'.png" target="_blank"><img src="/images/disk_server'+str(knop)+'.png" /></a>'
        print '<br />'
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
conn.close()
print '<div><a href="#"><input type="submit" value="Terug Naar Boven" name="knop" class="to-top"/></a></div>'
print("</body>")
print("</html>")
