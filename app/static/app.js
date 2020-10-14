let socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');
let myName = null;

setTimeout(show_state, 200);

let updSizes = function () {
  document.body.style.zoom = '110%';

  let fieldsWidths = [25, 60, 60];

  isMobile = window.innerHeight * 1.5 > window.innerWidth;

  for (elementId of ['login', 'socket_state', 'serv_reply', 'vote_3', 'vote_5', 'vote_8', 'mark', 'vote_1', 'vote_2', 'vote_9', 'vote_0', 'vote_c'])
    document.getElementById(elementId).style.width = fieldsWidths[0].toString() + '%';
  for (elementId of ['gr_1', 'gr_2', 'resp_auth'])
    document.getElementById(elementId).style.width = fieldsWidths[1].toString() + '%';
  for (elementId of [])
    document.getElementById(elementId).style.width = fieldsWidths[2].toString() + '%';
};


window.onload = function () {
  updSizes();

  document.getElementById('mark').addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      vote();
    }
  });

  document.getElementById('login').addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      connect();
    }
  });
};

window.onresize = function () {
  updSizes();
};

function show_state() {
  if (socket && socket.OPEN)
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
  let login = document.getElementById('login').value;

  if (login) {
    socket.send(JSON.stringify({'connect': login}));
    setTimeout(show_state, 200);
    showPool();
  } else {
    document.getElementById('socket_state').value = 'enter login and press connect';
    document.getElementById('resp_auth').value = 'Please, enter login and press connect';
  }
}

function showPool() {
  $('#sLogin').collapse('toggle');
  $('#sPool').collapse('show');
}

function showLogin() {
  $('#sPool').collapse('toggle');
  $('#sLogin').collapse('show');
}

function getResults(server_reply) {
  let output = '';
  let is_over = server_reply["percent_complete"] === 100;
  for (let res of server_reply["users"]) {
      output += res['name'];
      if (is_over)
        output += ': ' + res['mark'];
      else
        output += res['state'] === 1 ? ' ready' : ' think';
      if (server_reply["users"].indexOf(res) !== server_reply["users"].length - 1)
        output += '\n';
    }
  return output;
}

socket.onmessage = function(event) {
    let msg = JSON.parse(event.data);
    if (msg !== undefined) {
        if (Object.keys(msg)[0] === "connected") {
           myName = msg["connected"];
        } else if (myName !== null && Object.keys(msg)[0] === "disconnect") {
           disconnect();
           alert(msg["disconnect"] + " reset users. login again");
        } else if (Object.keys(msg)[0] === "error") {
           disconnect();
           alert(msg["error"]);
        } else {
            document.getElementById('progressBar').style.width = msg['percent_complete'] + '%';
            if (msg['perc_complete'] === 100)
              $('#progressBar').removeClass().addClass('progress-bar progress-bar-success');
            else
              $('#progressBar').removeClass().addClass('progress-bar progress-bar-success progress-bar-striped');

            results = getResults(msg);
            document.getElementById('serv_reply').style.height = (msg["users"].length * 35).toString() + 'px';
            document.getElementById('serv_reply').value = results;

            document.getElementById('resp_auth').value = msg["text"];
        }
    } else {
        document.getElementById('resp_auth').value = "something goes wrong =(";
    }
}

socket.onclose = function(event) {
    disconnect();
}

function disconnect() {
  if (socket && socket.OPEN) {
    socket.send(JSON.stringify({'disconnect': myName}));
  }
  myName = null;
  document.getElementById('socket_state').value = 'enter login and press connect';
  document.getElementById('connect_button').style.visibility = 'visible';
  document.getElementById('disconnect_button').style.visibility = 'hidden';
  setTimeout(show_state, 200);
  location.reload();
  showLogin();
}

window.addEventListener
('beforeunload', function () {
    disconnect();
    return null;
  }
);

function reset_poll() {
  socket.send(JSON.stringify({'reset': myName}));
}

function reset_users() {
  socket.send(JSON.stringify({'reset_users': myName}));
  disconnect();
}

function vote(mark) {
  let new_mark = mark !== undefined ? mark.toString() : document.getElementById('mark').value;
  let data_to_send = {"vote": {"name": myName, "mark": new_mark}};
  socket.send(JSON.stringify(data_to_send));
}
