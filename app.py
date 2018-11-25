from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc


app = Flask(__name__)

table_name = 'tkg'

@app.route('/wifi/addPoints', methods=['POST'])
def add_points():
    if request.method == 'POST':
        req = request.get_json()
        if check_data_type(req) == 'error':
            return {'error': 'data type is wrong'}

        for r in req:
            if sql_add_query(r)['sql_status'] == 'error':
                return {500: 'sql error'}

        return {200: 'success!'}

@app.route('/wifi/updatePoints', methods=['POST'])
def update_points():
    if request.method == 'POST':
        req = request.get_json()
        if check_data_type(req) == 'error':
            return {'error': 'data type is wrong'}

        for r in req:
            if sql_update_query(r)['sql_status'] == 'error':
                return {500: 'sql error'}

        return {200: 'success!'}


@app.route('/wifi/getPoints', methods=['GET'])
def get_points():
    if request.method == 'GET':
        return {'datas': sql_get_query(), 200:'success!'}


def check_data_type(data):
    if type(data['id']) != int:
        return 'error'
    if type(data['name']) != str:
        return 'error'
    if type(data['ssid']) != str:
        return 'error'
    if type(data['address']) != str:
        return 'error'
    if type(data['postCode']) != int:
        return 'error'
    if type(data['hpUrl']) != str:
        return 'error'
    if type(data['latitude']) != float:
        return 'error'
    if type(data['longitude']) != float:
        return 'error'

    return 'ok'


def sql_add_query(point):
    sql_query = "INSERT INTO " + table_name + "(name, ssid, address, postCode, hpUrl, latitude, longitude)  \
                    VALUES(?, ?, ?, ?, ?, ?, ?)"
    values = (point['name'], point['ssid'], point['address'], point['postCode'],  \
                        point['hpUrl'], point['latitude'], point['longitude'])

    return execute_sql(sql_query, values)


def sql_get_query():
    sql_query = "SELECT * FROM " + table_name

    return execute_sql(sql_query)

# where ??
def sql_update_query(point):
    sql_query = "UPDATE " + table_name
                 + " SET name = ?, ssid = ?, address = ?, postCode = ?, hpUrl = ?, latitude = ?, longitude = ?"
                 + " WHERE "
    values = (point['name'], point['ssid'], point['address'], point['postCode'],  \
                    point['hpUrl'], point['latitude'], point['longitude'])

    return execute_sql(sql_query, values)


def execute_sql(sql_query, values=()):
    con = pyodbc.connect(r'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE=      .db;Trusted_connection=yes')
    cur = con.cursor()
    try:
        if len(values) != 0:
            cur.execute(sql_query,values)
            con.commit()
            con.close()
            return {'sql_status': 'ok'}
        else:
            data = pdsql.read_sql(sql_query, con).to_dict('records')
            con.close()
            return data
    except sqlite3.Error as e:
        return {'sql_status': 'error'}


if __name__ == '__main__':
    app.run(debug=True)
