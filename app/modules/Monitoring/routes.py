from threading import Thread
from datetime import datetime
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from flask_login import login_required, current_user
from config import MONGO_DB, MONGO_MONITORING_COLLECTION
from modules.Monitoring.controllers import monitoring_results
from flask import Blueprint, render_template, jsonify, request, escape, redirect, url_for

app = Blueprint('monitoring', __name__)


@app.route('/monitoring', methods=['GET'])
@login_required
@server_headers
def monitoring_view():
    try:
        return render_template('monitoring.html', csrf_token=CSRFClass().generate_CSRF(), error_msg='')

    except Exception as e:
        logger.exception(e)
        return render_template('monitoring.html', csrf_token=CSRFClass().generate_CSRF(), error_msg='Something went wrong!')


@app.route('/monitoring?<error_message>', methods=['GET'])
@login_required
@server_headers
def monitoring_error(error_message=''):
    try:
        return render_template('monitoring.html', csrf_token=CSRFClass().generate_CSRF(), error_message=escape(error_message))

    except Exception as e:
        logger.exception(e)
        return render_template('monitoring.html', csrf_token=CSRFClass().generate_CSRF(), error_msg='Something went wrong!')


@app.route('/monitoring/keyword-tags', methods=['POST'])
@login_required
@server_headers
def keyword_tags():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('monitoring.monitoring_error', error_message='Please refresh the page and try again!'))

        tags_list = request.form['keywords-tags']
        frequency = request.form['monitoring-frequency']

        if not tags_list or not frequency:
            return redirect(url_for('monitoring.monitoring_error', error_message='Tags input cannot be empty!'))

        if frequency not in ['3', '6', '12', '24', '48', '168']:
            return redirect(url_for('monitoring.monitoring_error', error_message='Please enter a valid monitoring frequency!'))

        tags_list = tags_list.split(',')

        mongo_client = mongoClient()
        col_monitoring = mongo_client[MONGO_DB][MONGO_MONITORING_COLLECTION]

       # FIX TOO HEAVY!!!!!!!!!!!!!
        monitor_list = []
        for tag in tags_list:
            monitor_list.append({
                'username': current_user.id,
                'monitoring_keyword': tag
            })

            existing_doc = col_monitoring.find_one({'username': current_user.id, 'monitoring_keyword': tag}, {'_id': 0})

            if existing_doc:
                col_monitoring.update_one({'username': current_user.id, 'monitoring_keyword': tag}, {'$set': {'edited_at': datetime.now(), 'frequency': frequency}})
                continue

            col_monitoring.insert_one({
                'username': current_user.id,
                'monitoring_keyword': tag,
                'frequency': frequency,
                'created_at': datetime.now(),
                'edited_at': None,
                'updated_at': 'Pending',
            })

        mongo_client.close()

        for item in monitor_list:
            thread = Thread(target=monitoring_results, args=(item, ))
            thread.start()

        return redirect(url_for('monitoring.monitoring_view', error_message=''))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('monitoring.monitoring_error', error_message='Something went wrong!'))


@app.route('/monitoring/datatable', methods=['GET'])
@login_required
@server_headers
def datatable_monitoring():
    try:
        mongo_client = mongoClient()
        col_monitoring = mongo_client[MONGO_DB][MONGO_MONITORING_COLLECTION]

        db_data = list(col_monitoring.find({'username': current_user.id}, {'_id': 0}))

        datatable_data = {'data': db_data}

        mongo_client.close()

        return jsonify(datatable_data) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200


@app.route('/monitoring/delete', methods=['GET'])
@login_required
@server_headers
def datatable_delete():
    try:
        delete_keyword = request.args['keyword']

        mongo_client = mongoClient()
        col_monitoring = mongo_client[MONGO_DB][MONGO_MONITORING_COLLECTION]

        col_monitoring.delete_one({'username': current_user.id, 'monitoring_keyword': delete_keyword})

        mongo_client.close()

        return '', 200

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('monitoring.monitoring_error', error_message='Something went wrong. please try again!'))
