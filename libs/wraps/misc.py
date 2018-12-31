from functools import wraps
import flask 

def construction(construction_mode):
    def construction_check(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            if construction_mode:
                return flask.render_template('construction.html')
            else:
                return method(*args, **kwargs)
        return wrapper
    return construction_check