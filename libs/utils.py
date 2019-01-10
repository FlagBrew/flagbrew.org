import markdown2 as md
import base64
import time
import datetime
import threading
import random
import string
import traceback
from functools import wraps
from github import Github
import base64
import io
import qrcode
import twitter
import arrow
import json
import jenkins
from dhooks import Webhook, Embed


def daemonize(delay):
    def daemonize_decorator(func):
        @wraps(func)
        def func_wrapper():
            while True:
                try:
                    func()
                except Exception:
                    print("===================================================================")
                    print("Error while running function %s:\n%s" % (func.__name__, str(traceback.format_exc())))
                    print("===================================================================")
                    pass
                time.sleep(int(delay))
        return threading.Thread(target=func_wrapper).start()
    return daemonize_decorator





def markdown(text):
    x = [
        'tables', 'footnotes', #'metadata',
        'fenced-code-blocks', 'header-ids',
        'wiki-tables', 'cuddled-lists', 'code-friendly'
    ]
    html = md.markdown(base64.b64decode(text), extras=x)
    html = html.replace("<img", '<img class="img-fluid" ')
    return html



def fetchGithubData(token):
    g = Github(token)
    members = []
    repos = []
    ignored = ['CacheBox', 'flagbrew.github.io', 'FlagBot', 'memecrypto', 'flagbrew.org']
    org = g.get_organization("Flagbrew")
    
    # first we get the members
    for member in org.get_members():
        members.append({
            "avatar": member.avatar_url,
            "bio": member.bio,
            "username": member.login,
            "name": member.name,
            "url": member.html_url
        })
    # Now we get the repos
    for repo in org.get_repos():
        # skip any ignored repos
        if repo.name in ignored:
            continue
        
        latest_release_cia = ""
        latest_release = ""
        readme = ""
        latest_cia = False
        latest_rel = False
        downloads = 0
        try:
            readme = repo.get_readme().content
        except:
            readme = "N/A"
        releases = repo.get_releases()
        for release in releases:
            if not latest_rel:
                latest_rel = True
                latest_release = release.html_url

            assets = release.get_assets()
            for asset in assets:
                if asset.name.endswith(".cia") and not latest_cia:
                    latest_cia = True
                    latest_release_cia = asset.browser_download_url
                downloads += asset.download_count
        # then we append
        repos.append({
            "name": repo.name,
            "readme": readme,
            "size": repo.size,
            "description": repo.description,
            "commits": repo.get_commits().totalCount,
            "forks": repo.forks_count,
            "stars": repo.get_stargazers().totalCount,
            "total_downloads": downloads,
            "latest_release_cia": latest_release_cia,
            "latest_release": latest_release,
            "downloads": [{
            "amount": downloads,
            "time": datetime.date.today().strftime("%m/%d/%Y")
            }]
        })
    return repos, members

def qrToB64(link):
    stream = io.BytesIO()
    img = qrcode.make(link)
    img.save(stream, 'PNG')
    data = base64.b64encode(stream.getvalue())
    return data.decode("utf-8") 


def twitterAPI(consumer, consumer_secret, access, access_secret):
    api = twitter.Api(consumer_key=consumer, consumer_secret=consumer_secret, access_token_key=access, access_token_secret=access_secret)
    tweets = api.GetUserTimeline(screen_name="FlagBrewOrg")
    data = []
    for tweet in tweets:
        tweet.created_at = str(arrow.get(tweet.created_at, 'ddd MMM DD HH:mm:ss Z YYYY').to('utc'))
        data.append(tweet.AsDict())
    return data

def randomcode(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def newBuild(server, user, key):
    # login to the server
    server = jenkins.Jenkins(server, username=user, password=key)
    # trigger the build
    server.build_job('PKSM')

def webHook(url, buildNum, project, downloadURL):
    hook = Webhook(url)
    embed = Embed(
		description="A new patreon build for " + project +  " has been compiled!",
		color=0xf96854,
		timestamp='now',
		url=downloadURL,
		title="New " + project + " build!"
	)
    embed.set_footer("Build: " + buildNum)
    hook.send(embed=embed)


def buildCheck(server, user, key):
    server = jenkins.Jenkins(server, username=user, password=key)
    job = server.get_running_builds()
    if len(job) == 0:
        return False
    else:
        return True
