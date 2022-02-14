import json
from flask import Flask, jsonify, request
from numpy import rec
import psycopg2
import psycopg2.extras
import pandas as pd

def store(record):
    print(record)
    hostname = 'ec2-52-214-125-106.eu-west-1.compute.amazonaws.com'
    database = 'd4p7l0ih5g9rs8'
    username = 'wuwxyfjeuoygow'
    pwd = '0037960a322b6f4b426db087a535e0f91a5a7940ee05f16e1a2a0a358060a5aa'
    port_id = 5432
    conn = None
    try:
        with psycopg2.connect(
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                insert  = 'INSERT INTO logerrors (sheet_id, script_id, function_name, user_name, error, timestamp) VALUES (%s, %s, %s, %s, %s, %s)'
                now = pd.to_datetime('today').isoformat()
                insert_values = (record['sheetID'], record['scriptID'], record['functionName'], record['user'], record['error'], now)
                cur.execute(insert, insert_values)

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            return insert_values

# create the Flask app
app = Flask(__name__)

@app.route('/execution_log')
def execution_log():
    record = {
      "sheetID": request.args.get('sheetID'),
      "scriptID": request.args.get('scriptID'),
      "functionName": request.args.get('functionName'),
      "user": request.args.get('user'),
      "error": request.args.get('error')
    }
    print(store(record))
    record = jsonify(record)
    return record

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

