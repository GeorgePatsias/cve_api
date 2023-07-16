import requests
from modules.Shared.Logger import logger
from config import GITHUB_URL, GITHUB_TOKEN
from flask import Blueprint, jsonify, request
from modules.Shared.Headers import server_headers
from modules.Shared.Authentication import auth_required

app = Blueprint('github', __name__)


@app.route('/github/cve', methods=['GET'])
@auth_required
@server_headers
def github_api():
    try:
        response = requests.get(GITHUB_URL, params=request.args, headers={'Authorization': f'Bearer {GITHUB_TOKEN}'})

        if response.status_code in [204, 404]:
            return jsonify({'status': 'No Content.'}), response.status_code

        response_data = response.json()

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'No Content.'}), 200

    return jsonify(response_data), 200
