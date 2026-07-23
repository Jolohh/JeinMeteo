import sqlite3
from src.jeinmeteo.configloader import ConfigLoader

config = ConfigLoader("broker.config").load()

registry_path : str = config["device_registry"]
device_types = config["device_types"]



class Device:
    def __init__(self,
                 id : str,
                 hwid : str,
                 name : str,
                 device_type : str
                 ):
        
        self.id = id
        self.hwid = hwid
        self.name = name
        self.device_type = device_type
        
    @classmethod
    def from_list(cls,l:list):
        return cls(l[0],l[1],l[2],l[3])



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
                            device_type text)""")

        
    def add_device(self, hwid:str, name:str, device_type:str):
        if device_type not in device_types:
            raise DeviceTypeError("""Gerätetyp muss "multisensor" oder "stromzaehler" sein""")
        else:
            try:
                self.cur.execute(f"INSERT INTO devices (hwid,name,device_type) VALUES(?,?,?)",[hwid,name,device_type])
            except sqlite3.IntegrityError:
                raise
            self.con.commit()


    def get_devices(self):
        self.cur.execute("SELECT * FROM devices ORDER BY id ASC")
        devices = self.cur.fetchall()
        l = []
        for device in devices:
            l.append(Device.from_list(device))
        return l 


    def get_devices_json(self):
        l = self.get_devices()
        l_dict = []
        for device in l:
            l_dict.append(device.__dict__)
        return l_dict


    def check_hwid(self,hwid):
        devices = self.get_devices()
        for device in devices:
            if hwid == device.hwid:
                return device
        return None
        
        
    def check_name(self,name):
        devices = self.get_devices()
        for device in devices:
            if name == device.name:
                return device
            
        return None
    

        
            

