from modules.Shared.Logger import logger
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from flask_login import login_required, current_user
from flask import Blueprint, jsonify, redirect, request
from config import MONGO_DB, MONGO_NOTIFICATIONS_COLLECTION

app = Blueprint('notifications', __name__)


@app.route('/notifications', methods=['GET'])
@login_required
@server_headers
def notifications():
    try:
        mongo_client = mongoClient()
        col_notifications = mongo_client[MONGO_DB][MONGO_NOTIFICATIONS_COLLECTION]

        db_data = col_notifications.find_one({'username': current_user.id}, {'_id': 0, 'data': 1})

        if not db_data:
            return {'count': 0, 'data': []}, 200

        notification_doccuments = db_data['data']
        result_doc = {
            'count': len(notification_doccuments),
            'data': notification_doccuments
        }

        return jsonify(result_doc), 200

    except Exception as e:
        logger.exception(e)
        return {'count': 0, 'data': []}, 200


@app.route('/notifications/delete', methods=['GET'])
@login_required
@server_headers
def notifications_delete():
    try:
        mongo_client = mongoClient()
        col_notifications = mongo_client[MONGO_DB][MONGO_NOTIFICATIONS_COLLECTION]

        col_notifications.update_one({'username': current_user.id}, {'$set':  {'data': []}})

        return redirect(request.referrer)

    except Exception as e:
        logger.exception(e)
        return {'count': 0, 'data': []}, 200
