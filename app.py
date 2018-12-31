import flask
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import urllib, json
import urllib.request
import datetime
from libs.utils import daemonize, markdown, fetchGithubData, qrToB64, twitterAPI
#import libs.wraps.auth as auth
import libs.wraps.misc as misc
import configparser
import libs.db as database

app = flask.Flask(__name__)
socket = SocketIO(app)
config = configparser.ConfigParser()
config.read("auth/auth.cfg")
construction_mode = False
running = False
updateTime = 3600
db = database.db(config['Database']['Address'])

if datetime.datetime.today().strftime('%Y-%m-%d') == "2018-12-31":
    updateTime = 600

@app.errorhandler(404)
def page_not_found(error):
    nav_projects = database.get_all(db, "repos", "name")
    return flask.render_template('404.html', nav_projects=nav_projects), 404


@app.route('/nav')
@app.route('/base')
@app.route('/project')
@app.route('/graph')
@app.route('/stats')
@app.route('/construction')
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

@app.route('/stats/downloads')
def downloadStats():
    nav_projects = database.get_all(db, "repos", "name")
    data = database.get_repo_downloads(db, "repos")
    return flask.render_template('stats.html', data=data, nav_projects=nav_projects)

@daemonize(updateTime)
def updateData():
    global running
    if running:
        print("damn looks like gunicorn is being a pain like always!")
    else:
        running = True
        if construction_mode:
            print("Data updater is disabled because construction mode is enabled!")
        else:
            repos, members = fetchGithubData(config['Github']['Token'])
            database.updateData(db, "repos", repos, True, True, False)
            database.updateData(db, "members", members, False, True, False)
            print("Done updating github data!")
            tweets = twitterAPI(config['Twitter']['Consumer_Key'], config['Twitter']['Consumer_Secret'], config['Twitter']['Access_Key'], config['Twitter']['Access_Secret'])
            database.updateData(db, "tweets", tweets, False, False, True)
            print("Done updating twitter data!")
        if updateTime == 600:
            if datetime.datetime.today().strftime('%Y-%m-%d') != "2018-12-31":
                updateTime = 3600
        print("Data will be updated once again in", updateTime/60 , "minutes!")
        running = False
    
@app.context_processor
def get_time():
    return {'now': datetime.datetime.now()}

@app.route('/')
@app.route('/<page>')
# @misc.construction(construction_mode)
def main(page="index"):
    nav_projects = database.get_all(db, "repos", "name")
    page += '.html'
    if os.path.isfile('templates/' + page):
        return flask.render_template(page, nav_projects=nav_projects)
    return flask.abort(404)

@app.route('/api/tweets')
def tweetApi():
    tweets = database.get_all(db, "tweets", None)
    return database.jsonify(database.json(tweets))


if __name__ == "__main__":
    if construction_mode:
        app.debug = True
        socket.run(app, host='127.0.0.1', port=4000, use_reloader=False)
    else:
        app.debug = False
        socket.run(app, host='127.0.0.1', port=4000, use_reloader=False)