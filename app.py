import flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = flask.Flask(__name__)
socket = SocketIO(app)
construction_mode = True

@app.route('/')
@app.route('/<page>')
def main(page="index"):
    page += '.html'
    if os.path.isfile('templates/' + page):
        return flask.render_template(page)
    return flask.abort(404)


if __name__ == "__main__":
    if construction_mode:
        app.debug = True
    else:
        app.debug = False
    socket.run(app, host='127.0.0.1', port=4000, use_reloader=True)