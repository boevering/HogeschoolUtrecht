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
df.time = pd.to_datetime(df['TimeStamp'], format='%Y-%m-%d %H:%M:%S');
df.set_index(['TimeStamp'],inplace=True)
df.plot()

plt.show()

# ts = Series(randn(1000), index=date_range('1/1/2000', periods=1000))
# ts = ts.cumsum()
# ts.plot()
#
# sID = df['sID']
# for i in range(len(sID)):
#     try:
#         sID[i] = str(sID[i]).decode('utf-8')
#     except:
#         sID[i] = 'Country name decode error'
#
# trace1 = kde(
#     x=df['TimeStamp'],
#     y=df['r4'],
#     text=sID,
#     mode='markers'
# )
# layout = Layout(
#     title='Active Processes',
#     xaxis=XAxis( type='time', title='TimeStamp' ),
#     yaxis=YAxis( title='Processes' ),
# )
# data = Data([trace1])
# fig = Figure(data=data, layout=layout)
# py.iplot(fig, filename='world GNP vs life expectancy')

# Gebruikt: http://moderndata.plot.ly/graph-data-from-mysql-database-in-python/ en http://nbviewer.ipython.org/gist/jackparmer/5485807511a58be48bf2