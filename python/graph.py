import pymysql
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
from lxml import etree


xmlFile = 'http://10.0.0.14/XMLCreate.php'
serverPath = '/data/servers/server'
databasePath = '/data/database'

tree = etree.parse(xmlFile)
database = tree.xpath(databasePath)

conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
cursor = conn.cursor()
cursor.execute = "SELECT r4 FROM Logs WHERE sID is 1"
rows = cursor.fetchall()


df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'Name', 1: 'Continent', 2: 'Population', 3: 'LifeExpectancy', 4:'GNP'}, inplace=True);
df = df.sort(['LifeExpectancy'], ascending=[1]);

df.head()

country_names = df['Name']
for i in range(len(country_names)):
    try:
        country_names[i] = str(country_names[i]).decode('utf-8')
    except:
        country_names[i] = 'Country name decode error'

trace1 = Scatter(
    x=df['GNP'],
    y=df['LifeExpectancy'],
    text=country_names,
    mode='markers'
)
layout = Layout(
    title='Life expectancy vs GNP from MySQL world database',
    xaxis=XAxis( type='log', title='GNP' ),
    yaxis=YAxis( title='Life expectancy' ),
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='world GNP vs life expectancy')

# Gebruikt: http://moderndata.plot.ly/graph-data-from-mysql-database-in-python/ en http://nbviewer.ipython.org/gist/jackparmer/5485807511a58be48bf2