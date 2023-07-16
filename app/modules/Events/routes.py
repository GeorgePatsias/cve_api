from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from flask_login import login_required, current_user
from config import MONGO_DB, MONGO_NOTIFICATIONS_COLLECTION
from flask import Blueprint, render_template, request, escape, jsonify

app = Blueprint('events', __name__)


@app.route('/events', methods=['GET'])
@login_required
@server_headers
def events_view():
    try:
        return render_template('events.html', csrf_token=CSRFClass().generate_CSRF(), error_message='', cve_id='', cve_data=None)

    except Exception as e:
        logger.exception(e)
        return render_template('events.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong!', cve_id=None, cve_data=None)


@app.route('/events/datatable', methods=['GET'])
@login_required
@server_headers
def events_datatable():
    try:
        mongo_client = mongoClient()
        col_cves = mongo_client[MONGO_DB][MONGO_NOTIFICATIONS_COLLECTION]

        db_data = col_cves.find_one({'username': current_user.id}, {'_id': 0})

        datatable_data = db_data.get('data')

        mongo_client.close()

        print(datatable_data)

        return jsonify({'data': datatable_data}) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200
