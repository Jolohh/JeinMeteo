import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


con = sqlite3.connect(config["broker.config"]["database_name"])
cur = con.cursor()

def get_tables(cur):
    cur.execute("""SELECT * FROM sqlite_master WHERE type='table' """)
    tables_raw = cur.fetchall()
    tables = []

    for d in tables_raw:
        tables.append(str(d[1]))
        
    return tables

with open("device_list.txt","w") as f:
    f.writelines(get_tables(cur))
    
con.close()