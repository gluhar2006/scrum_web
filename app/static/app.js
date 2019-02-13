
var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
let myName = null;

setTimeout(show_state, 200);

function show_state() {
  document.getElementById('socket_state').value = 'disconnected';
  if (socket && socket.connected === true)
    document.getElementById('socket_state').value = 'connected';
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
  myName = msg['login'];
  document.getElementById('resp_auth').value = msg.txt + msg.login;
});

socket.on('poll', function (results) {
  document.getElementById('serv_reply').value = JSON.stringify(results);
});

function disconnect() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
  setTimeout(show_state, 200);
}

function reset_poll() {
  socket.emit('reset');
}

function vote() {
  socket.emit('poll', {'login': myName, 'mark': document.getElementById('mark').value});
}

function clk() {
  if (socket)
    socket.emit('message', document.getElementById('str_data').value);
  console.log('click' + document.getElementById('str_data').value);
}

