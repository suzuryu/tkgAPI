from flask import Flask, jsonify, request
import json
import pandas.io.sql as pdsql
import pyodbc


app = Flask(__name__)

@app.route('/wifi', methods=['POST'])
def method_name():
    if request.method == 'POST':
        pass
   pass

@app.route('/wifi', methods=['POST'])
def method_name():
    if request.method == 'POST':
        pass
   pass
   
@app.route('/wifi', methods=['POST'])
def method_name():
    if request.method == 'POST':
        pass
   pass

if __name__ == '__main__':
    app.run()
    