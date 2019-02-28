from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'    # dn wtf is it
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0     # try to disable cache in browser
socketio = SocketIO(app)

POSSIBLE_MARKS = ('0', '1', '2', '3', '5', '8', '9')

pollResults = dict()


def emitResults():
    if len([name for name in pollResults if pollResults[name]['state'] is True]) == len(pollResults):
        resp = [{'name': name, 'mark': pollResults[name]['mark']} for name in pollResults]
    else:
        resp = [{'name': name, 'state': pollResults[name]['state']} for name in pollResults]
    emit('poll', resp, broadcast=True)


def emitBadMark():
    emit('auth_resp', 'Bad mark. Possible marks are: '+','.join(POSSIBLE_MARKS))
    resp = [{'name': name, 'state': pollResults[name]['state']} for name in pollResults]
    emit('poll', resp, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('auth')
def auth(login):
    resp = {'txt': 'Hello, ', 'login': login.capitalize()}
    pollResults[login.capitalize()] = {'mark': False, 'state': False}
    emit('auth_resp', resp)
    emitResults()


@socketio.on('disc')
def disc(login):
    try:
        pollResults.pop(str(login))
    except:
        pass
    finally:
        emitResults()
        disconnect()


@socketio.on('reset')
def reset():
    for name in pollResults:
        pollResults[name]['state'] = False
        pollResults[name]['mark'] = False
    emitResults()


@socketio.on('poll')
def poll(data):
    login = data.get('login')
    if not login:
        emit('auth_resp', 'please, enter your name and reconnect')
    else:
        mark = data.get('mark')
        if mark:
            if mark not in POSSIBLE_MARKS:
                pollResults[login]['state'] = False
                pollResults[login].update({'mark': False})
                emitBadMark()
            else:
                pollResults[login]['state'] = True
                pollResults[login].update({'mark': mark})
                emitResults()


if __name__ == '__main__':
    socketio.run(app, debug=True)
