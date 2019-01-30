# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc
from makeDB import create_table
from config.run_config import API_HOST, API_DEBUG, API_PORT
from . import create_app

app = create_app()

if __name__ == '__main__':
    create_table()
    app.run(debug=API_DEBUG, host=API_HOST, port=API_PORT)
