import os

import ujson
from sanic import Sanic, response
from websockets import ConnectionClosedOK

from classes import User, State
from texts import get_text

app = Sanic(__name__)

users: list[User] = []


async def emit_results():
    global users
    if not len(users):
        res = {"users": [], "text": "waiting for users", "percent_complete": 0}
    else:
        percent_complete = int(100 * len([user for user in users if user.state == State.ready]) / len(users))
        res = {"users": [user.as_dict() for user in users], "percent_complete": percent_complete,
               "text": get_text(users) if percent_complete == 100 else "vote in progress"}
    users_to_disc = []
    for user in users:
        try:
            await user.ws.send(ujson.dumps(res))
        except ConnectionClosedOK:
            users_to_disc.append(user.name)
            print(f"seems {user.name} disconnected")
    if users_to_disc:
        users = [user for user in users if user.name not in users_to_disc]
        for user in users:
            await user.ws.send(ujson.dumps(res))


@app.route('/')
def handle_request(request):
    return response.redirect('/index.html')


async def ws_handler(request, ws):
    global users
    while True:
        data = await ws.recv()
        try:
            parsed_data = ujson.loads(data)
            action = list(parsed_data)[0]
            if action == "connect":
                new_user_name = parsed_data[action]
                user_names = [user.name for user in users]
                if new_user_name in user_names:
                    await ws.send(ujson.dumps({"error": "user with this name already exists"}))
                    print(f"{new_user_name} already exists")
                else:
                    new_user = User(new_user_name, ws)
                    users.append(new_user)
                    await ws.send(ujson.dumps({"connected": new_user.name}))
                    print(f"{new_user.name} connected")
            elif action == "disconnect":
                user_name = parsed_data[action]
                users = [user for user in users if user.name != user_name]
                await ws.send(ujson.dumps({"disconnect": user_name}))
                print(f"{user_name} disconnected")
            elif action == "vote":
                data = parsed_data[action]
                user_name, mark = data["name"], data["mark"]
                user = [user for user in users if user.name == user_name][0]
                user.vote(mark)
                print(f"{user_name} voted {mark}")
            elif action == "reset":
                for user in users:
                    user.reset_mark()
                print(f"reset marks by {parsed_data[action]}")
            elif action == "reset_users":
                for user in users:
                    await user.ws.send(ujson.dumps({"disconnect": parsed_data[action]}))
                users = []
                print(f"reset users by {parsed_data[action]}")
            else:
                print("wrong action")
            await emit_results()
        except Exception as e:
            print(str(e))
            print(data)


app.static('/', os.path.join(os.path.abspath('.'), 'static'))
app.add_websocket_route(ws_handler, '/ws')
app.config['WEBSOCKET_PING_INTERVAL'] = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
