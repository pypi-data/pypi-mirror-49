from flask import request, current_app
from functools import wraps

class MissingItemInHeaders(Exception):

    pass

def requires_header_items(must_have_these_headers=[]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_fun(*args, **kwargs):
            not_seen_in_header = []
            for key in must_have_these_headers:
                if not key in request.headers:
                    not_seen_in_header.append(key)
                else:
                    kwargs[key] = request.headers.get(key)

            if len(not_seen_in_header) > 0:
                raise MissingItemInHeaders(", ".join(not_seen_in_header) + " not present in request headers.")
            else:
                return fn(*args, **kwargs) 


        return decorated_fun
    return wrapper