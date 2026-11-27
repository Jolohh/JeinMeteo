import sqlite3
from contextlib import closing
from dataclasses import dataclass
import json

from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.sensor_types import validate_device_type, create_table_sql, table_name, columns_for,validate_values, get_device_types

config = ConfigLoader("api.config").load()

DB_PATH = config["database_name"]


@dataclass(frozen=True)
class Device:
    id: int
    hwid: str
    name: str
    device_type: str


class UnknownDevice(ValueError):
    pass

class SensorDB:
    def __init__(self, path=DB_PATH):
        self.path = path
        with closing(self._connect()) as conn, conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS devices (
                            id INTEGER PRIMARY KEY, 
                            hwid text UNIQUE, 
                            name text UNIQUE, 
                            device_type text)""")
    
    def _connect(self,nofactory=False):
        conn = sqlite3.connect(self.path, timeout=10)
        if not nofactory:
            conn.row_factory = sqlite3.Row
        return conn
    
    
    
    def get_by_name(self,name,latest_only=False):
        device = self.find_device_name(name)
        
        cmd = f"""SELECT * FROM {table_name(device.hwid)} ORDER BY date DESC"""
        if latest_only:
            cmd += " LIMIT 1"
        
        with closing(self._connect()) as conn, conn:
                    rows = conn.execute(cmd).fetchall()
                    return [dict(row) for row in rows]
    
    
    
    def get_by_hwid(self,hwid,latest_only=False):
        device = self.find_device_hwid(hwid)
        
        cmd = f"""SELECT * FROM {table_name(device.hwid)} ORDER BY date DESC"""
        if latest_only:
            cmd += " LIMIT 1"
        
        with closing(self._connect()) as conn, conn:
                    rows = conn.execute(cmd).fetchall()
                    return [dict(row) for row in rows]
        
    
    

    def insert_values(self,hwid,values:dict):
        with closing(self._connect()) as conn, conn:
            row = conn.execute("SELECT hwid,device_type FROM devices WHERE hwid=? ", (hwid,)).fetchone()
            if row is None:
                raise UnknownDevice(f"device not found in registry: {hwid}")
            
            device_type = row["device_type"]
            hwid = row["hwid"]
            
            values = validate_values(device_type,values)
            values_tup = tuple(values[col] for col in values)

            conn.execute(f"""INSERT INTO {table_name(hwid)} VALUES ({','.join(['?'] * len(values_tup))})""", values_tup)

    
    #####
    #
    # Device Registry Methods
    #
    #####
    def get_devices(self) -> list[Device]:
        with closing(self._connect()) as conn, conn:
            rows = conn.execute("SELECT id, hwid, name, device_type FROM devices ORDER BY id ASC").fetchall()
            return [Device(*row) for row in rows]



    def find_device_hwid(self,hwid):
        with closing(self._connect()) as conn, conn:
            row = conn.execute("SELECT id, hwid, name, device_type FROM devices WHERE hwid=? ", (hwid,)).fetchone()
            if row is None:
                raise UnknownDevice(f"device not found in registry: {hwid}")
            else:
                return Device(row["id"],row["hwid"],row["name"],row["device_type"])



    def find_device_name(self,name):
        with closing(self._connect()) as conn, conn:
            row = conn.execute("SELECT id, hwid, name, device_type FROM devices WHERE name=? ", (name,)).fetchone()
            if row is None:
                raise UnknownDevice(f"device not found in registry: {name}")
            else:
                return Device(row["id"],row["hwid"],row["name"],row["device_type"])



    def add_device(self,name: str,hwid: str,device_type: str) -> Device:
        validate_device_type(device_type)
        
        with closing(self._connect()) as conn, conn:
            
            cur = conn.execute(
                "INSERT INTO devices (hwid, name, device_type) VALUES (?, ?, ?)",
                (hwid, name, device_type),
            )
            conn.execute(create_table_sql(table_name(hwid), device_type))
            
        return Device(cur.lastrowid, hwid, name, device_type)
            

    def get_device_types(self):
        return get_device_types()