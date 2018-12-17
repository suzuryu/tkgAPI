import sqlite3
from contextlib import closing

def create_table():
    DB_NAME = 'serverSide.db'

    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()

        # load spatiaLite
        c.execute('''SELECT load_extension('/home/suzuki/prefix/lib/mod_spatialite.so');''')

        # init spatiaLite
        c.execute('''SELECT InitSpatialMetaData();''')

        create_table = '''CREATE TABLE IF NOT EXISTS wifi (id INTEGER PRIMARY KEY AUTOINCREMENT, name CHAR(100), ssid CHAR(50) NOT NULL, address CHAR(100), postCode INT, hpUrl CHAR(100), geoPoint GEOMETORY NOT NULL);'''

        c.execute(create_table)
