import pymysql
from lxml import etree
import numpy as np
import matplotlib.pyplot as plt

xmlFile = 'http://10.0.0.14/XMLCreate.php'
serverPath = '/data/servers/server'
databasePath = '/data/database'

tree = etree.parse(xmlFile)
database = tree.xpath(databasePath)

conn = pymysql.connect(host=database[0][0].text, user=database[0][1].text, passwd=database[0][2].text, db=database[0][3].text)
conn.autocommit(True)
cur = conn.cursor()
cur.execute("SELECT lID,sID,TimeStamp,r4 FROM Monitor.Logs WHERE sID='1' ORDER BY TimeStamp desc LIMIT 15;")
rows = cur.fetchall()
cur.close()

fig = plt.figure()
ax = fig.add_subplot(111)

## the data

data = []
xTickMarks = []

for row in rows:
   data.append(int(row[3]))
   xTickMarks.append(str(row[2]))

ind = np.arange(len(data))                # the x locations for the groups
width = 0.35                      # the width of the bars

## the bars
rects1 = ax.bar(ind, data, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))

# axes and labels
ax.set_xlim(-width,len(ind)+width)
ax.set_ylim(0,200)


ax.set_ylabel('Y LABEL')
ax.set_xlabel('X LABEL')
ax.set_title('TITLE_HERE')

ax.set_xticks(ind+width)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)


plt.show()