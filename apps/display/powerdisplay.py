import pandas as pd
import matplotlib.pyplot as plt


from jeinmeteo.api import JeinMeteoAPI
from jeinmeteo.matplotlibtools import set_ystep, set_yunit, set_time_axis

#name = "Stromzaehler-HWR"
name = "Zimmer-Sensor-1"

api = JeinMeteoAPI()

data = api.get_data(name)


df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df["date"], format="%Y/%m/%d-%H:%M:%S")



fig, (ax1,ax2) = plt.subplots(2)


ax1.plot(df['date'], df['power'])
ax1.set_ylabel("Momentanleistung")


ax2.plot(df['date'], df['e_in'])
ax2.set_ylabel("Zählerstand")


# --------------
# Format Plot 1
# --------------

set_time_axis(ax1)
ax1.set_ylim(bottom=0)
set_yunit(ax1,"W")
set_ystep(ax1,1000)


# --------------
# Format Plot 2
# --------------

set_time_axis(ax2)
ax2.set_ylim(bottom=0,top=7000)
set_yunit(ax2,"kWh")


plt.show()