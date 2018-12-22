import flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import urllib, json
import urllib.request
from libs.utils import daemonize, markdown, fetchRepoData
import configparser

app = flask.Flask(__name__)
socket = SocketIO(app)
config = configparser.ConfigParser()
config.read("auth/auth.cfg")
construction_mode = True
cachebox = True

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404


@app.route('/nav')
@app.route('/base')
@app.route('/project')
def template_error_catch():
    return flask.abort(404)


@app.route('/project/<project>')
def project(project):
    if cachebox:
        data = ""
        # get stuff from url
        with urllib.request.urlopen("https://cachebox.fm1337.com/api/repos/"+project) as response:
            data = json.loads(response.read())
    else:
        # get stuff from mongodb
        print('not implemented yet')
    html = markdown(data['readme']['content'])
    return flask.render_template('project.html', project=data['name'], readme=html)


@daemonize(1800)
def updateGH():
    fetchRepoData(config['Github']['Token'])
    


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
    socket.run(app, host='127.0.0.1', port=4000, use_reloader=False)