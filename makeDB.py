import sqlite3
from contextlib import closing
import os

def create_table():
    DB_NAME = 'wifiInformations.db'

    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        # load spatiaLite
        c.execute("SELECT load_extension('/var/www/prefix/lib/mod_spatialite.so');")

        print("load spatiaLite")
        # init spatiaLite
        c.execute('''SELECT InitSpatialMetaData();''')
        print("init")
        create_table = '''CREATE TABLE IF NOT EXISTS wifi (id INTEGER PRIMARY KEY AUTOINCREMENT, name CHAR(100), ssid CHAR(50) NOT NULL, address CHAR(100), postCode INT, hpUrl CHAR(100), geoPoint GEOMETORY NOT NULL);'''

        c.execute(create_table)
        print("create table")

if __name__ == "__main__":
    create_table()
