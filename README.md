# JeinMeteo weather station
This Project is a sensor-network that supports multiple types of sensors that collect weather data and send it to a server via MQTT where it is stored and displayed on a webpage.

The Repository includes both the client code and the server code. In VsCode open each seperately as a workspace for it to work properly

## Server
### 1. Basic Setup
Create a virtual environment and install the python dependencies, also install custom library located in "src"

Copy defaultconfig.ini as config.ini in the config folder and set username and password for broker

You can add registered devices with "add_device.py", where you have to give the hwid of the device, a name and a sensor type.

---
### 2. Install gunicorn if not already:
```
pip install flask gunicorn
```
To manually start the server:
```
sudo gunicorn --bind 0.0.0.0:80 app:app
```
---
### 3. Create Service for Webserver:
```
sudo nano /etc/systemd/system/JeinMeteo.service
```
And Paste:
```
[Unit]
Description=JeinMeteo App
After=network-online.target
Wants=network-online.target

[Service]
User=jonah
WorkingDirectory=/home/jonah/JeinMeteo/server
ExecStart=/home/jonah/JeinMeteo/server/.venv/bin/gunicorn --bind 0.0.0.0:80 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Where home/jonah/JeinMeteo should be the path to the local repository and user should be your user Then start the service:
```
sudo systemctl daemon-reload
sudo systemctl enable JeinMeteo
sudo systemctl start JeinMeteo
```
---
### 4. Setup Mosquitto Broker
Install mosquitto:
```
sudo apt install -y mosquitto mosquitto-clients
```
Create config file:
```
sudo nano /etc/mosquitto/conf.d/local.conf
```

Create user, where "jonah" is your preferred username, the password chosen here will be used to connect to the broker later on
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd jonah
sudo chown mosquitto:mosquitto /etc/mosquitto/passwd
sudo chmod 640 /etc/mosquitto/passwd
```
Start the broker:
```
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```
---
### 5. Setup MQTT-Listener
```
sudo nano /etc/systemd/system/JeinMeteo-mqtt.service
```
Paste:
```
[Unit]
Description=JeinMeteo MQTT Listener
After=network-online.target mosquitto.service
Wants=network-online.target mosquitto.service
# Use for non-local broker
# After=network-online.target
# Wants=network-online.target

[Service]
User=jonah
WorkingDirectory=/home/jonah/JeinMeteo/server
ExecStart=/home/jonah/JeinMeteo/server/.venv/bin/python -u mqtt_listener.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Directory and user should be the same as with the webserver. Start Service:
```
sudo systemctl daemon-reload
sudo systemctl enable --now JeinMeteo-mqtt
```
### 6. Setup Watchdog
This uses a cronjob to check if the sensor has not sent data for some time (standard is 30 minutes), and notifies you with [ntfy](https://ntfy.sh/), the topic for which can be set in the config

You may have to make the script executable:
```
sudo chmod +x watchdog.py
```
To setup the cronjob:
```
crontab -e
```
And Paste:
```
*/10 * * * * /home/jonah/JeinMeteo/server/.venv/bin/python /home/jonah/JeinMeteo/server/apps/watchdog.py >> /home/jonah/JeinMeteo/server/data/watchdog.log 2>&1
```



## Client
Use the client folder as a workspace, for this project, the [Raspberry Pi Pico](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico) Extension was used on a Raspberry Pico 2w.
\
You need to create a config file by copying the `example_config.h` as `config.h` and setting the values to your values.

# MQTT Communication
For each client the payload is sent in  a Json Format, for Example:
``` 
 {"temperature":22.8500,"pressure":1073.09,"humidity":50.33,"battery_level":1.4531}
```
For the Sensor Data to be accepted and saved by the server, the device needs to be registered, which can be done with `add_device.py`. Each sensor creates a unique hwid, which is used in the topic:
```
sensor/{hwid}
```
To get the hwid, either monitor the serial output from the pico, or run the `mqttListenersimple.py` and watch for the sensor in the output. The name of the sensor can be freely set.

# Tasmota WattWächter
This project additionally supports the WattWächter Power-Meter to monitor your home power consumption. In the Tasmota Menu set in the MQTT-configuration:\
Topic:
```
WattWaechter_%06X
```
Full Topic:
```
Stromzaehler/%topic%/
```
