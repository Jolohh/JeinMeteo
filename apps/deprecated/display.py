import sqlite3
import matplotlib.pyplot as plt

from jeinmeteo.matplotlibtools import set_xstep, set_ystep, set_xunit, set_yunit
import numpy as np
import requests
import json
from datetime import datetime,timedelta


API_URL = "http://sensornet.fritz.box/api/weather"



request = requests.get(API_URL)
#print(x.content)
content = json.loads(request.content)

# region pure matplotlib functions



# region end




x = []
y = []    

def delta_t():
    for i,row in enumerate(content):
        try:
            t1 = datetime.strptime(content[i]["date"],"%Y/%m/%d-%H:%M:%S")
            t2 = datetime.strptime(content[i+1]["date"],"%Y/%m/%d-%H:%M:%S")
            #print("t1:",t1)
            #print("t2",t2)
            #print("---")
            dt = t1 - t2
            dt = dt.seconds/60
            now = datetime.now()
            date = datetime.strptime(row["date"],"%Y/%m/%d-%H:%M:%S")
            xdt = date - now             
            #print("----------")
            #print(datetime.strptime(row["date"],"%Y/%m/%d-%H:%M:%S"))
            #print("xdt:",xdt)
            #print("xdt,seconds:",xdt.seconds)
            xdt = xdt.total_seconds()/3600
            
        except:
            pass
   
        #print(float(dt))
        x.append(xdt)
        #y.append(float(row["battery_voltage"]))
        y.append(dt)

def battery_voltage():
    for row in content:
        x.append(datetime.strptime(row["date"],"%Y/%m/%d-%H:%M:%S"))
        y.append(float(row["battery_voltage"]))


delta_t()

# plot



fig, ax = plt.subplots()



#ax.set_xticks(np.arange(-2400,0,24))
print(x[-20:])


ax.plot(x, y,marker="x",linestyle="-", linewidth=2.0)

ax.set_ylim(0,60)
ax.set_xlim(-24,0)

set_xunit(ax,"h")
set_yunit(ax,"min")

set_xstep(ax,2)
set_ystep(ax,15)




plt.show()
