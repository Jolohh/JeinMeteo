import pandas as pd
import matplotlib.pyplot as plt


from jeinmeteo.api import JeinMeteoAPI
from jeinmeteo.device_registry import Device_registry
from jeinmeteo.matplotlibtools import set_time_axis, set_yunit
from jeinmeteo.tools import number_input, filter_gaps

api = JeinMeteoAPI()
registry = Device_registry()

devices = registry.get_devices()



# --------------
# Select Devices
# --------------

print("Bitte ein Gerät auswählen")
for i, device in enumerate(devices):
    if device.device_type != "multisensor":
        devices.remove(device)
    else:
        print(f"({i}): {device.name}")

i = number_input(0,len(devices)-1,"> ")

print(f"Gerät ausgewählt: {devices[i].name}")
device = devices[i]


data = api.get_data(device.name)


# --------------
# Create Dataframe
# --------------

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df["date"], format="%Y/%m/%d-%H:%M:%S")
df_filtered = filter_gaps(df,pd.Timedelta(minutes=40))




# --------------
# Plot
# --------------

fig, (ax1,ax2) = plt.subplots(2)


ax1.plot(df['date'], df['temperature'],linestyle="dotted",color="tab:blue")
ax1.plot(df_filtered['date'], df_filtered['temperature'],color="tab:blue")
ax1.set_ylabel("Temperatur")


ax2.plot(df['date'], df['battery_level'],linestyle="dotted",color="tab:blue")
ax2.plot(df_filtered['date'], df_filtered['temperature'],color="tab:blue")
ax2.set_ylabel("Batteriespannung")



# --------------
# Format Plots
# --------------

set_time_axis(ax1)
ax1.set_ylim(bottom=0)
set_yunit(ax1,"°C")


set_time_axis(ax2)
ax2.set_ylim(bottom=3,top=5)
set_yunit(ax2,"V")


plt.show()