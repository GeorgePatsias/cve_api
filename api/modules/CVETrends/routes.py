import requests
from flask import Blueprint, jsonify
from modules.Shared.Logger import logger
from modules.Shared.Headers import server_headers
from modules.Shared.Authentication import auth_required
from config import CVE_TRENDS_URL_24H, CVE_TRENDS_URL_7D, USER_AGENT

app = Blueprint('cve_trends', __name__)


@app.route('/cve-trends/24h', methods=['GET'])
@auth_required
@server_headers
def cve_trends_24h_api():
    try:
        response = requests.get(CVE_TRENDS_URL_24H, headers={'User-Agent': USER_AGENT})

        if response.status_code in [204, 404]:
            return jsonify({'status': 'No Content.'}), response.status_code

        response_data = response.json()
        
        return jsonify(response_data), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'No Content.'}), 400


@app.route('/cve-trends/7d', methods=['GET'])
@auth_required
@server_headers
def cve_trends_7d_api():
    try:
        response = requests.get(CVE_TRENDS_URL_7D, headers={'User-Agent': USER_AGENT})

        if response.status_code in [204, 404]:
            return jsonify({'status': 'No Content.'}), response.status_code

        response_data = response.json()

        return jsonify(response_data), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'No Content.'}), 400
