from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from flask import Blueprint, render_template, jsonify
from config import MONGO_DB, MONGO_CVE_NVD_COLLECTION

app = Blueprint('cvedb', __name__)


@app.route('/cve-db', methods=['GET'])
@login_required
@server_headers
def cve_db_view():
    try:
        return render_template('cve-db.html', csrf_token=CSRFClass().generate_CSRF())

    except Exception as e:
        logger.exception(e)
        return render_template('cve-db.html', cve_data=[{}], cve_creation_date='')


@app.route('/cve-db/datatable', methods=['GET'])
@login_required
@server_headers
def cve_db_datatable():
    try:
        mongo_client = mongoClient()
        col_cves = mongo_client[MONGO_DB][MONGO_CVE_NVD_COLLECTION]

        datatable_data = list(col_cves.find({}, {'_id': 0}))

        mongo_client.close()

        return jsonify({'data': datatable_data}) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200
