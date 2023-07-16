import json
import nvdlib
import requests
import datetime
from modules.Shared.Logger import logger
from flask import Blueprint, jsonify, request
from modules.Shared.Headers import server_headers
from modules.Shared.Authentication import auth_required
from config import NVD_CVE_URL, NVD_API_KEY, NVD_HISTORY_URL

app = Blueprint('nvd', __name__)

# https://nvd.nist.gov/developers/vulnerabilities


@app.route('/nvd/cve', methods=['GET'])
@auth_required
@server_headers
def nvd_cve_api():
    try:
        response = requests.get(NVD_CVE_URL, params=request.args, headers={'apiKey': NVD_API_KEY})

        if response.status_code in [204, 404]:
            return jsonify({'status': 'No Content.'}), response.status_code

        response_data = response.json()

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'Something went wrong.'}), 400

    return jsonify(response_data), 200


@app.route('/nvd/monitoring', methods=['GET'])
@auth_required
@server_headers
def nvdlib_api():
    try:
        keyword = request.args.get('keyword', None)

        if not keyword:
            return jsonify({'status': 'No Content.'}), 200

        date_time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # The maximum allowable range when using any date range parameters is 120 consecutive days.
        previous_month = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')


        response_data = nvdlib.searchCVE(keywordSearch=keyword, pubStartDate=previous_month, pubEndDate=date_time_now, key=NVD_API_KEY)

        if not response_data:
            return jsonify({}), 200

        cve_data = json.loads(json.dumps(response_data, default=lambda o: o.__dict__, sort_keys=True))

        return jsonify(cve_data), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'Something went wrong.'}), 400


@app.route('/nvd/history', methods=['GET'])
@auth_required
@server_headers
def nvd_history_api():
    try:
        response = requests.get(NVD_HISTORY_URL, params=request.args, headers={'apiKey': NVD_API_KEY})

        if response.status_code in [204, 404]:
            return jsonify({'status': 'No Content.'}), response.status_code

        response_data = response.json()

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'Something went wrong.'}), 400

    return jsonify(response_data), 200
