# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, abort
import json
import pandas.io.sql as pdsql
import pyodbc

api = Blueprint('api', __name__, url_prefix="/api")#親URLを設定


@api.route('/wifi/addPoints', methods=['POST'])
def add_points():
    if request.method == 'POST':
        req = request.get_json()
        for r in req:
            if sql_add_query(r)['sql_status'] == 'error':
                return {500: 'sql error'}

        return {200: 'success!'}


@api.route('/wifi/updatePoints', methods=['POST'])
def update_points():
    if request.method == 'POST':
        req = request.get_json()
        for r in req:
            if r['id'] is None:
                return {'error': 'data has no id'}
            if sql_update_query(r)['sql_status'] == 'error':
                return {500: 'sql error'}

        return {200: 'success!'}


@api.route('/wifi/getPoints', methods=['GET'])
def get_points():
    if request.method == 'GET':
        name_keyword = request.args.get('name')
        id = request.args.get('id')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        distance = request.args.get('distance')

        if name_keyword is not None:
            return {'datas': sql_get_by_name_query(name), 200: 'success!'}
        elif id is not None:
            return {'datas': sql_get_by_id_query(id), 200: 'success!'}
        elif latitude is not None and longitude is not None and distance is not None:
            return {'datas': sql_get_by_distance_query(latitude, longitude, distance), 200: 'success!'}
        else:
            return {400: 'wrong get params'}

def sql_add_query(point):
    sql_query = "INSERT INTO " + TABLE_NAME + "(name, ssid, address, postCode, hpUrl, geoPoint)  \
                    VALUES(?, ?, ?, ?, ?, GeomFromText('POINT(? ?)'))"
    values = (point['name'], point['ssid'], point['address'], point['postCode'],  \
                        point['hpUrl'], point['longitude'], point['latitude'])

    return execute_sql(sql_query, values)


def sql_get_by_distance_query(latitude, longitude, distance):
    sql_query = "SELECT id, name, ssid, address, postCode, hpUrl, X(geoPoint), Y(geoPoint) FROM " + TABLE_NAME \
                + "WHERE MBRIntersects(GeomFromText('LineString({x0} {y0}, {x1} {y2})'), geo)".format( \
                    longitude - distance, latitude - distance, longitude + distance, latitude + distance)

    return execute_sql(sql_query)

def sql_get_by_name_query(name):
    sql_query = "SELECT id, name, ssid, address, postCode, hpUrl, X(geoPoint), Y(geoPoint) FROM " + TABLE_NAME \
                + "WHERE name LIKE '{0}%'".format(name)

    return execute_sql(sql_query)

def sql_get_by_id_query(id):
    sql_query = "SELECT id, name, ssid, address, postCode, hpUrl, X(geoPoint), Y(geoPoint) FROM " + TABLE_NAME \
                    + "WHERE id == {0}".format(id)

    return execute_sql(sql_query)

def sql_update_query(point):
    sql_query = "UPDATE " + TABLE_NAME \
                + " SET name = ?, ssid = ?, address = ?, postCode = ?, hpUrl = ?, geoPoint = GeomFormText('POINT(? ?)')" \
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
