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



def fetchRepoData(token):
    g = Github(token)
    org = g.get_organization("Flagbrew")
    for member in org.get_members():
        print(member.bio)
    repos = org.get_repos()
    for repo in repos:
        try:
            print(repo.get_readme().content)
        except:
            print("no readme")