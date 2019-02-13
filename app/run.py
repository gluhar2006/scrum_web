from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

cnt = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

pollResults = dict()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('auth')
def auth(login):
    resp = {'txt': 'Hello, ', 'login': login.capitalize()}
    pollResults[login.capitalize()] = {'mark': False, 'state': False}
    emit('auth_resp', resp)


@socketio.on('reset')
def reset():
    global pollResults
    for name in pollResults:
        pollResults[name]['state'] = False
        pollResults[name]['mark'] = False
    states = [{name: pollResults[name]['state']} for name in pollResults]
    emit('poll', states, broadcast=True)


@socketio.on('poll')
def poll(data):
    login = data.get('login')
    if not login:
        emit('auth_resp', 'please, enter your name and reconnect')
    else:
        mark = data.get('mark')
        print(mark)
        pollResults[login] = {'state': True, 'mark': mark}

        if len([name for name in pollResults if pollResults[name]['state'] is True]) == len(pollResults):
            resp = [{name: pollResults[name]['mark']} for name in pollResults]
        else:
            resp = [{name: pollResults[name]['state']} for name in pollResults]
        emit('poll', resp, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
