import eventlet
# https://github.com/miguelgrinberg/python-socketio/issues/16
eventlet.monkey_patch()
import socketio
import threading
from flask import Flask, jsonify
from flask_cors import CORS
from pycolor import GREEN, END

def query(sql):
    print(GREEN + sql + END)
    conn = pymysql.connect(**MYSQL_SETTINGS)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

app = Flask(__name__)
CORS(app)
@app.route('/query/<path:sql>')
def flask_query(sql):
    return jsonify(query(sql))

sio = socketio.Server()
app = socketio.WSGIApp(sio, app)

@sio.event
def _query(sid, sql):
    return query(sql)

@sio.event
def _enter_room(sid, room_name):
    sio.enter_room(sid, room_name)


from os import getenv
import pymysql
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent

MYSQL_SETTINGS = {
    'host': getenv('MYSQL_HOST', '127.0.0.1'),
    'port': 3306,
    'user': getenv('MYSQL_ROOT_USER', 'root'),
    'passwd': getenv('MYSQL_ROOT_PASSWORD', ''),
    'database': getenv('MYSQL_DATABASE'),
    'charset': 'utf8mb4',
    'autocommit': True
}

def binlog():
    # server_id is your slave identifier, it should be unique.
    # set blocking to True if you want to block and wait for the next event at
    # the end of the stream
    only_events = [WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent]
    stream = BinLogStreamReader(connection_settings=MYSQL_SETTINGS, server_id=3, blocking=True, only_events=only_events)

    for binlogevent in stream:
        if sio.manager.rooms:
            values_key = 'after_values' if isinstance(binlogevent, UpdateRowsEvent) else 'values'
            for row in binlogevent.rows:
                room = binlogevent.table + '/' + str(row[values_key][binlogevent.primary_key])
                sio.emit(room, (row, binlogevent.__class__.__name__), room=room)
            sio.emit(binlogevent.table, (binlogevent.rows, binlogevent.__class__.__name__), room=binlogevent.table)
    stream.close()


if __name__ == '__main__':
    threading.Thread(target=binlog).start()
    host = getenv('FIRESQL_HOST', '')
    port = getenv('FIRESQL_PORT', 8080)
    eventlet.wsgi.server(eventlet.listen((host, port)), app)
