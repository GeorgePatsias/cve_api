from datetime import datetime
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from flask import Blueprint, render_template, jsonify
from modules.Dashboard.controllers import get_latest_cves
from config import MONGO_DB, MONGO_CVE_TRENDS_COLLECTION

app = Blueprint('dashboard', __name__)


@app.route('/dashboard', methods=['GET'])
@login_required
@server_headers
def dashboard_view():
    try:
        mongo_client = mongoClient()
        col_cves = mongo_client[MONGO_DB][MONGO_CVE_TRENDS_COLLECTION]

        cve_results = list(col_cves.find({}).sort([('created_at', -1)]).limit(1))

        if not cve_results:
            cve_results = get_latest_cves()
            col_cves.insert_one(cve_results)

        if type(cve_results) is list:
            cve_results = cve_results[0]

        cve_data_creation = cve_results.get('created_at').date()

        if cve_data_creation != datetime.now().date():
            cve_results = get_latest_cves()
            col_cves.insert_one(cve_results)

        cve_data_creation = str(cve_results.get('created_at')).rsplit('.', 1)[0]

        mongo_client.close()

        cves = cve_results.get('data')
        doc = {}
        for item in cves:
            doc['cve_id'] = item.get('cve')
            doc['description'] = item.get('cve')

        return render_template('dashboard.html', csrf_token=CSRFClass().generate_CSRF(), cve_data=doc, cve_creation_date=cve_data_creation)

    except Exception as e:
        logger.exception(e)
        return render_template('dashboard.html', cve_data=[{}], cve_creation_date='')


@app.route('/dashboard/datatable', methods=['GET'])
@login_required
@server_headers
def datatable_dashboard():
    try:
        mongo_client = mongoClient()
        col_cves = mongo_client[MONGO_DB][MONGO_CVE_TRENDS_COLLECTION]

        datatable_data = list(col_cves.find({}, {'_id': 0, 'data.cve': 1, 'data.description': 1, 'data.severity': 1}).sort([('created_at', -1)]).limit(1))[0]

        mongo_client.close()

        for item in datatable_data.get('data'):
            for k, v in item.items():
                if not item[k]:
                    item[k] = 'Pending'

        return jsonify(datatable_data) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200


@app.route('/dashboard/trending-posts', methods=['GET'])
@login_required
@server_headers
def trending_posts_dashboard():
    try:
        mongo_client = mongoClient()
        col_cves = mongo_client[MONGO_DB][MONGO_CVE_TRENDS_COLLECTION]

        datatable_data = list(col_cves.find({}, {'_id': 0, 'data.cve': 1, 'data.audience_size': 1, 'data.publishedDate': 1}).sort([('created_at', -1)]).limit(1))[0]

        mongo_client.close()

        return jsonify(datatable_data.get('data')) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200
