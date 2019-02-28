let socket = io.connect('http://' + document.domain + ':' + location.port + '/');
let myName = null;

setTimeout(show_state, 200);

function show_state() {
    document.getElementById('socket_state').value = 'disconnected';
    if (socket && socket.connected === true)
        if (myName !== null) {
            document.getElementById('socket_state').value = 'connected';
        } else {
            document.getElementById('socket_state').value = 'enter login and press connect';
        }
}

function connect() {
    if (!socket)
        socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    let login = document.getElementById('login').value;

    if (login) {
        socket.emit('auth', login);
        setTimeout(show_state, 200);
    } else {
        document.getElementById('socket_state').value = 'disconnected';
        document.getElementById('resp_auth').value = 'Please, enter login and press connect';
    }
}

socket.on('auth_resp', function (msg) {
    let name_ = msg['login'];
    if (name_ !== undefined) {
        myName = name_;
        document.getElementById('resp_auth').value = msg.txt + msg.login;
    } else {
        document.getElementById('resp_auth').value = msg;
    }
});

socket.on('poll', function (results) {
    let output = '';
    for (let res of results) {
        output += res['name'];
        if (res['state'] === true) {
            output += ' ready';
        } else if (res['state'] === false) {
            output += ' think';
        } else if (res['mark']) {
            output += ': ' + res['mark'];
        } else {
            output += ' spectractor';
        }
        output += '\n';
    }
    document.getElementById('serv_reply').value = output;
});

function disconnect() {
    if (socket) {
        socket.emit('disc', myName);
        socket = null;
    }
    setTimeout(show_state, 200);
}

window.onbeforeunload = function () {
    disconnect();
}

function reset_poll() {
    socket.emit('reset');
}

function vote() {
    socket.emit('poll', {'login': myName, 'mark': document.getElementById('mark').value});
}
