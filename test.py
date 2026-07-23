from datetime import datetime


values_dict = {
    "humidity": None,
    "pressure": None,
    "temperature": None,
    "pm2.5": None,
    "pm10": None,
    "date": datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
    }



data_dict = {
    "humidity": None,
    "pressure": None,
    "temperature": None,
    "pm2.5": None,
    "pm10": None,
    "date": datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
    "battery_level": None}

values_dict.update(data_dict)

print(values_dict)