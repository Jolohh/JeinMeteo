import requests as re
from datetime import datetime

URL = "http://192.168.1.83/api/device"

params = {
    "name":"Stromzaehler"
}

response = re.get(URL,params).json()

pwr_sum = sum(entry["power"] for entry in response)


#print(f"power_sum: {(pwr_sum/1000):0.2f}kW ")

avg = pwr_sum / len(response)

print(f"average power: {avg:0.2f}W")