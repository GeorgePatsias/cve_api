from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_CVE_TRENDS_COLLECTION
from modules.Investigate.controllers import investigate_cve
from flask import Blueprint, render_template, request, escape, redirect, jsonify

app = Blueprint('investigate', __name__)


@app.route('/investigate', methods=['GET'])
@login_required
@server_headers
def investigate_view():
    try:
        return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='', cve_id='', cve_data=None)

    except Exception as e:
        logger.exception(e)
        return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong!', cve_id=None, cve_data=None)


@app.route('/investigate/search', methods=['POST'])
@login_required
@server_headers
def investigate_search_view():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Please refresh the page and try again!', cve_id=None, cve_data=None)

        search_data = request.form['search-data']

        if not search_data:
            return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Please enter a valid search term!', cve_id=None, cve_data=None)

        search_data = escape(search_data).strip()

        return redirect(f'/investigate/{search_data}', code=302)

    except Exception as e:
        logger.exception(e)
        return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong!', cve_id=None, cve_data=None)


@app.route('/investigate/<cve_id>', methods=['GET'])
@login_required
@server_headers
def investigate_cve_view(cve_id):
    try:
        if not cve_id:
            return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong!', cve_id=None, cve_data=None)

        cve_id = escape(cve_id).strip()

        cve_data = investigate_cve(cve_id)

        return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='', cve_id=cve_id, cve_data=cve_data)

    except Exception as e:
        logger.exception(e)
        return render_template('investigate.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong!', cve_id=None, cve_data=None)


@app.route('/investigate/twitter-traffic', methods=['GET'])
@login_required
@server_headers
def twitter_traffic_dashboard():
    try:
        cve_id = escape(request.args['cveId'])

        mongo_client = mongoClient()
        col_cves = mongo_client[MONGO_DB][MONGO_CVE_TRENDS_COLLECTION]

        datatable_data = list(col_cves.find({'data.cve': cve_id}, {'_id': 0, 'data.timegraph_data': 1, 'data.cve': 1}).sort([('created_at', -1)]).limit(1))

        if not datatable_data:
            return [{}], 200

        datatable_data = datatable_data[0]

        results = {}
        for doc in datatable_data.get('data'):
            if doc.get('cve') == cve_id:
                results = doc.get('timegraph_data')
                break

        mongo_client.close()

        sorted_results = sorted(results, key=lambda k: k['timestamp_start'])

        return jsonify(sorted_results) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200
