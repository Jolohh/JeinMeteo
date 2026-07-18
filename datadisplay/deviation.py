import requests
import json
from datetime import datetime




API_URL = "http://sensornet.fritz.box/api/weather"



request = requests.get(API_URL)

content = json.loads(request.content)



def deviation_t(stop):
    l = []
    average = 0
    for i in range(stop):
        try:
            t1 = datetime.strptime(content[i]["date"],"%Y/%m/%d-%H:%M:%S")
            t2 = datetime.strptime(content[i+1]["date"],"%Y/%m/%d-%H:%M:%S")

            dt = t1 - t2
            dt = dt.seconds/60
            l.append(dt)
            average += dt
        except:
            pass
    return l,average/len(l)


n = int(input("How many values: "))

l ,average =deviation_t(n)
deviation_s = abs(average - 15) * 60

print(f"Deviation in seconds over the last {n} values: {deviation_s}")

