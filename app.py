import flask
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import urllib, json
import urllib.request
import datetime
from libs.utils import daemonize, markdown, fetchGithubData, qrToB64
import configparser
import libs.db as database

app = flask.Flask(__name__)
socket = SocketIO(app)
config = configparser.ConfigParser()
config.read("auth/auth.cfg")
construction_mode = False
running = False
db = database.db(config['Database']['Address'])

@app.errorhandler(404)
def page_not_found(error):
    nav_projects = database.get_all(db, "repos", "name")
    return flask.render_template('404.html', nav_projects=nav_projects), 404


@app.route('/nav')
@app.route('/base')
@app.route('/project')
@app.route('/graph')
def template_error_catch():
    return flask.abort(404)


@app.route('/project/<project>')
def project(project):
    data = database.get_one(db, "repos", project)
    nav_projects = database.get_all(db, "repos", "name")
    qr = ""
    if data == None:
        return flask.render_template('404.html', nav_projects=nav_projects), 404
    if data['latest_release'] != "":
        qr = qrToB64(data['latest_release'])
    if data['readme'] == None:
        data['readme'] = "<p>No ReadMe Available!</p>"
    else:
        html = markdown(data['readme'])
        data['readme'] = html
    return flask.render_template('project.html', project=data, nav_projects=nav_projects, qr=qr)

@app.route('/about')
def about():
    data = database.get_all(db, "members", None)
    nav_projects = database.get_all(db, "repos", "name")
    return flask.render_template('about.html', members=data, nav_projects=nav_projects)


@daemonize(3600)
def updateGH():
    global running
    if running:
        print("damn looks like gunicorn is being a pain like always!")
    else:
        running = True
        if construction_mode:
            print("Github data updater is disabled while I work on the other stuff, see you in 8 hours!")
        else:
            repos, members = fetchGithubData(config['Github']['Token'])
            database.updateData(db, "repos", repos, True)
            database.updateData(db, "members", members, False)
            print("Done updating github data, checking again in 8 hours!")
        running = False
    
@app.context_processor
def get_time():
    return {'now': datetime.datetime.now()}


@app.route('/')
@app.route('/<page>')
def main(page="index"):
    nav_projects = database.get_all(db, "repos", "name")
    page += '.html'
    if os.path.isfile('templates/' + page):
        return flask.render_template(page, nav_projects=nav_projects)
    return flask.abort(404)


if __name__ == "__main__":
    if construction_mode:
        app.debug = True
    else:
        app.debug = False
    socket.run(app, host='127.0.0.1', port=4000, use_reloader=False)