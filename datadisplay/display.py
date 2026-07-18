import sqlite3
import matplotlib.pyplot as plt
import numpy as np

database_name = "data/database_new.db"


con = sqlite3.connect(database_name)
cur = con.cursor()

def get_tables(cur):
    cur.execute("""SELECT * FROM sqlite_master WHERE type='table' """)
    tables_raw = cur.fetchall()
    tables = []

    for d in tables_raw:
        tables.append(d[1])
        
    return tables


tables = get_tables(cur)

print("Tables:",tables)



#table = "211097D05BECC882"
table = """28463F17F7D0A774"""

ref = cur.execute(f"""SELECT * FROM "{table}" """)
#print(ref.description)
contents = cur.fetchall()

#cur.execute(f"""PRAGMA table_info("{table}") """)

#print(column_names)
#print(contents)


# make data
x = []
y = []

print("Differences:")
for row in contents:
    x.append(row[5])#
    print(row[0])
    y.append(row[0])




# plot
fig, ax = plt.subplots()

ax.plot(x, y, linewidth=2.0)

plt.show()

con.close()