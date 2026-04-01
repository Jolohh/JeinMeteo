import sqlite3
import paho.mqtt.client as mqtt
from typing import Dict

table_name: str = "sensors"
subscriber_id: str = "teamB"
database_name: str = "database.db"

measure_types : Dict[str, str] = {
    "humidity": "REAL",
    "pressure": "REAL",
    "temperature": "REAL",
    "pm2.5": "REAL",
    "pm10": "REAL",
    "date": "TEXT"
    }

#region global variables
data_length = len(measure_types)
data_dict = {}
#endregion

def on_Myconnect(client, userdata, flags, rc):
    client.subscribe(f"{subscriber_id}/#")
    print("Connected with result code "+str(rc))
    data_dict.clear()

def on_MyMessage(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    data = msg.topic.split("/")[1]
    # Depends on the type of data,
    # convert the value to the correct type
    match measure_types[data]:
        case "REAL":
            value = float(msg.payload)
        case "TEXT":
            value = str(msg.payload, "utf-8")
        case "INTEGER":
            value = int(msg.payload)
    data_dict[data] = value

    print(f"{data_dict=}")

    #If get all the data
    if len(data_dict) == data_length:
        cur.execute(f"""INSERT INTO {table_name} VALUES ({
            ','.join(['?'] * data_length)})""",
            tuple(data_dict[col] for col in measure_types)
            )
        data_dict.clear()
        con.commit()

#region Database setup

con = sqlite3.connect(database_name)
cur = con.cursor()
cur.execute(f"DROP TABLE IF EXISTS {table_name}")
# check if the table already exists
# ? prevent special characters like ":" to insert them in the database
res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
if res.fetchone() is None: 
    columns_string = ", ".join(
        f'"{name}" {type}' for name, type in measure_types.items())
    cur.execute(f"CREATE TABLE {table_name} ({columns_string})")

#Check if the table was created successfully
res = cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
    (table_name,))
if res.fetchone() is None:
    print("Table creation failed")
else:
    print("Table created successfully")
    
con.commit()

#endregion

#region MQTT setup

client = mqtt.Client()
client.on_connect = on_Myconnect
client.on_message = on_MyMessage
client.username_pw_set("user1", "bouter20XX")
client.connect("147.210.103.14", 1883, 60)
client.loop_forever()
print("Connected to MQTT broker")


#endregion