import requests
from datetime import datetime
from flask_login import current_user
from modules.Shared.Logger import logger
from modules.Shared.MongoClient import mongoClient
from modules.Investigate.controllers import get_final_result_cve
from config import API_URL, API_TOKEN, MONGO_DB, MONGO_MONITORING_COLLECTION, MONGO_CVE_NVD_COLLECTION, MONGO_NOTIFICATIONS_COLLECTION


def monitoring_results(data):
    try:
        username = data.get('username', None)
        keyword = data.get('monitoring_keyword', None)

        if not username or not keyword:
            return None

        keyword = keyword.strip()

        response_data = requests.get(f'{API_URL}/nvd/monitoring?keyword={keyword}', headers={'x-api-token': API_TOKEN}).json()

        if not response_data:
            return None

        mongo_client = mongoClient()
        col_nvd = mongo_client[MONGO_DB][MONGO_CVE_NVD_COLLECTION]
        col_monitoring = mongo_client[MONGO_DB][MONGO_MONITORING_COLLECTION]
        col_notifications = mongo_client[MONGO_DB][MONGO_NOTIFICATIONS_COLLECTION]

        col_monitoring.update_one({'username': username, 'monitoring_keyword': keyword}, {'$set': {'updated_at': datetime.now()}})

        for cve_data in response_data:
            cve_results = get_final_result_cve(cve_data.get('id'), cve_data)

            col_nvd.update_one({'cve': cve_data.get('id')}, {'$set': cve_results}, upsert=True)

            db_res = col_notifications.update_one({'username': username, 'data.cve': {'$ne': cve_data.get('id')}}, {
                '$push': {
                    'data': {
                        'cve': cve_data.get('id'),
                        'keyword': keyword
                    }
                }
            })

            if db_res.matched_count == 0:
                col_notifications.insert_one({
                    'username': username,
                    'data': [{
                        'cve': cve_data.get('id'),
                        'keyword': keyword
                    }]
                })

        mongo_client.close()

        return True

    except Exception as e:
        logger.exception(e)
        return None


def monitoring_scheduler():
    try:
        logger.info(f'Executing Scheduler: {datetime.now()}')

        mongo_client = mongoClient()
        col_monitoring = mongo_client[MONGO_DB][MONGO_MONITORING_COLLECTION]

        results = list(col_monitoring.find({}, {'_id': 0}))

        if not results:
            logger.info('Nothing to monitor for Scheduler...')
            return

        for item in results:
            try:
                keyword = item.get('monitoring_keyword')

                last_updated_time = item.get('updated_at', "")
                current_time = datetime.now()

                if type(last_updated_time) != str:
                    delta_time_difference = current_time - last_updated_time
                    diff_in_hours = delta_time_difference.total_seconds() / 60 / 60

                    logger.info(f'[{keyword}] - Difference in hours: {diff_in_hours}')

                    if diff_in_hours < float(item.get('frequency')):
                        continue

                monitoring_results({'username': item.get('username'), 'monitoring_keyword': keyword})

            except Exception as e:
                logger.exception(e)
                continue

        return

    except Exception as e:
        logger.exception(e)
        return
