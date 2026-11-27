import datetime as dt
from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.sensordb import SensorDB
import requests
import json
import os

config = ConfigLoader("broker.config").load()
watchdog_config = ConfigLoader("watchdog.config").load()


if watchdog_config["statefile_location"] == "None":
    raise Exception("No statefile location has been set in config.ini")


STATEFILE_LOCATION = watchdog_config["statefile_location"]
MAX_INTERVAL_MIN =  int(watchdog_config["max_interval_min"])
NOTIFICATION_INTERVAL_H = int(watchdog_config["notification_interval_h"])

db = SensorDB()

devices = db.get_devices()


def notify(msg):
    requests.post(f"https://ntfy.sh/{watchdog_config["topic"]}",
                  data=msg.encode(encoding="utf-8"))



def format_timedelta(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"



def canNotify(path):
        if not os.path.exists(path):
            return True
        
        else:
            with open(path,"r") as f:
                timestamp = dt.datetime.strptime(f.read(),"%Y/%m/%d-%H:%M:%S")
            if dt.datetime.now() - timestamp > dt.timedelta(hours=NOTIFICATION_INTERVAL_H):
                return True
            else:
                return False
            


# main function
for device in devices:
    device_path = os.path.join(STATEFILE_LOCATION,device.name+"_state.txt")

    # get latest response and calculate difference to current time
    try:
        latest = db.get_by_name(device.name,latest_only=True)[0]
    except IndexError:
        print(f"list index out of range, table for {device.name}  might be empty")

    timestamp = dt.datetime.strptime(latest["date"],"%Y/%m/%d-%H:%M:%S")
    dT = dt.datetime.now() - timestamp

    now_str = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    
    # if sensor has not responded and notification can be sent, send alert
    if dT > dt.timedelta(minutes=MAX_INTERVAL_MIN) and canNotify(device_path):    
        alert = f"[{now_str}]: {device.name} offline alert! , sensor has not responded in {format_timedelta(dT)}"
        print(alert)        
        notify(alert)
        with open(device_path,"w") as f:
            f.write(now_str)
    
    # If sensor has responded and state is active, reset state, send alert
    elif dT < dt.timedelta(minutes=MAX_INTERVAL_MIN) and os.path.exists(device_path):
        alert = f"[{now_str}]: {device.name} is back online !"
        print(alert)
        notify(alert)
        os.remove(device_path)