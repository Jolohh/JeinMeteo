import sqlite3
import matplotlib.pyplot as plt
from matplotlibtools import set_xstep, set_ystep, set_xunit, set_yunit
import numpy as np
import requests
import json
from datetime import datetime,timedelta

import matplotlibtools

dev_ids = ["211097D05BECC882","28463F17F7D0A774"]

API_URL = "http://sensornet.fritz.box/api/weather/device?dev_id="



content = {}

for dev_id in dev_ids:
    request = requests.get(API_URL+dev_id)
    response = json.loads(request.content)
    content[dev_id] = response

# region pure matplotlib functions


print(content.keys())
    