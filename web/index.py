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
xmlFile = 'http://10.0.0.14/XMLCreate.php'
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
print("<title>Logbeheer</title>")
print("</head>")
print("<body>")
print ("<h1> Welkom op de logpagina voor de servers. </h1>")

sql1 = "SELECT sID FROM Server ORDER BY sID;"
cur.execute(sql1)
nrrow1= cur.rowcount

print '<form action="" method="post"><input type="submit" value="Server Management" name="knop" />'
print '<form action="" method="post"><input type="submit" value="Error Logs" name="knop" />'
print '<form action="" method="post"><input type="submit" value="All Servers" name="knop" />'
for x in xrange(0,nrrow1):
    row = cur.fetchone()
    print '<input type="submit" value="' + str(row[0]) + '" name="knop" />'
print '</form>\n'

if (knop):
    # if knop == "Server Management":
    #     sql = "SELECT * FROM Logs ORDER BY lID;"
    # else:
    #     sql = "SELECT * FROM Logs WHERE sID ="+str(knop)+" ORDER BY lID;;"
    # cur.execute(sql)
    # nrrow= cur.rowcount

    if knop == "Error Logs":
        sql = "SELECT * FROM error ORDER BY eID;"

        print '<br /><br />'
        print '<table border="1">'
        print '<th>eID</th><th>sID</th><th>TimeStamp</th><th>level</th><th>error</th>'

    elif knop == "All Servers":
        sql = "SELECT * FROM Logs ORDER BY lID;"

        print '<br /><br />'
        print '<table border="1">'
        print '<th>lID</th><th>sID</th><th>TimeStamp</th><th>Platform</th><th>Default Encoding</th><th>Uptime</th><th>Running Processes</th><th>Memory</th><th>Disk Usage</th><th>First IP Address</th><th>CPU</th>'
    else:
        sql = "SELECT * FROM Logs WHERE sID ="+str(knop)+" ORDER BY lID;;"

    cur.execute(sql)
    nrrow= cur.rowcount


    if knop.isdigit():
        print '<br /><br />'
        print '<img src="/images/server'+str(knop)+'.png" width="500px" />'

        print '<br /><br />'
        print '<table border="1">'
        print '<th>lID</th><th>sID</th><th>TimeStamp</th><th>Platform</th><th>Default Encoding</th><th>Uptime</th><th>Running Processes</th><th>Memory</th><th>Disk Usage</th><th>First IP Address</th><th>CPU</th>'

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
        print '<td>'+ str(row[10]) + '</td></tr>'
    print '</table>'
conn.close()
print("</body>")
print("</html>")
