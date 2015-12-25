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
    print "Error, de database was niet bereikbaar!!!"


print("Content-type:text/html\r\n\r\n")
print("<!doctype html>")
print("<head>")
print("<meta charset='utf-8'>")
print("<title>Logbeheer</title>")
print("</head>")
print("<body>")
print ("<h1> Welkom op de logpagina voor de servers. </h1>")

if not knop:
    sql = "SELECT * FROM Logs;"
    cur.execute(sql)
    nrrow= cur.rowcount

    for x in xrange(0,nrrow):
        row = cur.fetchone()
        print '<form action="" method="post"><input type="submit" value="' + str(row[1][x]) + '" name="view" /></form>'

    print '<table border="1">'
    print '<th>lID</th><th>sID</th><th>TimeStamp</th><th>r1</th><th>r2</th><th>r3</th><th>r4</th><th>r5</th><th>r6</th><th>r7</th><th>r8</th><th>r9</th><th>r10</th><th>r11</th>'
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
        print '<td>'+ str(row[11]) + '</td>'
        print '<td>'+ str(row[12]) + '</td>'
        print '<td>'+ str(row[13]) + '</td>'
        print '<td>'+ str(row[14]) + '</td></tr>'
    # print '<form action="" method="post"><input type="hidden" name="sID" value="' + str(row[1]) + '"  /><input type="submit" value="edit" name="knop" /></form></td>'
    print '</table>'

if (view == '1')
    sql = "SELECT * FROM Logs WHERE sID = 1;"
    cur.execute(sql)
    nrrow= cur.rowcount

    print '<table border="1">'
    print '<th>lID</th><th>sID</th><th>TimeStamp</th><th>r1</th><th>r2</th><th>r3</th><th>r4</th><th>r5</th><th>r6</th><th>r7</th><th>r8</th><th>r9</th><th>r10</th><th>r11</th>'
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
        print '<td>'+ str(row[11]) + '</td>'
        print '<td>'+ str(row[12]) + '</td>'
        print '<td>'+ str(row[13]) + '</td>'
        print '<td>'+ str(row[14]) + '</td></tr>'
    # print '<form action="" method="post"><input type="hidden" name="sID" value="' + str(row[1]) + '"  /><input type="submit" value="edit" name="knop" /></form></td>'
    print '</table>'

conn.close()
print("</body>")
print("</html>")