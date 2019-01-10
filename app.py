# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc
import api
from makeDB import create_table
from config.run_config import API_HOST, API_DEBUG, API_PORT

app = api.create_app()

TABLE_NAME = 'wifi'
DB_NAME = 'wifiInformations.db'

if __name__ == '__main__':
    create_table()
    app.run(debug=API_DEBUG, host=API_HOST, port=API_PORT)
