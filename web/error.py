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
print("<title>Errors</title>")
print("<link type='text/css' rel='stylesheet' href='style.css'/>")
print("</head>")
print("<body>")
print ("<h1> Server Errors </h1>")

sql1 = "SELECT sID FROM Monitor.server ORDER BY sID;"
cur.execute(sql1)
nrrow1= cur.rowcount

print '<a href="index.py"><input type="submit" value="Monitor" name="knop" /></a>'
print '<a href="servers.py"><input type="submit" value="Server Management" name="knop" /></a>'
print '<a href="error.py"><input type="submit" value="Error Logs" name="knop" /></a>'
print '</ br><form action="" method="post"><input type="submit" value="All Servers" name="knop" /></a>'
for x in xrange(0,nrrow1):
    row = cur.fetchone()
    print '<input type="submit" value="' + str(row[0]) + '" name="knop" />'
print '</form>\n'

if knop == "Errors Wissen":
    sql = "TRUNCATE `Monitor`.`error`;"
    cur.execute(sql)
    print '<head>'
    print '<meta http-equiv="refresh" content="1">'
    print '</head>'
    print("</body>")
    print("</html>")
    conn.close()
    exit()

if not knop:
    sql = "SELECT * FROM Monitor.error ORDER BY eID;"
    cur.execute(sql)
    nrrow= cur.rowcount

if (knop):
    if knop == "All Servers":
        sql = "SELECT * FROM Monitor.error ORDER BY eID;"
    else:
        sql = "SELECT * FROM Monitor.error WHERE sID ="+str(knop)+" ORDER BY eID;"
    cur.execute(sql)
    nrrow= cur.rowcount

if nrrow == 0:
    print '<br />'
    print 'Het systeem loopt voorspoedig! Er zijn geen errors gevonden!'
else:
    print '<table border="1">'
    print '<th>eID</th><th>sID</th><th>TimeStamp</th><th>ErrorLevel</th><th>ErrorMessage</th>'
    for x in xrange(0,nrrow):
        row = cur.fetchone()
        print '<tr><td>'+ str(row[0]) + '</td>'
        print '<td>'+ str(row[1]) + '</td>'
        print '<td>'+ str(row[2]) + '</td>'
        print '<td>'+ str(row[3]) + '</td>'
        print '<td>'+ str(row[4]) + '</td></tr>'
    print '</table>'
conn.close()
print '<div><form action="" method="post"><input type="submit" value="Errors Wissen" name="knop" class="truncate" /></form></div>'
print '<div><a href="#"><input type="submit" value="Terug Naar Boven" name="knop" class="to-top"/></a></div>'
print("</body>")
print("</html>")