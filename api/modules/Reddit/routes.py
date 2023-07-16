import requests
from modules.Shared.Logger import logger
from config import REDDIT_URL, USER_AGENT
from flask import Blueprint, jsonify, request
from modules.Shared.Headers import server_headers
from modules.Shared.Authentication import auth_required

app = Blueprint('reddit', __name__)


@app.route('/reddit', methods=['GET'])
@auth_required
@server_headers
def reddit_api():
    try:
        response_data = requests.get(
            REDDIT_URL,
            params=request.args,
            headers={
                'User-Agent': USER_AGENT
            }).json()

        return jsonify(response_data), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'Something went wrong.'}), 400
