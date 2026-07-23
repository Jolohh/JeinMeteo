""""
Weather Station API
To run: python app.py
Then open http://localhost:5001/api/weather in your browser to see the data (json)
And for the website select the index.html -> open in browser
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sqlite3

from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.device_registry import Device_registry

app = Flask(__name__)
CORS(app)


config = ConfigLoader("broker.config").load()
DB_PATH = config["database_name"]


registry = Device_registry()



# index page
@app.route("/")
def index():
    #return "index"
    return render_template("index.html")



# returns all sensor data
@app.route("/api/weather")
def get_weather():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "211097D05BECC882" ORDER BY date DESC""")
    rows = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(rows)



# returns only the latest reading
@app.route("/api/weather/latest")
def get_latest():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "211097D05BECC882" ORDER BY date DESC LIMIT 1""")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return jsonify({})
    return jsonify(dict(row))



@app.route("/api/device")
def get_weather_all():
    hwid = request.args.get("hwid")
    name = request.args.get("name")
    device_found = False
    
    if device := registry.check_hwid(hwid):
        hwid = device.hwid
        device_found = True

    if device := registry.check_name(name):
        hwid = device.hwid
        device_found = True
        

    if device_found:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM "{hwid}" ORDER BY date DESC""")
            
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
            
        return jsonify(rows)
    
    return "Device not found"



@app.route("/api/stromzaehler")
def get_stromzaehler():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "WattWaechter_6C6287" ORDER BY date DESC""")
    rows = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(rows)   


@app.route("/api/devices")
def get_devices():
    devices = registry.get_devices_json()
    print(devices)
    return jsonify(devices)
    
if __name__ == "__main__":
    print("API running at http://localhost:5001")
    app.run(debug=True,host="0.0.0.0", port=5001)