from flask import make_response
from functools import wraps, update_wrapper


def server_headers(view):
    @wraps(view)
    def decorator(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        # response.headers['Expires'] = '-1'
        # response.headers['Pragma'] = 'no-cache'
        response.headers['Server'] = 'Microsoft'  # Static files not getting the HEADERS
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        response.headers['Expect-CT'] = 'max-age=86400, enforce'

        return response

    return update_wrapper(decorator, view)