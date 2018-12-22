import markdown2 as md
import base64
import time
import threading
import traceback
from functools import wraps
from github import Github


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
    return html



def fetchGithubData(token):
    g = Github(token)
    members = []
    repos = []
    org = g.get_organization("Flagbrew")

    
    # first we get the members
    for member in org.get_members():
        members.append({
            "avatar": member.avatar_url,
            "bio": member.bio,
            "name": member.name,
            "url": member.url
        })
    # Now we get the repos
    for repo in org.get_repos():
        readme = ""
        try:
            readme = repo.get_readme().content
        except:
            readme = "N/A"
        repos.append({
            "name": repo.name,
            "readme": readme,
            "size": repo.size,
            "commits": len(repo.get_commits()),
            "forks": repo.forks_count,
            "stars": len(repo.get_stargazers())
            
        })