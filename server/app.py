"""
Weather Station API
To run: python app.py
Then open http://localhost:5001/api/weather in your browser to see the data (json)
And for the website select the index.html -> open in browser
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sqlite3
import socket

from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.device_registry import Device_registry

from jeinmeteo.sensordb import SensorDB


app = Flask(__name__)
CORS(app)


config = ConfigLoader("broker.config").load()


DB_PATH = config["database_name"]

db = SensorDB()



registry = Device_registry()

# index page
@app.route("/")
def index():
    api_url = request.host_url.rstrip("/") + "/api"
    print("using api_url:",api_url)
    return render_template("index(1).html",api_url=api_url)



# returns all sensor data for a preset sensor (for testing)
@app.route("/api/weather")
def get_weather():
    rows = db.get_by_hwid("28463F17F7D0A774")
    
    return jsonify(rows)

# returns only the latest reading
@app.route("/api/weather/latest")
def get_latest():
    rows = db.get_by_hwid("28463F17F7D0A774",latest_only=True)
    
    return jsonify(rows)



@app.route("/api/device")
def get_by_device():
    hwid = request.args.get("hwid")
    name = request.args.get("name")
    latest = request.args.get(key="latest",default="false")
    
 
    try:
        device = db.find_device_name(name)
    except:
        try:
            device = db.find_device_hwid(hwid)
        except:
            return "device not found in registry"

    
    if latest.lower() == "true":
        rows = db.get_by_hwid(device.hwid,latest_only=True)
    else:
        rows = db.get_by_hwid(device.hwid)

    return jsonify(rows)



@app.route("/api/stromzaehler")
def get_stromzaehler():
    rows = db.get_by_hwid("WattWaechter_6C6287")
    
    return jsonify(rows)



@app.route("/api/devices")
def get_devices():
    devices = db.get_devices() 
    print(devices)
    return jsonify(devices)
    
    
if __name__ == "__main__":
    print("API running at http://localhost:5001")
    app.run(debug=True,host="0.0.0.0", port=5001)
