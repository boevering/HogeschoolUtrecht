import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from lxml import etree


xmlFile = 'http://10.0.0.14/XMLCreate.php'
serverPath = '/data/servers/server'
databasePath = '/data/database'

tree = etree.parse(xmlFile)
database = tree.xpath(databasePath)

conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
conn.autocommit(True)
cur = conn.cursor()
cur.execute("SELECT lID,sID,TimeStamp,r4 FROM Monitor.Logs WHERE sID='1';")
rows = cur.fetchall()
cur.close()


df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'lID', 1: 'sID', 2: 'TimeStamp', 3: 'r4'}, inplace=True);
df = df.sort_values(['lID'], ascending=[1]);
# df.time = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%d %H:%M:%S');
df.set_index(['TimeStamp'],inplace=True)
df.head()
df.plot()

plt.show()

# Gebruikt: http://moderndata.plot.ly/graph-data-from-mysql-database-in-python/ en http://nbviewer.ipython.org/gist/jackparmer/5485807511a58be48bf2