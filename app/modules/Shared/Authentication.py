from functools import wraps
from config import API_TOKEN
from modules.Shared.Logger import logger
from flask import request, make_response, jsonify


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-api-token' in request.headers:
            token = request.headers['x-api-token']

        if not token:
            logger.info('Empty token request - login failed.')
            return make_response(jsonify({
                'code': 401,
                'name': 'Unauthorized access.',
                'description': 'The given authentication is not valid.',
            }), 401)

        try:
            if token != API_TOKEN:
                logger.info(f'Invalid token request - login failed for {token}.')
                return make_response(jsonify({
                    'code': 401,
                    'name': 'Unauthorized access.',
                    'description': 'The given authentication is not valid.',
                }), 401)

        except Exception as e:
            logger.exception(e)
            return make_response(jsonify({
                'code': 401,
                'name': 'Unauthorized access.',
                'description': 'The given authentication is not valid.',
            }), 401)

        return f(*args, **kwargs)
    return decorator
