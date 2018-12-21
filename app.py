from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socket = SocketIO(app)
construction_mode = False

@app.route("/")
def hello():
    return "Coming Soon (in the mean time check out our <a href='https://github.com/flagbrew/'>github</a>)"

if __name__ == "__main__":
    if construction_mode:
        app.debug = True
    else:
        app.debug = False
    socket.run(app, host='127.0.0.1', port=4000, use_reloader=True)