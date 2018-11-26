import sqlite3
from contextlib import closing

def create_table():
    DB_NAME = 'serverSide.db'

    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()

        # load spatiate
        c.execute("SELECT load_extension('PATH TO mod_spatialite.so');")

        # init spatiate
        c.execute('SELECT InitSpatialMetaData();')

        create_table = '''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name CHAR(100), ssid CHAR(50) NOT NULL, address CHAR(100), postCode INT, hpUrl CHAR(100), geoPoint GEOMETORY NOT NULL)'''

        c.execute(create_table)
