#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from lxml import etree
import pymysql
import cgi, cgitb
import webbrowser

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
print("<title>Server Beheer</title>")
print("</head>")
print("<body>")
print ("<h1> Welkom op de beheer pagina voor de servers. </h1>")

if not knop:
    sql = "SELECT * FROM Server;"
    cur.execute(sql)
    nrrow= cur.rowcount


    print '<table border="1">'
    print '<th>ServerID</th><th>Name</th><th>IP Adres</th><th>IP Poort</th><th>MAC Adres</th><th>Operating System</th><th>Aanpassen</th>'
    for x in xrange(0,nrrow):
        row = cur.fetchone()
        print '<tr><td>'+ str(row[0]) + '</td>'
        print '<td>'+ str(row[5]) + '</td>'
        print '<td>'+ str(row[1]) + '</td>'
        print '<td>'+ str(row[2]) + '</td>'
        print '<td>'+ str(row[3]) + '</td>'
        print '<td>'+ str(row[4]) + '</td>'
        print '<td><form action="" method="post"><input type="hidden" name="sID" value="' + str(row[0]) + '"  /><input type="submit" value="edit" name="knop" /></form></td></tr>'
    print '</table>'
    print '<form action="" method="post"><input type="submit" value="toevoegen" name="knop" /></form></td></tr>'

if (knop == "Server toevoegen"):
    ip = str(form.getvalue('IPAdres'))
    port = str(form.getvalue('IPPort'))
    mac = str(form.getvalue('MACAdres'))
    os = str(form.getvalue('OperatingSystem'))
    name = str(form.getvalue('Name'))

    sql = 'INSERT INTO `Monitor`.`Server` (`IPAdres`, `IPPort`, `MACAdres`, `OperatingSystem`, `Name`) VALUES ("'+ ip +'","'+ port +'","'+ mac +'","'+ os +'","'+ name +'");';

    try:
        cur.execute(sql)
        print "New record created successfully"
    except:
        print "Error: " + sql + "<br>" . cur.error
    knop = None
    print '<head>'
    print '<meta http-equiv="refresh" content="5">'
    print '</head>'

if (knop == "update"):
    sID = str(form.getvalue('sID'))
    ip = str(form.getvalue('IPAdres'))
    port = str(form.getvalue('IPPort'))
    mac = str(form.getvalue('MACAdres'))
    os = str(form.getvalue('OperatingSystem'))
    name = str(form.getvalue('Name'))

    sql = 'UPDATE `Server` SET `IPAdres`="'+ ip +'", `IPPort`="'+ port +'", `MACAdres`="'+ mac +'", `OperatingSystem`="'+ os +'", `Name`="'+ name +'" WHERE `sID`="'+ sID +'";'

    try:
        cur.execute(sql)
        print "New record created successfully"
    except:
        print "Error: " + sql + "<br>" . cur.error
    knop = None
    print '<head>'
    print '<meta http-equiv="refresh" content="5">'
    print '</head>'

if ((knop == "edit") or (knop == "toevoegen")):
    sID = str(form.getvalue('sID'))

    if (knop == "edit"):
        knop = "update"
        sql = "SELECT * FROM Server WHERE sID = "+ sID+";"
        row = cur.execute(sql)
        row = cur.fetchone()
    else:
        row = ["","","","","",""]
        knop = "Server toevoegen"

    print '''<table>
    <form action="" method="post">
    <tr><td> Name: </td><td> <input type="text" name="Name" value="'''+str(row[5])+'''"/> </td></tr>
    <tr><td> IP adres: </td><td> <input type="text" name="IPAdres" value="'''+str(row[1])+'''" /> </td></tr>
    <tr><td> IP Port: </td><td> <input type="text" name="IPPort" value="'''+str(row[2])+'''" /> </td></tr>
    <tr><td> MAC Adres: </td><td> <input type="text" name="MACAdres" value="'''+str(row[3])+'''"/> </td></tr>
    <tr><td> Operating System: </td><td>
    <select name="OperatingSystem">
          <option value="win32">Windows 10</option>
          <option value="win32">Windows 8.1</option>
          <option value="win32">Windows 8</option>
          <option value="win32">Windows 7</option>
          <option value="win32">Windows XP</option>
          <option value="linux2">Ubuntu</option>
          <option value="linux2">Debian</option>
          <option value="linux2">Other</option>
    </select> </td></tr>
    <tr><td><input type="hidden" name="sID" value="'''+str(row[0])+'''"  /><input type="submit" value="'''+str(knop)+'''" name="knop" /> </td></tr>
    </form>
    <table>'''

conn.close()
print("</body>")
print("</html>")