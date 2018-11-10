from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc


app = Flask(__name__)

@app.route('/wifi/addPoints', methods=['POST'])
def add_points():
    if request.method == 'POST':
        req = request.get_json()
   pass

@app.route('/wifi/getPoints', methods=['GET'])
def get_points():
    if request.method == 'GET':
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        distance = request.args.get('distance')
   pass

@app.route('/wifi/updatePoints', methods=['POST'])
def update_points():
    if request.method == 'POST':
        req = request.get_json()
   pass

def sql_add_query():
    pass

def sql_get_query():
    pass

def sql_update_query():
    pass

if __name__ == '__main__':
    app.run(debug=True)
