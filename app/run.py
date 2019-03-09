from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # dn wtf is it
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # try to disable cache in browser
socketIO = SocketIO(app)

POSSIBLE_MARKS = ('-1', '0', '1', '2', '3', '5', '8', '9')

pollResults = dict()


def getMark(name: str):
    markInPool = pollResults[name]['mark']
    if markInPool == '0':
        return 'xz'
    elif markInPool == '9':
        return 'decompose'
    else:
        return markInPool


def emitComment():
    nameAndMarkDict = {k: v['mark'] for k, v in pollResults.items()}
    markList = list(nameAndMarkDict.values())
    markListWithNumbers = [int(m) for m in markList if m in POSSIBLE_MARKS[2:-1]]
    averageMark = sum(markListWithNumbers)/len(markListWithNumbers)
    msg = f'Voting is over. Average mark is {averageMark}'
    marksCount = len(set(markList))
    if marksCount == 1:
        msg = f'Unanimously! {markList[0]}!'
    elif marksCount == 2 and len(markList) > 2:
        for mark in markList:
            if markList.count(mark) == 1:
                revResults = dict(zip(nameAndMarkDict.values(), nameAndMarkDict.keys()))
                popularMark = [m for m in markList if m != mark][0]
                msg = f'All voted {popularMark}, except for {revResults[mark]} - voted {getMark(revResults[mark])}'
    emit('auth_resp', 'Not sure, but '+msg, broadcast=True)


def emitResults():
    global pollResults
    if len([name for name in pollResults if pollResults[name]['state'] is True]) == len(pollResults):
        resp = [{'name': name, 'mark': getMark(name)} for name in pollResults]
        try:
            emitComment()
        except:
            pass
        completedPerc = "100%"
    else:
        resp = [{'name': name, 'state': pollResults[name]['state']} for name in pollResults]
        if len(resp):
            completedPerc = f"{100 * len([q for q in resp if q.get('state')]) / len(pollResults)}%"
        else:
            completedPerc = "0%"
    resp.append({'perc_complete': completedPerc})
    emit('poll', resp, broadcast=True)


def emitBadMark():
    emit('auth_resp', 'Bad mark. Possible marks are: ' + ','.join(POSSIBLE_MARKS))
    resp = [{'name': name, 'state': pollResults[name]['state']} for name in pollResults]
    emit('poll', resp, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pool')
def pool_route():
    return render_template('pool.html')


@socketIO.on('auth')
def auth(login):
    global pollResults
    if login.capitalize() not in pollResults:
        resp = {'txt': 'Hello, ', 'login': login.capitalize()}
        pollResults[login.capitalize()] = {'mark': False, 'state': False}
        emit('auth_resp', resp)
        emitResults()
    else:
        emit('auth_resp', f'{login} already exists')


@socketIO.on('disc')
def disc(login):
    global pollResults
    try:
        pollResults.pop(str(login))
    except:
        pass
    finally:
        emitResults()
        disconnect()


@socketIO.on('reset')
def reset():
    """
    Clear all marks for all users
    """
    global pollResults
    for name in pollResults:
        pollResults[name] = {'state': False, 'mark': False}
    emitResults()
    emit('auth_resp', 'New poll has been started', broadcast=True)


@socketIO.on('reset_users')
def reset():
    """
    Need to fix results after disconnect failed or something else
    """
    global pollResults
    pollResults = dict()
    emitResults()


@socketIO.on('poll')
def poll(data):
    login = data.get('login')
    if not login:
        emit('auth_resp', 'please, enter your name and reconnect')
    else:
        mark = data.get('mark')
        if mark is None or mark not in POSSIBLE_MARKS:
            pollResults[login] = {'state': False, 'mark': False}
            emitBadMark()
        elif mark == '-1':
            pollResults[login] = {'state': False, 'mark': False}
            emitResults()
        else:
            pollResults[login] = {'state': True, 'mark': mark}
            emitResults()


if __name__ == '__main__':
    socketIO.run(app, debug=True, host='0.0.0.0')
