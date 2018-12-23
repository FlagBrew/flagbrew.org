import markdown2 as md
import base64
import time
import datetime
import threading
import traceback
from functools import wraps
from github import Github
import base64
import io
import qrcode


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
    ignored = ['CacheBox', 'flagbrew.github.io', 'FlagBot', 'memecrypto']
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
        
        latest_release = ""
        readme = ""
        latest = False
        downloads = 0
        try:
            readme = repo.get_readme().content
        except:
            readme = "N/A"
        releases = repo.get_releases()
        for release in releases:
            assets = release.get_assets()
            for asset in assets:
                if asset.name.endswith(".cia") and not latest:
                    latest = True
                    latest_release = asset.browser_download_url
                downloads += asset.download_count
        # then we append
        repos.append({
            "name": repo.name,
            "readme": readme,
            "size": repo.size,
            "commits": repo.get_commits().totalCount,
            "forks": repo.forks_count,
            "stars": repo.get_stargazers().totalCount,
            "total_downloads": downloads,
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