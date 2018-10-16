#!/usr/bin/env python

### PARTE 3
##### STREAM FILTRANDO ID DE JORNAIS.
##### APP COM SOCKETS DISPONIBILIZA NOVOS 

from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import twitter_stream_app as twitter_api

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def background_thread():

    resourse = twitter_api.inicializa_cliente_twitter()

    for data in resourse.stream():
        
        if "retweeted_status" in data:
            ret = data.retweeted_status.id
        else:
            ret = False

        newt = [data.id,data.created_at,data.text,data.in_reply_to_status_id,ret]
        #resultado.append(data)
        socketio.emit('new_tweet',
                    {'data': 'New Tweet', 'tweet': newt},
                    namespace='/test')

        


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'tweet': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True,  host='localhost', port=80)
   
