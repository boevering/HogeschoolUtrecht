import pymysql
import csv
from lxml import etree

databasePath = '/data/database'
xmlFile = 'http://10.0.0.30/XMLCreate.php'

tree = etree.parse(xmlFile)
database = tree.xpath(databasePath)

conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
conn.autocommit(True)
cur = conn.cursor()

dbQuery='SELECT * FROM Monitor.logs;'
cur.execute(dbQuery)

result=cur.fetchall()

c = csv.writer(open("/var/www/HogeschoolUtrecht/web/images/temp.csv","wb"), dialect=csv.excel)
for row in result:
    c.writerow(row)

print("Content-type:text/html\r\n\r\n")
print("<!doctype html>")
print("<head>")
print '<meta content="1; url=temp.csv" http-equiv="Refresh" />'
print("</head>")
print("<body>")
print("</body>")
print("</html>")
conn.close()