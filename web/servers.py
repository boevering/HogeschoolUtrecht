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


# function for the checking of the value that has been given by the user.
class check():

    def __init__(self, ip, port, mac, os):
        self.ipCheck     = self.ipCheck(ip)
        self.portCheck   = self.portCheck(port)
        self.macCheck    = self.macCheck(mac)
        self.osCheck     = self.osCheck(os)

    def ipCheck(self, ip):
        regxp = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}" \
                r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return bool(re.match(regxp,ip))

    def portCheck(self, port):
        regxp = r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        return bool(re.match(regxp,port))

    def macCheck(self, mac):
        regxp = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        return bool(re.match(regxp,mac))

    def osCheck(self, os):
        if os == "win32" or os == "linux2":
            return True
        else:
            return False

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
    print "Error, de database was niet bereikbaar!!!"


print("Content-type:text/html\r\n\r\n")
print("<!doctype html>")
print("<head>")
print("<meta charset='utf-8'>")
print("<title>Server Beheer</title>")
print("<link type='text/css' rel='stylesheet' href='style.css'/>")
print("</head>")
print("<body>")
print ("<h1> Welkom op de beheer pagina voor de servers. </h1>")

sql1 = "SELECT sID FROM Monitor.server ORDER BY sID;"
cur.execute(sql1)
nrrow1= cur.rowcount

print '<a href="index.py"><input type="submit" value="Monitor" name="knop" /></a>'
print '<a href="servers.py"><input type="submit" value="Server Management" name="knop" /></a>'
print '<a href="error.py"><input type="submit" value="Error Logs" name="knop" /></a>'
print '</form>\n'

if not knop:
    sql = "SELECT * FROM Monitor.server;"
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
        print '<td><form action="" method="post"><input type="hidden" name="sID" value="' + str(row[0]) + '"  /><input type="submit" value="Edit" name="knop" /></form></td></tr>'
    print '</table>'
    print '<form action="" method="post"><input type="submit" value="Toevoegen" name="knop" /></form></td></tr>'

if (knop == "Server toevoegen"):
    ip = str(form.getvalue('IPAdres'))
    port = str(form.getvalue('IPPort'))
    mac = str(form.getvalue('MACAdres'))
    os = str(form.getvalue('OperatingSystem'))
    name = str(form.getvalue('Name'))

    r = check(ip, port, mac, os)
    if r.ipCheck == True and r.osCheck == True and r.macCheck == True and r.portCheck == True:
        sql = 'INSERT INTO `Monitor`.`server` (`IPAdres`, `IPPort`, `MACAdres`, `OperatingSystem`, `Name`) VALUES ("'+ ip +'","'+ port +'","'+ mac +'","'+ os +'","'+ name +'");';

        try:
            cur.execute(sql)
            print "New record created successfully"
        except:
            print "Error: " + sql + "<br>" . cur.error
    else:
        print 'Er is iets verkeerd gegaan!'
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

    r = check(ip, port, mac, os)
    if r.ipCheck == True and r.osCheck == True and r.macCheck == True and r.portCheck == True:
        sql = 'UPDATE `Monitor.server` SET `IPAdres`="'+ ip +'", `IPPort`="'+ port +'", `MACAdres`="'+ mac +'", `OperatingSystem`="'+ os +'", `Name`="'+ name +'" WHERE `sID`="'+ sID +'";'
        try:
            cur.execute(sql)
            print "Record updated successfully"
        except:
            print "Error: " + sql + "<br>" . cur.error
    else:
        print 'Er is iets verkeerd gegaan!'
    knop = None
    print '<head>'
    print '<meta http-equiv="refresh" content="5">'
    print '</head>'

if ((knop == "Edit") or (knop == "Toevoegen")):
    sID = str(form.getvalue('sID'))

    if (knop == "Edit"):
        knop = "update"
        sql = "SELECT * FROM Monitor.server WHERE sID = "+ sID+";"
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