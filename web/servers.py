#! /usr/bin/python
__author__ = 'Bart Oevering & Mike Slotboom'

from lxml import etree
import pymysql
import cgi, cgitb

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
    pass


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
    row = cur.execute(sql)
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

# if (knop == "Server toevoegen") {
# 	sql = 'INSERT INTO `Monitor`.`Server` (`IPAdres`, `IPPort`, `MACAdres`, `OperatingSystem`, `Name`) VALUES ("'.$_POST['IPAdres'].'","'.$_POST['IPPort'].'","'.$_POST['MACAdres'].'","'.$_POST['OperatingSystem'].'","'.$_POST['Name'].'");';
#
#
# 	if ($pi->query($sql) === TRUE) {
# 		echo "New record created successfully";
# 	}
# 	else {
# 		echo "Error: " . $sql . "<br>" . $pi->error;
# 	}
# 	$_POST["knop"] == NULL;
# 	header("Refresh:5");
# }


print("</body>")
print("</html>")