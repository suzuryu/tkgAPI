from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc


app = Flask(__name__)

@app.route('/wifi/addPoints', methods=['POST'])
def add_points():
    if request.method == 'POST':
        req = request.get_json()
        for r in req:
            sql_add_query(r)

        return {'200':'success!'}

@app.route('/wifi/getPoints', methods=['GET'])
def get_points():
    if request.method == 'GET':
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        distance = request.args.get('distance')

        return {sql_get_query(latitude, longitude, distance), {'200':'success!'}}


@app.route('/wifi/updatePoints', methods=['POST'])
def update_points():
    if request.method == 'POST':
        req = request.get_json{'200':'success!'}()
        for r in req:
            sql_update_query(r)

        return {'200':'success!'}

def sql_add_query(point):
    sql_query = ""

def sql_get_query(latitude, longitude, distance):
    sql_query = ""

def sql_update_query(point):
    sql_query = ""

if __name__ == '__main__':
    app.run(debug=True)
