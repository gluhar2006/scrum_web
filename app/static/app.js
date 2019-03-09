let socket = io.connect('http://' + document.domain + ':' + location.port + '/');
let myName = null;

setTimeout(show_state, 200);

let updSizes = function () {
    document.body.style.zoom = '120%';

    let fieldsWidths = [20, 30, 60];

    isMobile = window.innerHeight * 1.5 > window.innerWidth;

    if (isMobile)
        for (val in fieldsWidths)
            fieldsWidths[val] *= 1.5;

    for (elementId of ['login', 'socket_state', 'resp_auth', 'serv_reply', 'vote_3', 'vote_5', 'vote_8', 'mark'])
        document.getElementById(elementId).style.width = fieldsWidths[0].toString()+'%';
    for (elementId of ['gr_1', 'gr_2', 'gr_3', 'gr_4', 'vote_1', 'vote_2', 'vote_9', 'vote_0'])
        document.getElementById(elementId).style.width = fieldsWidths[1].toString()+'%';
    for (elementId of ['vote_c'])
        document.getElementById(elementId).style.width = fieldsWidths[2].toString()+'%';
};


window.onload = function () {
    updSizes();
};

// window.onresize = function () {
//     updSizes();
// };

function show_state() {
    if (socket && socket.connected === true)
        if (myName !== null) {
            document.getElementById('socket_state').value = 'status: connected';
            document.getElementById('connect_button').style.visibility = 'hidden';
            document.getElementById('disconnect_button').style.visibility = 'visible';
        } else {
            document.getElementById('socket_state').value = 'enter login and press connect';
            document.getElementById('connect_button').style.visibility = 'visible';
            document.getElementById('disconnect_button').style.visibility = 'hidden';
        }
}

function connect() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    let login = document.getElementById('login').value;

    if (login) {
        socket.emit('auth', login);
        setTimeout(show_state, 200);
    } else {
        document.getElementById('socket_state').value = 'enter login and press connect';
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
        if (results.indexOf(res) !== results.length - 1)
            output += '\n';
    }
    document.getElementById('serv_reply').style.height = (results.length * 25).toString() + 'px';
    document.getElementById('serv_reply').value = output;
});

function disconnect() {
    if (socket) {
        socket.emit('disc', myName);
        socket = null;
    }
    document.getElementById('socket_state').value = 'enter login and press connect';
    document.getElementById('connect_button').style.visibility = 'visible';
    document.getElementById('disconnect_button').style.visibility = 'hidden';
    setTimeout(show_state, 200);
    location.reload();
}

window.addEventListener
('beforeunload'
  , function () {
      disconnect();
      return null;
  }
);

function reset_poll() {
    socket.emit('reset');
}

function reset_users() {
    socket.emit('reset_users')
}

function vote(mark) {
    if (mark !== undefined)
        socket.emit('poll', {'login': myName, 'mark': mark.toString()});
    else
        socket.emit('poll', {'login': myName, 'mark': document.getElementById('mark').value});
}
