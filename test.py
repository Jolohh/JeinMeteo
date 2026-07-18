import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("config.ini")



device_registry: str = config["broker.config"]["device_registry"]

def check_device_registry(id_string):
    con = sqlite3.connect(device_registry)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS devices (hwid REAL, sid INTEGER PRIMARY KEY)")
    
    cur.execute("SELECT hwid, sid FROM devices WHERE hwid = ?", (id_string,))
    row = cur.fetchone()
    
    print(row)
    
check_device_registry("test")