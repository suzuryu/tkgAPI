from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc


app = Flask(__name__)

TABLE_NAME = 'tkg'
DB_NAME = 'serverSide.db'

@app.route('/wifi/addPoints', methods=['POST'])
def add_points():
    if request.method == 'POST':
        req = request.get_json()
        for r in req:
            if sql_add_query(r)['sql_status'] == 'error':
                return {500: 'sql error'}

        return {200: 'success!'}


@app.route('/wifi/updatePoints', methods=['POST'])
def update_points():
    if request.method == 'POST':
        req = request.get_json()
        for r in req:
            if r['id'] is None:
                return {'error': 'data has no id'}
            if sql_update_query(r)['sql_status'] == 'error':
                return {500: 'sql error'}

        return {200: 'success!'}


@app.route('/wifi/getPoints', methods=['GET'])
def get_points():
    if request.method == 'GET':
        return {'datas': sql_get_query(), 200:'success!'}


def sql_add_query(point):
    sql_query = "INSERT INTO " + TABLE_NAME + "(name, ssid, address, postCode, hpUrl, geoPoint)  \
                    VALUES(?, ?, ?, ?, ?, GeomFromText('POINT(? ?)'))"
    values = (point['name'], point['ssid'], point['address'], point['postCode'],  \
                        point['hpUrl'], point['longitude'], point['latitude'])

    return execute_sql(sql_query, values)


def sql_get_query(latitude, longitude, distance):
    sql_query = "SELECT id, name, ssid, address, postCode, hpUrl, X(geoPoint), Y(geoPoint) FROM " + TABLE_NAME
                + "WHERE MBRIntersects(GeomFromText('LineString({x0} {y0}, {x1} {y2})'), geo)".format(
                        longitude - distance, latitude - distance, longitude + distance, latitude + distance)

    return execute_sql(sql_query)

# where ??
def sql_update_query(point):
    sql_query = "UPDATE " + TABLE_NAME
                 + " SET name = ?, ssid = ?, address = ?, postCode = ?, hpUrl = ?, geoPoint = GeomFormText('POINT(? ?)')"
                 + " WHERE id == ?"
    values = (point['name'], point['ssid'], point['address'], point['postCode'],  \
                    point['hpUrl'], point['longitude'], point['latitude'], point['id'])

    return execute_sql(sql_query, values)


def execute_sql(sql_query, values=()):
    con = pyodbc.connect(r'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE='+ DB_NAME + ';Trusted_connection=yes')
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
