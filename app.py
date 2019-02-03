# -*- coding: utf-8 -*-
from api import create_app
from flask import Flask, jsonify, request
from makeDB import create_table
from config.run_config import API_HOST, API_DEBUG, API_PORT

app = create_app()

if __name__ == '__main__':
    create_table()
    app.run(debug=API_DEBUG, host=API_HOST, port=API_PORT, processes=10)
