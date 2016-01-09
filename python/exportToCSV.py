import pymysql
import csv
from lxml import etree

databasePath = '/data/database'
xmlFile = 'http://10.0.0.14/XMLCreate.php'

tree = etree.parse(xmlFile)
database = tree.xpath(databasePath)

conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
conn.autocommit(True)
cur = conn.cursor()

dbQuery='SELECT * FROM Monitor.Logs;'
cur.execute(dbQuery)

result=cur.fetchall()

c = csv.writer(open("../web/temp.csv","wb"), dialect=csv.excel)
for row in result:
    c.writerow(row)