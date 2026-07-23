import sqlite3
import configparser
from config.configloader import ConfigLoader

config = ConfigLoader("broker.config").load()

registry_path : str = config["device_registry"]
device_types = config["device_types"]


class DeviceTypeError(Exception):
    pass


class Device_registry:
    def __init__(self) -> None:
        self.con = sqlite3.connect(registry_path)
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS devices (
                            id INTEGER PRIMARY KEY, 
                            hwid text UNIQUE, 
                            name text UNIQUE, 
                            type text)""")

        
    def add_device(self, hwid:str, name:str, device_type:str):
        if device_type not in device_types:
            raise DeviceTypeError("""Gerätetyp muss "multisensor" oder "stromzaehler" sein""")
        else:
            try:
                self.cur.execute(f"INSERT INTO devices (hwid,name,type) VALUES(?,?,?)",[hwid,name,device_type])
            except sqlite3.IntegrityError:
                raise
            self.con.commit()


    def get_devices(self):
        self.cur.execute("SELECT * FROM devices ORDER BY id ASC")
        devices = self.cur.fetchall()
        return devices 

    def check_hwid(self,hwid):
        devices = self.get_devices()
        for device in devices:
            if hwid == device[1]:
                return device
            
        return [None,None,None,None]
        
    def check_name(self,name):
        devices = self.get_devices()
        for device in devices:
            if name == device[2]:
                return device
            
        return [None,None,None,None]
            
            

