# -*- coding: utf-8 -*-

from flask import current_app, Flask, redirect, abort, jsonify, make_response, request
import pandas.io.sql as pdsql
import sqlite3, pyodbc, json
from config.run_config import APP_DEBUG, APP_TESTING
from tqdm import tqdm


TABLE_NAME = 'wifi'
DB_NAME = 'wifiInformations.db'

def logp(p):
    print(p)

def create_app(debug=APP_DEBUG, testing=APP_TESTING, config_overrides=None):
    """

    :param config:
    :param debug:
    :param testing:
    :param config_overrides:
    :return:
    """
    app = Flask(__name__)
    app.debug = debug
    app.testing = testing
    app.config['JSON_AS_ASCII'] = False

    if config_overrides:
        app.config.update(config_overrides)

    @app.route('/api/health')
    def health_check():
        """

        :return:
        """
        response = {
            'status_code': 200,
            'status_msg': 'health is ok',
        }

        return make_response(jsonify(response)), 200

    @app.route('/')
    @app.route('/api')
    def index():
        """

        :return:
        """

        return redirect('/api/health')

    #\@app.errorhandler(204)  # 文章が意味をなしておらず、判定しなかった
    @app.errorhandler(400)  # リクエストが不正である。定義されていないメソッドを使うなど、クライアントのリクエストがおかしい場合に返される。
    @app.errorhandler(401)  # 認証が必要である。Basic認証やDigest認証などを行うときに使用される。
    @app.errorhandler(403)  # 禁止されている。リソースにアクセスすることを拒否された。
    @app.errorhandler(404)  # 未検出。リソースが見つからなかった。
    @app.errorhandler(405)  # 許可されていないメソッド。許可されていないメソッドを使用しようとした。
    @app.errorhandler(406)  # 受理できない。Accept関連のヘッダに受理できない内容が含まれている場合に返される。
    @app.errorhandler(408)  # リクエストタイムアウト。リクエストが時間以内に完了していない場合に返される。
    @app.errorhandler(413)  # ペイロードが大きすぎる。リクエストエンティティがサーバの許容範囲を超えている場合に返す。
    @app.errorhandler(500)  # サーバ内部エラー。サーバ内部にエラーが発生した場合に返される。
    @app.errorhandler(503)  # サービス利用不可。サービスが一時的に過負荷やメンテナンスで使用不可能である。
    def server_error(e):
        """

        :param e:
        :return:
        """

        response = {
            'status_code': int(e.code),
            'status_msg': str(e)
        }

        return make_response(jsonify(response)), e.code

#main api
    @app.route('/api/wifi/addPoints', methods=['POST'])
    def add_points():
        if request.method == 'POST':
            req = request.get_json()["datas"]
            logp("Start add points for {} count".format(len(req)))
            points = []
            for point in tqdm(req):
                points.append([point['name'], point['ssid'], point['address'], point['postCode'],point['hpUrl'],
                              'POINT({} {})'.format(point['longitude'], point['latitude'])])
            if sql_add_query(points)['sql_status'] == 'error':
                abort(500)

            logp("Finish add points")
            response = {
                'status_code': 200,
                'status_msg': 'success',
            }

            return make_response(jsonify(response)), 200



    @app.route('/api/wifi/updatePoints', methods=['POST'])
    def update_points():
        if request.method == 'POST':
            req = request.get_json()["datas"]
            logp("Start update points for {} count".format(len(req)))
            points = []
            for point in tqdm(req):
                if point['id'] is None:
                    abort(400)
                points.append([point['name'], point['ssid'], point['address'], point['postCode'],point['hpUrl'],
                              'POINT({} {})'.format(point['longitude'], point['latitude']), point['id']])

            if sql_update_query(points)['sql_status'] == 'error':
                abort(500)
            logp("Finish update points")
            response = {
                'status_code': 200,
                'status_msg': 'success',
            }

            return make_response(jsonify(response)), 200


    @app.route('/api/wifi/getPoints', methods=['GET'])
    def get_points():
        if request.method == 'GET':
            name_keyword = request.args.get('name')
            id = request.args.get('id')
            latitude = request.args.get('latitude')
            longitude = request.args.get('longitude')
            distance = request.args.get('distance')

            if name_keyword is not None:
                if not name_keyword != "":
                    abort(400)
                response = {
                    'datas': sql_get_by_name_query(name_keyword),
                    'status_code': 200,
                    'status_msg': 'success',
                }
                return make_response(jsonify(response)), 200
            elif id is not None:
                if not id != "":
                    abort(400)
                response = {
                    'datas': sql_get_by_id_query(id),
                    'status_code': 200,
                    'status_msg': 'success',
                }
                return make_response(jsonify(response)), 200
            elif latitude is not None and longitude is not None and distance is not None:
                if not (latitude != "" and longitude != "" and distance != ""):
                    abort(400)
                response = {
                    'datas': sql_get_by_distance_query(latitude, longitude, distance),
                    'status_code': 200,
                    'status_msg': 'success',
                }
                return make_response(jsonify(response)), 200
            else:
                abort(400)

    def sql_add_query(points):
        sql_query = "INSERT INTO " + TABLE_NAME + "(name, ssid, address, postCode, hpUrl, geoPoint)  \
                        VALUES(?, ?, ?, ?, ?, GeomFromText(?))"
        values = points

        return execute_sql(sql_query, values)


    def sql_get_by_distance_query(latitude, longitude, distance):
        sql_query = "SELECT" + " id, name, ssid, address, postCode, hpUrl, Y(geoPoint), X(geoPoint) FROM " + TABLE_NAME \
                    + " WHERE MBRIntersects(GeomFromText('LineString({x0} {y0}, {x1} {y2})'), geo)".format( \
                        longitude - distance, latitude - distance, longitude + distance, latitude + distance)

        return execute_sql(sql_query)

    def sql_get_by_name_query(name):
        sql_query = "SELECT" + " id, name, ssid, address, postCode, hpUrl, Y(geoPoint), X(geoPoint) FROM " + TABLE_NAME \
                    + " WHERE (name LIKE '{0}%' OR address LIKE '{0}%')".format(name, name)

        return execute_sql(sql_query)

    def sql_get_by_id_query(id):
        sql_query = "SELECT" + " id, name, ssid, address, postCode, hpUrl, Y(geoPoint), X(geoPoint) FROM " + TABLE_NAME \
                        + " WHERE id == {0}".format(id)

        return execute_sql(sql_query)

    def sql_update_query(points):
        sql_query = "UPDATE " + TABLE_NAME \
                    + " SET name = ?, ssid = ?, address = ?, postCode = ?, hpUrl = ?, geoPoint = GeomFromText(?)" + " WHERE id == ?"
        values = points

        return execute_sql(sql_query, values)


    def execute_sql(sql_query, values=()):
        con = pyodbc.connect(r'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE='+ DB_NAME + ';Trusted_connection=yes')
        cur = con.cursor()
        cur.execute("SELECT load_extension('mod_spatialite.so');")

        try:
            if len(values) != 0:
                cur.executemany(sql_query,values)
                con.commit()
                con.close()
                return {'sql_status': 'ok'}
            else:
                data = pdsql.read_sql(sql_query, con).to_dict('records')
                con.close()
                return data
        except sqlite3.Error as e:
            return {'sql_status': 'error'}

    return app
